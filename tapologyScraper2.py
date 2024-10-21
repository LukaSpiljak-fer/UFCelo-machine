from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import locale
import time


def RejectCookies():                    #reject cookies svaki put kad se promjeni stranica
    try:
        WebDriverWait(driver, 7).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Reject all')]"))
        )
        driver.find_element(By.XPATH, "//*[contains(text(), 'Reject all')]").click()
    except:
        pass

def DateIsPast(eventDate):
    global checkTime
    try:
        date_format = "%A, %B %d, %Y"
        eventDate = datetime.strptime(eventDate, date_format)
        currDate = datetime.now()
        return eventDate < currDate
    except:                             #ponekad je datum u drukcijem formatu, zato treba provjerit posebno
        print("PROVJERI DATUM: ", eventDate)
        return True
    




csvFile = open("D:\\UFCELOMDB\\allFightHistory2.txt", "w", encoding='utf-8', newline='')
data = ""
site = 'https://www.tapology.com/fightcenter/promotions/1-ultimate-fighting-championship-ufc'
service = Service(executable_path="./chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(site)

eventDate = "no"
checkTime = False
finished = False


RejectCookies()

try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "last"))
    ).click()
except:
    print("failed to load main page")      #goto last site


while True:
    RejectCookies()
    content = driver.find_element(By.ID, "content")

    pageEvents = content.find_elements(By.CSS_SELECTOR, "div.flex.flex-col.border-b.border-solid.border-neutral-700")


    for event in reversed(pageEvents):      #ide po redu po eventima unatrag
        eventDetails = event.find_element(By.CSS_SELECTOR, ".promotion.flex.flex-wrap.items-center.leading-6.whitespace-nowrap.overflow-hidden")
        eventDate = eventDetails.find_elements(By.TAG_NAME, "span")[3].text

        if(DateIsPast(eventDate)):          #provjerava jel se event dogodil

            try:
                fightCard = event.find_element(By.CSS_SELECTOR, "div.w-full.mb-6")
                fightsOnCard = fightCard.find_elements(By.CSS_SELECTOR, "div.flex.h-12.md\\:h-10.bg-white.even\\:bg-neutral-100.w-full.items-center.justify-start.md\\:px-1")

                for fight in reversed(fightsOnCard):
                    fightDetails = fight.find_element(By.CSS_SELECTOR, "div.flex.items-center.justify-start.gap-1.md\\:gap-1\\.5.text-neutral-700")
                    try:
                        outcomeLayer = fightDetails.find_element(By.TAG_NAME, "div")
                        outcome = outcomeLayer.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
                    except:
                        break
                    fighters = fightDetails.find_elements(By.CLASS_NAME, "link-primary-red")
                    fighter1 = fighters[0].get_attribute("innerHTML")
                    fighter2 = fighters[1].get_attribute("innerHTML")
                    data += outcome + "," + fighter1 + "," + fighter2 + "\n"
            except:
                print("Greska datum: " + eventDate)


        else:
            print("FINISHED!")
            csvFile.write(data)             #ako se fight jos nije dogodil, to znaci da smo gotovi posto idemo unatrag
            finished = True
            break

    if(not finished):
        try:
            driver.find_element(By.XPATH, '//*[@rel="prev"]').click()
        except:
            break

csvFile.write(data)
