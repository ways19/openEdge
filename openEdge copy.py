from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pygetwindow as gw
import pyautogui
import configparser
from pathlib import Path


# ====== PATH RELATIF ======
BASE_DIR = Path(__file__).resolve().parent
EDGE_DRIVER_PATH = BASE_DIR / "driver" / "msedgedriver.exe"

# ====== SETUP WEBDRIVER ======
options = webdriver.EdgeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-software-rasterizer")
options.add_experimental_option("detach", True)

service = Service(executable_path=str(EDGE_DRIVER_PATH))
driver = webdriver.Edge(service=service, options=options)

# Buat objek configparser
config = configparser.ConfigParser()

# Baca file konfigurasi
config.read('config.ini')

# Ambil nilai dari file config
url = config.get('DEFAULT', 'url')  # Bagian default
klinik = config.get('DEFAULT', 'klinik')
username = config.get('DEFAULT', 'username')
password = config.get('DEFAULT', 'password')


# Buka aplikasi web
driver.get(url)

time.sleep(3)
# Cek apakah jendela ditemukan sebelum mengaksesnya
windows = gw.getWindowsWithTitle("Sistem")

if windows:
    edge_window = windows[0]  # Ambil jendela pertama yang cocok
    screen_width, screen_height = pyautogui.size()
 # Pindahkan Edge ke layar kedua (geser ke kanan)
    edge_window.moveTo(screen_width + 50, 100)  # Geser ke layar kedua
    pyautogui.press("f11")  # Aktifkan fullscreen
else:
    exit()
time.sleep(3)
# Cari elemen input username dan password (pastikan selector sesuai dengan elemen di halaman)
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

# time.sleep(30)
# Tutup browser (opsional)
# driver.quit()