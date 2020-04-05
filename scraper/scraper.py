from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Headers para que idealista no bloquee el scraper
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

# Creamos el objeto BeautifulSouo
req = requests.get("https://www.idealista.com/alquiler-viviendas/alicante-alacant-alicante/", headers = headers)
soup = BeautifulSoup(req.text, "html.parser")

# Lista de anuncios
anuncios = soup.find_all("div", "item-info-container")

# Extracción de datos de cada anuncio
precios = [anuncio.find("span", "item-price h2-simulated").text for anuncio in anuncios]
habitaciones = [anuncio.find_all("span", "item-detail")[0].text for anuncio in anuncios]
metros = [anuncio.find_all("span", "item-detail")[1].text for anuncio in anuncios]
#plantas = [anuncio.find_all("span", "item-detail")[2].text for anuncio in anuncios]

#print(precios[0])
#print(habitaciones[0])
#print(metros[0])
#print(plantas[0])

#print(re.findall(r"^\d+", precios[0])[0])
#print(re.findall(r"^\d+", habitaciones[0])[0])
#print(re.findall(r"^\d+", metros[0])[0])

precios_sin_unidad = [re.findall(r"^\d+\.*\d*", precio)[0] for precio in precios]
habitaciones_sin_unidad = [re.findall(r"^\d+", habitacion)[0] for habitacion in habitaciones]
metros_sin_unidad = [re.findall(r"^\d+", metro)[0] for metro in metros]

data = {"Precio (€)": precios_sin_unidad,
        "Habitaciones": habitaciones_sin_unidad,
        "Tamaño (m2)": metros_sin_unidad}
df = pd.DataFrame(data)
print(df)