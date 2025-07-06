# -*- coding: utf-8 -*-
"""
Модуль для автоматического обновления статистики сервера в названиях каналов.
"""
import discord
from discord.ext import commands, tasks
import asyncio

# --- КОНФИГУРАЦИЯ ---
# Как часто (в минутах) обновлять статистику. 
# Не ставьте слишком низкое значение, чтобы не получить бан от Discord. 10 - оптимально.
UPDATE_INTERVAL_MINUTES = 10

# Префиксы каналов, которые бот будет искать для обновления.
# Важно, чтобы они в точности совпадали с названиями в файле структуры.
MEMBER_CHANNEL_PREFIX = "╔ 📚・Участники:"
BOT_CHANNEL_PREFIX = "╚ 📚・Боты:"


class StatsUpdater(commands.Cog):
    """
    Ког, отвечающий за автоматическое обновление статистики
    сервера (количество участников и ботов) в названиях голосовых каналов.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_stats_task.start()

    def cog_unload(self):
        """Вызывается при выгрузке кога, останавливает задачу."""
        self.update_stats_task.cancel()

    @tasks.loop(minutes=UPDATE_INTERVAL_MINUTES)
    async def update_stats_task(self):
        """
        Главная задача, которая периодически запускает обновление
        статистики для всех серверов, где находится бот.
        """
        print("Запускаю фоновую задачу обновления статистики каналов...")
        for guild in self.bot.guilds:
            try:
                await self._update_single_guild(guild)
            except Exception as e:
                print(f"Критическая ошибка при обновлении статистики для сервера {guild.name} ({guild.id}): {e}")
        print("Задача обновления статистики завершена.")
    
    @update_stats_task.before_loop
    async def before_update_stats(self):
        """Ожидает полной готовности бота перед первым запуском задачи."""
        await self.bot.wait_until_ready()
        print("Модуль статистики готов к работе. Запускаю цикл обновлений.")

    async def _update_single_guild(self, guild: discord.Guild):
        """Обновляет статистику для одного конкретного сервера."""
        
        # Ищем каналы по префиксам. Используем discord.utils.find для эффективности.
        member_channel = discord.utils.find(lambda c: c.name.startswith(MEMBER_CHANNEL_PREFIX), guild.voice_channels)
        bot_channel = discord.utils.find(lambda c: c.name.startswith(BOT_CHANNEL_PREFIX), guild.voice_channels)
        
        # Если на сервере нет нужных каналов, ничего не делаем.
        if not member_channel and not bot_channel:
            return

        # --- Вычисляем статистику ---
        # guild.member_count - самый надежный способ получить общее число участников.
        total_members = guild.member_count
        # Для подсчета ботов необходим кеш участников, который должен быть включен.
        bot_count = sum(1 for member in guild.members if member.bot)
        
        # --- Обновляем канал с участниками ---
        if member_channel:
            new_name = f"{MEMBER_CHANNEL_PREFIX} {total_members}"
            # Обновляем имя, только если оно изменилось, чтобы избежать лишних запросов к API.
            if member_channel.name != new_name:
                try:
                    await member_channel.edit(name=new_name, reason="Обновление статистики участников")
                    print(f"Сервер '{guild.name}': Канал участников обновлен ({total_members}).")
                    # Небольшая пауза, чтобы не отправлять запросы слишком часто.
                    await asyncio.sleep(2)
                except discord.Forbidden:
                    print(f"Ошибка на сервере '{guild.name}': нет прав для редактирования канала участников.")
                except Exception as e:
                    print(f"Непредвиденная ошибка при обновлении канала участников на '{guild.name}': {e}")
        
        # --- Обновляем канал с ботами ---
        if bot_channel:
            new_name = f"{BOT_CHANNEL_PREFIX} {bot_count}"
            if bot_channel.name != new_name:
                try:
                    await bot_channel.edit(name=new_name, reason="Обновление статистики ботов")
                    print(f"Сервер '{guild.name}': Канал ботов обновлен ({bot_count}).")
                except discord.Forbidden:
                    print(f"Ошибка на сервере '{guild.name}': нет прав для редактирования канала ботов.")
                except Exception as e:
                    print(f"Непредвиденная ошибка при обновлении канала ботов на '{guild.name}': {e}")


def setup(bot: commands.Bot):
    """Функция, которую discord.py вызывает для загрузки кога."""
    bot.add_cog(StatsUpdater(bot)) 