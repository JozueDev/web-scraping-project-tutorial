import os
from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd
from io import StringIO


#DESCARGA
resource_url = "https://es.wikipedia.org/wiki/Anexo:Canciones_m%C3%A1s_reproducidas_en_Spotify"
response = requests.get(resource_url)
soup = BeautifulSoup(response.text, 'html.parser')

#BUSQUEDA Y DESPLIEGUE DE TABLA
tabla = soup.find('table', {'class': 'wikitable sortable'})
df = pd.read_html(StringIO(str(tabla)))[0]
 

#MOSTRAR DF
#print(df.head())

#CONEXION DB
conexion = sqlite3.connect('top100_spotify.db')

#GUARDAR EL DF EN UNA TABLA
df.to_sql('Canciones_mas_reproducidas', con=conexion, if_exists='replace', index=False)

#VERIFICAR SI SE INSERTARON LOS DATOS
cursor = conexion.cursor()
cursor.execute('SELECT * FROM Canciones_mas_reproducidas LIMIT 5')
registros = cursor.fetchall()
for fila in registros:
    print(fila)

#CONTADOR DE REGISTROS
cursor.execute('SELECT COUNT(*) FROM Canciones_mas_reproducidas')
cantidad = cursor.fetchone()[0]
print(f'Número de registros: {cantidad}')

#CERRAR CONEXION DB 
conexion.close()


