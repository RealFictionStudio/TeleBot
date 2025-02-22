from bot import bot
from os import getenv
from dotenv import load_dotenv

if not load_dotenv():
    print("No new Variables.")


def main():
    bot_token = getenv("DISCORD_TOKEN")
    if bot_token == None:
        exit(-1)
    bot.run(bot_token)


main()
