from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

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

# Tüm satırları çekmek için döngü oluştur
ligler = []
row_index = 1

while True:
    try:
        # Dinamik XPath ile sıradaki satırı bul
        row_xpath = f"//table/tbody/tr[{row_index}]"
        row_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, row_xpath))
        )
        
        # Satırdan metni al ve listeye ekle, sırayla numara ver
        lig_text = row_element.text.strip()
        ligler.append({"sıralama": row_index, "lig": lig_text})
        
        print(f"{row_index}. satır bulundu: {lig_text}")
        row_index += 1  # Bir sonraki satıra geç
        
    except:
        # Eğer satır bulunamazsa döngüyü kır
        print("Tüm satırlar işlendi.")
        break

# Veriyi JSON dosyasına kaydet
with open("osm_ligler.json", "w", encoding="utf-8") as f:
    json.dump(ligler, f, ensure_ascii=False, indent=4)

# Tarayıcıyı kapat
driver.quit()
