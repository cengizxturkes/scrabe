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
            
            # Takım ID'lerini al
            all_team_ids = []
            for group in team_groups:
                teams = group.get("teams", [])
                for team in teams:
                    team_id = team.get("id")
                    if team_id:
                        all_team_ids.append(team_id)
            print(f"Toplam {len(all_team_ids)} takım ID bulundu: {all_team_ids}")
        else:
            print("Team Groups bulunamadı.")
    except Exception as e:
        print(f"Veriyi işlerken hata oluştu: {e}")
else:
    print("Koleksiyonda doküman bulunamadı!")
