import json
import discord
import random
from discord.ext import commands, tasks
import asyncio
from datetime import timedelta
import general

class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    async def user_embed(self, user_id, avatar):
        embed = discord.Embed(title = f"\u200B", description = f"**<:moneybag:748664223005016134>Баланс: {general.users_info[user_id]['balance']} защекоинов.\n<:shirt:751862336347701289>Скин: {general.users_info[user_id]['skin']}.\n<:luggage:752332031240700044>Инвентарь: *inv **\n \u200B", color = discord.Colour.blurple())
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
        skin_slots = general.skins[skin]
        return [skin_slots[random.randint(0, len(skin_slots) - 1)], skin_slots[random.randint(0, len(skin_slots) - 1)], skin_slots[random.randint(0, len(skin_slots) - 1)]]


    async def win_bonus(self, skin, slots):
        return (skin.index(slots[0]) + 1) * 3

    async def scrolling(self, ctx, bet):
        user_id = str(ctx.message.author.id)
        user_skin = general.users_info[user_id]["skin"]
        slots = await self.get_slots(user_skin)
        general.users_info[user_id]["balance"] -= bet
        scroll_message = await ctx.send(embed = await self.scrolling_embed_create(slots, ctx.message.author.avatar_url, general.users_info[user_id]["balance"], bet))
        for _ in range(4):
            slots = await self.get_slots(user_skin)
            await scroll_message.edit(embed = await self.scrolling_embed_create(slots, ctx.message.author.avatar_url, general.users_info[user_id]["balance"], bet))
            await asyncio.sleep(0.5)
        if slots[0] == slots[1] and slots[0] == slots[2]:
            bonus = await self.win_bonus(general.skins[user_skin], slots)
            gain = bet * bonus
            print(bonus, gain)
            general.users_info[user_id]["balance"] += gain
            await scroll_message.edit(embed = await self.win_embed_create(slots, ctx.message.author.avatar_url, general.users_info[user_id]["balance"], gain))
            return
        await scroll_message.edit(embed = await self.lose_embed_create(slots, ctx.message.author.avatar_url, general.users_info[user_id]["balance"], bet))
        return

    async def create_user(self, user_id):
        general.users_info[str(user_id)] = {"balance": 10000, "inventory": ["Standart"], "skin": "Standart"}

    async def save_users_info_file(self):
        with open('users_info.json', 'w') as f:
            json.dump(general.users_info, f)

    async def check_bet(self, ctx, bet):
        user_id = str(ctx.message.author.id)
        if general.users_info[user_id]["balance"] < bet:
            await ctx.send("Твой баланс меньше, чем ставка.")
            return False
        elif bet <= 0:
            await ctx.send("Невозможно поставить ставку, которая меньше или равна нулю.")
            return False
        return True 

    @commands.command(name='casino')
    async def start_play_in_casino(self, ctx, bet: int):
        if str(ctx.message.author.id) not in general.users_info:
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
        if str(ctx.message.author.id) not in general.users_info:
            await self.create_user(ctx.message.author.id)
        gift = random.randint(1, 1000)
        general.users_info[str(ctx.message.author.id)]["balance"] += gift
        await asyncio.gather(ctx.send(f"+{gift} защекоинов!"), self.save_users_info_file())

    async def get_inventory_user(self, user_id):
        inventory = []
        for item in general.users_info[str(user_id)]["inventory"]:
            if "chest" in item:
                inventory.append(f"**<:briefcase:752328412340682873>{item}**")
            else:
                inventory.append(f"**<:shirt:751862336347701289>{item}**")
        return inventory


    @commands.command(name='inv')
    async def show_inventory_user(self, ctx):
        if str(ctx.message.author.id) not in general.users_info:
            await self.create_user(ctx.message.author.id)
        inventory = await self.get_inventory_user(ctx.message.author.id)
        embed = discord.Embed(title="Инвентарь", description="\u200B", color=discord.Colour.blurple())
        embed.add_field(name="\u200B", value=", ".join(inventory))
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_author(name="Cyberiiokep", icon_url="https://w0.pngwave.com/png/1003/599/pixel-art-mario-coin-png-clip-art.png")
        await ctx.send(embed=embed)

    
    @commands.command(name='skin')
    async def set_skin_for_user(self, ctx, *, skin):
        if str(ctx.message.author.id) not in general.users_info:
            await self.create_user(ctx.message.author.id)
        if skin not in general.users_info[str(ctx.message.author.id)]['inventory']:
            await ctx.send(f"**{skin}** нет в вашем инвентаре.")
            return
        elif "chest" in skin:
            await ctx.send(f"Сундук нельзя установить как скин.")
            return
        general.users_info[str(ctx.message.author.id)]['skin'] = skin
        await asyncio.gather(ctx.send(f"Вы установили скин **{skin}**"), self.save_users_info_file())

    
    @get_money.error
    async def get_money_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            error_str = str(error).split()
            time = error_str[7]
            time = int(time[:len(time)-4])
            print(time)
            await ctx.send(f"Вы уже использовали эту команду. Попробуйте через: **{str(timedelta(seconds=time))}**")
            
        
def setup(bot):
    bot.add_cog(Casino(bot))
