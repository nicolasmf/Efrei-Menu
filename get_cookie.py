import json
import os
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException


def connect_manually() -> str:

    with open("variables.json", "r") as file:
        data = json.load(file)
        if data["browser"].lower() == "firefox":
            driver = webdriver.Firefox()
        else:
            driver = webdriver.Chrome()

    driver.get("https://auth.myefrei.fr/")

    WebDriverWait(driver, 120).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h5"), "Bienvenue sur myEfrei !")
    )

    cookies = driver.get_cookies()

    for i in cookies:
        if i["name"] == "myefrei.sid":
            myefrei_sid = unquote(i["value"])

    driver.close()

    return myefrei_sid


def connect_automatically() -> str:
    print("[*] Getting cookie...")

    with open("variables.json", "r") as file:
        data = json.load(file)
        if data["browser"].lower() == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

            driver = webdriver.Firefox(options=options)

        else:
            options = ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

            driver = webdriver.Chrome(options=options)

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

    # Check for possible captcha
    while True:
        try:
            if driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[1]/form/div[3]/div/div/div/iframe",
            ):
                print("[*] Captcha detected, please connect mannually")
                driver.close()
                return connect_manually()

        except NoSuchElementException:
            try:
                if driver.find_elements_by_xpath(
                    "/html/body/div/div[2]/main/div[3]/div/div/h5"
                ):
                    break
            except NoSuchElementException:
                pass

    cookies = driver.get_cookies()

    for i in cookies:
        if i["name"] == "myefrei.sid":
            myefrei_sid = unquote(i["value"])

    driver.close()

    return myefrei_sid


with open("variables.json", "r") as file:
    data = json.load(file)

    if data["username"] == "" and data["password"] == "":
        myefrei_sid = connect_manually()
    else:
        myefrei_sid = connect_automatically()

os.system("cls" if os.name == "nt" else "clear")
