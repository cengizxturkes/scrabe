from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
ea_sports_db = client["ea_sports"]  # Kaynak veritabanı
tr_menajer_db = client["TRMenajer"]  # Hedef veritabanı

# Kaynak koleksiyonlar
team_ratings_collection = ea_sports_db["team_ratings"]

# Hedef koleksiyonlar
teams_collection = tr_menajer_db["takimlar"]
players_collection = tr_menajer_db["oyuncular"]

# Tüm takımları al
all_teams = teams_collection.find()  # TRMenajer'deki tüm takımlar
for team in all_teams:
    team_id = team["_id"]  # Takımın kendi ID'si (MongoDB tarafından atanmış)
    league_id = team["league_id"]  # Lig ID'si
    original_team_id = team["id"]  # Kaynak `team_ratings` koleksiyonundaki takım ID'si

    # Kaynak `team_ratings` koleksiyonundan bu takımın oyuncularını al
    team_ratings_doc = team_ratings_collection.find_one({"team_id": original_team_id})
    if team_ratings_doc:
        players = team_ratings_doc.get("data", {}).get("items", [])
        for player in players:
            # Oyuncu verisine takım ve lig bilgisi ekle
            player_data = {
                **player,
                "team_id": team_id,  # MongoDB'deki takımın ID'si
                "league_id": league_id  # MongoDB'deki ligin ID'si
            }
            # Oyuncuyu `oyuncular` koleksiyonuna ekle
            players_collection.insert_one(player_data)
        print(f"{len(players)} oyuncu eklendi: Takım {team['label']}")
    else:
        print(f"Takım için oyuncu bulunamadı: {team['label']}")
