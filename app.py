from flask import Flask, request, jsonify, abort
import nacl.signing
import nacl.exceptions
import os
import time
import requests

app = Flask(__name__)

PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
cooldowns = {}

@app.route("/")
def home():
    return "Bot aktif 👻"

@app.route("/interactions", methods=["POST"])
def interactions():
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = request.data.decode('utf-8')

    try:
        verify_key = nacl.signing.VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except nacl.exceptions.BadSignatureError:
        abort(401, "Geçersiz imza")

    data = request.json

    if data["type"] == 1:
        return jsonify({"type": 1})

    if data["type"] == 2:
        command_name = data["data"]["name"]
        user = data["member"]["user"]
        user_id = user["id"]
        username = user["username"]
        current_time = time.time()

        # Cooldown kontrolü
        if user_id in cooldowns and current_time - cooldowns[user_id] < 5:
            return jsonify({
                "type": 4,
                "data": {
                    "content": f"Yavaş ol dostum! {round(5 - (current_time - cooldowns[user_id]), 1)} saniye bekle 👀",
                    "flags": 64
                }
            })

        cooldowns[user_id] = current_time

        if command_name == "mesaj_gönder":
            options = {opt["name"]: opt["value"] for opt in data["data"]["options"]}
            kanal_id = options.get("kanal")
            metin = options.get("metin")
            kullan_embed = options.get("embed", False)
            başlık = options.get("başlık", "")
            renk = options.get("renk", "#00ffff")
            imza = options.get("imza", "")

            headers = {
                "Authorization": f"Bot {BOT_TOKEN}",
                "Content-Type": "application/json"
            }

            if kullan_embed:
                try:
                    renk_int = int(renk.lstrip("#"), 16)
                except:
                    renk_int = 0x00ffff  # default fallback

                payload = {
                    "content": f"<@{user_id}> adlı kullanıcıdan bir mesajınız var:",
                    "embeds": [{
                        "title": başlık or f"{username} adlı kullanıcıdan mesaj",
                        "description": metin,
                        "color": renk_int,
                        "footer": {"text": imza or ""}
                    }]
                }
            else:
                payload = {
                    "content": f"📩 <@{user_id}> adlı kullanıcıdan bir mesajınız var:\n{metin}"
                }

            r = requests.post(
                f"https://discord.com/api/v10/channels/{kanal_id}/messages",
                headers=headers,
                json=payload
            )

            if r.status_code in [200, 201]:
                return jsonify({
                    "type": 4,
                    "data": {
                        "content": f"Mesaj başarıyla gönderildi <#{kanal_id}> ✅",
                        "flags": 64
                    }
                })
            else:
                return jsonify({
                    "type": 4,
                    "data": {
                        "content": f"Mesaj gönderilemedi ❌ ({r.status_code}): {r.text}",
                        "flags": 64
                    }
                })

    return jsonify({"error": "Bilinmeyen istek"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    
