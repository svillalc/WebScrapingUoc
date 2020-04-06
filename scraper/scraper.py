# -*- coding: cp1252 -*-
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import math

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
req = requests.get("https://www.idealista.com/alquiler-viviendas/alicante-alacant-alicante/", headers = headers)
soup = BeautifulSoup(req.text, "html.parser")

#Número de viviendas   SOLO SE PUEDE LANZAR UNA VEZ CADA 10 MIN APROX
required0 = soup.find_all("h1")

nviviendas= []

for i in required0:
    nviviendas.append(i.get_text())
    numero_viviendas=int(nviviendas[0].split()[0].replace(".", ""))
print(numero_viviendas)

#Numero de paginas
numero_paginas=math.ceil(numero_viviendas/30) -1 #restamos 1 por la que ultima pagina la recorreremos a parte

#Numero de elementos pagina final
elementos_pagina_final = numero_viviendas % 30


#Recogemos la información de las N-1 primeras paginas   CASI SEGURO QUE TENDREMOS QUE METER UN DELAY para que no sature 

precios=[]
habitaciones =[]
metros =[]

for i in range(numero_paginas):
    req2 = requests.get('https://www.idealista.com/alquiler-viviendas/alicante-alacant-alicante/pagina-' + str(i+1) + '.htm', headers = headers)
    print (i+1)
    soup2 = BeautifulSoup(req2.text, "html.parser")
    anuncios2 = soup.find_all("div", "item-info-container")

    precios2 = [anuncio2.find("span", "item-price h2-simulated").text for anuncio2 in anuncios2]
    habitaciones2 = [anuncio2.find_all("span", "item-detail")[0].text for anuncio2 in anuncios2]
    metros2 = [anuncio2.find_all("span", "item-detail")[1].text for anuncio2 in anuncios2]
    precios_sin_unidad2 = [re.findall(r"^\d+\.*\d*", precio)[0] for precio in precios2]
    
    
    precios = precios + precios_sin_unidad2
    habitaciones = habitaciones + habitaciones2
    metros = metros + metros2

#################################################################################################
#Hasta aqui añade las N-1 paginas y funciona, falta añadir la ultima pagina
###################################################################################################


#corregimos los metros que no vengan como tal sustituyendo como N/A
metros_corregido
for metro in metros:
    if (list(metro.split()[0])[0] =='1' or list(metro.split()[0])[0] =='2' or list(metro.split()[0])[0] =='3' or list(metro.split()[0])[0] =='4' or list(metro.split()[0])[0] =='5' or list(metro.split()[0])[0] =='6' or list(metro.split()[0])[0] =='7' or list(metro.split()[0])[0] =='8' or list(metro.split()[0])[0] =='9'):
           metros_corregido = metros_corregido +[metro.split()[0]]
    else:
       metros_corregido = metros_corregido +['N/A'] 
       

data = {"Precio (€)": precios,
        "Habitaciones": habitaciones,
       "Tamaño (m2)": metros_corregido}
df = pd.DataFrame(data)
print(df)
