import discord
import json
import asyncio
from discord.ext import commands, tasks
import general
import random


class Chest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    async def save_users_info_file(self):
        with open('users_info.json', 'w') as f:
            json.dump(general.users_info, f)


    async def create_user(self, user_id):
        if str(user_id) not in general.users_info:
            general.users_info[str(user_id)] = {"balance": 10000, "inventory": ["Standart"], "skin": "Standart"}

    
    async def check_chest(self, ctx, chest):
        if chest not in general.all_chests:
            await ctx.send(f"Cундука **{chest}** не существует.")
            return False
        elif chest not in general.users_info[str(ctx.message.author.id)]["inventory"]:
            await ctx.send(f"**{chest}** нет в вашем инвентаре.")
            return False
        return True

    async def choice_item_from_a_chest(self, chest):
        items_range = general.all_chests[chest]
        return random.choice(items_range)


    @commands.command(name='open')
    async def open_chest(self, ctx, *, chest):
        if str(ctx.message.author.id) not in general.users_info:
            await self.create_user(ctx.message.author.id)
        if not await self.check_chest(ctx, chest):
            return
        general.users_info[str(ctx.message.author.id)]["inventory"].remove(chest)
        open_chest_message = await ctx.send("Открываем сундук, подождите...")
        item = await self.choice_item_from_a_chest(chest)
        if type(item) == int:
            general.users_info[str(ctx.message.author.id)]["balance"] += item
            await asyncio.gather(open_chest_message.edit(content=f"В сундуке находится...\n**<:moneybag:748664223005016134>{item} защекоинов!**"), self.save_users_info_file())
        else:
            general.users_info[str(ctx.message.author.id)]["inventory"].append(item)
            await asyncio.gather(open_chest_message.edit(content=f"В сундуке находится...\n**<:shirt:751862336347701289>{item} скин!**"), self.save_users_info_file())


def setup(bot):
    bot.add_cog(Chest(bot))