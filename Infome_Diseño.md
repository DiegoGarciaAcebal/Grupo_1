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

La primera parte del código (luego de importar la librerías) define la configuración de la pagina mediante el .set_page_config de la librería STREAMLIT:

    st.set_page_config(page_title = 'Consulta de Stocks',
                       page_icon = 'moneybag:',
                       layout="wide")

Posteriormente se definen el Título y Subtítulo que apareceran en el DashBoard:

    st.title(':clipboard: Consulta de Stocks')
    st.subheader('ITBA TP - Grupo 1 - Certificación Python')
    st.markdown('##')

El primer paso es crear la conección a la base de datos mediante la libería SQLITE3,

    con = sqlite3.connect('base_datos_stock.db')
    cursor = con.cursor()

para luego mediante la librería PANDAS generar dos DataFrame con los datos de cada consultas:

    df = pd.read_sql("SELECT *  ,  substr(date , 1,7) as AnioMes  FROM base_datos_stock order by date desc , ticker asc  ", con)
    df2 = pd.read_sql ("SELECT    substr(date , 1,7) as AnioMes , date     , ticker  ,  close from  base_datos_stock group by substr(date , 1,7),date  , ticker order by date ", con)

El primer DataFrame (df) es un query a la base de datos donde se solicitan todos los datos disponibles.

El segundo DataFrame (df2) es un query a la base de datos donde se solicitan los datos necesarios para realizar la comparativa por fechas.

A continuación se definen una "Barra Lateral" (sidebar) donde el usuario podrá ingresar los 3 datos necesarios para realizar la consulta a la API y de esta manera actualizar la base de datos.

Los 3 datos a ingresar de acuerdo a lo solicitado en los RF son: Fechas Desde, Fecha Hasta y el código de la acción (Ticker).

    st.sidebar.header("Opciones para actualizar")      
    selected_dateD = st.sidebar.date_input("Seleccione Fecha Desde")
    selected_dateH = st.sidebar.date_input("Seleccione Fecha Hasta")
    input_string = st.sidebar.text_input("Ingreso Ticker", "")

Una vez definido el sidebar donde el usuario podrá ingresar los 3 parámetros de búsqueda, se define una función que recibe esos mismos tres parámetros y mediante la libreria SUBPROCESS ejectua el segundo archivo .py denominado TP_factualizar_p.py que es el que realiza la consulta a la API y actualiza la base de datos.

    def call_TP_actualizar(parameter1, parameter2, parameter3):
        try:
            result = subprocess.run(["python", "TP_factualizar_p.py", parameter1, parameter2, parameter3], capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error calling TP_actualizar_p.py: {e.stderr}")

A continuación se describe el funcionamiento del archivo TP_fconsultar_actualizar.py que como mencionamos anteriormente es el que "corre" y ejecuta la consulta cada vez que el usuario "hace click" en el sidebar Opciones para actualizar.

### TP_fconsultar_actualizar.py:

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

