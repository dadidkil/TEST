# -*- coding: utf-8 -*-
"""
Конфигурация ролей и каналов для сервера.
"""
from typing import Any, Dict, List

import discord
from discord import Color

# --- ОСНОВНЫЕ НАСТРОЙКИ ---

# Каналы, которые нельзя удалять боту
PROTECTED_CHANNELS = ["правила", "новости", "основной"]

# --- НАСТРОЙКА РОЛЕЙ ---

# Права для разных уровней персонала
# https://discordpy.readthedocs.io/en/stable/api.html#permissions
P_CREATOR = discord.Permissions(administrator=True)
P_ADMIN = discord.Permissions.all()
P_CURATOR = discord.Permissions(
    manage_channels=True, manage_roles=True, manage_webhooks=True, manage_events=True,
    kick_members=True, ban_members=True, manage_nicknames=True, manage_messages=True,
    moderate_members=True, move_members=True, view_audit_log=True)
P_HEAD_MOD = discord.Permissions(
    kick_members=True, ban_members=True, manage_messages=True, mute_members=True,
    view_audit_log=True, manage_nicknames=True, move_members=True, moderate_members=True)
P_MOD = discord.Permissions(
    manage_messages=True, mute_members=True, view_audit_log=True, manage_nicknames=True)
P_INTERN = discord.Permissions(manage_messages=True)
P_EVENTOLOG = discord.Permissions(manage_events=True, move_members=True)
P_DEFAULT = discord.Permissions.general()
P_NO_PERMS = discord.Permissions.none()

# Структура ролей (отображается в Discord сверху вниз)
# hoist: True - отображать роль отдельно от других участников
# mentionable: True - эту роль можно будет упоминать (@)

_ROLES: List[Dict[str, Any]] = [
    # ======================================================================================
    # Категория: Управление
    # ======================================================================================
    {'name': '━━━━━「 👑 УПРАВЛЕНИЕ 」━━━━━', 'type': 'separator'},
    {'name': '[ 👑 Создатель ]', 'permissions': P_CREATOR, 'color': Color.red(), 'hoist': True, 'mentionable': True, 'role_type': 'creator'},
    {'name': '[ 💎 Администратор ]', 'permissions': P_ADMIN, 'color': Color.orange(), 'hoist': True, 'mentionable': True, 'role_type': 'admin'},
    {'name': '[ 🛡️ Куратор ]', 'permissions': P_CURATOR, 'color': Color.gold(), 'hoist': True, 'mentionable': True, 'role_type': 'curator'},
    
    # ======================================================================================
    # Категория: Персонал
    # ======================================================================================
    {'name': '━━━━━「 👮 ПЕРСОНАЛ 」━━━━━', 'type': 'separator'},
    {'name': '[ 🎓 Главный Модератор ]', 'permissions': P_HEAD_MOD, 'color': Color.blue(), 'hoist': True, 'mentionable': True, 'role_type': 'head_mod'},
    {'name': '[ 🔨 Модератор ]', 'permissions': P_MOD, 'color': Color.from_rgb(0, 128, 128), 'hoist': True, 'mentionable': False, 'role_type': 'mod'},
    {'name': '[ ✏️ Стажёр ]', 'permissions': P_INTERN, 'color': Color.from_rgb(0, 255, 255), 'hoist': True, 'mentionable': False, 'role_type': 'intern'},
    {'name': '[ 🎉 Ивентолог ]', 'permissions': P_EVENTOLOG, 'color': Color.yellow(), 'hoist': True, 'mentionable': False, 'role_type': 'eventolog'},
    
    # ======================================================================================
    # Категория: Особые гости
    # ======================================================================================
    {'name': '━━━━━「 ✨ ОСОБЫЕ ГОСТИ 」━━━━━', 'type': 'separator'},
    {'name': '[ 💖 Premium Booster ]', 'permissions': P_DEFAULT, 'color': Color.from_rgb(255, 105, 180), 'hoist': True},
    {'name': '[ 💗 Booster ]', 'permissions': P_DEFAULT, 'color': Color.magenta(), 'hoist': True},
    {'name': '[ 💚 Sponsor ]', 'permissions': P_DEFAULT, 'color': Color.green(), 'hoist': True},
    {'name': '[ 💜 Partner ]', 'permissions': P_DEFAULT, 'color': Color.purple(), 'hoist': True},

    # ======================================================================================
    # Категория: Боты
    # ======================================================================================
    {'name': '━━━━━「 🤖 БОТЫ 」━━━━━', 'type': 'separator'},
    {'name': '[ 🤖 Боты ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(96, 125, 139), 'hoist': True},

    # ======================================================================================
    # Категория: Уровни
    # ======================================================================================
    {'name': '━━━━━「 ⭐ УРОВНИ 」━━━━━', 'type': 'separator'},
    {'name': '[ 🏆 LVL 100 | Бог Сервера ]', 'permissions': P_DEFAULT, 'color': Color.from_rgb(255, 215, 0), 'hoist': False},
    {'name': '[ 🏅 LVL 75 | Легенда ]', 'permissions': P_DEFAULT, 'color': Color.from_rgb(186, 85, 211), 'hoist': False},
    {'name': '[ 🎖️ LVL 50 | Ветеран ]', 'permissions': P_DEFAULT, 'color': Color.from_rgb(135, 206, 235), 'hoist': False},
    {'name': '[ 🎗️ LVL 25 | Бывалый ]', 'permissions': P_DEFAULT, 'color': Color.from_rgb(60, 179, 113), 'hoist': False},
    {'name': '[ ☀️ LVL 10 | Активный ]', 'permissions': P_DEFAULT, 'color': Color.from_rgb(192, 192, 192), 'hoist': False},
    {'name': '[ 🌱 LVL 1 | Участник ]', 'permissions': P_DEFAULT, 'color': Color.from_rgb(96, 125, 139), 'hoist': False},
    
    # ======================================================================================
    # Категория: Местоимения (для самоназначения)
    # ======================================================================================
    {'name': '━━━━━「 🏳️‍🌈 МЕСТОИМЕНИЯ 」━━━━━', 'type': 'separator'},
    {'name': '[ 🔵 Он/Его ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(173, 216, 230), 'hoist': False},
    {'name': '[ 🟣 Она/Её ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(255, 182, 193), 'hoist': False},
    {'name': '[ 🟢 Они/Их ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(144, 238, 144), 'hoist': False},

    # ======================================================================================
    # Категория: Интересы (для самоназначения)
    # ======================================================================================
    {'name': '━━━━━「 🎮 ИНТЕРЕСЫ 」━━━━━', 'type': 'separator'},
    {'name': '[ 🧱 Minecraft ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(139, 69, 19), 'hoist': False},
    {'name': '[ 🔫 Valorant ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(253, 69, 86), 'hoist': False},
    {'name': '[ 🍊 CS:GO ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(222, 133, 34), 'hoist': False},
    {'name': '[ ⚔️ Dota 2 / LoL ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(214, 40, 40), 'hoist': False},
    {'name': '[ 📦 Roblox ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(200, 200, 200), 'hoist': False},
    {'name': '[ 🌠 Genshin Impact ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(234, 222, 201), 'hoist': False},
    {'name': '[ 🎨 Art ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(255, 105, 180), 'hoist': False},
]

# Роли '49BT' и 'Night' со скриншота не имели категории.
# Добавляем их в начало списка, чтобы они были наверху иерархии, как на изображении.
_MISC_ROLES: List[Dict[str, Any]] = [
    # Роль '49BT' теперь настраивается автоматически и удалена из конфига.
    {'name': '[ 🌙 Night ]', 'permissions': P_NO_PERMS, 'color': Color.from_rgb(44, 47, 51), 'hoist': True},
]

ROLES_STRUCTURE: List[Dict[str, Any]] = _MISC_ROLES + _ROLES

# ======================================================================================
# --- НАСТРОЙКА ПРАВ ДОСТУПА ДЛЯ КАНАЛОВ ---
# ======================================================================================
# Здесь мы определяем, какие роли что могут делать в разных типах каналов.

CHANNEL_PERMISSIONS = {
    # --- Схемы для текстовых каналов и категорий ---
    
    # Категория/канал только для персонала. Полный доступ для всех сотрудников.
    'staff_only': {
        '@everyone': discord.PermissionOverwrite(view_channel=False),
        'creator': discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True),
        'admin': discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True),
        'curator': discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True),
        'head_mod': discord.PermissionOverwrite(view_channel=True, send_messages=True),
        'mod': discord.PermissionOverwrite(view_channel=True, send_messages=True),
        'intern': discord.PermissionOverwrite(view_channel=True, send_messages=True),
        'eventolog': discord.PermissionOverwrite(view_channel=True, send_messages=True),
    },
    
    # Канал для чтения (правила, новости). @everyone может только читать.
    'info_read_only': {
        '@everyone': discord.PermissionOverwrite(view_channel=True, send_messages=False, add_reactions=False),
        'admin': discord.PermissionOverwrite(send_messages=True),
    },
    
    # Общедоступный чат. @everyone может общаться, прикреплять файлы и ссылки.
    'public_chat': {
        '@everyone': discord.PermissionOverwrite(
            view_channel=True, 
            send_messages=True, 
            embed_links=True, 
            attach_files=True, 
            add_reactions=True, 
            use_external_emojis=True
        )
    },

    # Канал для альбома. @everyone может кидать файлы, но не текст.
    'album': {
        '@everyone': discord.PermissionOverwrite(
            view_channel=True,
            send_messages=False, # Запрещаем текст
            attach_files=True,   # Разрешаем файлы
            read_message_history=True,
            add_reactions=True
        ),
        'admin': discord.PermissionOverwrite(send_messages=True), # Администрация может комментировать
    },

    # Канал для предложений. @everyone может писать и обязательно добавлять реакции.
    'suggestions': {
         '@everyone': discord.PermissionOverwrite(
            view_channel=True, 
            send_messages=True, 
            add_reactions=True, # Обязательно для голосования
            read_message_history=True
        )
    },

    # Канал для анонсов мероприятий. Писать может только ивентолог и админы.
    'event_info': {
        '@everyone': discord.PermissionOverwrite(view_channel=True, send_messages=False),
        'eventolog': discord.PermissionOverwrite(send_messages=True, manage_messages=True),
        'admin': discord.PermissionOverwrite(send_messages=True, manage_messages=True),
    },

    # --- Схемы для голосовых каналов ---
    
    # Общедоступный голосовой канал
    'public_voice': {
        '@everyone': discord.PermissionOverwrite(view_channel=True, connect=True, speak=True, use_voice_activation=True)
    },

    # Голосовой канал-счетчик (только для просмотра)
    'stats_voice': {
        '@everyone': discord.PermissionOverwrite(view_channel=True, connect=False),
        'admin': discord.PermissionOverwrite(connect=True) # Админы могут зайти, если нужно
    },

    # Канал "Создать приватку"
    'voice_creator': {
        '@everyone': discord.PermissionOverwrite(view_channel=True, connect=True, speak=False)
    }
}

# ======================================================================================
# --- КАРТА ПРИМЕНЕНИЯ ПРАВ ---
# ======================================================================================
# Здесь мы связываем имена каналов и категорий с созданными выше схемами прав.

CHANNEL_CONFIG = {
    # Применяем права ко всей категории
    "category_map": {
        "╭───「 👑 Персонал 」───╮": 'staff_only',
        "๑▬▬▬۩〘 Разговоры 〙۩▬▬▬๑": 'public_voice', # Все каналы внутри станут голосовыми
        "╭───「 🔒 ПРИВАТКИ 」───╮": 'voice_creator', # Все каналы внутри станут создающими
    },
    # Применяем права к конкретным каналам
    "channel_map": {
        # Информация
        "╔ 📚・Участники: 146": 'stats_voice',
        "╚ 📚・Боты: 6": 'stats_voice',
        # Основное
        "╔📜・информация": 'info_read_only',
        "║📣・новости-проекта": 'info_read_only',
        "║🖼️・альбом": 'album',
        "║💡・предложения": 'suggestions',
        "╚💼・вакансии": 'info_read_only',
        # Чаты
        "╔📃・общий-чат": 'public_chat',
        "║📃・чат-мероприятия": 'event_info',
        "╚📃・спам": 'public_chat',
        # Minecraft
        "╔📰・мс-новости": 'info_read_only',
        "╚🌍・мс-чат": 'public_chat',
    }
} 