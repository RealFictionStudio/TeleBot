from os import getenv
from typing import final
from discord import Interaction, app_commands
from discord.app_commands import commands
from discord.ext import commands as cmds
from dotenv import load_dotenv

GROUPS = ["T1", "T2", "T3"]
SUBJECTS = ["ANL2", "PRM2", "SYCY"]

if not load_dotenv():
    print("No new Env Variables")

POWER_USERS = [int(i) for i in (getenv("POWER_USERS") or "").split(",")]
GUILDS = [int(i) for i in (getenv("GUILDS") or "").split(",")]


@final
class CalendarCMDS(cmds.Cog):
    def __init__(self, bot: cmds.Bot) -> None:
        self.bot = bot
        self._las_member = None

    @commands.command()
    @app_commands.guilds(*GUILDS)
    @app_commands.choices(
        group=[app_commands.Choice(name=group, value=group) for group in GROUPS],
        subject=[
            app_commands.Choice(name=subject, value=subject) for subject in SUBJECTS
        ],
    )
    @app_commands.describe(
        date="A date in format of dd(sep)mm(sep)yy where (sep) = - or / or :"
    )
    async def add_event(
        self, interaction: Interaction, date: str, group: str, subject: str, event: str
    ):
        """Adds described event to calendar using sqlite db"""
        print("Adding event: ")
        _ = await interaction.response.send_message(
            f"There will be {event} for {group} in {subject} at {date}"
        )
