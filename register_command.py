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
    "name": "mesaj_gönder",
    "description": "Belirtilen kanala mesaj gönderir",
    "type": 1,
    "options": [
        {
            "name": "kanal",
            "description": "Mesaj gönderilecek kanal",
            "type": 7,
            "required": True
        },
        {
            "name": "metin",
            "description": "Gönderilecek mesaj",
            "type": 3,
            "required": True
        },
        {
            "name": "embed",
            "description": "Mesaj embed mi olsun?",
            "type": 5,
            "required": False
        },
        {
            "name": "başlık",
            "description": "Embed başlığı (isteğe bağlı)",
            "type": 3,
            "required": False
        },
        {
            "name": "renk",
            "description": "Embed rengi (hex: #rrggbb)",
            "type": 3,
            "required": False
        },
        {
            "name": "imza",
            "description": "Embed imzası (footer)",
            "type": 3,
            "required": False
        }
    ]
}

response = requests.post(url, headers=headers, json=json_data)
print("✅ Slash komutu yüklendi!" if response.status_code == 200 else f"❌ Hata: {response.status_code}\n{response.text}")
