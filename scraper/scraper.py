# -*- coding: cp1252 -*-
from bs4 import BeautifulSoup
import requests
import pandas as pd
import math
import time

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

# Creamos el objeto BeautifulSoup
req = requests.get("https://www.idealista.com/alquiler-viviendas/alicante-alacant-alicante/", headers=headers)
soup = BeautifulSoup(req.text, "html.parser")

# Numero de viviendas   SOLO SE PUEDE LANZAR UNA VEZ CADA 10 MIN APROX
required0 = soup.find_all("h1")

nviviendas = []

for i in required0:
    nviviendas.append(i.get_text())
    numero_viviendas = int(nviviendas[0].split()[0].replace(".", ""))
print(numero_viviendas)

# Numero de paginas
numero_paginas = math.ceil(numero_viviendas / 30)

# restamos 1 porque la ultima pagina la recorreremos a parte <- Esto creo que no hace falta

# Numero de elementos pagina final
elementos_pagina_final = numero_viviendas % 30

# Recogemos la informacion de las N-1 primeras paginas   CASI SEGURO QUE TENDREMOS QUE METER UN DELAY para que no sature

precios = []
habitaciones = []
metros = []

for i in range(numero_paginas):
    req2 = requests.get(
        'https://www.idealista.com/alquiler-viviendas/alicante-alacant-alicante/pagina-' + str(i + 1) + '.htm',
        headers=headers)
    print(i + 1)
    soup2 = BeautifulSoup(req2.text, "html.parser")
    anuncios2 = soup2.find_all("div", "item-info-container")

    precios2 = []
    habitaciones2 = []
    metros2 = []

    # Lo recorremos asi para limpiar los datos erroneos antes de incluirlos en nuestras listas
    for anuncio2 in anuncios2:
        precios2.append(anuncio2.find("span", "item-price h2-simulated").text)
        numhabs = anuncio2.find_all("span", "item-detail")[0].text
        nummetros = anuncio2.find_all("span", "item-detail")[1].text

        if "hab" not in numhabs:
            if "m²" not in numhabs:
                nummetros, numhabs = None, None
            else:
                nummetros = numhabs
                numhabs = None
        elif "m²" not in nummetros:
            nummetros = None
        habitaciones2.append(numhabs)
        metros2.append(nummetros)

    # precios2 = [anuncio2.find("span", "item-price h2-simulated").text for anuncio2 in anuncios2]
    # habitaciones2 = [anuncio2.find_all("span", "item-detail")[0].text for anuncio2 in anuncios2]
    # metros2 = [anuncio2.find_all("span", "item-detail")[1].text for anuncio2 in anuncios2]
    # precios_sin_unidad2 = [re.findall(r"^\d+\.*\d*", precio)[0] for precio in precios2]

    precios = precios + precios2
    habitaciones = habitaciones + habitaciones2
    metros = metros + metros2
    time.sleep(10)

#################################################################################################
# Hasta aqui anyade las N-1 paginas y funciona, falta anyadir la ultima pagina
###################################################################################################


# corregimos los metros que no vengan como tal sustituyendo como N/A
# metros_corregido = []
# for metro in metros:
# if ("m²" in metro):
# metros_corregido = metros_corregido + [metro.split()[0]]
# else:
# metros_corregido = metros_corregido +['N/A']


data = {"Precio (Euros/Mes)": precios,
        "Habitaciones": habitaciones,
        "Tamanyo (m2)": metros}
df = pd.DataFrame(data)

df["Precio (Euros/Mes)"] = list(map(lambda x: x.replace(".", "").split("€")[0], df["Precio (Euros/Mes)"]))
df["Tamanyo (m2)"] = list(map(lambda x: x.split()[0], df["Tamanyo (m2)"]))
df["Euros/m2"] = round(df["Precio (Euros/Mes)"].astype(int) / df["Tamanyo (m2)"].astype(int), 2)
print(df)

# df.to_csv("dataset.csv")
