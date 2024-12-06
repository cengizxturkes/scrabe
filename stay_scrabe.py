import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service

# Operadriver ile Chrome WebDriver kullan
service = Service('/Users/cengizhanmehmetturkes/Downloads/operadriver_mac64/operadriver')  # Bu yolu güncelle
driver = webdriver.Chrome(service=False)

# URL'yi aç
url = "https://staybeautiful.com.tr/collections/bitkisel-urunler"
driver.get(url)
time.sleep(5)  # Sayfanın tamamen yüklenmesi için bekle

# Dinamik içerik varsa sayfanın sonuna kadar kaydır
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Yeni içeriklerin yüklenmesi için bekle
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Ürünlerin isimlerini, fiyatlarını ve URL'lerini bul
product_elements = driver.find_elements(By.CSS_SELECTOR, "ul li div div div div a span")
product_price_elements = driver.find_elements(By.CSS_SELECTOR, "ul li div div div div div div dl div dd span")
product_url_elements = driver.find_elements(By.CSS_SELECTOR, "ul li div div div div a")
product_image_elements = driver.find_elements(By.CSS_SELECTOR, "ul li div div div div div img")  # Görsel için

# Ürün isimleri, fiyatları ve URL'lerini eşleştir
products = []
for name_element, price_element, url_element in zip(product_elements, product_price_elements, product_url_elements):
    name = name_element.text.strip()
    price = price_element.text.strip()
    url = url_element.get_attribute('href')
    if name and price and url:  # Hem isim, hem fiyat, hem URL doluysa ekle
        products.append({"product_name": name, "price": price, "product_url": url})

# Sonuçları JSON dosyasına kaydet
output_file = "product_names_with_prices_and_urls.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(products, file, ensure_ascii=False, indent=4)

print(f"Ürün isimleri, fiyatları ve URL'leri '{output_file}' dosyasına JSON formatında kaydedildi.")

# Tarayıcıyı kapat
driver.quit()