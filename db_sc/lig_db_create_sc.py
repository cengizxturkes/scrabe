from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["ea_sports"]

# Koleksiyon
ratings_response_collection = db["ratings_response"]

# MongoDB'den ilk dokümanı al
doc = ratings_response_collection.find_one()

if doc:
    try:
        # `teamGroups` dizisini bul
        team_groups = doc.get("response", {}).get("pageProps", {}).get("ratingsFilters", {}).get("teamGroups", [])
        if team_groups:
            print(f"Team Groups bulundu: {len(team_groups)} grup.")
            
            # Lig bilgilerini al
            leagues = []
            for group in team_groups:
                league_name = group.get("label")  # `label` alanı lig adını içeriyor
                if league_name:
                    leagues.append(league_name)
            print(f"Toplam {len(leagues)} lig bulundu: {leagues}")
        else:
            print("Team Groups bulunamadı.")
    except Exception as e:
        print(f"Veriyi işlerken hata oluştu: {e}")
else:
    print("Koleksiyonda doküman bulunamadı!")
