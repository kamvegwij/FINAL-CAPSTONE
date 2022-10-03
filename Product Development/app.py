from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")

def home():
    return render_template("home.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)