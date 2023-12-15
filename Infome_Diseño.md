# Requerimientos Funcionales:

Se solicitó implementar un programa que permita leer datos de una API de finanzas, guardarlos en una base de datos y graficarlos.

El programa debía presentar un Menú Principal con las siguientes dos opciones:

 1. Actualización de Datos
 2. Visualización de Datos

## 1. Actualización de Datos

Al seleccionar está opción en el Menú Principal el programa debía solicitar al usuario el valor de un ticker, una fecha de inicio y una fecha de fin para luego pedir los valores a la API (https://polygon.io/docs/stocks/getting-started) y guardar estos datos en una base de datos SQL.

## 2. Visualización de Datos

Bajo está opción el programa debe permitir dos visualizaciones de datos:

 a) Resumen: Debe imprimir un resumen de los datos guardados en la base de datos.
 
    AAPL - 2022/01/01 <-> 2022/07/01

 b) Gráfico del Ticker: debe permitir graficar los datos guardados para un ticker específico.

# Informe de Diseño:

## Interfaz:

Se decidió utilizar STREAMLIT como interfaz para que el usuario pueda utilizar el programa de manera más amigable y no dependa de la terminal.

## Modularización:

Dado que se solicitó un programa que presentara un Menú Principal con dos opciones (Actualizar y Visualizar Datos) se definió modularizar el programa de la siguiente manera:

INSERTAR IMAGEN

En dos archivos .py. El primero denominado TP_factualizar.py que realizar la consulta a la base de datos y el segundo denominado TP_fconsultar.py que permite visualizar el resumen o la información del Ticker...

TP_factualizar.py:

1) Importa las siguientes librerías: pandas, requests, json, sqlite3, datetime y time.
2) Crea la variable db de tipo str y le asigna el valor base_datos_stock.db.
3) Conecta o crea la base de datos.

4) Le asigna a la variable api_key la clave de la API Polygon.
5) Mediante las variables ticker, fecha_inicio y fecha_fin se le solicita al usuario que ingrese los datos.
6) Mediante un while se verifica que la fecha de inicio (fecha_inicio) sea anterior a la fecha de finalizacion (fecha_fin) y que el formato sea el correcto.
7) Posteriormente con un f string se construye la url de la API y se le asgina a la variable url.
8) mediante el paquete request se realiza la consulta con el método .get y la respuesta se pasa a formato json.
9) Se define una función para que luego de conectarse se inserten los datos.
10) Por último mediante un if se verifica si la solicitud fue exitosa aplicando el método .status_code sobre el response.
   
TP_fconsultar.py:

1)

