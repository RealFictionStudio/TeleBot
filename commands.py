from os import getenv
from typing import final
from discord import Interaction, app_commands
from discord.app_commands import commands
from discord.ext import commands as cmds
from dotenv import load_dotenv
from db_handler import manager as db_h
from helpers import parse_date

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
        """Adds described event to the calendar"""

        p_date = parse_date(e_date)

        if p_date == None:
            # Send message about wrong date format
            return
        try:
            # Add the record to database
            db_h.add_event(p_date, group, subject, event)
        except:
            print("Something went wrong while adding event.")

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
        """Chages described event in the calendar"""

        p_date = parse_date(e_date)

        if p_date == None:
            # Send message about wrong date format
            return
        try:
            # Change the record to database
            db_h.upd_event(p_date, group, subject, event)
        except:
            print("Something went wrong while changing event.")

        # Change google calendar event
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
        """Deletes described event from the calendar"""

        p_date = parse_date(e_date)

        if p_date == None:
            # Send message about wrong date format
            return
        try:
            # Delete the record to database
            db_h.del_event(p_date, group, subject)
        except:
            print("Something went wrong while deleting event.")

        # Delete google calendar event
        # Change the message on discord

        print("Deleting the event: ")
        _ = await interaction.response.send_message(
            f"Will delete event from {group} in {subject} at {e_date}"
        )
