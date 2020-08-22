import requests
import xmltodict

def get_rss(newspaper_name, nb):
  
  def url_auto(newspaper_name):
    rss = {
      "the lancet": "http://www.thelancet.com/rssfeed/lancet_current.xml",
      "le monde": "https://www.lemonde.fr/rss/une.xml",
      "ouest-france": "https://www.ouest-france.fr/rss-en-continu.xml",
      "l'express": "https://www.lexpress.fr/rss/alaune.xml"}
    for name in rss:
      if name == newspaper_name: return name, rss[name]
    return name, None


  name, url = url_auto(newspaper_name.lower())
  if not url: return None
  
  data = xmltodict.parse(requests.get(url).content)

  # --- TEST --- #
  if name == "ouest-france": print(data["html"]["body"].keys())
  return None
  # --- FIN --- #
  
  if name == "the lancet":
    data = data["rdf:RDF"]
  elif name in ("le monde", "l'express"): 
    data = data["rss"]["channel"]
  elif name == "ouest-france":
    data = data["html"]

  
  data = data["item"][0:nb]

  information = []
  for index, news in enumerate(data):
    information.append([news["title"], news["description"], news["link"]])
    
    if name == "le monde":
      information[index].append(news["media:content"]["@url"])
    elif name in ("ouest-france", "l'express"):
      information[index].append(news["enclosure"]["@url"])
    else:
      information[index].append(None)

  return information

# --- Information
# - Titre
# - Description
# - Lien
# - Image
# ---
    


