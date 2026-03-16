import os
import sys
import requests
import time
import configparser
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException
import pygetwindow as gw
import pyautogui
import ctypes
import re

# ====== 1. KONFIGURASI PATH DINAMIS ======
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent

DRIVER_DIR = BASE_DIR / "driver"
EDGE_DRIVER_PATH = DRIVER_DIR / "msedgedriver.exe"
CONFIG_PATH = BASE_DIR / "config.ini"
GITHUB_DRIVER_URL = "https://raw.githubusercontent.com/ways19/openEdge/main/driver/msedgedriver.exe"
def alert_app(message, title="Alert"):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

# ====== 2. FUNGSI DOWNLOAD DRIVER DARI GITHUB ======
def download_driver_from_github():
    print("Sedang mengunduh update driver terbaru ...")
    if not DRIVER_DIR.exists():
        DRIVER_DIR.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(GITHUB_DRIVER_URL, stream=True, timeout=30)
        if response.status_code == 200:
            with open(EDGE_DRIVER_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False
    except Exception:
        return False

# ====== 3. FUNGSI INISIALISASI DRIVER ======
def get_driver():
    options = webdriver.EdgeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-software-rasterizer")
    options.add_experimental_option("detach", True)

    # Cek fisik file
    if not EDGE_DRIVER_PATH.exists():
        if not download_driver_from_github():
            alert_app("Driver hilang dan gagal download. Cek internet!", "Error")
            sys.exit()

    try:
        service = Service(executable_path=str(EDGE_DRIVER_PATH))
        return webdriver.Edge(service=service, options=options)
    
    except SessionNotCreatedException as e:
        error_msg = str(e)
        error_msg = str(e)
        print(f"Terdeteksi masalah versi: {error_msg}")
        
        # MENGGUNAKAN REGEX UNTUK AMBIL ANGKA VERSI
        # Mencari pola angka seperti 144.xxx dan 146.xxx
        versions = re.findall(r'\d+\.\d+\.\d+\.\d+', error_msg)
        
        if len(versions) >= 2:
            driver_ver = int(versions[0].split('.')[0])   # Hasilnya: 144
            browser_ver = int(versions[1].split('.')[0])  # Hasilnya: 146
            
            if driver_ver < browser_ver:
                # Driver lama, Browser baru
                print("Driver ketinggalan. Mendownload driver baru dari GitHub...")
                if download_driver_from_github():
                    # Coba jalankan lagi setelah download
                    try:
                        service = Service(executable_path=str(EDGE_DRIVER_PATH))
                        return webdriver.Edge(service=service, options=options)
                    except:
                        alert_app("Gagal sinkronisasi. Hubungi IT RSTN!", "Error")
                        sys.exit()
            
            elif driver_ver > browser_ver:
                # Driver baru, Browser minta diupdate
                msg = f"Driver sudah versi {driver_ver}, tapi Microsoft Edge Anda masih Versi {browser_ver}.\n\nSilakan Update Edge di menu Settings -> About."
                alert_app(msg, "Update Edge Diperlukan")
                sys.exit()
        # Jika tidak ketemu angka versinya, coba download saja sebagai langkah terakhir
        download_driver_from_github()
        sys.exit()         
    except Exception as e:
        alert_app(f"Kesalahan Fatal: {e}", "Error")
        sys.exit()

# ====== 4. LOGIKA UTAMA ======
def main():
    if not CONFIG_PATH.exists():
        alert_app(f"File {CONFIG_PATH.name} tidak ditemukan!", "Error")
        sys.exit()
        
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    
    try:
        url = config.get('DEFAULT', 'url')
        klinik = config.get('DEFAULT', 'klinik')
        username = config.get('DEFAULT', 'username')
        password = config.get('DEFAULT', 'password')
    except Exception as e:
        alert_app(f"Isi config.ini tidak lengkap!\n{e}", "Error")
        sys.exit()

    driver = get_driver()
    driver.get(url)
    
    # Tunggu dan Pindah Layar
    time.sleep(3)
    windows = gw.getWindowsWithTitle("Sistem")
    if windows:
        edge_window = windows[0]
        screen_width, _ = pyautogui.size()
        edge_window.moveTo(screen_width + 50, 100)
        time.sleep(1)
        pyautogui.press("f11")

    wait = WebDriverWait(driver, 15)

    try:
        # Proses Login
        wait.until(EC.presence_of_element_located((By.NAME, "LOGIN"))).send_keys(username)
        driver.find_element(By.NAME, "PASSWORD").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "a#button-1041").click()
        
        # Navigasi Menu (Bagian yang Anda minta)
        print("Membuka Menu...")
        menu_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#button-1048-btnEl")))
        menu_btn.click()
        
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Informasi']"))).click()
        
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='thumb-title']//strong[text()='Informasi Pengunjung']"))).click()
        
        # Pilih Klinik
        time.sleep(2)
        xpath_klinik = f"//tr[td/div[contains(text(),'{klinik}')]]//div[@unselectable='on']"
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_klinik))).click()
        
        # Checkbox Utama
        driver.find_element(By.XPATH, "//input[@id='checkbox-1132-inputEl']").click()
        
        # Tombol Mulai
        time.sleep(1)
        driver.find_element(By.XPATH, "//a[@id='button-1135']//span[contains(text(),'Mulai')]").click()
        
        print("Automasi Berhasil!")

    except Exception as e:
        print(f"Terjadi kesalahan navigasi: {e}")
        # pyautogui.alert(f"Terjadi kesalahan: {e}", "Navigasi Gagal")

if __name__ == "__main__":
    main()