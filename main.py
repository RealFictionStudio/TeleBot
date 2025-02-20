from bot import client
from calendar.add_event import add_calendar_event
import os
from dotenv import load_dotenv
load_dotenv()


def main():
    client.run(getenv('DISCORD_TOKEN'))
