# Steam API Endpoint format:
# http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>
#
# Format can be any of:
#
#     json - The output will be returned in the JSON format
#     xml - Output is returned as an XML document
#     vdf - Output is returned as a VDF file.
#
# If you do not specify a format, your results will be returns in the JSON format.
import os
import requests
import datetime
import csv
from dotenv import load_dotenv

load_dotenv("secrets.env")

API_KEY = os.getenv("STEAM_API")
STEAM_ID = os.getenv("STEAM_ID")

ENDPOINT = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAM_ID}"

response = requests.get(ENDPOINT)
response.raise_for_status()
data = response.json()

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
game_count = data["response"]["game_count"]

file_exists = os.path.isfile("steam_game_count.csv")
with open("steam_game_count.csv", mode="a", encoding="UTF-8", newline="") as file:
    header = ["date", "game_count"]
    writer = csv.DictWriter(file, fieldnames=header)

    if not file_exists:
        writer.writeheader()

    writer.writerow({"date": current_date, "game_count": game_count})
