from flask import Flask, render_template, url_for, session, request, redirect
from flask_socketio import SocketIO, send
#from twilio.rest import Client

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

#chat server
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    print("Recieved message: " + message)
    send(session['username'] +  ": \n" + message, broadcast=True) #broadcast set to true send the message to everyone on the server chat.

#pages
@app.route("/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect('/home')

    return render_template("signup.html")

@app.route("/home", methods = ['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/help", methods = ['GET', 'POST'])
def help():
    return render_template("help.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
