# Requerimientos Funcionales:

Se solicitó implementar un programa que permita leer datos de una API de finanzas, guardarlos en una base de datos y graficarlos.

El programa debía presentar un Menú Principal con las siguientes dos opciones:

 1. Actualización de Datos
 2. Visualización de Datos

## 1. Actualización de Datos

Al seleccionar está opción en el Menú Principal el programa debía solicitar al usuario el valor de un ticker, una fecha de inicio y una fecha de fin para luego pedir los valores a la API **(https://polygon.io/docs/stocks/getting-started)** y guardar estos datos en una base de datos SQL.

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

python = 3.1.11

pandas==1.5.2

plotly==5.11.0

streamlit==1.15.2

openpyxl==3.0.10


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

A continuación se describe de manera resumida el funcionamiento del archivo **TP_factualizar.py** que como mencionamos anteriormente es el que "corre" y ejecuta la consulta a la API cada vez que el usuario lo solicita.

_1) Importa las siguientes librerías: pandas, requests, json, sqlite3, datetime y time._

_2) Recibe los **3 parámetros definidos** en la función **call_TP_actualizar** que son los parámetros definidos en los RF._

_3) Crea la variable **db** de tipo str y le asigna el valor **base_datos_stock.db**._

_4) Conecta o crea la base de datos si no existe._

_5) Si no existe crea la tabla con los siguientes datos: **ticker, date, open, high, low, close, y volume**_

_6) Le asigna a la variable **api_key** la clave de la API Polygon._

_7) Con un **while** se verifica que la **fecha de inicio (fecha_inicio)** sea anterior a la **fecha de finalizacion (fecha_fin)** y que el formato sea el correcto._

_9) Posteriormente con un **f string** se construye la url de la API y se le asgina a la variable **url**._

_10) Mediante el paquete **request** se realiza la consulta con el método **get()** y dado que la respuesta es en formato JSON, se utiliza el método **json()** para convertir la misma a un objeto de Python. Luego los datos convertidos se almacenan en la variable **data** y en la variable **a**, esta última en formato de lista._

_11) Luego se define la funcion **insertVaribleIntoTable** que recibe los 7 valores definidos en el punto (5) y la misma verifica si el valor existe en la tabla, y si no existe lo inserta._

_12) Por último mediante un **if** se verifica si la solicitud fue exitosa aplicando el un **status_code** sobre el response._

_13) De ser exitosa (código == 200) se verifica con otro **if** si el **queryCount** de la variable **data**. Si es == 0 indica que no se informaron datos para la selección. Caso contrario recorre la variable **a** con un **for** y llama a la función **insertVaribleIntoTable** para insertar lo valores._

_14) De no ser exitosa informa mediante un **print()** que no se pudieron obtener datos de la API._

Volviendo al programa principal (TP_fconsultar_actualizar.py)

Debemos agregar a la sidebar un boton para que el usuario "haga click" una vez introducidos los 3 parametos de búsqueda y llame a la función call_TP_actualizar, la cual como explicamos anteriormente recibe esos 3 parámetros y subejecuta el arhcivo TP_factualizar_p.py.

    optionActualizar = st.sidebar.button("Hacer Click para actualizar datos" )
    if optionActualizar == True:
        print("hiciste click en Actualizar fconsultar_actualizar")
        print (selected_dateD, selected_dateH, input_string)
        call_TP_actualizar(str(selected_dateD), str(selected_dateH), input_string)
        print(optionActualizar)

A continuación a fin de podes realizar filtros en los gráficos se deben generar en el sidebar dichos "botones". Los filtros permiten elegir el Ticker y la fecha (YYYY-MM): 

    st.sidebar.header("Consulta - Filtros:")
    
    sticker = st.sidebar.multiselect(
        "Seleccione el Ticker",
        options = df['ticker'].unique(),
        default = df['ticker'].unique()
    )

    saniomes = st.sidebar.multiselect(
        "Seleccione Fecha - YYYY-MM",
        options = df['AnioMes'].unique(),
        default = df['AnioMes'].unique()
    )

Una vez definidos los filtros, se deben conectar los "botones" selectores a la base de datos. Para esto mediante SQLITE3 se realizan 2 .query a los 2 DataFrame previamente generados (df y df2) donde el primer ticker es la columna y el segundo es el selector.

    df_seleccion = df.query("ticker == @sticker  & AnioMes == @saniomes" )
    df2_seleccion =  df2.query("ticker == @sticker  & AnioMes == @saniomes" )

Un paso adicional para poder graficar los datos en función del tiempo es hacer con PANDAS hacer un .pivot_table (similar al transpose de excel) sobre el segundo DataFrame:

    table = pd.pivot_table(df2_seleccion, values='close', index=['date'],
                           columns=['ticker'], aggfunc="max")

Antes de pasar a la generación de los gráficos se definen 2 variables que totalizan el Volumen Total y la Cantidad de Registros a fin de poder mostrarlas en el headear del dashboard,

    total_operaciones = int(df_seleccion['volume'].sum())

    total_registros = int(df_seleccion['date'].count())

    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader("Volumen total:")
        st.subheader(f"US $ {total_operaciones:,}")

    with right_column:
        st.subheader('Cantidad Registros:')
        st.subheader(f" {total_registros}")
   
    st.markdown("---")

y se muestra la tabla con el resumen de la información presente en la base de dato:

    st.dataframe(df_seleccion)

Por último se definen mostrar 3 gráficos:

Grafico de Volumen (de Operaciones) por Ticker y Grafico de Volúmen por Período (Mes) estos 2 en formato gráficos de barra mediante la librería PLOTLY; y un Grafico de Valor de Cierre por día en formato de linea que se genera mediante STREAMLIT.

Para generar ambos gráficos de barra primero hay que tener 2 variables que con al información necesaria que se generan mediante la agrupación, suma y ordenamientos de los DataFrames.

    volumen_por_ticker = (df_seleccion.groupby(by=['ticker']).sum()[['volume']].sort_values(by='volume'))
    valores_por_fecha = (df_seleccion.groupby(by=['AnioMes']).sum()[['volume']].sort_values(by='volume'))

Luego con PLOTLY se asigna el tipo de gráfico (.bar - de barra en este caso) y se definen los ejes, la orientación, el título y el color. Todo esto se guarda en una variable que luego será llama por STREMLIT para mostrar el gráfico en el dashboard.

Para el Grafico de Volumen (de Operaciones) por Ticker:

    fig_volumen_tickers = px.bar(
        volumen_por_ticker,
        x = 'volume',
        y=volumen_por_ticker.index,
        orientation= "h",
        title = "<b>Volumen por Ticker</b>", #con las b lo que hago es ponerlo en bold
        color_discrete_sequence = ["#1199bb"] * len(volumen_por_ticker),
        template='plotly_white',
    )

    fig_volumen_tickers.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis=(dict(showgrid = False))
    )

Para el Grafico de Volúmen por Período (Mes):

    fig_valores_por_fecha = px.bar(
        valores_por_fecha,
        x=valores_por_fecha.index,  
        y='volume',
        title = '<b>Volumen por Período</b>',
        color_discrete_sequence = ["#F5B932"]*len(valores_por_fecha),
        template = 'plotly_white',
    )

    fig_valores_por_fecha.update_layout(
        #xaxis=dict(tickmode='linear'), # se asegura que todos los ejes de X se muestren
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=(dict(showgrid=False)),
    )

Por último se define el layout dentro del dashboard, se agrega con un markdown abajo de la tabla resumen el Grafico de Valor de Cierre por día en formato de linea que se genera mediante STREAMLIT,

    st.markdown(" **Variación Diaria - Valor al Cierre (p/Ticker)**  ")
    st.line_chart(table)

y debajo los dos gráficos de barra generados con PLOTLY uno al lado del otro.

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_valores_por_fecha, use_container_width = True)
    right_column.plotly_chart(fig_volumen_tickers, use_container_width = True)

Fin del código.
