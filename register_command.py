import os
import requests
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")
GUILD_ID = os.getenv("YOUR_GUILD_ID")

if not DISCORD_TOKEN or not APPLICATION_ID or not GUILD_ID:
    print("❌ Ortam değişkenleri eksik! .env dosyanı kontrol et.")
    exit(1)

url = f"https://discord.com/api/v10/applications/{APPLICATION_ID}/guilds/{GUILD_ID}/commands"

headers = {
    "Authorization": f"Bot {DISCORD_TOKEN}",
    "Content-Type": "application/json"
}

# Slash komutları tanımı
commands = [
    {
        "name": "selam",
        "description": "Bot selam verir",
        "type": 1
    },
    {
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
                "description": "Embed rengi (#hex kodu)",
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
]

# Her komutu sırayla Discord'a gönder
for cmd in commands:
    response = requests.post(url, headers=headers, json=cmd)
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ Komut yüklendi: /{cmd['name']}")
    else:
        print(f"❌ Hata (/ {cmd['name']}): {response.status_code}\n{response.text}")
