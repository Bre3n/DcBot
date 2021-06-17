from threading import Thread

from flask import Flask, jsonify, request

app = Flask("")


@app.route("/")
def home():
    return "Bot jest ONLINE"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()