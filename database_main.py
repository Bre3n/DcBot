import os
import sqlite3
from asyncio import sleep

import module_main

przedmioty = [
    "1;money",
    "2;brudne",
    "3;mefedron",
    "4;amfetamina",
    "5;marihuana",
    "6;pistol",
    "7;mk2",
    "8;vintage",
    "9;pukawka",
    "10;pukawkamk2",
    "11;ammo",
]

players_js = os.environ.get("PLAYERS")
dynamic_js = os.environ.get("DYNAMIC")
bot_id_js = os.environ.get("BOT_ID")
update_channel_js = os.environ.get("UPDATE_CHANNEL")
update_massage_js = os.environ.get("UPDATE_MESSAGE")
update_channel_black_js = os.environ.get("UPDATE_CHANNEL_BLACK")
update_massage_black_js = os.environ.get("UPDATE_MESSAGE_BLACK")


def get_item():
    bufor = module_main.get_item(przedmioty)
    return bufor


def create_row(user):
    conn = sqlite3.connect("database.sqlite")
    sql = conn.cursor()
    for i in range(len(przedmioty)):
        bufor = przedmioty[i].split(";")
        sql.execute(f"SELECT rowid FROM {user} WHERE przedmiot = ?", (bufor[1],))
        data = sql.fetchall()
        if len(data) == 0:
            sql.execute(
                f""" INSERT INTO {user}(id,przedmiot,ile)
                    VALUES({bufor[0]},'{bufor[1]}',0) """
            )
    conn.commit()
    conn.close()


def create_user(user):
    jakie_przedmioty = []
    conn = sqlite3.connect("database.sqlite")
    sql = conn.cursor()

    sql.execute(
        f""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{user}' """
    )

    if sql.fetchone()[0] == 1:
        for i in range(len(przedmioty)):
            bufor = przedmioty[i].split(";")
            jakie_przedmioty.append(str(bufor[0]))
            sql.execute(
                f"SELECT rowid FROM {user}",
            )
            data = sql.fetchall()
            for i in range(len(data)):
                bufor = str(data[i]).replace("(", "").replace(",", "").replace(")", "")
                if bufor not in jakie_przedmioty:
                    sql.execute(f"DELETE FROM {user} WHERE id = ?", (bufor,))
    else:
        sql.execute(
            f"""CREATE TABLE {user}
                (id INTEGER, przedmiot TEXT, ile INTEGER)"""
        )
    conn.commit()
    conn.close()
    create_row(user)


def create_table():
    jakie_przedmioty = []
    conn = sqlite3.connect("database.sqlite")
    sql = conn.cursor()

    sql.execute(
        f""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='chest' """
    )

    if sql.fetchone()[0] == 0:
        sql.execute(
            f"""CREATE TABLE chest
                (id INTEGER, przedmiot TEXT, ile INTEGER)"""
        )
    conn.commit()
    for i in range(len(przedmioty)):
        bufor = przedmioty[i].split(";")
        jakie_przedmioty.append(str(bufor[0]))
        sql.execute("SELECT rowid FROM chest WHERE przedmiot = ?", (bufor[1],))
        data = sql.fetchall()
        if len(data) == 0:
            sql.execute(
                f""" INSERT INTO chest(id,przedmiot,ile)
                    VALUES({bufor[0]},'{bufor[1]}',0) """
            )
    conn.commit()
    sql.execute(
        "SELECT rowid FROM chest",
    )
    data = sql.fetchall()
    for i in range(len(data)):
        bufor = str(data[i]).replace("(", "").replace(",", "").replace(")", "")
        if bufor not in jakie_przedmioty:
            sql.execute(f"DELETE FROM chest WHERE id = ?", (bufor,))
    conn.commit()

    # * BLACKLISTA
    sql.execute(
        f""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='blacklist' """
    )
    if sql.fetchone()[0] == 0:
        sql.execute(
            """CREATE TABLE blacklist
                (kto TEXT, powod TEXT)"""
        )
    conn.commit()
    conn.close()


def connect_init():
    conn = sqlite3.connect("database.sqlite")
    sql = conn.cursor()

    sqlite_select_Query = "select sqlite_version();"
    sql.execute(sqlite_select_Query)
    record = sql.fetchall()
    record = (
        str(record)
        .replace("[", "")
        .replace("(", "")
        .replace("", "")
        .replace(",", "")
        .replace(")", "")
        .replace("]", "")
    )
    create_table()
    conn.close()
    return record


async def balance_item(ctx, bot, user, messagestr):
    message = []
    message = str(messagestr).split()
    conn = sqlite3.connect("database.sqlite")
    sql = conn.cursor()
    sql.execute(f"SELECT rowid FROM {user} WHERE przedmiot = ?", (str(message[0]),))
    data = sql.fetchall()
    if len(data) == 0:
        await ctx.send(
            "Przedmiot nie jest osługiwany. Sprawdź obługiwane itemy przez **?item**"
        )
        return 0
    else:
        #! DLA UZYTKOWNIKA
        sql.execute(f"SELECT ile FROM {user} WHERE przedmiot = ?", (str(message[0]),))
        data = sql.fetchall()
        data = (
            str(data)
            .replace("(", "")
            .replace(",", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
        )
        data = int(data) + int(message[1])
        sql.execute(
            f"UPDATE {user} SET ile = {str(data)} WHERE przedmiot = ?",
            (str(message[0]),),
        )
        #! DLA OGÓŁU
        sql.execute(f"SELECT ile FROM chest WHERE przedmiot = ?", (str(message[0]),))
        dataa = sql.fetchall()
        dataa = (
            str(dataa)
            .replace("(", "")
            .replace(",", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
        )
        dataa = int(dataa) + int(message[1])
        sql.execute(
            f"UPDATE chest SET ile = {str(dataa)} WHERE przedmiot = ?",
            (str(message[0]),),
        )
        conn.commit()
        conn.close()
        channel = bot.get_channel(int(update_channel_js))
        bufor = await module_main.get_update(ctx, bot, "chest")
        if update_massage_js != "None":
            msg = await channel.fetch_message(int(update_massage_js))
            await msg.edit(content=bufor)
        else:
            await channel.send(
                "Wiadomość wygenerowana na rzecz ID. Skopiuj ID wiadomości i wklej w UPDATE_MESSAGE .env"
            )
        user = user.replace("U", "")
        user = bot.get_user(int(user))
        if int(message[1]) >= 0:
            mess = f"Dodano {message[0]} {message[1]} do balansu dla {user}. Aktualne balans to {data}"
        else:
            mess = f"Odjęto {message[0]} {message[1]} od balansu dla {user}. Aktualny balans to {data}"
    return mess


async def blacklist(ctx, bot, var, name, powod):
    conn = sqlite3.connect("database.sqlite")
    sql = conn.cursor()
    if var == "add":
        sql.execute("SELECT rowid FROM blacklist WHERE kto = ?", (name,))
        data = sql.fetchall()
        if len(data) == 1:
            await ctx.send(
                "Personalia zostały już dodane do blacklisty! Aby zmodyfikować powód, usuń je z blacklisty."
            )
        else:
            sql.execute(
                f""" INSERT INTO blacklist (kto,powod)
                    VALUES('{name}','{powod}') """
            )
            conn.commit()
            conn.close()
            name = name.replace("-", " ")
            await ctx.send(f"{name} został dodany do blacklisty  :skull_crossbones:")
            bufor = await module_main.get_update(ctx, bot, "black")
            channel = bot.get_channel(int(update_channel_black_js))
            if update_massage_black_js != "None":
                msg = await channel.fetch_message(int(update_massage_black_js))
                await msg.edit(content=bufor)
            else:
                await channel.send(
                    "Wiadomość wygenerowana na rzecz ID. Skopiuj ID wiadomości i wklej w UPDATE_MESSAGE_BLACK .env"
                )
    elif var == "del":
        sql.execute("SELECT kto FROM blacklist")
        data = sql.fetchall()
        data = (
            str(data)
            .replace("(", "")
            .replace(",", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
        )
        data = data.split()
        bufor = data[int(name) - 1]
        sql.execute("DELETE from blacklist WHERE kto = ?", (bufor,))
        conn.commit()
        conn.close()
        await ctx.send(f"Usunięto {bufor} z blacklisty  :angel:")
        bufor = await module_main.get_update(ctx, bot, "black")
        channel = bot.get_channel(int(update_channel_black_js))
        if update_massage_black_js != "None":
            msg = await channel.fetch_message(int(update_massage_black_js))
            await msg.edit(content=bufor)
        else:
            await channel.send(
                "Wiadomość wygenerowana na rzecz ID. Skopiuj ID wiadomości i wklej w UPDATE_MESSAGE_BLACK .env"
            )
    elif var == "info":
        sql.execute("SELECT rowid FROM blacklist")
        data = sql.fetchall()
        if len(data) == 0:
            mess = "```\nNie ma nikogo na blackliście!\n```"
        else:
            sql.execute("SELECT kto FROM blacklist")
            data = sql.fetchall()
            data = (
                str(data)
                .replace("(", "")
                .replace(",", "")
                .replace(")", "")
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
            )
            data = data.split()
            sql.execute("SELECT powod FROM blacklist")
            dataa = sql.fetchall()
            dataa = (
                str(dataa)
                .replace("(", "")
                .replace(",", "")
                .replace(")", "")
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
            )
            dataa = dataa.split()
            mess = ":skull_crossbones:  :skull_crossbones:  :skull_crossbones:\n```\nBLACKLISTA\n\n"
            for i in range(len(data)):
                bufor = data[i].replace("-", " ")
                buforr = dataa[i].replace("-", " ")
                mess += f"{i+1}. {bufor} - {buforr}\n"
            mess += "```"
        conn.close()
        return mess
