import discord
import wikipedia
from googletrans import Translator
from urllib.parse import quote_plus
from random import randint
from eliza_lib import eliza

def page_content(name, limit = 1000):
  
  def image_detect(img):
    for i in img:
      if ".jpg" in i.lower(): return i
      
    return ""
  
  try:
    
    search = wikipedia.WikipediaPage(name)
    
    if len(search.content) > limit:
      content = search.content[:limit] + "…"
      
    else:
      content = search.content
      
    content = content.replace("()", "").replace("(listen)", "")

    if content.find("==") + 1:
      content = content[:content.find("==")]

    img = image_detect(search.images)
    return search.title, content.replace(" , ", ", "), search.url, img, True

  except:
    return name.capitalize(), "", "", "", False

def list_pages(l_page, title, description, limit = 1000):
  pages = discord.Embed(title=title, description=description, color=randint(0, 16777215))

  if type(l_page) == list:
    for j in [page_content(i, limit) for i in l_page]:
      if len(j[0]) and len(j[1]):
        pages.add_field(name=j[0], value=j[1], inline=False)

  else:
    j = page_content(l_page, limit)
    if len(j[0]) and len(j[1]):
      pages.add_field(name=j[0], value=j[1], inline=False)

  return pages

def page_random(nb):
  try:
    nb = int(nb)
    
    if nb < 1:
      nb = 1
      
    elif nb > 10:
      nb = 10
      
  except:
    nb = 1
    
  rand = wikipedia.random(nb)
  return list_pages(rand, "Random articles", f"{nb} random articles on Wikipedia", 500)

def page_search(name):
  rslt = wikipedia.search(name, results=5)
  
  if len(rslt):
    return list_pages(rslt, "Wikipedia research", f"Results of the research for '{name}'", 500)

  else:
    rep = discord.Embed(title="Wikipedia research", description=f"Results of the research for '{name}'", color=0xff0000)
    rep.add_field(name="Error", value="There is none article corresponds to your research. Please check your search terms.")
    return rep
  
def page_read(name):
  w_title, w_content, w_url, w_img, success = page_content(name)

  if success:
    page = discord.Embed(title=w_title, description="Wikipedia page", color=randint(0, 16777215))
    page.add_field(name="Summary", value=w_content, inline=False)
    if len(w_img): page.set_image(url = w_img)
    page.add_field(name="Page's link", value=w_url, inline=False)

  else:
    page = discord.Embed(title=w_title, description="Wikipedia page", color=0xff0000)
    page.add_field(name="Error", value=f"There is none page named : '{name}'. Please check the page's name.", inline=False)

  return page

def translation(text, dest_lang):
  trans = Translator()
  rep = discord.Embed(title="Translation", description="From {0} to {1}".format(trans.detect(text).lang, dest_lang), color=randint(0, 16777215))
  rep.add_field(name="Origin text", value=text, inline=True)
  rep.add_field(name="Translated text", value=trans.translate(text, dest_lang).text, inline=True)
  return rep

def eliza_call(message):
  language = Translator()
  if language.detect(message).lang != "en":
    return "I'm sorry, I only speak english…"
  return eliza(message)

