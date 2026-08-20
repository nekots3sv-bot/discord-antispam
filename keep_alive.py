from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Discord Anti-Spam Bot is running!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    thread = Thread(target=run)
    thread.start()