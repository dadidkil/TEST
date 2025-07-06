# -*- coding: utf-8 -*-
"""
Модуль для полной настройки сервера: роли + приватность каналов.
"""
import asyncio
import os
import json
import io
from typing import Any, Dict, List, Optional, Union

import discord
from discord.ext import commands

from . import roles_config


class ServerSetup(commands.Cog):
    """Модуль для полной настройки сервера."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.slash_command(
        name="setup-server",
        description="Полная настройка: роли + каналы из локальной копии структуры."
    )
    @commands.has_permissions(administrator=True)
    async def setup_server(self, ctx: discord.ApplicationContext):
        """Полная настройка: создает роли и копирует каналы из локального файла."""
        await ctx.respond("🚀 Начинаю полную настройку сервера...", ephemeral=True)
        
        if not ctx.guild:
            await ctx.followup.send("❌ Команда должна выполняться на сервере.", ephemeral=True)
            return

        guild = ctx.guild
        STRUCTURE_FILE_PATH = "main_server_structure.json"

        if not os.path.exists(STRUCTURE_FILE_PATH):
            await ctx.followup.send(
                "❌ Локальная копия структуры не найдена (`main_server_structure.json`).\n"
                "Пожалуйста, сначала выполните команду `/update-local-structure`.",
                ephemeral=True
            )
            return
        
        # --- Этап 1: Роли ---
        await ctx.followup.send("Этап 1: Настройка ролей...", ephemeral=True)
        roles_result = await self._setup_roles(guild)
        await ctx.followup.send("Этап 1: Настройка ролей... ✅ Готово!", ephemeral=True)
        
        # --- Этап 2: Загрузка и применение структуры каналов ---
        await ctx.followup.send(f"Этап 2: Загрузка структуры из `{STRUCTURE_FILE_PATH}`...", ephemeral=True)
        
        try:
            with open(STRUCTURE_FILE_PATH, 'r', encoding='utf-8') as f:
                structure = json.load(f)
        except Exception as e:
            await ctx.followup.send(f"❌ Не удалось прочитать файл `{STRUCTURE_FILE_PATH}`. Ошибка: {e}", ephemeral=True)
            return
            
        sync_channels_result = await self._apply_guild_structure(guild, structure)
        await ctx.followup.send("Этап 2: Применение структуры каналов... ✅ Готово!", ephemeral=True)
        
        # --- Финальный отчет ---
        roles_report = (f"Создано: **{roles_result.get('created', 0)}**, "
                        f"Обновлено: **{roles_result.get('updated', 0)}**, "
                        f"Удалено лишних: **{roles_result.get('deleted', 0)}**")
        
        channels_report = (f"Категорий создано/удалено: **{sync_channels_result.get('cats_created', 0)}/{sync_channels_result.get('cats_deleted', 0)}**\n"
                           f"Каналов создано/удалено: **{sync_channels_result.get('chans_created', 0)}/{sync_channels_result.get('chans_deleted', 0)}**")

        final_embed = discord.Embed(title="✅ Синхронизация сервера завершена", color=discord.Color.green())
        final_embed.add_field(name="🎖️ Роли", value=roles_report, inline=False)
        final_embed.add_field(name="🔄 Каналы", value=channels_report, inline=False)
        if roles_result.get('errors') or sync_channels_result.get('errors'):
            final_embed.add_field(name="⚠️ Ошибки", value=f"При обработке возникло **{roles_result.get('errors', 0) + sync_channels_result.get('errors', 0)}** ошибок. Проверьте консоль бота.", inline=False)
            final_embed.color = discord.Color.orange()
        
        try:
            await ctx.author.send(embed=final_embed)
            await ctx.followup.send("✅ Отчет о настройке отправлен вам в личные сообщения.", ephemeral=True)
        except discord.Forbidden:
            await ctx.followup.send("⚠️ Не смог отправить отчет в ЛС. Пожалуйста, проверьте настройки приватности. Вот отчет:", embed=final_embed, ephemeral=True)
        except discord.HTTPException as e:
            print(f"ℹ️ Не удалось отправить финальное сообщение в канал, возможно он был удален. Ошибка: {e}")

    # ======================================================================================
    # Секция: Вспомогательные методы для работы со структурой
    # ======================================================================================

    @discord.slash_command(
        name="update-local-structure",
        description="Скачивает структуру каналов с главного сервера и сохраняет локально."
    )
    @commands.has_permissions(administrator=True)
    async def update_local_structure(self, ctx: discord.ApplicationContext):
        """Скачивает и сохраняет структуру с главного сервера."""
        await ctx.defer(ephemeral=True)

        SOURCE_GUILD_ID = 1369754088941682830
        STRUCTURE_FILE_PATH = "main_server_structure.json"

        source_guild = self.bot.get_guild(SOURCE_GUILD_ID)
        if not source_guild:
            await ctx.followup.send(
                f"❌ Не удалось найти исходный сервер (ID: {SOURCE_GUILD_ID}).\n"
                "Убедитесь, что бот находится на этом сервере.",
                ephemeral=True
            )
            return
        
        await ctx.followup.send(f"✅ Начинаю сканирование сервера **{source_guild.name}**...", ephemeral=True)
        
        structure = self._get_guild_structure(source_guild)
        
        try:
            with open(STRUCTURE_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(structure, f, ensure_ascii=False, indent=4)
            await ctx.followup.send(f"✅ Структура каналов успешно сохранена в файл `{STRUCTURE_FILE_PATH}`.", ephemeral=True)
        except Exception as e:
            await ctx.followup.send(f"❌ Не удалось сохранить файл. Ошибка: {e}", ephemeral=True)

    def _get_guild_structure(self, guild: discord.Guild) -> Dict:
        """Собирает структуру каналов и категорий сервера в словарь."""
        structure = {"categories": []}
        
        # Сортируем для сохранения порядка
        sorted_categories = sorted(guild.categories, key=lambda c: c.position)
        
        # Каналы без категорий
        non_categorized_text = sorted([c for c in guild.text_channels if not c.category], key=lambda c: c.position)
        non_categorized_voice = sorted([c for c in guild.voice_channels if not c.category], key=lambda c: c.position)
        
        if non_categorized_text or non_categorized_voice:
            structure["categories"].append({
                "name": None, # Маркер для каналов без категории
                "channels": {
                    "text": [{"name": c.name} for c in non_categorized_text],
                    "voice": [{"name": c.name} for c in non_categorized_voice]
                }
            })

        # Каналы в категориях
        for category in sorted_categories:
            structure["categories"].append({
                "name": category.name,
                "channels": {
                    "text": [{"name": c.name} for c in sorted(category.text_channels, key=lambda c: c.position)],
                    "voice": [{"name": c.name} for c in sorted(category.voice_channels, key=lambda c: c.position)]
                }
            })
        return structure

    async def _apply_guild_structure(self, guild: discord.Guild, server_structure: Dict) -> Dict:
        """Синхронизирует каналы и категории на сервере, вместо полного удаления."""
        results = {'cats_created': 0, 'cats_deleted': 0, 'chans_created': 0, 'chans_deleted': 0, 'errors': 0}
        protected_channels = roles_config.PROTECTED_CHANNELS

        # --- 0. Получаем актуальные роли персонала ---
        staff_roles = await self._get_staff_roles(guild)

        # --- 1. Сбор информации ---
        config_cat_map = {cat['name']: cat for cat in server_structure.get('categories', [])}
        config_all_chan_names = {chan['name'] for cat_data in server_structure.get('categories', []) for chan_type in ['text', 'voice'] for chan in cat_data.get('channels', {}).get(chan_type, [])}
        server_cats_map = {cat.name: cat for cat in guild.categories}

        # --- 2. Синхронизация Категорий (Удаление и Создание) ---
        for cat_name, category in list(server_cats_map.items()):
            if cat_name not in config_cat_map:
                try:
                    await category.delete(reason="Синхронизация: удаление лишней категории")
                    results['cats_deleted'] += 1
                    del server_cats_map[cat_name]
                except Exception as e: results['errors'] += 1; print(f"Ошибка удаления категории {cat_name}: {e}")
        
        for cat_name in config_cat_map:
            if cat_name and cat_name not in server_cats_map:
                try:
                    overwrites = self._get_overwrites(cat_name, 'category', staff_roles)
                    new_cat = await guild.create_category(name=cat_name, overwrites=overwrites, reason="Синхронизация: создание категории")
                    server_cats_map[cat_name] = new_cat
                    results['cats_created'] += 1
                except Exception as e: results['errors'] += 1; print(f"Ошибка создания категории {cat_name}: {e}")
        
        await asyncio.sleep(1)

        # --- 3. Синхронизация Каналов (Удаление и Создание) ---
        server_all_chans = [c for c in guild.channels if not isinstance(c, discord.CategoryChannel)]
        for chan in server_all_chans:
            if chan.name not in config_all_chan_names and chan.name not in protected_channels:
                try:
                    await chan.delete(reason="Синхронизация: удаление лишнего канала")
                    results['chans_deleted'] += 1
                except Exception as e: results['errors'] += 1; print(f"Ошибка удаления канала {chan.name}: {e}")

        await asyncio.sleep(1)

        for cat_data in server_structure.get('categories', []):
            cat_name = cat_data.get('name')
            category_obj = server_cats_map.get(cat_name)
            
            # Определяем, где искать существующие каналы
            if category_obj: existing_chans_in_cat = {c.name for c in category_obj.channels}
            else: existing_chans_in_cat = {c.name for c in guild.channels if c.category is None and not isinstance(c, discord.CategoryChannel)}

            for chan_type in ['text', 'voice']:
                for chan_info in cat_data.get('channels', {}).get(chan_type, []):
                    chan_name = chan_info['name']
                    if chan_name not in existing_chans_in_cat:
                        creator = guild.create_text_channel if chan_type == 'text' else guild.create_voice_channel
                        try:
                            overwrites = self._get_overwrites(chan_name, 'channel', staff_roles, inherited_from=cat_name)
                            await creator(name=chan_name, category=category_obj, overwrites=overwrites, reason="Синхронизация: создание канала")
                            results['chans_created'] += 1
                            await asyncio.sleep(0.2)
                        except Exception as e: results['errors'] += 1; print(f"Ошибка создания канала {chan_name}: {e}")
        
        await asyncio.sleep(2)

        # --- 4. Финальная сортировка ---
        # Собираем ОДИН большой payload для ОДНОГО вызова API
        final_position_payload = {}
        position_counter = 0

        # Сначала категории
        for cat_data in server_structure.get('categories', []):
            cat_name = cat_data.get('name')
            if cat_name: # Пропускаем каналы без категории
                category_obj = discord.utils.get(guild.categories, name=cat_name)
                if category_obj:
                    if category_obj.position != position_counter:
                        final_position_payload[category_obj] = position_counter
                    position_counter += 1
        
        if final_position_payload:
            await guild.edit_channel_positions(positions=final_position_payload)
            await asyncio.sleep(1)
        
        # Затем каналы внутри категорий
        for cat_data in server_structure.get('categories', []):
            category_obj = discord.utils.get(guild.categories, name=cat_data.get('name'))
            # Каналы должны быть отсортированы внутри своей категории
            # С discord.py v2+ это делается через channel.edit(position=...)
            # или guild.edit_channel_positions с позициями относительно категории, что сложно.
            # Попробуем более простой и надежный способ - индивидуальное перемещение.
            
            all_chans_in_cat_config = cat_data.get('channels', {}).get('text', []) + cat_data.get('channels', {}).get('voice', [])
            
            if category_obj: # Обрабатываем каналы внутри реальной категории
                server_chans_in_cat = {c.name: c for c in category_obj.channels}
                for i, chan_info in enumerate(all_chans_in_cat_config):
                    chan_obj = server_chans_in_cat.get(chan_info['name'])
                    if chan_obj and chan_obj.position != i:
                        try:
                            # Для каналов внутри категорий их позиция относительна
                            await chan_obj.edit(position=i, reason="Синхронизация: сортировка каналов")
                        except Exception as e:
                            results['errors'] += 1; print(f"Ошибка сортировки канала {chan_obj.name}: {e}")

        return results

    async def _setup_roles(self, guild: discord.Guild) -> Dict:
        """Полностью пересоздает роли согласно конфигу для идеальной иерархии."""
        results = {'created': 0, 'deleted': 0, 'errors': 0}
        
        # --- 1. Удаление старых управляемых ролей ---
        config_role_names = {role['name'] for role in roles_config.ROLES_STRUCTURE}
        for role in guild.roles:
            if role.name in config_role_names:
                try:
                    await role.delete(reason="Синхронизация: полное пересоздание ролей")
                    results['deleted'] += 1
                except discord.HTTPException as e:
                    results['errors'] += 1
                    print(f"Ошибка при удалении старой роли {role.name}: {e}")
        
        await asyncio.sleep(2) # Пауза после массового удаления

        # --- 2. Создание ролей с нуля ---
        created_roles = []
        for role_data in roles_config.ROLES_STRUCTURE:
            try:
                role_name = role_data.get("name")
                if not role_name: continue

                target_props = {
                    'permissions': role_data.get("permissions", roles_config.P_NO_PERMS),
                    'color': role_data.get("color", discord.Color.default()),
                    'hoist': role_data.get("hoist", False),
                    'mentionable': role_data.get("mentionable", False)
                }
                
                new_role = await guild.create_role(name=role_name, **target_props, reason="Синхронизация: создание роли")
                created_roles.append(new_role)
                results['created'] += 1
                await asyncio.sleep(0.3)
            except Exception as e:
                results['errors'] += 1
                print(f"Ошибка при создании роли {role_data.get('name')}: {e}")

        # --- 3. Установка правильной иерархии ---
        # Discord API требует, чтобы позиции были от 1.
        # Мы переворачиваем наш список созданных ролей, чтобы верхние роли в конфиге получили наибольшую позицию.
        position_payload = {role: i + 1 for i, role in enumerate(reversed(created_roles))}
        
        try:
            await guild.edit_role_positions(positions=position_payload)
        except Exception as e:
            results['errors'] += 1
            print(f"Ошибка при установке иерархии ролей: {e}")

        # --- 4. Настройка роли самого бота ---
        bot_member = guild.get_member(self.bot.user.id)
        if bot_member:
            # Роль бота - это его интеграционная роль.
            bot_role = discord.utils.get(guild.roles, managed=True, name=bot_member.name)
            if bot_role:
                try:
                    await bot_role.edit(
                        name="[ ⚫ 49BT ]", 
                        color=discord.Color.from_rgb(114, 137, 218), 
                        hoist=True,
                        reason="Авто-настройка роли бота"
                    )
                except Exception as e:
                    results['errors'] += 1
                    print(f"Ошибка при настройке роли бота: {e}")

        return results

    def _get_overwrites(self, name: str, item_type: str, staff_roles: Dict[str, discord.Role], inherited_from: Optional[str] = None) -> Dict:
        """Собирает словарь прав для канала или категории на основе конфига."""
        
        permission_key = None
        if item_type == 'category':
            permission_key = roles_config.CHANNEL_CONFIG['category_map'].get(name)
        elif item_type == 'channel':
            # Права канала приоритетнее прав категории
            permission_key = roles_config.CHANNEL_CONFIG['channel_map'].get(name)
            if not permission_key and inherited_from:
                permission_key = roles_config.CHANNEL_CONFIG['category_map'].get(inherited_from)

        if not permission_key:
            return {}
            
        permission_data = roles_config.CHANNEL_PERMISSIONS.get(permission_key, {})
        overwrites = {}
        
        for role_key, permissions in permission_data.items():
            target = None
            if role_key == '@everyone':
                target = staff_roles.get('@everyone') # Используем default_role, добавленную в _get_staff_roles
            elif role_key in staff_roles:
                target = staff_roles[role_key]
            
            if target:
                overwrites[target] = permissions
        return overwrites

    async def _get_staff_roles(self, guild: discord.Guild) -> Dict[str, discord.Role]:
        """Находит все роли персонала и возвращает их в виде словаря."""
        staff_roles = {'@everyone': guild.default_role}
        for role_data in roles_config.ROLES_STRUCTURE:
            if 'role_type' in role_data:
                # Ищем роль на сервере по имени из конфига
                role = discord.utils.get(guild.roles, name=role_data['name'])
                if role:
                    staff_roles[role_data['role_type']] = role
        return staff_roles


def setup(bot: commands.Bot):
    bot.add_cog(ServerSetup(bot))
