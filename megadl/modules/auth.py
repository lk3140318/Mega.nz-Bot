# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Authorize mega account of users


from pyrogram import filters
from pyrogram.types import Message

from megadl import MegaCypher


@MegaCypher.on_message(filters.command("login"))
@MegaCypher.run_checks
async def mega_logger(client: MegaCypher, msg: Message):
    user_id = msg.chat.id

    email = await client.ask(user_id, "Enter your Mega.nz email:")
    if not email:
        return await msg.reply("You must send your Mega.nz email in order to login")
    password = await client.ask(user_id, "Enter your Mega.nz password:")
    if not password:
        return await msg.reply("You must send your Mega.nz password in order to login")

    # encrypt the email and password for security
    email = client.cipher.encrypt(email.text.encode())
    password = client.cipher.encrypt(password.text.encode())

    await client.database.mega_login(user_id, email, password)
    await msg.reply("Successfully logged in!")


@MegaCypher.on_message(filters.command("logout"))
@MegaCypher.run_checks
async def mega_logoutter(client: MegaCypher, msg: Message):
    really = await client.ask(msg.chat.id, "Are you sure you want to logout? (y/n)")
    if really.text.lower() == "y":
        await client.database.mega_logout(msg.chat.id)
        await msg.reply("Successfully logged out!")
    else:
        await msg.reply("Logout cancelled!")
