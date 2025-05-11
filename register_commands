import os
import requests

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")
GUILD_ID = os.getenv("YOUR_GUILD_ID")

url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands"

headers = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json"
}

json_data = {
    "name": "selam",
    "description": "Bot selam verir",
    "type": 1
}

response = requests.post(url, headers=headers, json=json_data)
print("Komut oluşturuldu:" if response.status_code == 200 else "Hata:", response.text)
