import discord
from discord.ext import commands, tasks


class CommandsBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = "*")
        super().load_extension('casino')

    async def on_ready(self):
        print("Ты, наверно, думаешь, что тебе выпало 18 карат невезения? Да нет, просто игра попалась нечестная.")
        game = discord.Game("*help")
        await bot.change_presence(status=discord.Status.online, activity=game)    

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Казино-бот", description="\u200B", color=discord.Colour.blurple())
        embed.add_field(name="Основные команды:", value="** *casino [cтавка]**: Запускает слот-машину.\n** *info**: Показывает информацию о вас(баланс, скин).\n** *getmoney**: Выдает валюту один раз в час.", inline=True)
        embed.add_field(name="\u200B", value="\n** *shop**: Открывает магазин с лут-боксами.\n** *buy [название товара]**: Покупка товара в магазине.")
        embed.set_thumbnail(url="https://memepedia.ru/wp-content/uploads/2018/03/ebanyy-rot-etogo-kazino.png")
        embed.set_author(name="Cyberiiokep", icon_url="https://w0.pngwave.com/png/1003/599/pixel-art-mario-coin-png-clip-art.png")
        embed.set_footer(text="Данный бот не имеет никакого отношения к настоящим казино.", icon_url="https://cdn.imgbin.com/3/11/12/imgbin-emoji-social-media-discord-sticker-emotion-emoji-stbYECVvRACa2ERnLwB8Hrih7.jpg")
        await ctx.send(embed=embed)


with open('token.txt', 'r') as f:
    token = f.read()

bot = CommandsBot()
bot.remove_command('help')
cog = General(bot)
bot.add_cog(cog)
bot.run(token)