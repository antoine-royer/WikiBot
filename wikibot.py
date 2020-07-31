import discord
import os
import wikilib as wl

client = discord.Client()
token = os.environ["token"]



@client.event
async def on_message(message):
  msg_content, rep = message.content, None
  
  if message.author == client.user or msg_content[0] != "/": return None

  msg_content = msg_content[1:].partition("#")

  msg_content[0] = msg_content[0].rstrip()

  language = msg_content[2].replace(" ", "")
  if not language:
    language = "en"
  wikipedia.set_lang(language)


  elif not msg_content[0].find("r "):
    rep = page_random(msg_content[0][2:])
    
  elif not msg_content[0].find("a "):
    rep = page_read(msg_content[0][2:])

  elif not msg_content[0].find("s "):
    rep = page_search(msg_content[0][2:])

  elif not msg_content[0].find("t "):
    rep = translation(msg_content[0][2:], language)

  elif not msg_content[0].find("e "):
    rep = eliza_call(msg_content[0][2:])

  elif msg_content[0] == "help":
    rep =discord.Embed(title="Help heading", description="List of available commands", color=randint(0, 16777215))
    rep.add_field(name="Random selection of articles", value="`/r < nb > [# < language >]`", inline=False)
    rep.add_field(name="Get an article", value="`/a < title > [# < language >]`", inline=False)
    rep.add_field(name="Translate a text", value="`/t < text > [# < language >]`", inline=False)
    rep.add_field(name="Make a research on wikipedia", value="`/s < search_terms > [# < language >]`", inline=False)
    rep.add_field(name="Talk with Eliza", value="`/e < message >`", inline=False)

  if not rep: return None
  
  if type(rep) == str:
    await message.channel.send(rep)
  else:
    await message.channel.send(embed = rep)

@client.event
async def on_ready():
  print("Online.")

client.run(token)
