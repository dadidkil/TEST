# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import json

class ServerStructure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def savestructure(self, ctx, guild_id: int):
        """Сохраняет структуру сервера в JSON файл."""
        await ctx.send(f"Начинаю сканирование сервера с ID: {guild_id}...")
        
        guild = self.bot.get_guild(guild_id)
        if not guild:
            await ctx.send(f"Не могу найти сервер с ID {guild_id}. Убедитесь, что бот находится на этом сервере.")
            return

        structure = {
            "categories": []
        }

        for category in guild.categories:
            category_data = {
                "name": category.name,
                "channels": {
                    "text": [],
                    "voice": []
                }
            }
            
            for channel in category.text_channels:
                category_data["channels"]["text"].append({"name": channel.name})
            
            for channel in category.voice_channels:
                category_data["channels"]["voice"].append({"name": channel.name})

            structure["categories"].append(category_data)

        file_name = f"new_server_structure_{guild_id}.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(structure, f, ensure_ascii=False, indent=4)

        await ctx.send(f"Структура сервера сохранена в файл `{file_name}`.")

def setup(bot):
    bot.add_cog(ServerStructure(bot)) 