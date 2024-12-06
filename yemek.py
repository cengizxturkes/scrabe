import requests
from pymongo import MongoClient
from time import sleep

# MongoDB'ye bağlan
client = MongoClient("mongodb://localhost:27017/")
db = client["yemek_tarifleri"]  # Veritabanı adı
collection = db["tarif"]  # Koleksiyon adı

# API URL'si
base_url = "https://zagorapi.yemek.com/search/recipe"

# İstek gönder ve sadece benzersiz Posts kısmını kaydet
for start in range(1, 25001):
    try:
        # API isteği
        params = {"start": start, "Rows": 1}
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Hatalar için kontrol

        # Yanıtı JSON olarak al
        data = response.json()

        # Sadece "Posts" kısmını al
        posts = data.get("Data", {}).get("Posts", [])
        for post in posts:
            # Her bir post için kontrol
            if not collection.find_one({"Id": post["Id"]}):
                collection.insert_one(post)
                print(f"Tarif kaydedildi: {post['Id']}")
            else:
                print(f"Tarif zaten mevcut: {post['Id']}")

        # Sunucuyu aşırı yüklememek için kısa bir bekleme süresi
        sleep(0.1)

    except requests.exceptions.RequestException as e:
        print(f"{start}. istekte hata: {e}")
    except Exception as e:
        print(f"{start}. kayıtta hata: {e}")

print("İşlem tamamlandı.")
