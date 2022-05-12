import asyncio
import os
import random
import sqlite3
from os import path
from unicodedata import name

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button, DiscordComponents
from pretty_help import DefaultMenu, PrettyHelp

import database_main
import keep_alive
import module_main

#! CAN CHANGE THIS
activity = "GBS - MŁOSY KORDEN, CYGAN9"


token_js = os.environ.get("TOKEN")
players_js = os.environ.get("PLAYERS")
dynamic_js = os.environ.get("DYNAMIC")
update_channel_js = os.environ.get("UPDATE_CHANNEL")
update_message_js = os.environ.get("UPDATE_MESSAGE")
update_channel_black_js = os.environ.get("UPDATE_CHANNEL_BLACK")
update_massage_black_js = os.environ.get("UPDATE_MESSAGE_BLACK")
info, debug, error, critical = "info", "debug", "error", "critical"

intents = discord.Intents.default()
intents.members = True

menu = DefaultMenu(page_left="👍", page_right="👎")
# Custom ending note
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}\nBot by: <@455430663114326016>"

client = discord.Client()
bot = commands.Bot(
    command_prefix="?",
    intents=intents,
    help_command=PrettyHelp(
        menu=menu, ending_note=ending_note, index_title="GTA RP BOT", show_index=False
    ),
)

admin_js = str(bot.get_user(455430663114326016))


@bot.event
async def on_ready():
    os.system("cls")
    if update_channel_js == "None":
        module_main.log(error, f"ERROR - update_channel IN .env HAS NOT BEEN SET")
    else:
        module_main.log(debug, f"DEBUG - UPDATE_CHANNEL = {update_channel_js}")
    if update_message_js == "None":
        module_main.log(
            error,
            f"ERROR - UPDATE_MESSAGE = update_message_js IN .env HAS NOT BEEN SET",
        )
    else:
        module_main.log(debug, f"DEBUG - UPDATE_MESSAGE = {update_message_js}")
    if path.exists("database.sqlite") == False:
        module_main.log(error, "ERROR - THERE IS NO DATABASE. CREATING A NEW ONE")
    record = database_main.connect_init()
    module_main.log(debug, f"DEBUG - CONNECTED TO DATABASE")
    module_main.log(
        debug, "DEBUG - SQLite DATABASE VERSION: {}".format(record.replace("'", ""))
    )
    dzien, czas = module_main.czas()
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=activity)
    )
    module_main.log(debug, "DEBUG - Logged as '{0.user}'".format(bot))
    module_main.log(debug, f"DEBUG - BOT ACTIVITY: '{activity}'")
    module_main.log(debug, f"DEBUG - ID = {bot.user.id}")
    bufor = module_main.check_ids()
    module_main.log(debug, f"DEBUG - CHECK_IDS - {bufor}")
    module_main.log(debug, f"DEBUG - DATE = {dzien}/{czas}")


class FiveM(commands.Cog, name="1. FiveM"):
    """FiveM commands"""

    @commands.command(
        brief="Show supported items. ?help item for more info",
        description="Shows currently supported items by bot. For example: money, pistol itp.",
    )
    async def items(self, ctx: commands.Context):
        module_main.log(debug, f"DEBUG - [item] - {ctx.message.author}")
        bufor = database_main.get_item()
        await ctx.send(bufor)

    @commands.command(
        brief="Shows who from DC Server is actualy playing on server. ?help players for more info",
    )
    async def players(self, ctx: commands.Context):
        pos = 0
        module_main.log(debug, f"DEBUG - [players] - {ctx.message.author}")
        while pos <= 5:
            try:
                user = []
                member_list = []
                member_list = module_main.get_players(ctx)
                for i in range(len(member_list)):
                    bufor = bot.get_user((int(str(member_list[i]).replace("e", ""))))
                    if bufor != "":
                        user.append(bufor)
                if member_list == error:
                    pos += 1
                else:
                    pos = 10
            except Exception:
                user = []
                member_list = []
                member_list = module_main.get_players(ctx)
                for i in range(len(member_list)):
                    bufor = bot.get_user((int(str(member_list[i]).replace("e", ""))))
                    if bufor != "":
                        user.append(bufor)
                if member_list == error:
                    pos += 1
                else:
                    pos = 10
        if pos <= 5:
            await ctx.send(
                "It looks like server is down. If you don't think this is the case, please try again."
            )
        else:
            if len(user) != 0:
                mess = "```\nCurrently playing on server:\n"
                for i in range(len(member_list)):
                    mess += f"{user[i]}\n"
                mess += "```"
                await ctx.send(mess)
            else:
                await ctx.send("Is anyone there? :( No")

    @commands.command(
        brief="Shows how many players currently playing on the server. F.E 100/200",
    )
    async def dynamic(self, ctx: commands.Context):
        pos = 0
        module_main.log(debug, f"DEBUG - [dynamic] - {ctx.message.author}")
        while pos <= 5:
            quote = module_main.get_dynamic()
            if quote == error:
                pos += 1
            else:
                pos = 10
        if pos <= 6:
            await ctx.send(
                "It looks like server is down. If you don't think this is the case, please try again."
            )
        else:
            await ctx.send(quote)
            return 0


class Admin(commands.Cog, name="4. Admin"):
    """Admin commands"""

    @commands.command(
        brief="Clears the specifed amount of messages. ?cls <amount of messages for delete>",
    )
    async def cls(self, ctx: commands.Context, number):
        module_main.log(debug, f"DEBUG - [cls-{number}] - {ctx.message.author}")
        role = discord.utils.get(ctx.guild.roles, name="*AllowAdmin")
        if role in ctx.author.roles or str(ctx.message.author) == str(admin_js):
            if number.isnumeric() == True:
                if int(number) < 2:
                    await ctx.send("You must enter value >= 2!")
                else:
                    await ctx.channel.purge(limit=int(number) + 1)
            else:
                if str(number) == "console":
                    os.system("cls")
                    await ctx.channel.purge(limit=1)
                else:
                    await ctx.send("You must enter value >= 2!")
                    await asyncio.sleep(1)
                    await ctx.channel.purge(limit=1)
        else:
            await ctx.send("Unfortunately, you do not have sufficient permissions!")
            await asyncio.sleep(1)
            await ctx.channel.purge(limit=2)
        pos = False

    @commands.command(
        brief="With this command you can give **AllowChest** permissions.",
    )
    async def verification(self, ctx: commands.Context, user: discord.Member):
        member = ctx.message.author
        role = discord.utils.get(member.guild.roles, name="*AllowAdmin")
        if role in ctx.author.roles or str(ctx.message.author) == str(admin_js):
            role = discord.utils.get(ctx.guild.roles, name="*AllowChest")
            username = module_main.get_user(ctx, bot, user)
            module_main.log(
                debug, f"DEBUG - [verification] - {ctx.message.author} - {username}"
            )
            await user.add_roles(role)
            database_main.create_user("U" + str(username))
            await ctx.send("Great, the user can now manage his balance.")
        else:
            await ctx.send(
                "Unfortunately, you do not have sufficient permissions! Please contact someone with **AllowAdmin** role!"
            )


class AllowChest(commands.Cog, name="2. Management"):
    """Blacklist and locker commands"""

    @commands.command(
        brief="Updates info about global chest and blacklist. (if for some reason it didn't happen automatically)",
    )
    async def update(self, ctx: commands.Context):
        module_main.log(debug, f"DEBUG - [update] - {ctx.message.author}")

        #! DO SZAFKI
        channel = bot.get_channel(int(update_channel_js))
        bufor = await module_main.get_update(ctx, bot, "chest")
        if update_message_js != "None":
            msg = await channel.fetch_message(int(update_message_js))
            await msg.edit(content=bufor)
        else:
            await channel.send(
                "Message generated for the ID. Copy the message ID and paste in UPDATE_MESSAGE .env"
            )

        #! DO BLACKLISTY
        bufor = await module_main.get_update(ctx, bot, "black")
        channel = bot.get_channel(int(update_channel_black_js))
        if update_massage_black_js != "None":
            msg = await channel.fetch_message(int(update_massage_black_js))
            await msg.edit(content=bufor)
        else:
            await channel.send(
                "Message generated for the ID. Copy the message ID and paste in UPDATE_MESSAGE_BLACK .env"
            )

    @commands.command(
        brief="Shows information about your chest or another player's chest.",
    )
    async def info(self, ctx: commands.Context, *message):
        if str(message) != "()":
            message = (
                str(message)
                .replace("(", "")
                .replace(")", "")
                .replace("'", "")
                .replace(",", "")
                .replace("@", "")
                .replace("<", "")
                .replace(">", "")
                .replace("!", "")
            )
            module_main.log(
                debug,
                f"DEBUG - [info] - {ctx.message.author} - {await bot.fetch_user(int(message))}",
            )

            user = message
            bufor = await module_main.get_update(ctx, bot, "U" + str(user))
            await ctx.send(bufor)
        else:
            role = discord.utils.get(ctx.guild.roles, name="*AllowChest")
            if role in ctx.author.roles:
                module_main.log(debug, f"DEBUG - [info] - {ctx.message.author}")
                user = str(ctx.message.author)
                user = "U" + str(module_main.get_user(ctx, bot, user))
                bufor = await module_main.get_update(ctx, bot, user)
                await ctx.send(bufor)
            else:
                module_main.log(
                    debug, f"DEBUG - [info] - {ctx.message.author} - No permission"
                )
                await ctx.send(
                    "Unfortunately, you can't check your locker because you don't have one.\nYou must first have a rank **AllowChest**, which you can get from a person with a rank **AllowAdmin**."
                )

    @commands.command(
        brief="Balance management of your locker. ?help b for more info",
        description="Balance management of your locker. F.E 'b money 500', or 'b money -500'. List of supported items on '?item'",
    )
    async def b(self, ctx: commands.Context, *message):
        role = discord.utils.get(ctx.guild.roles, name="*AllowChest")
        if role in ctx.author.roles:
            message = (
                str(message)
                .replace("(", "")
                .replace(")", "")
                .replace("'", "")
                .replace(",", "")
                .replace("@", "")
                .replace("<", "")
                .replace(">", "")
                .replace("!", "")
            )
            message = str(message).split()
            if len(message) == 3:
                role = discord.utils.get(ctx.guild.roles, name="*AllowAdmin")
                if role in ctx.author.roles or str(ctx.message.author) == str(admin_js):
                    user = "U" + str(message[2])
                    messagestr = str(message[0]) + " " + str(message[1])
                else:
                    await ctx.send("Hmm, that not what I meant ( ?b <item> <amount> )")
                    return 0
            else:
                user = str(ctx.message.author)
                user = "U" + str(module_main.get_user(ctx, bot, user))

            if len(message) == 2:
                messagestr = message[0] + " " + message[1]
            elif len(message) == 1:
                messagestr = str(message[0]) + " " + "1"
            elif len(message) > 3 or len(message) == 0 or str(message) == "()":
                await ctx.send("Hmm, that not what I meant ( ?b <item> <amount> )")
                return 0
            database_main.create_user(user)
            await ctx.channel.purge(limit=1)
            username = user.replace("U", "")
            username = await bot.fetch_user(int(username))
            module_main.log(
                debug,
                f"DEBUG - [balance] - {ctx.message.author} - {messagestr} {username}",
            )
            mess = await database_main.balance_item(ctx, bot, user, messagestr)
            if mess != 0:
                await ctx.send(mess)
            else:
                await asyncio.sleep(1)
                await ctx.channel.purge(limit=1)
        else:
            await ctx.send(
                "Unfortunately, you can't check your locker because you don't have one.\nYou must first have a rank **AllowChest**, which you can get from a person with a rank **AllowAdmin**."
            )

    @commands.command(
        brief="Blacklist management. ?help black for more info",
        description="Blacklist management.\nFor example 'black'-Shows blacklist, or 'black add Wiesław-Paleta Rozjebał-się-na-komendzie', or 'black del <personal ID>'.\n\nA SPACE BETWEEN THE WORDS REPLACE '-' !!!",
    )
    async def black(self, ctx: commands.Context, *message):
        role = discord.utils.get(ctx.guild.roles, name="*AllowChest")
        if role in ctx.author.roles:
            message = (
                str(message)
                .replace("(", "")
                .replace(")", "")
                .replace("'", "")
                .replace(",", "")
                .replace("@", "")
                .replace("<", "")
                .replace(">", "")
                .replace("!", "")
            )
            message = str(message).split()
            if len(message) > 0:
                if message[0] == "add":
                    if len(message) < 3 or len(message) > 3:
                        await ctx.send(
                            "Make sure all arguments are given ( <who> <reason> )\nREMEMBER TO USE  ' - '  BETWEEN WORDS!!!"
                        )
                        return 0
                    else:
                        module_main.log(
                            debug,
                            f"DEBUG - [black-add] - {ctx.message.author} - {message[1]}",
                        )
                        await ctx.channel.purge(limit=1)
                        await database_main.blacklist(
                            ctx, bot, "add", message[1], message[2]
                        )
                elif message[0] == "del":
                    if len(message) < 2 or len(message) > 2:
                        await ctx.send(
                            "Make sure all arguments are given ( <personal ID> )"
                        )
                    else:
                        module_main.log(
                            debug,
                            f"DEBUG - [black-del] - {ctx.message.author} - {message[1]}",
                        )
                        await ctx.channel.purge(limit=1)
                        await database_main.blacklist(ctx, bot, "del", message[1], "")
            else:
                await ctx.channel.purge(limit=1)
                bufor = await module_main.get_update(ctx, bot, "black")
                channel = bot.get_channel(int(update_channel_black_js))
                if update_massage_black_js != "None":
                    msg = await channel.fetch_message(int(update_massage_black_js))
                    await msg.edit(content=bufor)
                else:
                    await channel.send(
                        "Message generated for the ID. Copy the message ID and paste in UPDATE_MESSAGE_BLACK .env"
                    )


class Utils(commands.Cog, name="3. Utils"):
    """Utils"""

    @commands.command()
    async def fun(self, ctx: commands.Context, message):
        await ctx.channel.purge(limit=1)
        bufor = (
            str(message)
            .replace("(", "")
            .replace(")", "")
            .replace("'", "")
            .replace(",", "")
            .replace("@", "")
            .replace("<", "")
            .replace(">", "")
            .replace("!", "")
        )
        user = module_main.get_user(ctx, bot, ctx.message.author)
        buforr = await bot.fetch_user(int(bufor))
        if str(buforr) == str(admin_js):
            bufor = module_main.get_user(ctx, bot, ctx.message.author)
            await ctx.send(
                f"Słuchaj no <@{user}>, o coś z przodu twojej głowy to twarz, czy dupa?"
            )
        else:
            rand = random.randint(1, 5)
            if rand == 1:
                pass
                # await ctx.send(file=discord.File("konia.jpg"))
            await ctx.send(
                f"Słuchaj no {message}, to coś z przodu twojej głowy to twarz, czy dupa?"
            )


def run():
    bot.add_cog(FiveM(bot))
    bot.add_cog(Admin(bot))
    bot.add_cog(AllowChest(bot))
    bot.add_cog(Utils(bot))
    bot.run(os.environ["TOKEN"])
    bot.run(token_js)


run()

keep_alive.keep_alive()
