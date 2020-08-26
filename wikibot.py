# --------------------------------------------------
# WikiBot (Version 1.5.4)
# by Sha-Chan~
# last version released on the 26 of August 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

import discord
import os
import wikilib as wl
from random import randint

client = discord.Client()
token = os.environ["token"]


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
  
  if message.author == client.user or msg_content[0] != "/": return None

  msg_content = list(msg_content[1:].partition("#"))

  msg_content[0] = msg_content[0].rstrip()

  language = msg_content[2].replace(" ", "")
  
  if not language:
    language = "en"
  wl.wikipedia.set_lang(language)

  if not msg_content[0].find("r "):
    rep = make_embed(*wl.page_random(msg_content[0][2:]))
    
  elif not msg_content[0].find("a "):
    rep = make_embed(*wl.page_read(msg_content[0][2:]))

  elif not msg_content[0].find("s "):
    rep = make_embed(*wl.page_search(msg_content[0][2:]))

  elif not msg_content[0].find("t "):
    rep = make_embed(*wl.translation(msg_content[0][2:], language), True)

  elif not msg_content[0].find("e "):
    rep = wl.eliza_call(msg_content[0][2:])

  elif not msg_content[0].find("w "):
    city_name = msg_content[0][2:]
    rep = wl.weather(city_name, language)
    if not rep:
      rep = make_embed("Wheather", "Unknown city's name", [("Error", "No city were found for the name : '{city_name}'. Please check the city's name.")], 16711680, None)
    else:
      rep = make_embed("Weather", f"{city_name} on {rep[0][:10]}",
                       [("Wind speed", f"{rep[1]} km/h"),
                       ("Gust speed", f"{rep[2]} km/h"),
                       ("Wind direction", f"{rep[3]}°"),
                       ("Rain probability", f"{rep[4]}%"),
                       ("Temperature min", f"{rep[5]}°C"),
                       ("Temperature max", f"{rep[6]}°C"),
                       ("Frost probability", f"{rep[7]}%"),
                       ("Fog probability", f"{rep[8]}%")], None, None, True)
      rep.set_footer(text = "Weather provided by Météo Concept")

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
    rep = discord.Embed(title="Help heading", description="List of available commands", color=randint(0, 16777215))
    rep.add_field(name="Random selection of articles", value="`/r < nb > [# < language >]`", inline=False)
    rep.add_field(name="Get an article", value="`/a < title > [# < language >]`", inline=False)
    rep.add_field(name="Translate a text", value="`/t < text > [# < language >]`", inline=False)
    rep.add_field(name="Make a research on wikipedia", value="`/s < search_terms > [# < language >]`", inline=False)
    rep.add_field(name="Get some news", value="`/n < newspaper_name > [# < number_of_article >]`", inline=False)
    rep.add_field(name="Get the weather", value="`/w < city name > [# < day_of_forecast >]` for the day : 0 is today, 1 tomorrow…", inline=False)
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
  print("Online.")

client.run(token)
