from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import pygetwindow as gw
import pyautogui
import configparser
from pathlib import Path

# ====== SETUP WEBDRIVER ======
options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-software-rasterizer")
options.add_experimental_option("detach", True)

# pakai webdriver-manager agar driver selalu cocok dengan versi Edge
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

# ====== CONFIG ======
config = configparser.ConfigParser()
config.read('config.ini')

url = config.get('DEFAULT', 'url')
klinik = config.get('DEFAULT', 'klinik')
username = config.get('DEFAULT', 'username')
password = config.get('DEFAULT', 'password')

# ====== AKSI ======
driver.get(url)
time.sleep(3)

username_field = driver.find_element(By.NAME, "LOGIN")  # Ganti dengan selector yang sesuai
password_field = driver.find_element(By.NAME, "PASSWORD")  # Ganti dengan selector yang sesuai

login_button = driver.find_element(By.CSS_SELECTOR, "a#button-1041.x-btn.x-unselectable.x-btn-soft-saphire-small")
# login_button = driver.find_element(By.CSS_SELECTOR, "a#x-btn.x-unselectable.x-btn-soft-saphire-small")  # Ganti dengan selector yang sesuai

# Masukkan username dan password
username_field.send_keys(username)
password_field.send_keys(password)

# Klik tombol login
login_button.click()

# Tunggu beberapa detik untuk memastikan login berhasil
time.sleep(2)
menu_button = driver.find_element(By.CSS_SELECTOR, "#button-1048-btnEl.x-btn-button.x-btn-button-default-toolbar-small")
menu_button.click()
time.sleep(0.5)
informasi_element = driver.find_element(By.XPATH, "//div[text()='Informasi']")
informasi_element.click()
time.sleep(0.5)
driver.find_element(By.XPATH, "//div[@class='thumb-title']//strong[text()='Informasi Pengunjung']").click()
time.sleep(2)
# checkbox = driver.find_element(By.XPATH, "//tr[td/div[contains(text(),'Klinik Penyakit Dalam')]]//div[@unselectable='on']")
checkbox = driver.find_element(By.XPATH, f"//tr[td/div[contains(text(),'{klinik}')]]//div[@unselectable='on']")
checkbox.click()
checkbox1 = driver.find_element(By.XPATH, "//input[@id='checkbox-1132-inputEl']")
checkbox1.click()
time.sleep(2)

mulai_button = driver.find_element(By.XPATH, "//a[@id='button-1135']//span[contains(text(),'Mulai')]")
mulai_button.click()