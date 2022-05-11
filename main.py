import asyncio
import datetime
import logging
import os
import random
import sqlite3
from os import path

import coloredlogs
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord_components import Button, DiscordComponents
from pretty_help import DefaultMenu, PrettyHelp

import database_main
import keep_alive
import requests
import module_main

#! CAN CHANGE THIS
activity = "GBS - MŁOSY KORDEN, CYGAN9"


def logs():
    now_date = str(datetime.date.today())
    i = 1
    if path.exists(f"logs") == False:
        os.mkdir(f"logs")
    if path.exists(f"logs/SORT_BY_MODIFICATION_TIME.txt") == False:
        f = open(f"logs/SORT_BY_MODIFICATION_TIME.txt", "w")
        f.write("")
        f.close()
    if path.exists(f"logs/{now_date}-9.log") == True:
        os.remove(f"logs/{now_date}-9.log")
    if path.exists(f"logs/{now_date}.log") == True:
        while path.exists(f"logs/{now_date}-{i}.log") == True:
            i = i + 1
        os.rename(f"logs/{now_date}.log", f"logs/{now_date}-{i}.log")
    else:
        if path.exists(f"logs/latest.log") == True:
            os.rename(
                f"logs/latest.log",
                f"logs/{now_date}.log",
            )


logs()

logging.Formatter(fmt="%(asctime)s.%(msecs)03d", datefmt="%Y-%m-%d,%H:%M:%S")
logging.basicConfig(
    filename=f"logs/latest.log", format="%(asctime)s %(message)s", filemode="w"
)
logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

token_js = os.environ.get("TOKEN")
players_js = os.environ.get("PLAYERS")
dynamic_js = os.environ.get("DYNAMIC")
admin_js = requests.get(
    "https://raw.githubusercontent.com/Bre3n/DcBot/main/global_admin"
)
update_channel_js = os.environ.get("UPDATE_CHANNEL")
update_message_js = os.environ.get("UPDATE_MESSAGE")
update_channel_black_js = os.environ.get("UPDATE_CHANNEL_BLACK")
update_massage_black_js = os.environ.get("UPDATE_MESSAGE_BLACK")

description = f"""Bot do zarządzania dobrami organizacji przestępczych (w RolePlay'u)\n\nBot by: <@{admin_js}>"""

intents = discord.Intents.default()
intents.members = True

client = discord.Client()
bot = commands.Bot(
    command_prefix="?",
    description=description,
    intents=intents,
    help_command=PrettyHelp(no_category="Komendy"),
)


@bot.event
async def on_ready():
    os.system("cls")
    logger.debug(f"DEBUG - TOKEN = {token_js}")
    logger.debug(f"DEBUG - ADMIN = {admin_js}")
    if update_channel_js == "None":
        logger.error(f"ERROR - update_channel IN .env HAS NOT BEEN SET")
    else:
        logger.debug(f"DEBUG - UPDATE_CHANNEL = {update_channel_js}")
    if update_message_js == "None":
        logger.error(
            f"ERROR - UPDATE_MESSAGE = update_message_js IN .env HAS NOT BEEN SET"
        )
    else:
        logger.debug(f"DEBUG - UPDATE_MESSAGE = {update_message_js}")
    if path.exists("database.sqlite") == False:
        logger.error("ERROR - THERE IS NO DATABASE. CREATING A NEW ONE")
    record = database_main.connect_init()
    logger.debug(f"DEBUG - CONNECTED TO DATABASE")
    logger.debug("DEBUG - SQLite DATABASE VERSION: {}".format(record.replace("'", "")))
    dzien, czas = module_main.czas()
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=activity)
    )
    logger.debug("DEBUG - Logged as '{0.user}'".format(bot))
    logger.debug(f"DEBUG - BOT ACTIVITY: '{activity}'")
    logger.debug(f"DEBUG - ID = {bot.user.id}")
    bufor = module_main.check_ids()
    logger.debug(f"DEBUG - CHECK_IDS - {bufor}")
    logger.info(f" INFO - DATE = {dzien}/{czas}")


@bot.command(
    brief="Pokazuje obsługiwane przedmioty. ?help item po wiecej info",
    description="Pokazuje aktualnie obsługiwane przedmioty przez bota. Na przykład: money, pistol itp.",
)
async def item(ctx):
    logger.info(f" INFO - [item] - {ctx.message.author}")
    bufor = database_main.get_item()
    await ctx.send(bufor)


@bot.command(
    category="FiveM",
    brief="Pokazuje kto z serwera aktualnie gra. ?help players po wiecej info",
    description="Pokazuje kto z serwera discord aktualnie gra na serwerze FiveM.",
)
async def players(ctx):
    pos = 0
    logger.info(f" INFO - [players] - {ctx.message.author}")
    while pos <= 5:
        try:
            user = []
            member_list = []
            member_list = module_main.get_players(ctx)
            for i in range(len(member_list)):
                bufor = bot.get_user((int(str(member_list[i]).replace("e", ""))))
                if bufor != "":
                    user.append(bufor)
            if member_list == "error":
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
            if member_list == "error":
                pos += 1
            else:
                pos = 10
    if pos <= 5:
        await ctx.send(
            "Wygląda na to, że serwer jest wyłączony. Jeżeli sądzisz, że tak nie jest spróbuj jeszcze raz."
        )
    else:
        if len(user) != 0:
            mess = "```\nAktualnie na serwerze jest:\n"
            for i in range(len(member_list)):
                mess += f"{user[i]}\n"
            mess += "```"
            await ctx.send(mess)
        else:
            await ctx.send("Aktualnie nie ma nikogo na serwerze :(")


@bot.command(
    category="FiveM",
    brief="Pokazuje ile osób jest na serwerze. ?help dynamic po wiecej info",
    description="Pokazuje ile osób jest na serwerze, na maksymalną jego ilość. 100/200",
)
async def dynamic(ctx):
    pos = 0
    logger.info(f" INFO - [dynamic] - {ctx.message.author}")
    while pos <= 5:
        quote = module_main.get_dynamic()
        if quote == "error":
            pos += 1
        else:
            pos = 10
    if pos <= 6:
        await ctx.send(
            "Wygląda na to, że serwer jest wyłączony. Jeżeli sądzisz, że tak nie jest spróbuj jeszcze raz."
        )
    else:
        await ctx.send(quote)
        return 0


@bot.command(
    brief="Usuwa określoną ilość wiadomości. ?help cls po wiecej info",
    description="Usuwa określoną ilość wiadomości. ?cls <ilość wiadomości do usunięcia>",
)
async def cls(ctx, number):
    logger.info(f" INFO - [cls-{number}] - {ctx.message.author}")
    role = discord.utils.get(ctx.guild.roles, name="*AllowAdmin")
    if role in ctx.author.roles or str(ctx.message.author) == str(admin_js):
        if number.isnumeric() == True:
            if int(number) < 2:
                await ctx.send("Musisz wpisać liczbę większą, bądz równą 2")
            else:
                await ctx.channel.purge(limit=int(number) + 1)
        else:
            if str(number) == "console":
                os.system("cls")
                await ctx.channel.purge(limit=1)
            else:
                await ctx.send("Musisz wpisać liczbę!")
                await asyncio.sleep(1)
                await ctx.channel.purge(limit=1)
    else:
        await ctx.send("Niestety nie masz uprawnień aby tego dokonać!")
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=2)
    pos = False


@bot.command(
    brief="Za pomocą tej komendy możesz uzyskać dodatkowe permisje. ?help weryfikacja po wiecej info",
    description="Za użyciem tej komendy zostanie utworzona twoja baza danych oraz uzyskasz możliwość dodawania itemów do szafek. Na przykład 'add money 500'",
)
async def weryfikacja(ctx, user: discord.Member):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name="*AllowAdmin")
    if role in ctx.author.roles or str(ctx.message.author) == str(admin_js):
        role = discord.utils.get(ctx.guild.roles, name="*AllowChest")
        username = module_main.get_user(ctx, bot, user)
        logger.info(f" INFO - [weryfikacja] - {ctx.message.author} - {username}")
        await user.add_roles(role)
        database_main.create_user("U" + str(username))
        await ctx.send("Świetnie, użytkownik może już zarządzać swoim balansem.")
    else:
        await ctx.send(
            "Niestety, ale nie masz wystarczających permisji. Skontaktuj się z kimś z rangą **AllowAdmin**!"
        )


@bot.command(
    brief="Pokazuje obecny stan szafki, blacklisty. ?help update po wiecej info",
    description="Pokazuje obecny stan przedmiotów w szafce oraz blacklisty.",
)
async def update(ctx):
    logger.info(f" INFO - [update] - {ctx.message.author}")

    #! DO SZAFKI
    channel = bot.get_channel(int(update_channel_js))
    bufor = await module_main.get_update(ctx, bot, "chest")
    if update_message_js != "None":
        msg = await channel.fetch_message(int(update_message_js))
        await msg.edit(content=bufor)
    else:
        await channel.send(
            "Wiadomość wygenerowana na rzecz ID. Skopiuj ID wiadomości i wklej w UPDATE_MESSAGE .env"
        )

    #! DO BLACKLISTY
    bufor = await module_main.get_update(ctx, bot, "black")
    channel = bot.get_channel(int(update_channel_black_js))
    if update_massage_black_js != "None":
        msg = await channel.fetch_message(int(update_massage_black_js))
        await msg.edit(content=bufor)
    else:
        await channel.send(
            "Wiadomość wygenerowana na rzecz ID. Skopiuj ID wiadomości i wklej w UPDATE_MESSAGE_BLACK .env"
        )


@bot.command(
    brief="Pokazuje informacje o twojej szafce bądź szafce innego gracza. ?help info po wiecej info",
    description="Pokazuje informacje o twojej szafce bądź szafce innego gracza. Na przykłąd ?weryfikacja <użytkownik> (jeżeli chcesz zobaczyć stan kogoś szafki",
)
async def info(ctx, *message):
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
        logger.info(
            f" INFO - [info] - {ctx.message.author} - {await bot.fetch_user(int(message))}"
        )

        user = message
        bufor = await module_main.get_update(ctx, bot, "U" + str(user))
        await ctx.send(bufor)
    else:
        role = discord.utils.get(ctx.guild.roles, name="*AllowChest")
        if role in ctx.author.roles:
            logger.info(f" INFO - [info] - {ctx.message.author}")
            user = str(ctx.message.author)
            user = "U" + str(module_main.get_user(ctx, bot, user))
            bufor = await module_main.get_update(ctx, bot, user)
            await ctx.send(bufor)
        else:
            logger.info(f" INFO - [info] - {ctx.message.author} - Brak permisji")
            await ctx.send(
                "Niestety, ale nie możesz sprawdzić swojej szafki gdyż jej nie posiadasz.\nMusisz najpierw posiadać rangę **AllowChest**, którą możesz uzyskać u osoby z rangą **AllowAdmin**."
            )


@bot.command(
    brief="Zarządzanie balansem swojej szafki. ?help b po wiecej info",
    description="Zarządzanie balansem swojej szafki. Na przykład 'b money 500', albo 'b money -500'. Lista opsługiwanych itemów jest dostępna pod komendą '?item'",
)
async def b(ctx, *message):
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
                await ctx.send(
                    "Powiedz no, czy to coś w przodu twojej głowy to twarz czy dupa? ( ?b <item> <ile> )"
                )
                return 0
        else:
            user = str(ctx.message.author)
            user = "U" + str(module_main.get_user(ctx, bot, user))

        if len(message) == 2:
            messagestr = message[0] + " " + message[1]
        elif len(message) == 1:
            messagestr = str(message[0]) + " " + "1"
        elif len(message) > 3 or len(message) == 0 or str(message) == "()":
            await ctx.send(
                "Powiedz no, czy to coś w przodu twojej głowy to twarz czy dupa? ( ?b <item> <ile> )"
            )
            return 0
        database_main.create_user(user)
        await ctx.channel.purge(limit=1)
        username = user.replace("U", "")
        username = await bot.fetch_user(int(username))
        logger.info(
            f" INFO - [balance] - {ctx.message.author} - {messagestr} {username}"
        )
        mess = await database_main.balance_item(ctx, bot, user, messagestr)
        if mess != 0:
            await ctx.send(mess)
        else:
            await asyncio.sleep(1)
            await ctx.channel.purge(limit=1)
    else:
        await ctx.send(
            "Niestety, ale nie masz możliwości zarządzania swoją szafką!\nMusisz najpierw posiadać rangę **AllowChest**, którą możesz uzyskać u osoby z rangą **AllowAdmin**."
        )


@bot.command(
    brief="Zarządzanie blacklistą. ?help black po wiecej info",
    description="Wyświetlanie blacklisty/Zarządzanie blacklistą.\nNa przykład 'black'-Wyświetlanie blacklisty, lub 'black add Wiesław-Paleta Rozjebał-się-na-komendzie', albo 'black del <numer osoby>'.\n\nSPACJĘ POMIĘDZY SŁOWAMI ZASTĘPOWAĆ '-'!!!",
)
async def black(ctx, *message):
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
                        "Upewnij się że wszystkie argumenty zostały podane ( <kto> <powód> )\nPAMIĘTAJ O UŻYWANIU  ' - '  POMIĘDZY WYRAZAMI!!!"
                    )
                    return 0
                else:
                    logger.info(
                        f" INFO - [black-add] - {ctx.message.author} - {message[1]}"
                    )
                    await ctx.channel.purge(limit=1)
                    await database_main.blacklist(
                        ctx, bot, "add", message[1], message[2]
                    )
            elif message[0] == "del":
                if len(message) < 2 or len(message) > 2:
                    await ctx.send(
                        "Upewnij się że wszystkie argumenty zostały podane ( <numer osoby> )"
                    )
                else:
                    logger.info(
                        f" INFO - [black-del] - {ctx.message.author} - {message[1]}"
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
                    "Wiadomość wygenerowana na rzecz ID. Skopiuj ID wiadomości i wklej w UPDATE_MESSAGE_BLACK .env"
                )


@bot.command()
async def fun(ctx, message):
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
            await ctx.send(file=discord.File("konia.jpg"))
        await ctx.send(
            f"Słuchaj no {message}, to coś z przodu twojej głowy to twarz, czy dupa?"
        )


keep_alive.keep_alive()

bot.run(token_js)
