from discord import Client, Intents, Message
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class MyClient(Client):
    async def on_ready(self):
        print(f'READY PLAYER {self.user}')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        print(message)


intents = Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(getenv('DISCORD_TOKEN'))
