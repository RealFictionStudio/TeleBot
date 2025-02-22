from bot import client
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def main():
    client.run(getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
