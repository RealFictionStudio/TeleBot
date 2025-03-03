from typing import override
import discord
from discord import Guild, Intents, Message
from discord.ext import commands


class BotPlayer(commands.Bot):
    guilds_list: list[Guild] = []

    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        # self.tree = app_commands(self)

    async def on_ready(self):
        self.guilds_list = [guild async for guild in self.fetch_guilds(limit=150)]
        for guild_obj in self.guilds_list:
            gid = discord.Object(id=guild_obj.id)

            try:
                synced = await self.tree.sync(guild=gid)
            except Exception as e:
                print("ERROR SYNCING commands, aborting")
                print(e)
                exit(3)

            print(
                f"SYNCED {len(synced)} COMMANDS TO GUILD {guild_obj.name} {guild_obj.id}"
            )

        print(f"\t\tREADY PLAYER {self.user}")

    @override
    async def on_message(self, message: Message):
        print(f"Message from {message.author}: {message.content}")
        if "blob" in message.content:
            _ = await message.channel.send("bolb")


client = BotPlayer()
