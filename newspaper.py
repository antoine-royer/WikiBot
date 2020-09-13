import xmltodict
from weatherlib import *

def get_rss(newspaper_name, nb):
  
  def url_auto(newspaper_name):
    rss = {
      "the lancet": "http://www.thelancet.com/rssfeed/lancet_current.xml",
      "le monde": "https://www.lemonde.fr/rss/une.xml",
      "l'express": "https://www.lexpress.fr/rss/alaune.xml",
      "le figaro": "https://www.lefigaro.fr/rss/figaro_actualites.xml",
      "l'obs": "https://www.nouvelobs.com/a-la-une/rss.xml",
      "time": "https://time.com/rss",
      "the new york times": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
      "courrier international": "https://www.courrierinternational.com/feed/all/rss.xml"}
    
    for name in rss:
      if name == newspaper_name: return name, rss[name], None
    return name, None, list(rss.keys())

  def special_char(text):
    char = {"&quot;": "\"",
            "&#039;": "'",
            "&nbsp;": "",
            "\xa0": " "}
    for i in char: text = text.replace(i, char[i])
    
    start = text.find("<")
    stop = text.find(">", start)
    while start != -1:
      text = text[:start] + text[stop + 1:]
      start = text.find("<")
      stop = text.find(">", start)
    
    return text


  name, url, np_available = url_auto(newspaper_name.lower())
  if not url: return None, np_available
  
  data = xmltodict.parse(requests.get(url).content)

  # --- Get the list of articles
  
  if name == "the lancet":
    data = data["rdf:RDF"]
    
  elif name in ("le monde", "l'express", "le figaro", "l'obs", "time", "the new york times", "courrier international"): 
    data = data["rss"]["channel"]

  
  data = data["item"][0:nb]

  information = []
  for index, news in enumerate(data):
    
    # --- Title generation
    
    if name == "l'express":
      title = f"[{news['subhead']}] {news['title']}"
      
    elif name in ("le figaro", "l'obs"):
      title = f"[{news['category']}] {news['title']}"
      
    else:
      title = news["title"]
    
    information.append([title, special_char(news["description"]), news["link"]])

    # --- Get the article's image
    
    if name in ("le monde", "the new york times"):
      information[index].append(news["media:content"]["@url"])
      
    elif name in ("l'express", "l'obs"):
      information[index].append(news["enclosure"]["@url"])
      
    else:
      information[index].append(None)

  return information, None

# --- Information
# 0 Titre
# 1 Description
# 2 Lien
# 3 Image
# ---
    


