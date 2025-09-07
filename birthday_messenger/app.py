from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json, os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

FILENAME = "chat_history.json"
ME_NAME = "Marcus"
HER_NAME = "Ellen"

THEMES = {
    "calm": {
        "bg": "#f0f4f8",
        "me_bubble": "#d1e7dd",
        "her_bubble": "#f8d7da",
        "text": "#212529",
        "accent": "#0d6efd"
    }
}

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_history():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    history = load_history()
    return render_template("index.html", history=history, me_name=ME_NAME, her_name=HER_NAME, theme=THEMES["calm"])

@socketio.on("send_message")
def handle_send_message(data):
    sender = data.get("sender")
    text = data.get("text")
    if not text.strip():
        return
    msg = {"sender": sender, "text": text, "time": timestamp()}
    history = load_history()
    history.append(msg)
    save_history(history)
    emit("receive_message", msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
