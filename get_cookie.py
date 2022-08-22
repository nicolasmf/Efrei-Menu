import json
import os
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

with open("variables.json", "r") as file:
    data = json.load(file)

    if data["username"] == "" and data["password"] == "":

        driver = webdriver.Firefox()
        driver.get("https://auth.myefrei.fr/")

    else:
        print("[*] Getting cookie...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        driver = webdriver.Firefox(options=options)
        driver.get("https://auth.myefrei.fr/")

        username = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='username']"))
        )
        password = driver.find_element(By.XPATH, "//*[@id='password']")
        submit = driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[1]/form/div[4]/div/button"
        )

        username.send_keys(data["username"])
        password.send_keys(data["password"])

        submit.click()

WebDriverWait(driver, 120).until(
    EC.text_to_be_present_in_element((By.TAG_NAME, "h5"), "Bienvenue sur myEfrei !")
)

cookies = driver.get_cookies()

for i in cookies:
    if i["name"] == "myefrei.sid":
        myefrei_sid = unquote(i["value"])

os.system("cls" if os.name == "nt" else "clear")

driver.close()
