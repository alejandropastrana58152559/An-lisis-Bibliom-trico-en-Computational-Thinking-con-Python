from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Opciones de navegación
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') 
options.add_argument('--disable-extensions')  

driver_path = 'D:\\algoritmos\\chromeDrive\\chromedriver-win64\\chromedriver.exe'
service = Service(driver_path)

# Inicializar el driver Chrome
driver = webdriver.Chrome(service=service, options=options)

# Navegar a la página
driver.get('https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ifkv=ARpgrqe9o73hJoXwRDJJ_XK5lfhkfjoypi-3hkSNZeOc7HSXkToo2drOtAUAqJkJQV5ow_UafVqrWg&rip=1&sacu=1&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-82393520%3A1727402714969828&ddm=0')

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#identifierId')))\
    .send_keys('')

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.BqKGqe.Jskylb.TrZEUc.lw1w4b')))\
    .click()

time.sleep(5)

WebDriverWait(driver, 15)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.whsOnd.zHQkBf')))\
    .send_keys('')

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.BqKGqe.Jskylb.TrZEUc.lw1w4b')))\
    .click()

driver.get('https://library.uniquindio.edu.co/')

# Esperar a que el campo de búsqueda esté disponible y escribir "computational thinking"
WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#edit-search-form-stacks-external-catalogs-customdescubridor-eds-search-bar-container-query')))\
    .send_keys('computational thinking')

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#edit-search-form-stacks-external-catalogs-customdescubridor-eds-search-bar-container-actions-submit')))\
    .click()

driver.get('https://login.intelproxy.com/v2/conector/google/solicitar?cuenta=7Ah6RNpGWF22jjyq&url=ezp.2aHR0cHM6Ly9zZWFyY2guZWJzY29ob3N0LmNvbS9sb2dpbi5hc3B4PyZkaXJlY3Q9dHJ1ZSZzaXRlPWVkcy1saXZlJmF1dGh0eXBlPWlwJmN1c3RpZD1uczAwNDM2MyZnZW9jdXN0aWQ9Jmdyb3VwaWQ9bWFpbiZwcm9maWxlPWVkcyZicXVlcnk9Y29tcHV0YXRpb25hbCt0aGlua2luZw--')


WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.svg-inline--fa.fa-caret-down.fa-w-10')))\
    .click()

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li#downshift-0-item-0')))\
    .click()


WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.eb-button.eb-button--flat-icon.eb-tool-button__button')))\
    .click()

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[13]/div/div/div[2]/div/div[2]/fieldset/div/span[3]')))\
    .click()

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.eb-button.eb-button--default.nuc-bulk-download-modal-footer__button')))\
    .click()

 
time.sleep(10000)
