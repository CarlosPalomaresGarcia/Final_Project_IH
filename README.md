# Proyecto de Base de Datos de Películas de Streaming

Este es un proyecto personal que consiste en mantener una base de datos actualizada con todas las películas disponibles en las plataformas de streaming más populares, como Netflix, HBO Max, Amazon Prime Video y Disney+.

El proyecto se ha desarrollado siguiendo los siguientes pasos:

## 1. Web Scraping
Se ha utilizado la librería Selenium en Python para automatizar el proceso de extracción de datos. El código extrae las URL de cada película y luego obtiene información relevante como género, actores, año de lanzamiento, sinopsis y plataforma de streaming en la que esta disponible..

## 2. Configuración de Azure
He utilizado Microsoft Azure para implementar la infraestructura necesaria y garantizar un entorno de ejecución remoto y escalable.

## 3. Máquina Virtual y Contenedor en BlobStorage
He creado una Máquina Virtual en Azure para ejecutar el código de forma remota, eliminando la necesidad de mantener tu ordenador encendido. También he configurado un contenedor en Azure BlobStorage para almacenar la base de datos de películas en la nube en formato json.

## 4. Programación Automatizada
He utilizado el "Scheduled Task" de Microsoft dentro de la Máquina Virtual para automatizar la ejecución diaria del código Python y mantener la base de datos actualizada.

## 5. Dashboard de Power BI
He creado un Dashboard en Power BI para visualizar los datos de las plataformas. El origen de los datos se actualizan diariamente de forma automatica a traves de la cuenta de BlobStorage de Azure.

## 6. Actualización Automática de la Base de Datos
He completado el codigo en Python para generar automáticamente un archivo JSON actualizado y cargarlo en la cuenta de BlobStorage. Esto asegura que la base de datos esté siempre actualizada con las últimas películas disponibles en las plataformas de streaming.