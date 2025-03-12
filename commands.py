from os import getenv
from typing import final
from discord import Interaction, Message, app_commands
from discord.app_commands import commands
from discord.ext import commands as cmds
from dotenv import load_dotenv
from googleapiclient.errors import HttpError
from requests.models import HTTPError
from db_handler import manager as db_h
from google_handler.manager import create_event, del_event
from helpers import dc_msg_gen, parse_date

GROUPS = ["Grupa 1", "Grupa 2", "Grupa 3", "Grupa 4", "Grupa Wykładowa"]
SUBJECTS = ["ANL2", "PRM2", "SYCY"]

if not load_dotenv():
    print("No new Env Variables")

POWER_USERS = [int(i) for i in (getenv("POWER_USERS") or "").split(",")]
GUILDS = [int(i) for i in (getenv("GUILDS") or "").split(",")]


@final
class CalendarCMDS(cmds.Cog):
    _las_member = None

    def __init__(self, bot: cmds.Bot, msg: Message) -> None:
        self.bot = bot
        self.msg = msg

    @commands.command()
    @app_commands.guilds(*GUILDS)
    @app_commands.choices(
        group=[
            app_commands.Choice(name=group, value=GROUPS.index(group))
            for group in GROUPS
        ],
    )
    @app_commands.choices(
        subject=[
            app_commands.Choice(name=subject, value=subject) for subject in SUBJECTS
        ],
    )
    @app_commands.describe(
        e_date="A date in format of dd(sep)mm(sep)yy where (sep) = - or / or :"
    )
    async def add_event(
        self,
        interaction: Interaction,
        e_date: str,
        group: int,
        subject: str,
        desc: str,
    ):
        """Adds described event to the calendar"""

        p_date = parse_date(e_date)

        if p_date == None:
            # Send message about wrong date format
            return

        # Add event to google calendar
        ggl_id_a, ggl_id_g = create_event(p_date, group, subject, desc)

        # Add the record to database
        db_h.add_event(ggl_id_a, ggl_id_g, p_date, group, subject, desc)

        # Change the message on discord
        _ = await self.msg.edit(content=dc_msg_gen())

        print("Database state", dc_msg_gen())

        print("Adding event: ")
        _ = await interaction.response.send_message(
            f"There will be {desc} for {group} in {subject} at {e_date}"
        )

    @commands.command()
    @app_commands.guilds(*GUILDS)
    @app_commands.choices(
        group=[
            app_commands.Choice(name=group, value=GROUPS.index(group))
            for group in GROUPS
        ],
    )
    @app_commands.choices(
        subject=[
            app_commands.Choice(name=subject, value=subject) for subject in SUBJECTS
        ],
    )
    @app_commands.describe(
        e_date="A date in format of dd(sep)mm(sep)yy where (sep) is - or / or :"
    )
    async def change_event(
        self,
        interaction: Interaction,
        event_id: int,
        e_date: str,
        group: int,
        subject: str,
        event: str,
        upd_desc: str,
    ):
        """Chages described event in the calendar"""

        p_date = parse_date(e_date)

        if p_date == None:
            # Send message about wrong date format
            return
        try:
            # Change the record to database
            ggl_id_a, ggl_id_g = db_h.upd_event(event_id, p_date, subject, upd_desc)

            if ggl_id_g == None or ggl_id_a == None:
                _ = await interaction.response.send_message(
                    f"There is no event with that id"
                )
                return

            # Change google calendar event and retreve the id-s

            # Change the message on discord
            _ = await self.msg.edit(content=dc_msg_gen())

        except HttpError as err:
            print("Something went wrong while changing event.", err)

        print("Changing the event: ")
        _ = await interaction.response.send_message(
            f"There will be {event} for {group} in {subject} at {e_date}"
        )

    @commands.command()
    @app_commands.guilds(*GUILDS)
    async def delete_event(self, interaction: Interaction, event_id: int):
        """Deletes described event from the calendar"""
        try:
            # Delete the record to database
            ggl_id_a, ggl_id_g, group = db_h.del_event(event_id)

            print(ggl_id_a, ggl_id_g, group)
            if ggl_id_g == None or ggl_id_a == None or group == None:
                _ = await interaction.response.send_message(
                    f"There is no event with that id"
                )
                return
            # Delete google calendar event
            del_event(ggl_id_a, ggl_id_g, group)

            # Change the message on discord
            _ = await self.msg.edit(content=dc_msg_gen())
        except HTTPError as err:
            print("Something went wrong when deleting the event: ", err)

        print("Deleting the event: ")
        _ = await interaction.response.send_message(
            f"Will delete event with id {event_id}"
        )
