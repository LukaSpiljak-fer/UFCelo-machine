from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="./chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Consent')]"))
)
try:
    driver.find_element(By.XPATH, "//*[contains(text(), 'Consent')]").click()
except:
    pass

WebDriverWait(driver, 4).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)
if(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))):
    driver.find_element(By.XPATH, "//*[contains(text(), 'English')]").click()

WebDriverWait(driver, 4).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
)

bigCookie = driver.find_element(By.ID, "bigCookie")


while True:
    cookiesCount = driver.find_element(By.ID, "cookies").text.split(" ")[0]
    cookiesCount = int(cookiesCount.replace(",", ""))

    for i in range(4):
        try:
            productPrice = int(driver.find_element(By.ID, "productPrice" + str(i)).text.replace(",", ""))
        except:
            continue

        if(cookiesCount >= productPrice):
            driver.find_element(By.ID, "product" + str(i)).click()
            break

    bigCookie.click()
