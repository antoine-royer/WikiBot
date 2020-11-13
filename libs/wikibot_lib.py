import wikipedia
import requests
from deep_translator import GoogleTranslator

from libs.newspaper_lib import NewsPaper
from libs.weather_lib import get_weather
from libs.eliza_lib import eliza

def math_formula_detection(text, source_code, index = 0):
    def get_start(source_code, index = 0):
        end = source_code.find('<span class="mwe-math-element">', index)
        if end == -1: return None
        start = end
        while not source_code[start].isupper(): start -= 1
        return text_formater(source_code[start: end])
    
    def get_end(source_code, index = 0):
        start = 10 + source_code.find(' alttext="', source_code.find('<span class="mwe-math-element">', index))
        end = source_code.find('"', start)
        return text_formater(source_code[start: end]), end

    def chevrons(text):
        if text.find(">") < text.find("<"): text = "<" + text
        while "<" in text or ">" in text:
            start = text.find("<")
            end = text.find(">", start) + 1
            text = text[:start] + " " + text[end:]
        return text

    def text_formater(text):
        char = "\n .:!?,;0123456789&#"
        for pattern in ("amp;", ""):
            text = text.replace(pattern, "")
        text = chevrons(text)
        return text.replace("  ", " ").strip(char).rstrip(char)

    start = get_start(source_code, index)
    if not start: return text
    lenght_start = len(start)    
    start = text.find(start)
    
    end, index = get_end(source_code, index)
    lenght_end = len(end)
    end = text.find(end)

    
    if start == -1 or end == -1: return text
    else:
        return text[:start + lenght_start].rstrip("\n ") + " [ *formule* ].\n" + math_formula_detection(text[end + lenght_end:].strip("\n ."), source_code, index) 

def page_content(name, limit = 1000):
  
  def image_detect(source_code):
    start = source_code.find("//upload")
    end = [source_code.find(ext, start) for ext in (".PNG", ".png", ".JPG", ".jpg")]
    end = min([ext for ext in end if ext != -1]) + 4
     
    if not source_code[start:end]:
      return None
    else:
      url = "https:" + source_code[start:end]
      if not ".svg" in url: url = url.replace("/thumb", "")
      if url not in (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Disambig_colour.svg/20px-Disambig_colour.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Arithmetic_symbols.svg/24px-Arithmetic_symbols.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Racine_carr%C3%A9e_bleue.svg/24px-Racine_carr%C3%A9e_bleue.svg.png"
        ):
        return url
  
  try:
    
    search = wikipedia.WikipediaPage(name)
    source_code = requests.get(search.url).text
    
    summary = math_formula_detection(search.summary, source_code)   
    
    for i in ("()", "(audio)", "(listen)"):
      summary = summary.replace(i, "")

    if len(summary) > limit:
      summary = summary[:limit] + "…"

    img = image_detect(source_code)
        
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

def translation(text, language):
  dest_lang, src_lang = language, "auto"

  if " " in language:
    dest_lang, src_lang = language.split()

  translation = GoogleTranslator(source = src_lang, target = dest_lang).translate(text = text) 
  rep = ["Translation", f"From {src_lang} to {dest_lang}", [], None, None]
  rep[2].append(["Origin text", text])
  rep[2].append(["Translated text", translation])
  return rep

def eliza_call(message):
  return eliza(message)

def get_news(newspaper_name, number):
	newspaper = NewsPaper()
	plus = False
	if number.endswith("+"):
		plus = True
		try:
			number = int(number[:-1])
		except:
			number = 1
	else:
		try:
			number = int(number)
		except:
			number = 1
  
	return newspaper_name.title(), newspaper.get_rss(newspaper_name, number, plus)

def weather(city_name, nb_day):
  try:
    nb_day = int(nb_day)
    if nb_day < 0 or nb_day > 7: nb_day = 0
  except:
    nb_day = 0

  try:
    weather_data = get_weather(city_name, nb_day)
    return [(value.partition("#")[0], f'{weather_data[index]}{value.partition("#")[2]}') for index, value in enumerate(("Description", "Temperature#°C", "Feels like#°C", "Dew point#°C", "Pressure# hPa", "Humidity# %", "Wind speed# km/h", "Wind direction#°", "Cloudiness# %", "Rain probability# %"))], weather_data[-2], nb_day, weather_data[-3], weather_data[-1]
  except:
    return None, 0, 0, 0, 0
