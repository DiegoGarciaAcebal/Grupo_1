import pandas as pd
import requests
import json
import sqlite3
import datetime
import time
import sys
#Certificación Profesional en Python del ITBA - Grupo_1 (Alonso Roberto, Anconetani Alejandra, Aragona Micaela, García Acebal Diego y Tomás Rodriguez)
#Entrega 21-12-2023

print("Inicia ejecucion TP_factualizar_p")
#Recibe argumentos desde TP_fconsultar_actualizar.py ( Pantalla Streamlit)   
fecha_inicio = sys.argv[1]
fecha_fin = sys.argv[2]
ticker = sys.argv[3]

# Nombre de la base de datos
db = 'base_datos_stock.db'

# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect(db)
cursor = conn.cursor()

# Crear una tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS base_datos_stock (
     ticker TEXT,
        date DATETIME,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume INTEGER
       )
''')


# Configura tu clave de API de Polygon 
api_key = 'BKBQV4W8f6AhUrMr_7TV0Q1Rgp16RZ5N'

# Validar las fechas
while True:
    try:
        fecha_inicio = pd.to_datetime(fecha_inicio)
        fecha_fin = pd.to_datetime(fecha_fin)
        if fecha_inicio <= fecha_fin:
            break
        else:
            print("La fecha de inicio debe ser anterior a la fecha final. Inténtalo de nuevo.")
            fecha_inicio = input(">>> Ingrese fecha de inicio (formato YYYY-MM-DD):\n")
            fecha_fin = input(">>> Ingrese fecha de fin (formato YYYY-MM-DD):\n")
    except ValueError:
        print("Formato de fecha incorrecto. Inténtalo de nuevo.")
        fecha_inicio = input(">>> Ingrese fecha de inicio (formato YYYY-MM-DD):\n")
        fecha_fin = input(">>> Ingrese fecha de fin (formato YYYY-MM-DD):\n")

print(">>> Pidiendo datos a la API  ...\n")

# Construir la URL de la API
url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fecha_inicio.strftime("%Y-%m-%d")}/{fecha_fin.strftime("%Y-%m-%d")}?apiKey={api_key}'
print(url)
# Realizar la solicitud a la API y obtener los datos en formato JSON
response = requests.get(url)
data = response.json()
a = [response.json()]

#Configuramos esta subfunción para que luego de conectar se inserten los datos 
def insertVaribleIntoTable( ticker  , date , open, high , low , close, volume ):
    try:
    # Antes de realizar la solicitud a la API, verificar si los datos ya existen en la base de datos
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM base_datos_stock
        WHERE ticker = ? AND  date = ?
        ''', (ticker, str(date) ))

        result = cursor.fetchone()

        if result and result[0] > 0:
            print(f"Los datos para el ticker {ticker} y fecha  de {date} ya existen en la base de datos. No se realizará insert.")
        else:
            print(">>> Ejecuta insert de datos  ...\n")
            sqlite_insert_with_param = """INSERT INTO base_datos_stock
                          (ticker  , date , open, high , low , close, volume  )
                          VALUES (?, ?, ?, ?, ? , ?, ? );"""
            data_tuple = ( ticker  , date , open, high , low , close, volume   )
            cursor.execute(sqlite_insert_with_param, data_tuple)
            conn.commit()
            cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if conn:
            conn.close()
      
# Verificar si la solicitud fue exitosa --> Valor OK = 200 
if response.status_code == 200:
    print("Ya solicité los datos y volvieron ok")
    # Extraer los valores que te interesan del JSON, por ejemplo, el array de 'results'
    # validamos que results tenga info preguntando la cantidad del 'queryCount' si viene en cero no tiene datos 
    if data['queryCount'] == 0:
          print("No se informan datos para la seleccion") 
    else:
        results = data['results']
        for i in range(len(a)):

            b = a[i].get('results')

            for j in range(len(b)):
                insertVaribleIntoTable( ticker , datetime.date.fromtimestamp(b[j].get('t')/1000.00) ,float(b[j].get('o'))  ,float(b[j].get('h')),float(b[j].get('l')) ,float(b[j].get('c')) ,float(b[j].get('v')))
else:
    print(f"Error al obtener datos de la API. Código de estado: {response.status_code}")
    print(f"Mensaje de error: {data['error']}")
