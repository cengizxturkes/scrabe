import requests
from pymongo import MongoClient

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]
collection = db["your_collection_name"]

# cURL'deki başlıklar
headers = {
    "accept": "application/json; charset=utf-8",
    "accept-language": "tr-TR, en-GB",
    "appversion": "3.215.0",
    "authorization": "Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjU4MDY5MDIwNCIsIndvcmxkIjoiMSIsInRlYW0iOiIxODUwOTI0MjEsMTgiLCJuYmYiOjE3MzI2MDcyODcsImV4cCI6MTczMjYwODQ4NywiaXNzIjoiT1NNLkF1dGhlbnRpY2F0aW9uIn0.ih9mWdgkrFnD8yqwiR8ugqzMnGoxwr0Wv_YZJ6r2i6w...",
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

# API URL
url = "https://web-api.onlinesoccermanager.com/api/v1/leagueTypes"

# GET isteği
response = requests.get(url, headers=headers)

# İstek başarılı mı kontrol et
if response.status_code == 200:
    data = response.json()  # JSON veriyi al
    print("API'den gelen veri:", data)

    # MongoDB'ye kaydetme
    if isinstance(data, list):
        collection.insert_many(data)  # Eğer veri bir liste ise
    elif isinstance(data, dict):
        collection.insert_one(data)  # Eğer veri bir sözlük ise

    print("Veri MongoDB'ye başarıyla kaydedildi!")
else:
    print(f"İstek başarısız oldu! Durum kodu: {response.status_code}")
    print("Hata mesajı:", response.text)
