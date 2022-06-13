import os
import discord
import json
import logging
from dotenv import load_dotenv
import aiohttp
import mimetypes
from discord.ext import bridge

# import subprocess

bot = bridge.Bot(
    command_prefix=";",
    intents=discord.Intents.all(),
    case_insensitive=True,
    debug_guilds=[513084268092850185],
)  # note to self. add admincraft id to this
load_dotenv()

logging.basicConfig(
    filename="console.log",
    level=logging.ERROR,
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger()


@bot.event
async def on_ready():
    # Marks bot as running
    print(f"[🟢] {bot.user} is ready")


@bot.event
async def on_message(message):

    # checks if we have an attachment or not
    if len(message.attachments) > 0:
        # if its from the bot ignore it
        if message.author.bot:
            return
        # check if we can send messages in that channel
        perms = message.channel.permissions_for(message.guild.me)
        # for now we wont do anything but future update perhaps send it to them via dms?
        if not perms.send_messages:
            return

        # good way to remove forbidden files
        for i in range(len(message.attachments)):
            if (
                message.attachments[i]
                .url.lower()
                .endswith((".jar", ".exe", ".com", ".deb", ".msi"))
                == False
            ):
                # removes the message since it contains forbidden file
                # lets the user know why
                await message.reply(
                    "For safety reasons we do not allow executables to be sent as they might contain malware. If you're compiling for someone please DM them and as a reminder. We cannot verify if a compiled jar has not been tampered in any way"
                )
                return await message.delete()

        if not message.attachments[0].url.lower().endswith((".html")):
            file_type = mimetypes.guess_type(message.attachments[0].url)
            if not file_type[0] == None:
                try:
                    file_type = file_type[0].split("/")[0]
                except:
                    logging.info(file_type + " failed while being parsed")

            if (
                message.attachments[0]
                .url.lower()
                .endswith(
                    (
                        ".log",
                        ".txt",
                        ".json",
                        ".yml",
                        ".yaml",
                        ".css",
                        ".py",
                        ".js",
                        ".sh",
                        ".config",
                        ".conf",
                        ".properties",
                    )
                )
                or file_type == "text"
            ):
                text = await discord.Attachment.read(
                    message.attachments[0], use_cached=False
                )
                text = text.decode("Latin-1")
                text = "\n".join(text.splitlines())
                truncated = False
                body = {"content": text}
                print("text is stored")
                if len(text) > 100000:
                    text = text[:99999]
                    truncated = True
                # POST request to mclo.gs with content from the attachment
                # returns 3 response: status, raw url and url
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        "https://api.mclo.gs/1/log",
                        data={"content": text},
                        headers={"content-type": "application/x-www-form-urlencoded"},
                    ) as req:
                        key = json.loads(await req.read())
                response = key["url"]
                response = response + "\nRequested by " + message.author.mention
                if truncated:
                    response = (
                        response + "\n(file was truncated because it was too long.)"
                    )
                embed_var = discord.Embed(
                    title="Please use a paste service", color=0x1D83D4
                )
                embed_var.description = response
                try:
                    print("sucessfuly sent embed")
                    await message.channel.send(embed=embed_var)
                except:
                    print("Permission error")
                logging.info(
                    f"File uploaded by {message.author} ({message.author.id}): {key}"
                )
    # Pastebin is blocked in some countries
    words = message.content.replace("\n", " ").split(" ")
    for word in words:
        if word.startswith("https://pastebin.com/") and len(word) == 29:
            pastebinkey = word[len(word) - 8 :]
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://pastebin.com/raw/{pastebinkey}") as r:
                    text = await r.text()
                    truncated = False
                    if len(text) > 100000:
                        text = text[:99999]
                        truncated = True
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.mclo.gs/1/log",
                    data={"content": text},
                    headers={"content-type": "application/x-www-form-urlencoded"},
                ) as req:
                    key = json.loads(await req.read())["url"]
            response = key
            response = response + "\nRequested by " + message.author.mention
            await session.close()
            await session.close()
            if truncated:
                response = response + "\n(file was truncated because it was too long.)"
            embed_var = discord.Embed(
                title="Pastebin is blocked in some countries so it has been converted.",
                color=0x1D83D4,
            )
            embed_var.description = response
            try:
                await message.channel.send(embed=embed_var)
            except:
                print("Permission error")
    timings = bot.get_cog("Timings")
    await timings.analyze_timings(message)
    await bot.process_commands(message)


@bot.slash_command()
async def ping(ctx):
    await ctx.defer()
    await ctx.respond(f"Timings bot ping is {round(bot.latency * 1000)}ms")



# Dynamic way of loading in cogs
for file_name in os.listdir("./cogs"):
    if file_name.endswith(".py"):
        print(f"[🟢] IMPORTED | {file_name}")
        bot.load_extension(f"cogs.{file_name[:-3]}")


bot.run(os.getenv("token"))
