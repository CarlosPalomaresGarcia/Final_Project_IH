

import pandas as pd

#Selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


#driver configuration
opciones=Options()

opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
opciones.headless=False    # si True, no aperece la ventana (headless=no visible)
opciones.add_argument('--start-maximized')         # comienza maximizado
opciones.add_argument('user-data-dir=selenium')    # mantiene las cookies
opciones.add_argument('--incognito')


# URLS para utilizar
url_noeleccion = 'https://www.justwatch.com/es'   # Web vacia
url_netflix = 'https://www.justwatch.com/es/proveedor/netflix'
url_amazon = 'https://www.justwatch.com/es/proveedor/amazon-prime-video'
url_disney = 'https://www.justwatch.com/es/proveedor/disney-plus'
url_hbo = 'https://www.justwatch.com/es/proveedor/hbo-max'


from selenium.webdriver.chrome.options import Options
# opciones del driver
opciones=Options()
# quita la bandera de ser robot
opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
opciones.add_experimental_option('useAutomationExtension', False)
# guardar las cookies
opciones.add_argument('user-data-dir=cookies')    # mantiene las coockies



# Ruta al controlador del navegador (en este caso, Chrome)
driver_path = 'ruta_al_controlador_del_navegador'

# Configurar opciones para el navegador
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Descomenta esta línea si deseas ejecutar el navegador en modo sin cabeza

# Crear una instancia del navegador
driver = webdriver.Chrome(driver_path, options=options)

# Navegar a la página
driver.get('https://www.justwatch.com/es/proveedor/netflix')

# Esperar a que aparezca la ventana emergente de cookies
try:
    wait = WebDriverWait(driver, 10)
    accept_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-testid="uc-accept-all-button"]')))
    accept_button.click()
except (TimeoutException, NoSuchElementException):
    pass

# Realizar otras acciones en la página si es necesario

# Cerrar el navegador
driver.quit()



results_netflix = driver.find_elements(By.CLASS_NAME,'title-list-grid__item--link')
results_netflix

hipervinculos = []
for link in results_netflix:
    link = link.get_attribute('href')
    hipervinculos.append(link)

titles = []
for url in hipervinculos:
    parts = url.split('/')
    last_part = parts[-1]
    title = last_part.replace('-', ' ')
    title = title.capitalize()
    titles.append(title)
    
titles

df = pd.DataFrame(titles)

df.to_json('C:\Users\carlo\Labs IronHack\Final_Project_IH\code\prueba.json', orient='records')