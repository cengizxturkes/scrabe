import requests
from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["osm_database"]  # Veritabanı adı
leagues_collection = db["leagues"]  # Lig bilgileri
teams_collection = db["teams"]  # Takım bilgileri
players_collection = db["players"]  # Oyuncu bilgileri

# cURL'deki başlıklar
headers = {
    "accept": "application/json; charset=utf-8",
    "accept-language": "tr-TR, en-GB",
    "appversion": "3.215.0",
    "authorization": "Bearer eyJhbGciOiJodHRwOi8vd3d3...",
    "content-type": "application/json; charset=utf-8",
    "origin": "https://tr.onlinesoccermanager.com",
    "platformid": "13",
    "priority": "u=1, i",
    "referer": "https://tr.onlinesoccermanager.com/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Opera";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
}

# Ligler URL
leagues_url = "https://web-api.onlinesoccermanager.com/api/v1/leagueTypes"

# Ligleri çek ve MongoDB'ye kaydet
response = requests.get(leagues_url, headers=headers)

if response.status_code == 200:
    leagues_data = response.json()  # Lig bilgilerini al
    leagues_collection.insert_many(leagues_data)  # Ligleri kaydet

    for league in leagues_data:
        league_id = league["id"]

        # Her ligin takımlarını çek
        teams_url = f"https://web-api.onlinesoccermanager.com/api/v1/leagueTypes/{league_id}/teams"
        team_response = requests.get(teams_url, headers=headers)

        if team_response.status_code == 200:
            teams_data = team_response.json()
            for team in teams_data:
                team["league_id"] = league_id  # Lig ID'sini ekle
                teams_collection.insert_one(team)  # Takımı kaydet

                team_id = team["id"]

                # Her takımın oyuncularını çek
                players_url = f"https://web-api.onlinesoccermanager.com/api/v1/leagueTypes/{league_id}/teams/{team_id}/players"
                player_response = requests.get(players_url, headers=headers)

                if player_response.status_code == 200:
                    players_data = player_response.json()
                    for player in players_data:
                        player["team_id"] = team_id  # Takım ID'sini ekle
                        player["league_id"] = league_id  # Lig ID'sini ekle
                        players_collection.insert_one(player)  # Oyuncuyu kaydet

    print("Tüm veriler başarıyla MongoDB'ye kaydedildi!")
else:
    print(f"Ligleri alma başarısız oldu! Durum kodu: {response.status_code}")
    print("Hata mesajı:", response.text)
