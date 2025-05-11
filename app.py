from flask import Flask, request, jsonify, abort
import nacl.signing
import nacl.exceptions
import os
import time

app = Flask(__name__)

# Discord doğrulama için public key
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

# Cooldown sistemi için kullanıcı son kullanımlarını tutarız
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

    # Discord'un doğrulama PING'i
    if data["type"] == 1:
        return jsonify({"type": 1})

    # Slash komut geldiğinde
    if data["type"] == 2:
        user_id = data["member"]["user"]["id"]
        current_time = time.time()

        # Cooldown kontrolü
        if user_id in cooldowns:
            elapsed = current_time - cooldowns[user_id]
            if elapsed < 5:  # 5 saniye cooldown
                return jsonify({
                    "type": 4,
                    "data": {
                        "content": f"Yavaş ol dostum! {round(5 - elapsed, 1)} saniye bekle 👀",
                        "flags": 64  # ephemeral (sadece kullanıcı görür)
                    }
                })

        # Cooldown'u güncelle
        cooldowns[user_id] = current_time

        return jsonify({
            "type": 4,
            "data": {
                "content": "Hayalet bot buradayım 😎"
            }
        })

    return jsonify({"error": "Bilinmeyen istek"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
