from flask import Flask, request, jsonify, abort
import nacl.signing
import nacl.exceptions
import os

app = Flask(__name__)

PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")  # Discord Developer Portal'dan al

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
        abort(401, "invalid request signature")

    data = request.json

    if data["type"] == 1:
        return jsonify({"type": 1})

    elif data["type"] == 2:
        return jsonify({
            "type": 4,
            "data": {
                "content": "Hayalet bot buradayım 😎"
            }
        })

    return jsonify({"error": "unknown type"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
