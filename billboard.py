import requests
from datetime import datetime

BASE_URL = "https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main"

def get_valid_date_for_month(year, month):
    url = f"{BASE_URL}/valid_dates.json"
    dates = requests.get(url).json()

    # Filtra datas do mês/ano escolhidos
    candidates = [
        d for d in dates
        if d.startswith(f"{year}-{month:02d}")
    ]

    if not candidates:
        return None

    # Retorna a primeira semana válida do mês
    return sorted(candidates)[0]

def get_top_songs(year, month, limit=20):
    valid_date = get_valid_date_for_month(year, month)

    if not valid_date:
        return []

    url = f"{BASE_URL}/date/{valid_date}.json"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    songs = []
    for entry in data["data"][:limit]:
        songs.append(f"{entry['song']} — {entry['artist']}")

    return songs

