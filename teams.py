from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import json
import time
import gc  # Çöp toplayıcıyı içe aktar
import os  # Dosya varlığını kontrol etmek için

# Operadriver ile Chrome WebDriver kullan
service = Service('/Users/cengizhanmehmetturkes/Downloads/operadriver_mac64/operadriver')  # Bu yolu güncelle
driver = webdriver.Chrome(service=False)

# Manuel giriş yapmanı bekle
print("Lütfen giriş yap ve ardından https://tr.onlinesoccermanager.com/LeagueTypes sayfasına git.")
driver.get("https://tr.onlinesoccermanager.com/LeagueTypes")

# Girişten sonra belirtilen sayfaya gittiğinde işlemleri başlat
while True:
    if driver.current_url == "https://tr.onlinesoccermanager.com/LeagueTypes":
        print("LeagueTypes sayfasına yönlendirildin, işlemler başlatılıyor.")
        break
    time.sleep(1)

# JSON dosyasının adı
json_file = "osm_lig_bilgileri.json"

# Tüm ligleri çekmek için döngü oluştur
row_index = 5

while True:
    try:
        # Dinamik XPath ile sıradaki lig satırını bul
        print(f"{row_index}. lig satırını arıyor...")
        row_xpath = f"//table/tbody/tr[{row_index}]"
        
        try:
            # Lig satırını bul ve tıkla
            lig_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, row_xpath))
            )
            lig_adi = lig_element.text.strip()
            print(f"{row_index}. lig bulundu: {lig_adi}")
            
            # Lig satırına tıklayarak detay sayfasına git
            lig_element.click()
            time.sleep(1)  # Lig sayfasının yüklenmesini bekle
            print(f"{lig_adi} sayfasına gidildi.")

            # Takımların isimlerini bul ve her biri için tıklayıp oyuncu bilgilerini topla
            kulup_row_index = 1  # Kulüplerin başladığı satır

            while True:
                try:
                    # Takım adının XPath'ini tanımla
                    kulup_xpath = f"                    /html/body/div[3]/div[4]/div/div/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[{kulup_row_index}]/td[1]"
                    kulup_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, kulup_xpath))
                    )
                    kulup_adi = kulup_element.text.strip()
                    print(f"{kulup_row_index}. takım bulundu: {kulup_adi}")

                    # Takım sayfasına git
                    kulup_element.click()
                    time.sleep(1)

                    # Oyuncu bilgilerini pozisyonlarına göre topla
                    oyuncu_bilgileri = []

                    for position_index in range(1, 5):  # 1: Forvet, 2: Orta saha, 3: Defans, 4: Kaleci
                        oyuncu_row_index = 1

                        while True:
                            try:
                                oyuncu_adi_xpath = f"/html/body/div[3]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div/table/tbody[{position_index}]/tr[{oyuncu_row_index}]/td[1]/span"


                                oyuncu_pozisyon_xpath = f"/html/body/div[3]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div/table/tbody[{position_index}]/tr[{oyuncu_row_index}]/td[2]"

                                oyuncu_yetenek_xpath = f"/html/body/div[3]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div/table/tbody[{position_index}]/tr[{oyuncu_row_index}]/td[9]"
                                oyuncu_yetenek_def= f"/html/body/div[3]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div/table/tbody[{position_index}]/tr[{oyuncu_row_index}]/td[7]"
                                oyuncu_yetenek_ort= f"/html/body/div[3]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div/table/tbody[{position_index}]/tr[{oyuncu_row_index}]/td[8]"
                                age= f"/html/body/div[3]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div/table/tbody[{position_index}]/tr[{oyuncu_row_index}]/td[3]"
                                oyuncu_yetenek_for= f"/html/body/div[3]/div[4]/div/div/div/div[1]/div[2]/div/div/div/div/table/tbody[{position_index}]/tr[{oyuncu_row_index}]/td[6]"

                                oyuncu_ucret_xpath = f"/tbody[{position_index}]/tr[{oyuncu_row_index}]/td[11]/span/span[2]"

                                oyuncu_adi = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, oyuncu_adi_xpath))
                                ).text.strip()

                                oyuncu_pozisyon = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, oyuncu_pozisyon_xpath))
                                ).text.strip()
                                oyuncu_def_yetenek = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, oyuncu_yetenek_def))
                                ).text.strip()
                                oyuncu_ort_yetenek = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, oyuncu_yetenek_ort))
                                ).text.strip()
                                oyuncu_for_yetenek = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, oyuncu_yetenek_for))
                                ).text.strip()
                                oyuncu_yas = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, age))
                                ).text.strip()

                                print("oyuncu_for_yetenek"+oyuncu_def_yetenek)
                            

                                oyuncu_ucret = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, oyuncu_ucret_xpath))
                                ).text.strip()

                                # Oyuncu bilgilerini kaydet
                                oyuncu_bilgileri.append({
                                    "playerName": oyuncu_adi,
                                    "position": oyuncu_pozisyon,
                                    "money": oyuncu_ucret,
                                    "defence": oyuncu_def_yetenek,
                                    "midfield": oyuncu_ort_yetenek,
                                    "forward": oyuncu_for_yetenek,
                                    "age": oyuncu_yas,

                                    
                                })
                                print(f"{kulup_adi} - {oyuncu_adi} ({oyuncu_pozisyon}) bilgisi alındı")
                                print(
                                      f" Defans: {oyuncu_yetenek_def}"+
                                        f" Orta saha: {oyuncu_yetenek_ort}"+
                                        f" Forvet: {oyuncu_yetenek_for}")
                                oyuncu_row_index += 1

                            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                                print(f"{kulup_adi} takımında tüm {position_index}. pozisyondaki oyuncular alındı.")
                                break

                    # Yeni kulüp bilgisi
                    yeni_kulup = {
                        "kulup_adi": kulup_adi,
                        "oyuncu_bilgileri": oyuncu_bilgileri
                    }

                    # JSON dosyasını aç, varsa veriyi yükle, yoksa boş bir liste başlat
                    if os.path.exists(json_file):
                        with open(json_file, "r", encoding="utf-8") as f:
                            lig_bilgileri = json.load(f)
                    else:
                        lig_bilgileri = []

                    # Lig zaten mevcut mu kontrol et, yoksa yeni lig oluştur
                    lig_bulundu = False
                    for lig in lig_bilgileri:
                        if lig["lig"] == lig_adi:
                            lig["kulup_bilgileri"].append(yeni_kulup)
                            lig_bulundu = True
                            break

                    if not lig_bulundu:
                        lig_bilgileri.append({
                            "lig": lig_adi,
                            "kulup_bilgileri": [yeni_kulup]
                        })

                    # Güncellenmiş veriyi JSON dosyasına kaydet
                    with open(json_file, "w", encoding="utf-8") as f:
                        json.dump(lig_bilgileri, f, ensure_ascii=False, indent=4)

                    # Çöp toplayıcıyı çalıştır
                    gc.collect()

                    # Bir önceki sayfaya geri dön (Lig sayfasına)
                    driver.back()
                    time.sleep(1)
                    kulup_row_index += 1

                except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                    print(f"{lig_adi} ligi için tüm takımlar alındı.")
                    break

            # Ana sayfaya geri dön ve bir sonraki lige geç
            driver.get("https://tr.onlinesoccermanager.com/LeagueTypes")
            time.sleep(1)
            row_index += 1

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"{row_index}. lig satırında hata oluştu veya tüm ligler işlendi: {e}")
            break

    except Exception as e:
        print(f"Bilinmeyen bir hata oluştu: {e}")
        break

# Tarayıcıyı kapat
driver.quit()
