import wikipedia
from newspaper import NewsPaper, get_weather
from googletrans import Translator
from eliza_lib import eliza

import requests

def page_content(name, limit = 1000):
  
  def image_detect(code_source):
    start = code_source.find("//upload")
    end = [code_source.find(ext, start) for ext in (".PNG", ".png", ".JPG", ".jpg")]
    end = min([ext for ext in end if ext != -1]) + 4
     
    if not code_source[start:end]:
      return None
    else:
      url = "https:" + code_source[start:end]
      if not ".svg" in url: url = url.replace("/thumb", "")
      return url
    
  try:
    
    search = wikipedia.WikipediaPage(name)
    
    if len(search.summary) > limit:
      summary = search.summary[:limit] + "…"
    else:
      summary = search.summary

    math_formula_start = summary.find("\n\n  ")
    math_formula_end = 7 + summary.find("}\n  \n", math_formula_start)
    if math_formula_start != -1 and math_formula_end != -1:
      while summary[math_formula_end:][0].isspace(): math_formula_end += 1
      summary = summary[:math_formula_start] + " [formule]\n" + summary[math_formula_end].upper() + summary[1 + math_formula_end:]

    for i in ("()", "(audio)", "(listen)"):
      summary = summary.replace(i, "")

    img = image_detect(requests.get(search.url).text)
        
    return search.title, summary.replace(" , ", ", "), search.url, img, True

  except:
    return name.capitalize(), "", "", "", False

def list_pages(l_page, title, description, limit = 1000):
  pages = [title, description, [], None, None]

  if type(l_page) == list:
    for page in [page_content(i, limit) for i in l_page]:
      if len(page[0]) and len(page[1]):
        pages[2].append([page[0], page[1]])

  else:
    page = page_content(l_page, limit)
    if len(page[0]) and len(page[1]):
      pages[2].append([page[0], page[1]])

  return pages

def page_random(nb):
  try:
    nb = int(nb)
    
    if nb < 1: nb = 1
    elif nb > 10: nb = 10
      
  except:
    nb = 1
    
  rand = wikipedia.random(nb)
  return list_pages(rand, "Random articles", f"{nb} random articles on Wikipedia", 500)

def page_search(name):
  rslt = wikipedia.search(name, results=5)
  
  if len(rslt):
    return list_pages(rslt, "Wikipedia research", f"Results of the research for '{name}'", 500)

  else:
    rep = ["Wikipedia research", f"Results of the research for '{name}'", [], 0xff0000, None]
    rep[2].append(["Error", "There is none article corresponds to your research. Please check your search terms."])
    return rep
  
def page_read(name, automatic_correction = False):
  def auto_name(name):
    try:
      return wikipedia.search(name, results = 1)[0]
    except:
      return name

  if automatic_correction: name = auto_name(name)
  w_title, w_content, w_url, w_img, success = page_content(name)
    
  if success:
    page = [w_title, "Wikipedia page", [], None, w_img]
    page[2].append(["Summary", w_content])
    page[2].append(["Page's link", w_url])

  else:
    page = [w_title, "Wikipedia page", [], 0xff0000, None]
    page[2].append(["Error", f"There is none page named : '{name}'. Please check the page's name."])

  return page

def translation(text, dest_lang):
  trans = Translator()
  rep = ["Translation", "From {0} to {1}".format(trans.detect(text).lang, dest_lang), [], None, None]
  rep[2].append(["Origin text", text])
  rep[2].append(["Translated text", trans.translate(text, dest_lang).text])
  return rep

def eliza_call(message):
  language = Translator()
  if language.detect(message).lang != "en":
    return "I'm sorry, I only speak english…"
  return eliza(message)

def get_news(newspaper_name, number):
  newspaper = NewsPaper()
  try:
    number = int(number)
  except:
    number = 1
  
  return newspaper_name.title(), newspaper.get_rss(newspaper_name, number)

def weather(city_name, nb_day):
  try:
    nb_day = int(nb_day)
    if nb_day < 0 or nb_day > 7: nb_day = 0
  except:
    nb_day = 0

  try:
    weather_data = get_weather(city_name, nb_day)
    return [(value.partition("#")[0], f'{weather_data[index]}{value.partition("#")[2]}') for index, value in enumerate(("Description", "Temperature#°C", "Feels like#°C", "Dew point#°C", "Pressure# hPa", "Humidity# %", "Wind speed# km/h", "Wind direction#°", "Cloudiness# %", "Rain probability# %"))], weather_data[-1], nb_day, weather_data[-2]
  except:
    return None, 0, 0, 0
