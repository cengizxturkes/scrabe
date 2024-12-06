import requests
import pymongo
from pymongo import MongoClient
import hashlib
import json
import logging
from colorama import Fore, Style

# Initialize colorama
from colorama import init
init(autoreset=True)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["ea_sports_db"]
collection = db["ratings"]

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(message)s")

def log_colored(message, color=Fore.WHITE):
    print(f"{color}{message}{Style.RESET_ALL}")

def save_to_json(file_name, data):
    with open(file_name, "a", encoding="utf-8") as f:
        for record in data:
            json.dump(record, f, ensure_ascii=False)
            f.write("\n")

def fetch_and_save_ratings(base_url, locale="tr", limit=100):
    offset = 0
    headers = {
        "accept": "application/json",
        "user-agent": "Mozilla/5.0"
    }

    while True:
        url = f"{base_url}?locale={locale}&limit={limit}&offset={offset}"
        response = requests.get(url, headers=headers)
        log_colored(f"Response for offset {offset}:", Fore.YELLOW)

        if response.status_code != 200:
            log_colored(f"API call failed: {response.status_code}", Fore.RED)
            break

        try:
            response_data = response.json()
        except ValueError:
            log_colored("Response is not in JSON format.", Fore.RED)
            break

        log_colored(f"Response data keys: {response_data.keys()}", Fore.BLUE)

        data = response_data.get("items", [])
        total_items = response_data.get("totalItems", 0)
        log_colored(f"Length of data: {len(data)}", Fore.CYAN)
        log_colored(f"Total items: {total_items}", Fore.CYAN)

        if not data:
            log_colored("No data found or data has ended.", Fore.MAGENTA)
            break

        new_records = []
        for record in data:
            record_hash = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()

            if collection.find_one({"hash": record_hash}):
                log_colored("Record already exists, skipping.", Fore.YELLOW)
                continue

            record["hash"] = record_hash
            collection.insert_one(record)
            log_colored(f"Record inserted with hash: {record_hash}", Fore.GREEN)

            # Remove '_id' before saving to JSON
            record_without_id = record.copy()
            record_without_id.pop('_id', None)
            new_records.append(record_without_id)

        if new_records:
            save_to_json("ratings.json", new_records)
            log_colored(f"{len(new_records)} records saved to JSON.", Fore.GREEN)
        else:
            log_colored("No new records to save.", Fore.MAGENTA)

        offset += limit
        log_colored(f"Offset updated to {offset}/{total_items}.", Fore.YELLOW)
        if offset >= total_items:
            log_colored("All records have been processed.", Fore.GREEN)
            break

base_url = "https://drop-api.ea.com/rating/ea-sports-fc"
fetch_and_save_ratings(base_url)
