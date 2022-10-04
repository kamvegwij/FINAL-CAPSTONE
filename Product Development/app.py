from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET'] = '123'
#chat server
socketio = SocketIO(app, core_allowed_origins='*')

@socketio.on('message')
def handle_message(message):
    print("Recieved message: " + message)
    if message != "User connected":
        send(message, broadcast=True)

#pages
@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/help", methods = ['GET', 'POST'])
def help():
    return render_template("help.html")

@app.route("/chat", methods = ['GET', 'POST'])
def chat():
    return render_template("chat.html")

if __name__ == "__main__":
    socketio.run(app, host="localhost")