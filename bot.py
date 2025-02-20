from discord import Client, Intents, Message, app_commands, Interaction
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class BotPlayer(Client):
    async def on_ready(self):
        print(f'READY PLAYER {self.user}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if "blob" in message.content:
            await message.channel.send("bolb")


intents = Intents.default()
intents.message_content = True
client = BotPlayer(intents=intents)
tree = app_commands(client)
client.tree = tree


@client.tree.command("add_event", description="Adds described event to calendar")
@app_commands.describe(message="You need to specify: Date(dd:mm:yy), Group, Subject, type of event")
async def add_event_to_calendar(interaction: Interaction, date: str, group: int, subject: str, type_of_event: str) -> None:
    await Interaction.response.send_message(date, group, subject, type_of_event)
