import wikipedia
from newspaper import NewsPaper, get_weather
from googletrans import Translator
from eliza_lib import eliza


def page_content(name, limit = 1000):
  
  def image_detect(img, code_html):
    img = [i for i in img if i.endswith(".jpg")]

    print("Début du process : ")
    for i in img: print(i)
    
    for index, value in enumerate(img):
      value = value.split("/commons/")
      img[index] = value[0][6:] + "/commons/thumb/" + value[1]

    for url in img:
      if url in code_html: return "https:" + url

    return None

    
  try:
    
    search = wikipedia.WikipediaPage(name)
    if len(search.summary) > limit:
      summary = search.summary[:limit] + "…"
    else:
      summary = search.summary
      
    summary = summary.replace("()", "").replace("(listen)", "")

    if summary.find("==") + 1:
      summary = summary[:summary.find("==")]
      
    img = image_detect(search.images, search.html())
    
    print(f"Fin du process : {img}")
    
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
  
def page_read(name):
  try:
    name = wikipedia.search(name, results = 1)[0]
    w_title, w_content, w_url, w_img, success = page_content(name)
  except:
    sucess = False

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
