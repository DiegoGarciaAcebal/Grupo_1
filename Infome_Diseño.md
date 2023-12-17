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

A fin de presentar el menú principal y los diferentes gráficos de manera más amigable, se recurrió a la libería STREAMLIT dado que la misma genera una interfaz gráfica intuitiva y facil de usar, evitando que el usuario tenga que ejecutar los comandos desde la terminal.

## Modularización:

Dado que se solicitó un programa que presentara un Menú Principal con dos opciones (Actualizar y Visualizar Datos) se definió modularizar el programa de la siguiente manera:

Un archivo principal denominado TP_fconsultar_actualizar.py que define el marco en Streamlit y que cuando es solicitado ejecuta la consulta para actualizar a la base de datos mediante la ejecución del archivo TP_factualizar_p.py.

## Liberías:

Las liberías utilizadas son:




A continuación se describe el funcionamiento y la lógica del programa: 

### TP_fconsultar_actualizar.py:

La primera parte del códico luego de importar la librerías

   st.set_page_config(page_title = 'Consulta de Stocks', #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = 'moneybag:', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

   st.title(':clipboard: Consulta de Stocks') #Titulo del Dash
   st.subheader('ITBA TP - Grupo 1 - Certificación Python')
   st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown


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

