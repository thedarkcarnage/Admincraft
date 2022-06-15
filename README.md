# Admincraft's utility bot

# Credits-original code belongs to Birdflop Bot (Botflop)
- [Click here](https://discord.com/api/oauth2/authorize?client_id=787929894616825867&permissions=0&scope=bot) to invite Botflop to your server.
- [click here](https://github.com/Pemigrade/botflop) to see source code for original bot
-  Most likely will include credits in help command (if not i'll remove this comment)

# Current abilities
## Analyze timings reports
Paste a timings report to review an in-depth description of potential optimizations

## pastebin links/file uploads converts
The converts text files and pastebin links into universally accessible bin links which also uses a special highlight and strips IP's

## safeguards against executable uploads
The bot scans messages containing executable files. While the user might good intent we cant verify the safety of the compiled file  being sent publicly hence this was added. This also helps deal with potential piracy such as people uploading jars of premium plugins.

## Read The Fucking Manual (RTFM)
Yup. The bot currently can search through PaperMc, PurpurMC docs for their configuration. This uses Website scraping.
The bot can also do bukkit.yml and hopefully others when i can be asked to do so

## Guides command
Easy way for users to find relevent guides. 


# setup guide
1) git clone or download this repo
2) open up command prompt or use linux's Command line and make sure you're in the area where this project is located
3) you have two choices for this part:
- ``pip install -r req.txt`` which will install the required Libraries needed to run this project. Good for production
- ``python -m venv venv``  to go for the virtual enviroment route. Good for development
4) create a .env file and put ``token=Your_discord_bot's_token`` (if you havent got one then generate one [here](https://discord.com/developers)) and ``id=[list_of_your_guild_ids]``

Note: this bot specifically was made to help the Admincraft server so some features might not be suited for others
  


