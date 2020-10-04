# --------------------------------------------------
# WikiBot (Version 1.7.5)
# by Sha-chan~
# last version released on the 4 of October 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

import discord
import os
import libs.wikibot_lib as wl

from random import randint

client = discord.Client()
token = os.environ["token"]
__version__ = "1.7.5"


def make_embed(title, description, field, color, image, in_line = False):
  if not color: color = randint(0, 16777215)
  answer = discord.Embed(title=title, description=description, color=color)

  for i in field:
    answer.add_field(name=i[0], value=i[1], inline=in_line)
    
  if image:
    answer.set_image(url=image)
  return answer

@client.event
async def on_message(message):
  msg_content, rep = message.content, None
  if message.author == client.user: return None
  try:
    if msg_content[0] != "/": return None
  except:
    return None

  print(f"{message.author.name} : {message.content}")

  msg_content = list(msg_content[1:].partition("&"))

  msg_content[0] = msg_content[0].rstrip()

  language = msg_content[2].replace(" ", "")
  
  if not language:
    language = "en"
  wl.wikipedia.set_lang(language)

  if not msg_content[0].find("r "):
    rep = make_embed(*wl.page_random(msg_content[0][2:]))
    
  elif not msg_content[0].find("p+ "):
    rep = make_embed(*wl.page_read(msg_content[0][2:], True))

  elif not msg_content[0].find("p "):
    rep = make_embed(*wl.page_read(msg_content[0][2:]))

  elif not msg_content[0].find("s "):
    rep = make_embed(*wl.page_search(msg_content[0][2:]))

  elif not msg_content[0].find("t "):
    rep = make_embed(*wl.translation(msg_content[0][2:], language), True)

  elif not msg_content[0].find("e "):
    rep = wl.eliza_call(msg_content[0][2:])

  elif not msg_content[0].find("w "):
    city_name = msg_content[0][2:]
    rep, img, day, timezone, datetime = wl.weather(city_name, language)
    
    if not rep:
      rep = make_embed("Weather", "Unknown city's name", [("Error", f"No city were found for the name : '{city_name}'. Please check the city's name.")], 16711680, None)
    else:
      if day == 0: day = f"today : {datetime}"
      elif day == 1: day = f"tomorrow : {datetime}"
      else: day = f"in {day} days : {datetime}"
      rep = make_embed("Weather", f"{city_name} {day} ({timezone})", rep, None, img, True)

      rep.set_footer(text = "Weather forecast provided by OpenWeather", icon_url = "https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png")

  elif not msg_content[0].find("n "):
    name, news = wl.get_news(msg_content[0][2:], language)
    embed_title = f"**{name}**"
    if news[0]:
      news = news[0]
      rep = []
      for article in news:
        rep.append(make_embed(embed_title, article[0], (("Summary", article[1]), ("Link", article[2])), None, article[3]))
    else:
      rep = make_embed(embed_title, "Unknown newspaper", (("Error", "The newspaper requested isn't registrated"), ("Newspapers available", " - ".join(news[1]))), 16711680, None)
    
  elif msg_content[0] == "help":
    rep = discord.Embed(title=f"Help pannel (WikiBot v{__version__})", description="List of available commands", color=randint(0, 16777215))
    rep.add_field(name="Make a research on wikipedia", value="`/s < search_terms > [& < language >]`", inline=False)
    rep.add_field(name="Get an article from Wikipedia with the exact title", value="`/p < title > [& < language >]`", inline=False)
    rep.add_field(name="Get an article with an automatic correction on the title", value="`/p+ < title > [& < language >]`", inline=False)
    rep.add_field(name="Random selection of articles from Wikipedia", value="`/r < nb > [& < language >]`", inline=False)
    rep.add_field(name="Translate a text", value="`/t < text > [& < language >]`", inline=False)
    rep.add_field(name="Get some news", value="`/n < newspaper_name > [& < number_of_article >]`", inline=False)
    rep.add_field(name="Get the weather", value="`/w < city name > [& < day_of_forecast >]` for the day : 0 is today, 1 tomorrow…", inline=False)
    rep.add_field(name="Talk with Eliza", value="`/e < message >`", inline=False)
    rep.add_field(name="Complete documentation", value="https://github.com/Shadow15510/WikiBot/blob/master/README.md", inline=False)

  if not rep: return None
  
  if type(rep) == str:
    await message.channel.send(rep)
  elif type(rep) == list:
    for msg in rep: await message.channel.send(embed = msg)
  else:
    await message.channel.send(embed = rep)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
  print("Online.")

client.run(token)
