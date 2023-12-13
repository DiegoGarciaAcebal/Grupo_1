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





