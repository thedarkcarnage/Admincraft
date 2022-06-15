from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command,
)
from discord.ext import commands

import discord

guides = {
    "server.properties": "https://minecraft.fandom.com/wiki/Server.properties#Java_Edition_2",
    "paper": "https://docs.papermc.io/paper",
    "purpur": "https://purpurmc.org/docs/",
    "bukkit": "https://bukkit.fandom.com/wiki/Bukkit.yml",
    "spigot": "https://www.spigotmc.org/wiki/spigot/",
    "hilltty flags": "https://github.com/hilltty/hilltty-flags/blob/main/english-lang.md",
    "aikar flags": "https://aikar.co/mcflags.html",
    "offline mode": "You really shouldnt be using offline mode. See this: https://archive.ph/jWqGW",
}
guide_group = []
for i in guides:
    guide_group.append(discord.OptionChoice(name=i, value=i))


class Guide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        description="sends relvent guides", debug_guilds=[513084268092850185]
    )  # Create a slash command for the supplied guilds.
    async def guides(
        self, ctx, guide: discord.Option(str, "guide", choices=guide_group)
    ):
        print()
        await ctx.respond(f"{guides[guide]}")


def setup(bot):
    bot.add_cog(Guide(bot))
