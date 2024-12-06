import requests
from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["ea_sports"]
collection = db["ratings_response"]

# İstek atılacak URL
url = "https://www.ea.com/_next/data/abgpRgHLo-w-pXJN7yvAN/en/games/ea-sports-fc/ratings.json?gender=0&team=45&franchiseSlug=ea-sports-fc"

try:
    # API'ye GET isteği
    response = requests.get(url)
    response.raise_for_status()  # Hata varsa raise et
    
    # JSON yanıtını al
    data = response.json()
    
    # Yanıtı MongoDB'ye kaydet
    collection.insert_one({"url": url, "response": data})
    print("Veri başarıyla kaydedildi!")
except Exception as e:
    print(f"Hata oluştu: {e}")
