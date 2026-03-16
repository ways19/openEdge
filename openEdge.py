import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import pygetwindow as gw
import pyautogui
import configparser
from pathlib import Path

# ====== CONFIGURATION ======
config = configparser.ConfigParser()
config.read('config.ini')

url = config.get('DEFAULT', 'url')
klinik = config.get('DEFAULT', 'klinik')
username = config.get('DEFAULT', 'username')
password = config.get('DEFAULT', 'password')

# Matikan log download agar tampilan bersih
os.environ['WDM_LOG_LEVEL'] = '0'

# ====== SETUP WEBDRIVER (HYBRID ONLINE/OFFLINE) ======
options = webdriver.EdgeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_experimental_option("detach", True)

try:
    # 1. Coba install/update driver (Membutuhkan Internet)
    print("Mengecek versi driver...")
    driver_path = EdgeChromiumDriverManager().install()
    service = Service(executable_path=driver_path)
    driver = webdriver.Edge(service=service, options=options)
    print("Driver siap (Online Mode).")

except Exception as e:
    # 2. Jika gagal (Offline), coba cari di cache lokal
    print("Koneksi gagal atau Offline. Mencoba menggunakan driver yang ada...")
    try:
        # Menghubungkan ke driver yang terakhir kali didownload
        from webdriver_manager.core.driver_cache import DriverCacheManager
        cache = DriverCacheManager()
        # Cari path driver terakhir di folder WDM
        last_driver = cache.find_driver(EdgeChromiumDriverManager().driver)
        
        if last_driver:
            service = Service(executable_path=last_driver)
            driver = webdriver.Edge(service=service, options=options)
            print("Driver ditemukan di cache (Offline Mode).")
        else:
            raise Exception("Tidak ada driver di cache. Harap hubungkan internet sekali saja.")
            
    except Exception as offline_err:
        print(f"FATAL ERROR: {offline_err}")
        input("Tekan Enter untuk keluar...")
        exit()

# ====== PROSES AUTOMASI ======
driver.get(url)
time.sleep(3)

# Pindah ke layar kedua & Fullscreen
windows = gw.getWindowsWithTitle("Sistem")
if windows:
    edge_window = windows[0]
    screen_width, _ = pyautogui.size()
    edge_window.moveTo(screen_width + 50, 100)
    time.sleep(1)
    pyautogui.press("f11")
else:
    print("Jendela tidak ditemukan, lanjut tanpa pindah layar.")

# Gunakan WebDriverWait agar lebih stabil dibanding time.sleep manual
wait = WebDriverWait(driver, 10)

try:
    # Login Process
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "LOGIN")))
    password_field = driver.find_element(By.NAME, "PASSWORD")
    
    username_field.send_keys(username)
    password_field.send_keys(password)
    
    login_button = driver.find_element(By.CSS_SELECTOR, "a#button-1041.x-btn.x-unselectable.x-btn-soft-saphire-small")
    login_button.click()

    # Navigasi Menu
    time.sleep(2)
    menu_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#button-1048-btnEl.x-btn-button.x-btn-button-default-toolbar-small")))
    menu_button.click()
    
    time.sleep(0.5)
    informasi_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Informasi']")))
    informasi_element.click()
    
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//div[@class='thumb-title']//strong[text()='Informasi Pengunjung']").click()
    
    # Pilih Klinik dari Config
    time.sleep(2)
    checkbox_klinik = wait.until(EC.element_to_be_clickable((By.XPATH, f"//tr[td/div[contains(text(),'{klinik}')]]//div[@unselectable='on']")))
    checkbox_klinik.click()
    
    checkbox_utama = driver.find_element(By.XPATH, "//input[@id='checkbox-1132-inputEl']")
    checkbox_utama.click()
    
    time.sleep(1)
    mulai_button = driver.find_element(By.XPATH, "//a[@id='button-1135']//span[contains(text(),'Mulai')]")
    mulai_button.click()

    print("Automasi berhasil dijalankan.")

except Exception as e:
    print(f"Terjadi kesalahan saat navigasi: {e}")

# Driver dibiarkan terbuka karena opsi "detach" aktif