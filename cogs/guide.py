from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command,
)
from discord.ext import commands

import discord

# hard coding guide options. Admincraft primarily uses carl for other tags
# maybe in the future i could store this in a database and create a way to manage the guides
guides = {
    "optimization": discord.Embed(
        title="Trouble with optimizing your server?",
        color=discord.Color.random(),
        description="Consider reading [paper chan's guide](https://eternity.community/index.php/paper-optimization) and this [other guide](https://github.com/YouHaveTrouble/minecraft-optimization)",
    ),
    "port forwarding": discord.Embed(
        title="Short guide on port forwarding",
        color=discord.Color.random(),
        description="""
        **What is port forwarding??**
        port forwarding is a technique used to allow external services/things access the device. For example port 22 is usually open to allow SSH connections from outside the computer. Without port 22 being opened you wouldn't be able to SSH into the device. Minecraft needs certain ports open for others to be able to join.
        People will often be opening ports for various reasons such as maybe them wanting to host a website/web panel, wanting to create a database (MYSQL) and more.

        **How do i port forward?**
        - **hosts** usually will do port forwarding for you by default but some will either open more on request or just give you a section to open ports so check your control panel!

        - **Self hosted/your own device** You'd need to head to your router configuration homepage and open it. As everyone uses a different provider you'll need to search "How do i open ports on X provider" (example provider is verizon)

        - **VPS** will usually have something on the dashboard manager that lets you control the network security things such as what ports are open. Just google how to open port on your VPS provider.

        - Linux users might need to mess with [Iptables](https://www.hostinger.co.uk/tutorials/iptables-tutorial) or [ufw for ubuntu](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-20-04) (This guide was written for Ubuntu 20.04 so other versions may have different syntax. other linux flavours have different ways. So please do some research before blindly trying something)

        **How do i check if my port is open?**
        You can use this [port scanner](https://www.yougetsignal.com/tools/open-ports/) or [dnschecker's port scanner](https://dnschecker.org/port-scanner.php) which allow multiple port scans.

        **Please do not attempt to port forward unless you're fully aware of what it is, what it does, the dangers and how to properly do it. It'd be pretty embarrassing if you lost access to your VPS because you closed port 22**
        """,
    ),
    "server.properties": "https://minecraft.fandom.com/wiki/Server.properties#Java_Edition_2",
    "purpur": discord.Embed(
        title="PurpurMc",
        color=discord.Color.random(),
        description="""
        Purpur is a fork of paperMc (purpur contains pufferfish, tuinity and airplane patches) which best features is the fact it has more configuration/features or ways to change Gameplay\n
        [Download](https://purpurmc.org/downloads)
        [Documentation](https://purpurmc.org/docs)
        [Github](https://github.com/PurpurMC/Purpur)
        """,
    ),
    "panels": discord.Embed(
        title="Server panels",
        color=discord.Color.random(),
        description="""
        A game server management panel lets you manage your game server just through a website hosting your panel. Most hosting providers will have one but if you're self hosting or setting one up on a VPS you'll need to install one by yourself. Down below i'll list some choices but i encourage you to look into the subject yourself and choose one best for yourself
        [pterodactyl](https://pterodactyl.io/) [linux]
        [PufferPanel](https://www.pufferpanel.com/) [linux]
        [Multicraft](https://www.multicraft.org/) [linux] [windows]
        [AMP](https://cubecoders.com/AMP) [linux] [windows]
        [crafty](https://craftycontrol.com/) [linux] [windows] [mac] (uses python)
        [More found here](https://minecraftservers.fandom.com/wiki/Server_wrappers)
        """,
    ),
    "pufferfish": discord.Embed(
        title="Pufferfish",
        color=discord.Color.random(),
        description="""
        Pufferfish is a fork of paperMc (pufferfish contains airplane patches) which is useful for bigger server and promises a lot of performance tweaks. Check the github for a better explanation \n
        [Download](https://ci.pufferfish.host/) (dont use pufferfish plus. its for their hosting users only)
        [Documentation](https://docs.pufferfish.host/)
        [Github](https://github.com/pufferfish-gg/Pufferfish)
        """,
    ),
    "paper": discord.Embed(
        title="PaperMC",
        color=discord.Color.random(),
        description="""
        Paper is a fork of Spigot (paper contains tuinity patches too!) which is recommended to use since it gives 2x the performance you get with spigot although it may have unwanted features as it also promises to fix a ton of bugs\n
        [Download](https://papermc.io/downloads)
        [Documentation](https://docs.papermc.io/)
        [Github](https://github.com/PaperMC/Paper)
        """,
    ),
    "spigot": discord.Embed(
        title="SpigotMC",
        color=discord.Color.random(),
        description="""
        SpigotMc is a fork of bukkit which is the base of all the other forks you heard of such as paper. When a new version comes out you'll see this one being updated first\n
        [no downloads available, must compile using buildTools](https://www.spigotmc.org/wiki/buildtools/)
        [Documentation](https://www.spigotmc.org/wiki/spigot-configuration/)
        [github](https://github.com/spigotmc/)
        """,
    ),
    "bukkit": "https://bukkit.fandom.com/wiki/Bukkit.yml",
    "hilltty flags": "https://github.com/hilltty/hilltty-flags/blob/main/english-lang.md",
    "aikar flags": "https://aikar.co/mcflags.html",
    "offline mode": discord.Embed(
        title="Offline mode = bad",
        color=discord.Color.random(),
        description="Offline mode is against Minecraft's [Eula](https://www.minecraft.net/en-us/eula) and provides a ton of security risks which can be read in this [blog](https://madelinemiller.dev/blog/minecraft-offline-mode). There are some legit uses such as testing/development",
    ),
    "piracy": discord.Embed(
        title="Piracy smh",
        color=discord.Color.random(),
        description="Admincraft does not tolerate nor approve of piracy in the slightest, redistributing paid for/premium plugins, cracked minecraft clients or just directly violating Minecraft's [Eula](https://www.minecraft.net/en-us/eula) by having your server in offline mode ([read here about offline mode](https://madelinemiller.dev/blog/minecraft-offline-mode)) are one of the common ways of promoting piracy.",
    ),
    "eula/terms": "https://www.minecraft.net/en-us/eula & https://www.minecraft.net/en-us/terms",
    "java/JDK": discord.Embed(
        title="Use the right java!",
        color=discord.Color.random(),
        description="""Java and Minecraft go hand to hand, without java you wouldn't be able to run a Minecraft server so its important to have the right version installed.\n
        You should not use any of Oracle's OpenJDK below JDK 17  on your public server as it has serious licensing issues. Even if you're using above 17 its not recommended.  You should use [Adoptium](https://adoptium.net/temurin/releases) instead.\n
        **what JDK version do i need???**
           - 1.12.2 or below: Use JDK 8
           - 1.16.5: Use JDK 11
           - 1.17.1: Use JDK 16 or 17. Both work on 1.17
           - 1.18.1 or higher: Use JDK 17 \n
           __**Always use the recommended version of java rather than latest, most plugins/mods are coded against said version and other versions might not work as intended**__
        """,
    ),
}
#
guide_group = []
for i in guides:
    guide_group.append(discord.OptionChoice(name=i, value=i))


class Guide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        description="sends relevant guides", debug_guilds=[513084268092850185]
    )  # Create a slash command for the supplied guilds.
    async def guides(
        self, ctx, guide: discord.Option(str, "guide", choices=guide_group)
    ):
        # if its a string then just send string
        if type(guides[guide]) is str:
            await ctx.respond(f"{guides[guide]}")
        # if the value stored is an embed then send value as an embed.
        elif type(guides[guide]) is discord.embeds.Embed:
            await ctx.respond(embed=guides[guide])


def setup(bot):
    bot.add_cog(Guide(bot))
