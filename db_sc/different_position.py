from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
tr_menajer_db = client["TRMenajer"]  # Veritabanı

# Koleksiyonlar
players_collection = tr_menajer_db["oyuncular"]

# Pozisyonları bul
def find_unique_positions():
    # Tüm oyuncuları al ve pozisyon bilgilerini kontrol et
    all_positions = players_collection.distinct("position.label")
    if all_positions:
        print(f"Toplam {len(all_positions)} farklı pozisyon bulundu.")
        for position in all_positions:
            print(f"Pozisyon: {position}")
    else:
        print("Hiç pozisyon bulunamadı!")

# Scripti çalıştır
find_unique_positions()
