from os import getenv
from typing import final
from discord import Interaction, app_commands
from discord.app_commands import commands
from discord.ext import commands as cmds
from dotenv import load_dotenv

GROUPS = ["W", "1", "2", "3", "4"]
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
        self,
        interaction: Interaction,
        e_date: str,
        group: str,
        subject: str,
        event: str,
    ):
        """Adds described event to calendar"""

        # Add the record to database
        # Add event to google calendar
        # Change the message on discord

        print("Adding event: ")
        _ = await interaction.response.send_message(
            f"There will be {event} for {group} in {subject} at {e_date}"
        )

    @commands.command()
    @app_commands.guilds(*GUILDS)
    @app_commands.choices(
        group=[app_commands.Choice(name=group, value=group) for group in GROUPS],
        subject=[
            app_commands.Choice(name=subject, value=subject) for subject in SUBJECTS
        ],
    )
    @app_commands.describe(
        date="A date in format of dd(sep)mm(sep)yy where (sep) is - or / or :"
    )
    async def change_event(
        self,
        interaction: Interaction,
        e_date: str,
        group: str,
        subject: str,
        event: str,
    ):
        """Chages described event to calendar"""

        # Change record in database
        # change google calendar event
        # Change the message on discord

        print("Changing the event: ")
        _ = await interaction.response.send_message(
            f"There will be {event} for {group} in {subject} at {e_date}"
        )

    @commands.command()
    @app_commands.guilds(*GUILDS)
    @app_commands.choices(
        group=[app_commands.Choice(name=group, value=group) for group in GROUPS],
        subject=[
            app_commands.Choice(name=subject, value=subject) for subject in SUBJECTS
        ],
    )
    @app_commands.describe(
        date="A date in format of dd(sep)mm(sep)yy where (sep) is - or / or :"
    )
    async def delete_event(
        self,
        interaction: Interaction,
        e_date: str,
        group: str,
        subject: str,
    ):
        """Deletes described event to calendar"""

        # Delete the record from database
        # Delete google calendar event
        # Change the message on discord

        print("Deleting the event: ")
        _ = await interaction.response.send_message(
            f"Will delete {group} in {subject} at {e_date}"
        )
