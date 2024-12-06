from pymongo import MongoClient
import random

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
tr_menajer_db = client["TRMenajer"]

# Koleksiyonlar
teams_collection = tr_menajer_db["takimlar"]
players_collection = tr_menajer_db["oyuncular"]
active_leagues_collection = tr_menajer_db["active_league"]

# Pozisyon benzerlik haritası
position_alternatives = {
    "Kaleci": [],
    "Stoper": ["Sağ Bek", "Sol Bek"],
    "Sağ Bek": ["Stoper", "Sağ Kanat"],
    "Sol Bek": ["Stoper", "Sol Kanat"],
    "Merkez Defansif Orta Saha Oyuncusu": ["Merkez Orta Saha Oyuncusu"],
    "Merkez Orta Saha Oyuncusu": ["Merkez Ofansif Orta Saha Oyuncusu", "Merkez Defansif Orta Saha Oyuncusu"],
    "Sağ Kanat": ["Sağ Orta Saha"],
    "Sol Kanat": ["Sol Orta Saha"],
    "Santrfor": ["Sol Kanat", "Sağ Kanat"]
}

# Kullanıcıdan bir takım seçmesini isteyelim
selected_team_name = "Fenerbahçe"  # Örnek takım adı
selected_team = teams_collection.find_one({"label": selected_team_name})

if not selected_team:
    print(f"{selected_team_name} adlı takım bulunamadı!")
else:
    # Takım bilgilerini al
    league_id = selected_team["league_id"]
    league_teams = list(teams_collection.find({"league_id": league_id}))

    if not league_teams:
        print(f"Ligde ({league_id}) hiç takım bulunamadı!")
    else:
        print(f"\n{selected_team_name} takımı ve ligindeki diğer takımlar işleniyor...")

        # Aktif Lig Kontrolü
        active_league = active_leagues_collection.find_one({"is_active": True})
        if not active_league:
            active_league_data = {
                "name": f"{selected_team_name} ve Lig Takımları Ligi",
                "is_active": True,
                "active_league_teams": []  # Takım ve oyuncu bilgileri burada saklanacak
            }
            active_league_id = active_leagues_collection.insert_one(active_league_data).inserted_id
            active_league = active_leagues_collection.find_one({"_id": active_league_id})
            print(f"Yeni aktif lig oluşturuldu: {active_league['name']}")

        # 4-3-3 Formasyonu
        formation = {
            "Kaleci": 1,
            "Stoper": 2,
            "Sağ Bek": 1,
            "Sol Bek": 1,
            "Merkez Defansif Orta Saha Oyuncusu": 1,
            "Merkez Orta Saha Oyuncusu": 2,
            "Sağ Kanat": 1,
            "Sol Kanat": 1,
            "Santrfor": 1
        }

        # Lig takımlarını ve oyuncularını aktif lige ekle
        for team in league_teams:
            print(f"\nTakım: {team['label']} işleniyor...")

            # Takım oyuncularını al
            team_players = list(players_collection.find({"team.id": team["id"]}))
            if not team_players:
                print(f"{team['label']} için oyuncu bulunamadı!")
                continue

            # Başlangıç 11 için en iyi oyuncuları seç
            starting_11 = []
            substitutes = []

            for position, count in formation.items():
                # Bu pozisyon için en iyi oyuncuları seç
                position_players = [
                    player for player in team_players
                    if player.get("position", {}).get("label") == position or
                       (player.get("alternatePositions") and isinstance(player.get("alternatePositions"), list) and
                        any(alt.get("label") == position for alt in player.get("alternatePositions")))
                ]

                # Eğer pozisyona uygun oyuncu yoksa, alternatif pozisyonlardan oyuncu seç
                if not position_players:
                    for alt_position in position_alternatives.get(position, []):
                        position_players = [
                            player for player in team_players
                            if player.get("position", {}).get("label") == alt_position or
                               (player.get("alternatePositions") and isinstance(player.get("alternatePositions"), list) and
                                any(alt.get("label") == alt_position for alt in player.get("alternatePositions")))
                        ]
                        if position_players:
                            print(f"{position} pozisyonu için {alt_position} pozisyonundan oyuncu seçildi.")
                            break

                # Eğer hala uygun oyuncu yoksa
                if not position_players:
                    print(f"Pozisyon için uygun oyuncu bulunamadı: {position}")
                    continue

                sorted_position_players = sorted(position_players, key=lambda p: p.get("overallRating", 0), reverse=True)
                best_players_for_position = sorted_position_players[:count]
                starting_11.extend(best_players_for_position)

            # Geri kalan oyunculardan yedekleri seç (Maksimum 7 yedek)
            remaining_players = [player for player in team_players if player not in starting_11]
            sorted_remaining_players = sorted(remaining_players, key=lambda p: p.get("overallRating", 0), reverse=True)
            substitutes = sorted_remaining_players[:7]

            # Tüm oyuncuları işaretleme
            players_data = []
            print("\nİlk 11 Oyuncuları:")
            for player in team_players:
                is11 = player in starting_11
                is_sub = player in substitutes
                player_data = {
                    **player,  # Tüm özellikleri ekle
                    "is11": is11,
                    "is11_position": player.get("position", {}).get("label") if is11 else None,
                    "isSubstitute": is_sub
                }
                players_data.append(player_data)

                # İlk 11'deki oyuncuları yazdır
                if is11:
                    print(f"- {player.get('firstName', '')} {player.get('lastName', '')} ({player.get('position', {}).get('label', 'Bilinmiyor')})")

            print("\nYedek Oyuncular:")
            for sub in substitutes:
                print(f"- {sub.get('firstName', '')} {sub.get('lastName', '')}")

            # Takım ve oyuncu bilgilerini aktif lige ekle
            active_league_team = {
                "team_id": team["_id"],
                "team_name": team["label"],
                "league_id": league_id,
                "players": players_data
            }
            active_leagues_collection.update_one(
                {"_id": active_league["_id"]},
                {"$push": {"active_league_teams": active_league_team}}
            )
            print(f"{team['label']} aktif lige oyuncularıyla birlikte eklendi.")

        print("Tüm takımlar ve oyuncular başarıyla aktif lige eklendi.")
