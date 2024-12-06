from pymongo import MongoClient
# Takım Bulma
# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
tr_menajer_db = client["TRMenajer"]  # Hedef veritabanı

# Hedef koleksiyonlar
teams_collection = tr_menajer_db["takimlar"]

# Tüm takımları al
all_teams = list(teams_collection.find())  # Takımları liste olarak alıyoruz
if len(all_teams) > 0:
    for team in all_teams:
        team_id = team["_id"]  # Takımın kendi ID'si (MongoDB tarafından atanmış)
        league_id = team["league_id"]  # Lig ID'si
        team_name = team["label"]  # Takım adı (label alanından alınıyor)

        # Takım bilgilerini yazdır
        print(f"Takım adı: {team_name} (ID: {team_id}, Lig ID: {league_id})")
else:
    print("Hiç takım bulunamadı!")
