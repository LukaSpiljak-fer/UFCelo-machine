from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import locale
import time


def RejectCookies():
    WebDriverWait(driver, 5).until(                    #Reject all cookies
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accept all')]"))
    )
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Accept all')]").click()
    except:
        pass

def DateIsPast(eventDate):
    date_format = "%A, %B %d, %Y"
    eventDate = datetime.strptime(eventDate, date_format)
    currDate = datetime.now()
    return eventDate < currDate


csvFile = open("D:\\UFCELOMDB\\allFightHistory.txt", "w")
data = ""
site = 'https://www.tapology.com/fightcenter/promotions/1-ultimate-fighting-championship-ufc'
service = Service(executable_path="./chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(site)



RejectCookies()

try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "last"))
    ).click()
except:
    print("failed to load main page")      #goto last site

try:
    while True:
        RejectCookies()

        content = driver.find_element(By.ID, "content")

        pageEvents = content.find_elements(By.CSS_SELECTOR, ".div.flex.flex-col.border-b.border-solid.border-neutral-700")

        for event in reversed(pageEvents):      #ide po redu po eventima unatrag
            eventDetails = event.find_element(By.CSS_SELECTOR, ".promotion.flex.flex-wrap.items-center.leading-6.whitespace-nowrap.overflow-hidden")
            
            eventName = eventDetails.find_element(By.CSS_SELECTOR, ".border-b.border-tap_3.border-dotted.hover\\:border-solid")
            eventDate = eventDetails.find_elements(By.TAG_NAME, "span")[3].text

            if(DateIsPast(eventDate)):          #provjerava jel se event dogodil, ak je ide na stranicu eventa
                eventName.click()
                RejectCookies()

                fightCardDiv = driver.find_element(By.ID, "sectionFightCard")
                fightCard = fightCardDiv.find_elements(By.TAG_NAME, "li")

                for fight in reversed(fightCard):
                    fighter1 = fight.find_elements(By.CLASS_NAME, "link-primary-red")[0].text
                    fighter2 = fight.find_elements(By.CLASS_NAME, "link-primary-red")[2].text
                    data += fighter1 + "-" + fighter2 + ","

                
                driver.back()
                RejectCookies()
            else:
                csvFile.write(data)             #ako se fight jos nije dogodil to znaci da smo gotovi lets go
                print("FINISHED!")
                break
        csvFile.write(data)
        try:
            driver.find_element(By.XPATH, '//*[@rel="prev"]').click()
        except:
            break

except Exception as e:
    print("Error in scraping:", e)