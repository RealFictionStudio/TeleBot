from bot import client
from os import getenv, getcwd, listdir, path
from dotenv import load_dotenv

if not load_dotenv():
    print("No new env variables")


def load_plugins(plugin_path: str = getcwd()):
    for file in list(listdir(plugin_path)):
        if path.isdir(file) and file[0] not in "_.":
            try:
                print(f"Trying to load plugin: {file}")
            except Exception as e:
                print(e)


def main():
    client.run(getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
