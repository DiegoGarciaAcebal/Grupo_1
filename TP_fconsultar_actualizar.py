import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit
import sqlite3
import subprocess

#Streamlit run pantalla de consulta de datos y para datos de entrada para actualizar BD
#Certificación Profesional en Python del ITBA - Grupo_1 (Alonso Roberto, Anconetani Alejandra, Aragona Micaela, García Acebal Diego y Tomás Rodriguez
#Entrega 21-12-2023

st.set_page_config(page_title = 'Reporte de Stocks', #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = 'moneybag:', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")


st.title(':clipboard: Reporte de Stocks') #Titulo del Dash
st.subheader('ITBA TP - Grupo 1 - Certificación Python')
st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown

# Creamos una conexión con la base de datos
con = sqlite3.connect('base_datos_stock.db')
 
# Creamos el curso para interactuar con los datos
cursor = con.cursor()

x = 7
 
df= pd.read_sql("SELECT *  ,  substr(date , 1,7) as AnioMes  FROM base_datos_stock order by date desc , ticker asc  ", con)
df2 = pd.read_sql (" select    substr(date , 1,7) as AnioMes , date     , ticker  ,  close from  base_datos_stock group by substr(date , 1,7),date  , ticker order by date ", con) 
       
#st.dataframe(df)
st.sidebar.header("Opciones para actualizar")      
    # Get a date input from the user
selected_dateD = st.sidebar.date_input("Seleccione Fecha Desde")
    # Get a date input from the user
selected_dateH = st.sidebar.date_input("Seleccione Fecha Hasta")
    # Get a string input from the user
input_string = st.sidebar.text_input("Ingreso Ticker", "")
 

def call_TP_actualizar(parameter1, parameter2, parameter3):
    try:
        # Call script2.py and pass the parameters
        result = subprocess.run(["python", "TP_factualizar_p.py", parameter1, parameter2, parameter3], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error calling TP_actualizar_p.py: {e.stderr}")
        
# Agregas botones buttons to the sidebar        
optionActualizar = st.sidebar.button("Hacer Click para actualizar datos" )
if optionActualizar == True:
        #st.sidebar.write("hiciste click en Actualizar  - llama a función TP1")
        print("hiciste click en Actualizar fconsultar_actualizar")
        print (selected_dateD, selected_dateH, input_string)
        call_TP_actualizar(str(selected_dateD), str(selected_dateH), input_string)
        print( optionActualizar)
        
st.sidebar.header("Opciones a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
sticker = st.sidebar.multiselect(
    "Seleccione el Ticker",
    options = df['ticker'].unique(),
    default = df['ticker'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

 
saniomes = st.sidebar.multiselect(
    "Seleccione Fecha - YYYY-MM",
    options = df['AnioMes'].unique(),
    default = df['AnioMes'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)
   
 ###Aqui es donde se conectan los selectores con la base de datos
df_seleccion = df.query("ticker == @sticker  & AnioMes == @saniomes" ) #el primer ticker es la columna y el segundo es el selector
df2_seleccion =  df2.query("ticker == @sticker  & AnioMes == @saniomes" )
table = pd.pivot_table(df2_seleccion, values='close', index=['date'],
                       columns=['ticker'], aggfunc="max")

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

#Muestra la Grilla Resumen  
st.dataframe(df_seleccion) 
#Trabajo los querys de agrupaciones para los graficos
#Grafico de Volumen de operaciones por Ticket
volumen_por_ticker = (df_seleccion.groupby(by=['ticker']).sum()[['volume']].sort_values(by='volume'))

#Guardar el gráfico de barras en la siguiente variable

fig_volumen_tickers = px.bar(
    volumen_por_ticker,
    x = 'volume',
    y=volumen_por_ticker.index, #se pone el index porque esta como index esa columna dentro del df nuevo que creamos que esta agrupado
    orientation= "h", #horizontal bar chart
    title = "<b>Volumen por Ticker</b>", #con las b lo que hago es ponerlo en bold
    color_discrete_sequence = ["#1199bb"] * len(volumen_por_ticker),
    template='plotly_white',

)

fig_volumen_tickers.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid = False))
    
)

#Grafico de Variación de Volúmen de Operaciones por Año mes 
valores_por_fecha = (
    df_seleccion.groupby(by=['AnioMes']).sum()[['volume']].sort_values(by='volume')
)



#Crear la gráfica de barras para los volumenes por Año y Mes
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

## AGREGO DEBAJO DE LA TABLA -- > Chart de lineas
st.markdown(" **Variación Diaria - Valor al Cierre (p/Ticker)**  ")
st.line_chart(table)

## AGREGO DEBAJO DOS GRAFICAS AGRUPADAS UNA POR FECHA Y OTRA POR TICKER - UNA AL LADO DE LA OTRA

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_valores_por_fecha, use_container_width = True) #esta va al lado izquierdo
right_column.plotly_chart(fig_volumen_tickers, use_container_width = True)


#####################################################################

# Hide Streamlit Style

hide_st_style = """
            <style>
   
            footer {visibility: hidden;}
           
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html= True)
