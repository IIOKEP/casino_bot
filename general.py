import discord
from discord.ext import commands, tasks


class CommandsBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = "*")
        super().load_extension('casino')

    async def on_ready(self):
        print("Ты, наверно, думаешь, что тебе выпало 18 карат невезения? Да нет, просто игра попалась нечестная.")


with open('token.txt', 'r') as f:
    token = f.read()

bot = CommandsBot()
bot.run(token)