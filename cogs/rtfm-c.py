import discord
from discord.ext import commands

import aiohttp
from bs4 import BeautifulSoup
import re
import json


class RTFM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description="lets you search values in docs <documents> -> paper | bukkit | purpur "
    )
    async def rtfm(
        self,
        ctx,
        document: str,
        lookup: str,
    ):
        lookup = lookup.lower()
        if lookup == None or lookup == "":
            return await ctx.reply("RTFM < paper | purpur | bukkit > <lookup term>")
        if len(lookup) < 3:
            return await ctx.reply("Minimum search length is 3")
        await ctx.defer()
        # checks to see what type of document we want to lookup in
        if document.lower() in ["paper", "papermc", "pa"]:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://docs.papermc.io/paper/reference/paper-global-configuration"
                ) as response:
                    html = await response.text()
                async with session.get(
                    "https://docs.papermc.io/paper/reference/world-configuration"
                ) as response:
                    html2 = await response.text()

            # Here we're scraping the paper page
            soup = BeautifulSoup(html, "html.parser")
            # paper uses h3 tag for config settings
            anchor = soup.findAll("h3")

            soup2 = BeautifulSoup(html2, "html.parser")
            # paper uses h3 tag for config settings
            anchor2 = soup2.findAll("h3")
            # used to store all the linkable content

            configuruation = []
            #  stores every potential config link in here
            for i in anchor:
                configuruation.append(
                    f"https://docs.papermc.io/paper/reference/paper-global-configuration#{str(i.next_element)}"
                )
            for i in anchor2:
                configuruation.append(
                    f"https://docs.papermc.io/paper/reference/paper-global-configuration#{str(i.next_element)}"
                )

            # preparing found array
            found = []
            # result will be the embed description
            result = ""
            # looping through potential configuration to search for what the user wants
            for i in configuruation:
                if re.search(f"{lookup}", i.rsplit('#')[1]):
                    # returns url, setting value
                    found.append(i)
            # Looping through potential found values to append to the embed description
            for i in found:
                result = result + f"\n[{i.rsplit('#')[1]}]({i})"
            # if we couldnt find the value then lets tell them to check the doc themselves
            if found == []:
                result = "Could not find any matches. Try checking the [docs](https://docs.papermc.io/paper/reference/paper-global-configuration) or another command"
            # creating the embed that the user wants to see
            embed = discord.Embed(
                title=f"[PaperMC] best match(es) for {lookup}",
                description=result,
                color=discord.Colour.random(),
            )
            # close session as its not needed
            await session.close()

        # check the type of document we wish to search through
        if document.lower() in ["purpur", "purpurmc", "pu"]:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://purpurmc.org/docs/Configuration/"
                ) as response:
                    html = await response.text()
            # Here we're scraping the paper page
            soup = BeautifulSoup(html, "html.parser")
            # paper uses h3 tag for config settings
            anchor = soup.findAll("h3") + soup.findAll("h4")
            # used to store all the linkable content
            configuruation = []
            #  stores every potential config link in here
            for i in anchor:
                configuruation.append(
                    f"https://purpurmc.org/docs/Configuration/#{str(i.next_element)}"
                )
            # preparing found array
            found = []
            # result will be the embed description
            result = ""
            # looping through potential configuration to search for what the user wants
            for i in configuruation:
                if re.search(f"{lookup}", i):
                    # returns url, setting value
                    found.append(i)
            # Looping through potential found values to append to the embed description
            for i in found:
                result = result + f"\n[{i.rsplit('#')[1]}]({i})"
            # if we couldnt find the value then lets tell them to check the doc themselves
            if found == []:
                result = "Could not find any matches. Try checking the [docs](https://purpurmc.org/docs/Configuration/) or another command"
            # creating the embed that the user wants to see
            embed = discord.Embed(
                title=f"[PurpurMC] best match(es) for {lookup}",
                description=result,
                color=discord.Colour.random(),
            )
            # close session as its not needed
            await session.close()
        # check the type of document we wish to search through
        if document.lower() in ["bukkit", "buk", "bu"]:
            # Instead of using the website we're using a local prepared copy. this is because the wiki  values rarely change
            file = open("assets/bukkit.yml.json")
            configuruation = json.load(file)
            # preparing found array
            found = []
            # result will be the embed description
            result = ""
            # looping through potential configuration to search for what the user wants
            for i in configuruation:
                if re.search(f"{lookup}", i[0]):
                    # returns setting value, url  value
                    found.append(i)
            # Looping through potential found values to append to the embed description
            for i in found:
                result = result + f"\n[{i[0]}]({i[1]})"
            # if we couldnt find the value then lets tell them to check the doc themselves
            if found == []:
                result = "Could not find any matches. Try checking the [docs](https://bukkit.gamepedia.com/Bukkit.yml/) or another command"
            # creating the embed that the user wants to see
            embed = discord.Embed(
                title=f"[bukkit] best match(es) for {lookup}",
                description=result,
                color=discord.Colour.random(),
            )

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(RTFM(bot))
