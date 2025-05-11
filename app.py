from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot aktif 👻"

@app.route("/interactions", methods=["POST"])
def interactions():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
