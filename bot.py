from datetime import date
from discord import Client, Intents, Message, app_commands, Interaction
from discord.ext import commands
from dotenv import load_dotenv

if not load_dotenv():
    print("No new Env Variables")


# Podejrzewam że wolisz jak stworzymy classe oddzielną do tego :.(
class Event:
    e_date: date
    e_group: str
    e_subject: str

    def __init__(self):
        self.e_date = date(1, 1, 1)
        self.e_group = "def"
        self.e_subject = "def"

    def from_str(self, smth: list[str]):
        # TODO Dodać sprawdzanie czy ilość argumentów się zgadza, czy argumenty spełniają requirementy
        self.e_date = date(int(smth[0]), int(smth[1]), int(smth[2]))
        self.e_group = smth[3]
        self.e_subject = smth[4]


class BotPlayer(Client):
    async def on_ready(self):
        print(f"READY PLAYER {self.user}")

    async def on_message(self, message: Message):
        print(f"Message from {message.author}: {message.content}")
        if "blob" in message.content:
            _ = await message.channel.send("bolb")


intents = Intents.default()
intents.message_content = True

client = BotPlayer(intents=intents)

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.command(description="Adds described event to calendar")
@app_commands.describe(
    message="You need to specify: Date(dd:mm:yy), Group, Subject, type of event"
)
async def add_event(ctx, *args):
    """Adds described event to calendar"""
    pass


# tree = app_commands(client)
# client.tree = tree


# @client.tree.command("add_event", description="Adds described event to calendar")
@app_commands.describe(
    message="You need to specify: Date(dd:mm:yy), Group, Subject, type of event"
)
async def add_event_to_calendar(
    interaction: Interaction, date: str, group: int, subject: str, type_of_event: str
) -> None:
    _ = await interaction.response.send_message((date, group, subject, type_of_event))
