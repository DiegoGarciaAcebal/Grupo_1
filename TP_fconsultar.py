#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#pip install openpyxl
import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit
import sqlite3

#Streamlit run Ventas.py

st.set_page_config(page_title = 'Reporte de Stocks', #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = 'moneybag:', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")


st.title(':clipboard: Reporte de Stocks') #Titulo del Dash
st.subheader('ITBA TP1 - Certificación Python')
st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown

# Creamos una conexión con la base de datos
con = sqlite3.connect('base_datos_stock.db')
 
# Creamos el curso para interactuar con los datos
cursor = con.cursor()

x = 7
 
df= pd.read_sql("SELECT *  ,  substr(date , 1,7) as AnioMes  FROM base_datos_stock", con)

#st.dataframe(df) 
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

 ###Aqui es donde pasa la MAGIA. conectar los selectores con la base de datos


df_seleccion = df.query("ticker == @sticker  & AnioMes == @saniomes" ) #el primer ticker es la columna y el segundo es el selector



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
    color_discrete_sequence = ["#f5b932"] * len(volumen_por_ticker),
    template='plotly_white',

)

fig_volumen_tickers.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid = False))
    
)

#Grafico de Variación de Valuacion de Cierre por Ticket/año mes 
valores_por_fecha = (
    df_seleccion.groupby(by=['AnioMes']).sum()[['volume']].sort_values(by='volume')
)



#Crear la gráfica de barras para los vendedores
fig_valores_por_fecha = px.bar(
    valores_por_fecha,
    x=valores_por_fecha.index,  
    y='volume',
    title = '<b>Volumen por Fecha</b>',
    color_discrete_sequence = ["#F5B932"]*len(valores_por_fecha),
    template = 'plotly_white',
)

fig_valores_por_fecha.update_layout(
    xaxis=dict(tickmode='linear'), # se asegura que todos los ejes de X se muestren
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=False)),
   
)    

## QUIERO PONER LAS DOS GRAFICAS A CADA LADO, UNA AL LADO DE LA OTRA

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
