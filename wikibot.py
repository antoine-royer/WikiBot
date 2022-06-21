# --------------------------------------------------
# WikiBot (Version 2.2.0)
# by Sha-chan~
# last version released on the 21 of June 2022
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

import discord
from discord.ext import commands
import discord_slash

import os
import libs.wikibot_lib as wl

from random import randint

intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents)
slash = discord_slash.SlashCommand(client, sync_commands=True)
token = os.environ["token"]
__version__ = "2.2.0"
guild_ids = [658281779408535552]

def make_embed(title, description, field, color, image, in_line = False, thumb = False):
    if not color: color = randint(0, 16777215)
    answer = discord.Embed(title=title, description=description, color=color)

    for i in field:
        answer.add_field(name=i[0], value=i[1], inline=in_line)
    
    if image:
        if thumb: answer.set_thumbnail(url=image)
        else: answer.set_image(url=image)
    return answer


@slash.slash(name="r", description="Random selection of articles from Wikipedia", guild_ids=guild_ids)
async def r(ctx, number: int, language: str="en"):
    wl.wikipedia.set_lang(language.split()[0])
    await ctx.send(embed=make_embed(*wl.page_random(number)))


@slash.slash(name="p-auto", description="Get an article with an automatic correction on the title", guild_ids=guild_ids)
async def pauto(ctx, research: str, language: str="en"):
    wl.wikipedia.set_lang(language.split()[0])
    await ctx.send(embed=make_embed(*wl.page_read(research, True)))


@slash.slash(name="p", description="Get an article from Wikipedia with the exact title", guild_ids=guild_ids)
async def p(ctx, research: str, language: str="en"):
    wl.wikipedia.set_lang(language.split()[0])
    await ctx.send(embed=make_embed(*wl.page_read(research)))


@slash.slash(name="s", description="Make a research on wikipedia", guild_ids=guild_ids)
async def s(ctx, research: str, language: str="en"):
    wl.wikipedia.set_lang(language.split()[0])
    await ctx.send(embed=make_embed(*wl.page_search(research)))


@slash.slash(name="w", description="Get the weather", guild_ids=guild_ids)
async def w(ctx, city_name: str, forecast: int=1):
    rep, img, day, timezone, datetime = wl.weather(city_name, forecast)
    if not rep:
        rep = make_embed("Weather", "Unknown city's name", [("Error", f"No city were found for the name : '{city_name}'. Please check the city's name.")], 16711680, None)
    else:
        if day == 0: day = f"today : {datetime}"
        elif day == 1: day = f"tomorrow : {datetime}"
        else: day = f"in {day} days : {datetime}"
        rep = make_embed("Weather", f"{city_name} {day} ({timezone})", rep, None, img, True, True)

        rep.set_footer(text = "Weather forecast provided by OpenWeather", icon_url = "https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png")
    await ctx.send(embed=rep)


@slash.slash(name="n", description="Get some news", guild_ids=guild_ids)
async def n(ctx, newspaper: str, nb_article: int=1, is_selected: bool=False):
    name, news, selection = wl.get_news(newspaper, nb_article, is_selected)
    embed_title = f"**{name}**"
    if news[0]:
        news = news[0]
        rep = []
        if not selection:
            for index, article in enumerate(news):
                rep.append(make_embed(f"{embed_title} (#{index + 1})", article[0], (("Summary", article[1]), ("Link", article[2])), None, article[3]))
        else:
            rep.append(make_embed(f"{embed_title} (#{selection})", news[0][0], (("Summary", news[0][1]), ("Link", news[0][2])), None, news[0][3]))
    else:
        rep = make_embed(embed_title, "Unknown newspaper", (("Error", "The newspaper requested isn't registrated"), ("Newspapers available", " - ".join(news[1]))), 16711680, None)
    for article in rep: await ctx.send(embed=article)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
    print("Online.")

client.run(token)
