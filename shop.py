import discord
import json
import asyncio
from discord.ext import commands, tasks
import general

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_user(self, user_id):
        if str(user_id) not in general.users_info:
            general.users_info[str(user_id)] = {"balance": 10000, "inventory": ["Standart"], "skin": "Standart"}


    async def check_product_and_balance_user(self, ctx, product, user_id):
        if product not in general.all_products:
            await ctx.send("Товар не найден.")
            return False
        elif general.all_products[product]["cost"] > general.users_info[user_id]["balance"]:
            await ctx.send("Недостаточно денег для совершения покупки.")
            return False
        return True


    async def save_users_info_file(self):
        with open('users_info.json', 'w') as f:
            json.dump(general.users_info, f)


    @commands.command(name='shop')
    async def show_all_products(self, ctx):
        embed = discord.Embed(title="Магазин", description="\u200B", color=discord.Colour.blurple())
        for product in general.all_products:
            embed.add_field(name=f'{product} - {general.all_products[product]["cost"]}₴', value=f'{general.all_products[product]["description"]}', inline=True)
        embed.set_image(url="https://compass-ssl.xboxlive.com/assets/35/68/35686a71-12b6-4e7c-afbf-c154df49c468.jpg?n=GHSpotlight_Artwork_1600.jpg")
        embed.set_footer(text="\nХочешь купить какой-то товар?\n*buy [название товара]", icon_url="https://cdn.iconscout.com/icon/premium/png-256-thumb/treasure-chest-11-1181010.png")
        embed.set_author(name="Cyberiiokep", icon_url="https://w0.pngwave.com/png/1003/599/pixel-art-mario-coin-png-clip-art.png")
        await ctx.send(embed=embed)

    @commands.command(name='buy')
    async def buy_prpduct_in_shop(self, ctx, *, product):
        await self.create_user(ctx.message.author.id)
        if not await self.check_product_and_balance_user(ctx, product, str(ctx.message.author.id)):
            return
        general.users_info[str(ctx.message.author.id)]["balance"] -= general.all_products[product]["cost"]
        general.users_info[str(ctx.message.author.id)]["inventory"].append(product)
        await asyncio.gather(self.save_users_info_file(), ctx.send(f"**{product}** добавлен в ваш инвентарь.\nТекущий баланс: {general.users_info[str(ctx.message.author.id)]['balance']} защекоинов."))


def setup(bot):
    bot.add_cog(Shop(bot))