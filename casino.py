import json
import discord
import random
from discord.ext import commands, tasks
import asyncio

with open('users_info.json', 'r') as f:
    users_info = json.load(f)
with open('skins.json', 'r') as f:
    skins = json.load(f)

class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    async def user_embed(self, user_id, avatar):
        embed = discord.Embed(title = f"\u200B", description = f"**<:moneybag:748664223005016134>Баланс: {users_info[user_id]['balance']} защекоинов.\n<:shirt:751862336347701289>Скин: {users_info[user_id]['skin']}.**\n \u200B", color = discord.Colour.blurple())
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text="\nХочешь больше защекоинов? \nПиши *getmoney раз в час", icon_url="https://i.imgur.com/8Dz6ckB.png")
        return embed        


    async def win_embed_create(self, slots, avatar, balance, gain):
        embed = discord.Embed(title = f"Баланс: {balance} защекоинов.\nВыиграно: {gain} защекоинов.", description = f"{'|'.join(slots)}", color = 0x3d9970)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text="\nХочешь больше защекоинов? \nПиши *getmoney раз в час", icon_url="https://i.imgur.com/8Dz6ckB.png")
        return embed

    async def lose_embed_create(self, slots, avatar, balance, losing):
        embed = discord.Embed(title = f"Баланс: {balance} защекоинов.\nПроиграно: {losing} защекоинов.", description = f"{'|'.join(slots)}", color = 0xff4136)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text="\nХочешь больше защекоинов? \nПиши *getmoney раз в час", icon_url="https://i.imgur.com/8Dz6ckB.png")
        return embed

    async def scrolling_embed_create(self, slots, avatar, balance, bet):
        embed = discord.Embed(title = f"Баланс: {balance} защекоинов.\nСтавка: {bet} защекоинов.", description = f"{'|'.join(slots)}", color = discord.Colour.blurple())
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text="\nХочешь больше защекоинов? \nПиши *getmoney раз в час", icon_url="https://i.imgur.com/8Dz6ckB.png")
        return embed

    async def get_slots(self, skin):
        skin_slots = skins[skin]
        return [skin_slots[random.randint(0, len(skin_slots) - 1)], skin_slots[random.randint(0, len(skin_slots) - 1)], skin_slots[random.randint(0, len(skin_slots) - 1)]]


    async def win_bonus(self, skin, slots):
        return (skin.index(slots[0]) + 1) * 3

    async def scrolling(self, ctx, bet):
        user_id = str(ctx.message.author.id)
        user_skin = users_info[user_id]["skin"]
        slots = await self.get_slots(user_skin)
        scroll_message = await ctx.send(embed = await self.scrolling_embed_create(slots, ctx.message.author.avatar_url, users_info[user_id]["balance"], bet))
        for _ in range(4):
            slots = await self.get_slots(user_skin)
            await scroll_message.edit(embed = await self.scrolling_embed_create(slots, ctx.message.author.avatar_url, users_info[user_id]["balance"], bet))
            await asyncio.sleep(0.5)
        if slots[0] == slots[1] and slots[0] == slots[2]:
            bonus = await self.win_bonus(skins[user_skin], slots)
            gain = bet * bonus
            print(bonus, gain)
            users_info[user_id]["balance"] += gain
            await scroll_message.edit(embed = await self.win_embed_create(slots, ctx.message.author.avatar_url, users_info[user_id]["balance"], gain))
            return
        users_info[user_id]["balance"] -= bet
        await scroll_message.edit(embed = await self.lose_embed_create(slots, ctx.message.author.avatar_url, users_info[user_id]["balance"], bet))
        return

    async def create_user(self, user_id):
        users_info[str(user_id)] = {"balance": 10000, "inventory": ["Стандартный"], "skin": "Стандартный"}

    async def save_users_info_file(self):
        with open('users_info.json', 'w') as f:
            json.dump(users_info, f)

    async def check_bet(self, ctx, bet):
        user_id = str(ctx.message.author.id)
        if users_info[user_id]["balance"] < bet:
            await ctx.send("Твой баланс меньше, чем ставка.")
            return False
        elif bet <= 0:
            await ctx.send("Невозможно поставить ставку, которая меньше или равна нулю.")
            return False
        return True 

    @commands.command(name='casino')
    async def start_play_in_casino(self, ctx, bet: int):
        if str(ctx.message.author.id) not in users_info:
            await self.create_user(ctx.message.author.id)
            await self.save_users_info_file()
        if not await self.check_bet(ctx, bet):
            return
        await self.scrolling(ctx, bet)
        await self.save_users_info_file()

    @commands.command(name='info')
    async def infotmation_about_user(self, ctx):
        await ctx.send(embed = await self.user_embed(str(ctx.message.author.id), ctx.message.author.avatar_url))

    
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(name='getmoney')
    async def get_money(self, ctx):
        if str(ctx.message.author.id) not in users_info:
            self.create_user(ctx.message.author.id)
        gift = random.randint(1, 1000)
        users_info[str(ctx.message.author.id)]["balance"] += gift
        await asyncio.gather(ctx.send(f"+{gift} защекоинов!"), self.save_users_info_file())
        
        
        

def setup(bot):
    bot.add_cog(Casino(bot))
