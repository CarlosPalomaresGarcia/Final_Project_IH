# Importaciones

import pandas as pd
import os

# Importaciones Selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import time


#driver configuration Selenium
opciones=Options()
opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.headless=False    # si True, no aperece la ventana (headless=no visible)
opciones.add_argument('--start-maximized')         # comienza maximizado
opciones.add_argument('user-data-dir=selenium')    # mantiene las cookies
opciones.add_argument('--incognito')
opciones.add_argument('user-data-dir=cookies')    # mantiene las coockies


# URLS Plataformas
url_netflix = 'https://www.justwatch.com/es/proveedor/netflix'
url_amazon = 'https://www.justwatch.com/es/proveedor/amazon-prime-video'
url_disney = 'https://www.justwatch.com/es/proveedor/disney-plus'
url_hbo = 'https://www.justwatch.com/es/proveedor/hbo-max'


# COMIENZA EL WEB SCRAPING

PATH = ChromeDriverManager().install()    # instala driver de chrome
options = webdriver.ChromeOptions() 
options.add_argument('user-data-dir=C:\\Users\\CarlosIronHack1\\AppData\\Local\\Google\\Chrome\\User Data')
driver = webdriver.Chrome('C:\\Users\\CarlosIronHack1\\.wdm\\drivers\\chromedriver\\win32\\114.0.5735.90\\chromedriver.exe',chrome_options=options)      # abre una ventana de chrome

# Entrar en la web
driver.get(url_netflix)

# time.sleep(5)

# shadow_parent = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
# outer = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)
# inner = outer.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
# inner.click()


# Pagina dinamica: Scroll para visualizar todas la lista de las peliculas
for i in range(25):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # todo el scroll
    time.sleep(3)

# Sacar los links de las peliculas
results = driver.find_elements(By.CLASS_NAME,'title-list-grid__item--link')

hipervinculos = []
for link in results:
    link = link.get_attribute('href')
    hipervinculos.append(link)

# Cerrar el navegador cuando acabe de sacar los datos
driver.quit()


hipervinculos = hipervinculos[0:150]

# COMENZAR SCRAPING DE CADA URL (PELICULA)

titulos_lista = []
año_lista = []
genero_lista = []
actores_lista = []
rating_lista = []

f = open('C:\\Users\\CarlosIronHack1\\Desktop\\FinalProject\\readme.txt', 'w')

for i in hipervinculos:
    try:
        ##PATH = ChromeDriverManager().install()    # instala driver de chrome

        driver = webdriver.Chrome('C:\\Users\\CarlosIronHack1\\.wdm\\drivers\\chromedriver\\win32\\114.0.5735.90\\chromedriver.exe',chrome_options=options)      # abre una ventana de chrome

        driver.get(i)

        # time.sleep(2)

        # shadow_parent = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
        # outer = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)
        # inner = outer.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
        # inner.click()


        try:
            titulo = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/h1').text
            
        except:
            try:
                titulo = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/h1').text
            except:
                    titulo = "No Info"
                    pass

        
        try:
            año = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/span').text.split('(')[1]
            año = año.split(')')[0]
            
        except:
            try:
                año = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/span').text.split('(')[1]
                año = año.split(')')[0]
            except:
                    año = "No Info"
                    pass
            
        try:
            genero = driver.find_elements(By.CLASS_NAME, 'detail-infos__value')
            
        except:
            try:
                genero = driver.find_elements(By.CLASS_NAME, 'detail-infos__value')
            except:
                    genero = "No Info"
                    pass
            
        lista_genero = []
        for gen in genero:
            gen = gen.text.strip()
            lista_genero.append(gen)

        genero = lista_genero[1]


        try:
            rating = driver.find_element(By.CLASS_NAME, 'jw-scoring-listing__rating').text
            
        except:
            try:
                rating = driver.find_element(By.CLASS_NAME, 'jw-scoring-listing__rating').text
            except:
                    rating = "No Info"
                    pass


        try:
            actores = driver.find_elements(By.CLASS_NAME, 'title-credit-name')
            
        except:
            try:
                actores = driver.find_element(By.CLASS_NAME, 'title-credit-name')
            except:
                    actores = "No Info"
                    pass

        lista_actores = []
        for act in actores:
            act = act.text.strip()
            lista_actores.append(act)

        driver.quit()

        titulos_lista.append(titulo)
        año_lista.append(año)
        genero_lista.append(genero)
        rating_lista.append(rating)
        actores_lista.append(lista_actores)
        with open('C:\\Users\\CarlosIronHack1\\Desktop\\FinalProject\\readme.txt', 'a') as f: f.write('\n he hecho una peli de netflix ' + i)

    except :
        print("error en la pelicula")  


# Crear diccionario para las columnas del DataFrame

diccionario = {
    'Titulo': titulos_lista,
    'Año': año_lista,
    'Genero': genero_lista,
    'Actores': actores_lista,
    'Rating': rating_lista,
    }

# Crear DataFrame con los datos de cada pelicula

df_netflix = pd.DataFrame(diccionario)

# LIMPIEZA DE COLUMNAS DATA FRAME

df_netflix['Plataforma'] = 'Netflix'

df_netflix['Genero'] = df_netflix['Genero'].str.split().str[0] # Me quedo solo con el primer Genero
#df_netflix['Genero'] = df_netflix['Genero'].str.rstrip(',') # Para quitar la coma que se queda al final

df_netflix['Actores'] = df_netflix['Actores'].str.join(', ')














# COMIENZA EL WEB SCRAPING

##PATH = ChromeDriverManager().install()    # instala driver de chrome

driver = webdriver.Chrome('C:\\Users\\CarlosIronHack1\\.wdm\\drivers\\chromedriver\\win32\\114.0.5735.90\\chromedriver.exe',chrome_options=options)      # abre una ventana de chrome

# Entrar en la web
driver.get(url_amazon)

# time.sleep(5)

# shadow_parent = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
# outer = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)
# inner = outer.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
# inner.click()


# Pagina dinamica: Scroll para visualizar todas la lista de las peliculas
for i in range(25):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # todo el scroll
    time.sleep(3)

# Sacar los links de las peliculas
results = driver.find_elements(By.CLASS_NAME,'title-list-grid__item--link')

hipervinculos = []
for link in results:
    link = link.get_attribute('href')
    hipervinculos.append(link)

# Cerrar el navegador cuando acabe de sacar los datos
driver.quit()


hipervinculos = hipervinculos[0:150]

# COMENZAR SCRAPING DE CADA URL (PELICULA)

titulos_lista = []
año_lista = []
genero_lista = []
actores_lista = []
rating_lista = []


for i in hipervinculos:
    try:
        #PATH = ChromeDriverManager().install()    # instala driver de chrome

        driver = webdriver.Chrome('C:\\Users\\CarlosIronHack1\\.wdm\\drivers\\chromedriver\\win32\\114.0.5735.90\\chromedriver.exe',chrome_options=options)      # abre una ventana de chrome

        driver.get(i)

        # time.sleep(2)

        # shadow_parent = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
        # outer = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)
        # inner = outer.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
        # inner.click()


        try:
            titulo = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/h1').text
            
        except:
            try:
                titulo = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/h1').text
            except:
                    titulo = "No Info"
                    pass

        
        try:
            año = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/span').text.split('(')[1]
            año = año.split(')')[0]
            
        except:
            try:
                año = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/span').text.split('(')[1]
                año = año.split(')')[0]
            except:
                    año = "No Info"
                    pass
            
        try:
            genero = driver.find_elements(By.CLASS_NAME, 'detail-infos__value')
            
        except:
            try:
                genero = driver.find_elements(By.CLASS_NAME, 'detail-infos__value')
            except:
                    genero = "No Info"
                    pass
            
        lista_genero = []
        for gen in genero:
            gen = gen.text.strip()
            lista_genero.append(gen)

        genero = lista_genero[1]


        try:
            rating = driver.find_element(By.CLASS_NAME, 'jw-scoring-listing__rating').text
            
        except:
            try:
                rating = driver.find_element(By.CLASS_NAME, 'jw-scoring-listing__rating').text
            except:
                    rating = "No Info"
                    pass


        try:
            actores = driver.find_elements(By.CLASS_NAME, 'title-credit-name')
            
        except:
            try:
                actores = driver.find_element(By.CLASS_NAME, 'title-credit-name')
            except:
                    actores = "No Info"
                    pass

        lista_actores = []
        for act in actores:
            act = act.text.strip()
            lista_actores.append(act)

        driver.quit()

        titulos_lista.append(titulo)
        año_lista.append(año)
        genero_lista.append(genero)
        rating_lista.append(rating)
        actores_lista.append(lista_actores)
        with open('C:\\Users\\CarlosIronHack1\\Desktop\\FinalProject\\readme.txt', 'a') as f: f.write('\n he hecho una peli de amazon ' + i)
    except :
        print("error en la pelicula")  


# Crear diccionario para las columnas del DataFrame

diccionario = {
    'Titulo': titulos_lista,
    'Año': año_lista,
    'Genero': genero_lista,
    'Actores': actores_lista,
    'Rating': rating_lista,
    }

# Crear DataFrame con los datos de cada pelicula

df_amazon = pd.DataFrame(diccionario)

# LIMPIEZA DE COLUMNAS DATA FRAME

df_amazon['Plataforma'] = 'Amazon Prime Video'

df_amazon['Genero'] = df_amazon['Genero'].str.split().str[0] # Me quedo solo con el primer Genero
#df_amazon['Genero'] = df_amazon['Genero'].str.rstrip(',') # Para quitar la coma que se queda al final

df_amazon['Actores'] = df_amazon['Actores'].str.join(', ')















# COMIENZA EL WEB SCRAPING

#PATH = ChromeDriverManager().install()    # instala driver de chrome

driver = webdriver.Chrome('C:\\Users\\CarlosIronHack1\\.wdm\\drivers\\chromedriver\\win32\\114.0.5735.90\\chromedriver.exe',chrome_options=options)      # abre una ventana de chrome

# Entrar en la web
driver.get(url_disney)

# time.sleep(5)

# shadow_parent = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
# outer = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)
# inner = outer.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
# inner.click()


# Pagina dinamica: Scroll para visualizar todas la lista de las peliculas
for i in range(25):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # todo el scroll
    time.sleep(3)

# Sacar los links de las peliculas
results = driver.find_elements(By.CLASS_NAME,'title-list-grid__item--link')

hipervinculos = []
for link in results:
    link = link.get_attribute('href')
    hipervinculos.append(link)

# Cerrar el navegador cuando acabe de sacar los datos
driver.quit()


hipervinculos = hipervinculos[0:150]

# COMENZAR SCRAPING DE CADA URL (PELICULA)

titulos_lista = []
año_lista = []
genero_lista = []
actores_lista = []
rating_lista = []


for i in hipervinculos:
    try:
        #PATH = ChromeDriverManager().install()    # instala driver de chrome

        driver = webdriver.Chrome('C:\\Users\\CarlosIronHack1\\.wdm\\drivers\\chromedriver\\win32\\114.0.5735.90\\chromedriver.exe',chrome_options=options)      # abre una ventana de chrome

        driver.get(i)

        # time.sleep(2)

        # shadow_parent = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
        # outer = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)
        # inner = outer.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
        # inner.click()


        try:
            titulo = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/h1').text
            
        except:
            try:
                titulo = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/h1').text
            except:
                    titulo = "No Info"
                    pass

        
        try:
            año = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/span').text.split('(')[1]
            año = año.split(')')[0]
            
        except:
            try:
                año = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/span').text.split('(')[1]
                año = año.split(')')[0]
            except:
                    año = "No Info"
                    pass
            
        try:
            genero = driver.find_elements(By.CLASS_NAME, 'detail-infos__value')
            
        except:
            try:
                genero = driver.find_elements(By.CLASS_NAME, 'detail-infos__value')
            except:
                    genero = "No Info"
                    pass
            
        lista_genero = []
        for gen in genero:
            gen = gen.text.strip()
            lista_genero.append(gen)

        genero = lista_genero[1]


        try:
            rating = driver.find_element(By.CLASS_NAME, 'jw-scoring-listing__rating').text
            
        except:
            try:
                rating = driver.find_element(By.CLASS_NAME, 'jw-scoring-listing__rating').text
            except:
                    rating = "No Info"
                    pass


        try:
            actores = driver.find_elements(By.CLASS_NAME, 'title-credit-name')
            
        except:
            try:
                actores = driver.find_element(By.CLASS_NAME, 'title-credit-name')
            except:
                    actores = "No Info"
                    pass

        lista_actores = []
        for act in actores:
            act = act.text.strip()
            lista_actores.append(act)

        driver.quit()

        titulos_lista.append(titulo)
        año_lista.append(año)
        genero_lista.append(genero)
        rating_lista.append(rating)
        actores_lista.append(lista_actores)
        with open('C:\\Users\\CarlosIronHack1\\Desktop\\FinalProject\\readme.txt', 'a') as f: f.write('\n he hecho una peli de disney ' + i)
    except :
        print("error en la pelicula")  


# Crear diccionario para las columnas del DataFrame

diccionario = {
    'Titulo': titulos_lista,
    'Año': año_lista,
    'Genero': genero_lista,
    'Actores': actores_lista,
    'Rating': rating_lista,
    }


# Crear DataFrame con los datos de cada pelicula

df_disney = pd.DataFrame(diccionario)

# LIMPIEZA DE COLUMNAS DATA FRAME

df_disney['Plataforma'] = 'Disney +'

df_disney['Genero'] = df_disney['Genero'].str.split().str[0] # Me quedo solo con el primer Genero
#df_disney['Genero'] = df_disney['Genero'].str.rstrip(',') # Para quitar la coma que se queda al final

df_disney['Actores'] = df_disney['Actores'].str.join(', ')












# COMIENZA EL WEB SCRAPING

#PATH = ChromeDriverManager().install()    # instala driver de chrome

driver = webdriver.Chrome('C:\\Users\\CarlosIronHack1\\.wdm\\drivers\\chromedriver\\win32\\114.0.5735.90\\chromedriver.exe',chrome_options=options)      # abre una ventana de chrome

# Entrar en la web
driver.get(url_hbo)

# time.sleep(5)

# shadow_parent = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
# outer = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)
# inner = outer.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
# inner.click()


# Pagina dinamica: Scroll para visualizar todas la lista de las peliculas
for i in range(25):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # todo el scroll
    time.sleep(3)

# Sacar los links de las peliculas
results = driver.find_elements(By.CLASS_NAME,'title-list-grid__item--link')

hipervinculos = []
for link in results:
    link = link.get_attribute('href')
    hipervinculos.append(link)

# Cerrar el navegador cuando acabe de sacar los datos
driver.quit()


hipervinculos = hipervinculos[0:150]

# COMENZAR SCRAPING DE CADA URL (PELICULA)

titulos_lista = []
año_lista = []
genero_lista = []
actores_lista = []
rating_lista = []


for i in hipervinculos:
    try:
        #PATH = ChromeDriverManager().install()    # instala driver de chrome

        driver = webdriver.Chrome('C:\\Users\\CarlosIronHack1\\.wdm\\drivers\\chromedriver\\win32\\114.0.5735.90\\chromedriver.exe',chrome_options=options)      # abre una ventana de chrome

        driver.get(i)

        # time.sleep(2)

        # shadow_parent = driver.find_element(By.CSS_SELECTOR, '#usercentrics-root')
        # outer = driver.execute_script('return arguments[0].shadowRoot', shadow_parent)
        # inner = outer.find_element(By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')
        # inner.click()


        try:
            titulo = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/h1').text
            
        except:
            try:
                titulo = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/h1').text
            except:
                    titulo = "No Info"
                    pass

        
        try:
            año = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/span').text.split('(')[1]
            año = año.split(')')[0]
            
        except:
            try:
                año = driver.find_element(By.XPATH, '//*[@id="base"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/span').text.split('(')[1]
                año = año.split(')')[0]
            except:
                    año = "No Info"
                    pass
            
        try:
            genero = driver.find_elements(By.CLASS_NAME, 'detail-infos__value')
            
        except:
            try:
                genero = driver.find_elements(By.CLASS_NAME, 'detail-infos__value')
            except:
                    genero = "No Info"
                    pass
            
        lista_genero = []
        for gen in genero:
            gen = gen.text.strip()
            lista_genero.append(gen)

        genero = lista_genero[1]


        try:
            rating = driver.find_element(By.CLASS_NAME, 'jw-scoring-listing__rating').text
            
        except:
            try:
                rating = driver.find_element(By.CLASS_NAME, 'jw-scoring-listing__rating').text
            except:
                    rating = "No Info"
                    pass


        try:
            actores = driver.find_elements(By.CLASS_NAME, 'title-credit-name')
            
        except:
            try:
                actores = driver.find_element(By.CLASS_NAME, 'title-credit-name')
            except:
                    actores = "No Info"
                    pass

        lista_actores = []
        for act in actores:
            act = act.text.strip()
            lista_actores.append(act)

        driver.quit()

        titulos_lista.append(titulo)
        año_lista.append(año)
        genero_lista.append(genero)
        rating_lista.append(rating)
        actores_lista.append(lista_actores)
        with open('C:\\Users\\CarlosIronHack1\\Desktop\\FinalProject\\readme.txt', 'a') as f: f.write('\n he hecho una peli de HBO ' + i)
    except :
        print("error en la pelicula")  


# Crear diccionario para las columnas del DataFrame

diccionario = {
    'Titulo': titulos_lista,
    'Año': año_lista,
    'Genero': genero_lista,
    'Actores': actores_lista,
    'Rating': rating_lista,
    }


# Crear DataFrame con los datos de cada pelicula

df_hbo = pd.DataFrame(diccionario)

# LIMPIEZA DE COLUMNAS DATA FRAME

df_hbo['Plataforma'] = 'HBO Max'

df_hbo['Genero'] = df_hbo['Genero'].str.split().str[0] # Me quedo solo con el primer Genero
#df_hbo['Genero'] = df_hbo['Genero'].str.rstrip(',') # Para quitar la coma que se queda al final

df_hbo['Actores'] = df_hbo['Actores'].str.join(', ')



basededatos = pd.concat([df_netflix, df_hbo, df_disney, df_amazon])

# GUARDAR EL ARCHIVO EN FORMATO JSON

if os.path.exists('C:/Users/CarlosIronHack1/Desktop/FinalProject/allFilms.json'):
    # Eliminar el archivo existente
    os.remove('C:/Users/CarlosIronHack1/Desktop/FinalProject/allFilms.json')
    basededatos.to_json('C:/Users/CarlosIronHack1/Desktop/FinalProject/allFilms.json', orient='records')
else:
    basededatos.to_json('C:/Users/CarlosIronHack1/Desktop/FinalProject/allFilms.json', orient='records')





#BLOBSTORAGE
connection_string = 'DefaultEndpointsProtocol=https;AccountName=blobpeliculas;AccountKey=DUnbRQ+BAYdP+ZcCn0mDiSVcCohlp1/J2CT0LQwjICIA36XlTiR3HFfU5pVpaD+XNDVKpkmoYSuJ+AStmSK81Q==;EndpointSuffix=core.windows.net'
container_name = 'contenedorproyectopeliculas'
blob_name = 'blobpeliculas'
file_path = 'C:/Users/CarlosIronHack1/Desktop/FinalProject/allFilms.json'

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
containers = blob_service_client.list_containers()
for container in containers:
    print(container.name)

# Create the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# DeleteBlobStorage
try:
    blob_client = blob_service_client.get_blob_client(container=container_name, blob="blobpeliculas")
    blob_client.delete_blob()
except:
    print("no existe el archivo")

#create file
with open(file_path, "rb") as data:
    blob_client.upload_blob(data)
