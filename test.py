from os import getenv
from dotenv import load_dotenv


_ = load_dotenv()


def test_env():
    GUILDS = getenv("GUILDS")
    if not GUILDS:
        print("Could not find GUILDS in env")
        return
    print(f"{eval(GUILDS)}")


if __name__ == "__main__":
    test_env()
