# -*- coding: utf-8 -*-
import os
import discord
import asyncio
import sys
from discord.ext import commands

# --- НАСТРОЙКИ БОТА ---


BOT_TOKEN = "MTM3NDc1MDc1MTYxNTg4MTM1Ng.GJpDqW.pUiIAQqabRtdk66u5zaSlUE-c01pOI-UtlSHf0"

# Настраиваем "намерения" (Intents) для бота. 
# Default подходит для большинства случаев, но для доступа к списку участников нужны все.
intents = discord.Intents.all()

# Создаем экземпляр бота
bot = commands.Bot(command_prefix="!", intents=intents)


# --- ЗАГРУЗКА МОДУЛЕЙ (COGS) ---

@bot.event
async def on_ready():
    """Событие, которое вызывается, когда бот успешно подключился к Discord."""
    print(f'✅ Бот {bot.user.name} успешно запущен!')
    print(f'ID бота: {bot.user.id}')
    print('------')
    
    # Загружаем все модули из папки 'cogs'
    loaded_cogs = 0
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and 'config' not in filename:
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"  -> Модуль {filename} загружен.")
                loaded_cogs += 1
            except Exception as e:
                print(f"  ❌ Не удалось загрузить модуль {filename}: {e}")
    
    print('------')
    print(f"🚀 Всего загружено модулей: {loaded_cogs}")

    print('------')
    print("🔄 Синхронизирую команды с Discord...")
    try:
        await bot.sync_commands()
        print("✅ Команды синхронизированы.")
    except Exception as e:
        print(f"❌ Ошибка синхронизации команд: {e}")


# --- ЗАПУСК БОТА ---

if __name__ == "__main__":
    if BOT_TOKEN == "ВАШ_СУПЕР_СЕКРЕТНЫЙ_ТОКЕН":
        print("======================================================")
        print("!!! ВНИМАНИЕ !!!")
        print("Вы не указали токен бота в файле main.py.")
        print("Пожалуйста, замените 'ВАШ_СУПЕР_СЕКРЕТНЫЙ_ТОКЕН'")
        print("на настоящий токен вашего бота от Discord.")
        print("======================================================")
    else:
        bot.run(BOT_TOKEN) 