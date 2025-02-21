from bot import client
from calendar.add_event import add_calendar_event
from os import getenv
from dotenv import load_dotenv

if not load_dotenv():
    print("Not new Variables.")


def main():
    bot_token = getenv("DISCORD_TOKEN")
    if bot_token == None:
        exit(-1)
    client.run(bot_token)
