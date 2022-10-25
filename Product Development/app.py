from flask import Flask, render_template, url_for, session, request, redirect
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from twilio.rest import Client

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

#chat server
socketio = SocketIO(app)



###########################################################################################################################################
# database creation and connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickhelp_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# TABLES

class User(db.Model):
    # columns in the user table
    user_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    user_name = db.Column(db.String(30), nullable=False)
    user_last_name = db.Column(db.String(30), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    user_contact_no = db.Column(db.String(20), nullable=False)
    user_password = db.Column(db.String(30), nullable=False)

    def __init__(self, name, lastname, email, contact, password):
        self.user_name = name
        self.user_last_name = lastname
        self.user_email = email
        self.user_contact_no = contact
        self.user_password = password
        
    def __repr__(self):
        return f'{self.user_id}~{self.user_name}~{self.user_last_name}~{self.user_email}~{self.user_contact_no}~{self.user_password}'


class Psychologist(db.Model):
    # columns in the psychologist table
    psychologist_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    psychologist_name = db.Column(db.String(30), nullable=False)
    psychologist_last_name = db.Column(db.String(30), nullable=False)
    psychologist_email = db.Column(db.String(50), nullable=False)
    psychologist_contact_no = db.Column(db.String(20), nullable=False)
    psychologist_availability_time = db.Column(db.String(20), nullable=False)
    psychologist_password = db.Column(db.String(30), nullable=False)

    def __init__(self, name, lastname, email, contact, availability_time, password):
        self.psychologist_name = name
        self.psychologist_last_name = lastname
        self.psychologist_email = email
        self.psychologist_contact_no = contact
        self.psychologist_availability_time = availability_time
        self.psychologist_password = password

    def __repr__(self):
        return f'{self.psychologist_id}~{self.psychologist_name}~{self.psychologist_last_name}~{self.psychologist_email}~{self.psychologist_contact_no}~{self.psychologist_availability_time}~{self.psychologist_password}'


class Helpline(db.Model):
    # columns in the helpline table
    helpline_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=False)
    category = db.Column(db.String(20), nullable=False)
    tell_number = db.Column(db.String(20), nullable=False)

    def __init__(self, category, tell_number):
        self.category = category
        self.tell_number = tell_number
    
    def __repr__(self):
        return f'{self.helpline_id}~{self.category}~{self.tell_number}'


class Message(db.Model):
    # columns in the message table
    message_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    message = db.Column(db.String(10000), nullable=False)
    message_to = db.Column(db.String(30), nullable=False)
    message_from = db.Column(db.String(30), nullable=False)
    sent_datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    psychologist_id = db.Column(db.Integer, db.ForeignKey("psychologist.psychologist_id"))

    def __init__(self,message, messageto, messagefrom, sentdatetime, userid, psychologistid):
        self.message = message
        self.message_to = messageto
        self.message_from = messagefrom
        self.sent_datetime = sentdatetime
        self.user_id = userid
        self.psychologist_id = psychologistid
    
    def __repr__(self):
        return f'{self.message_id}~{self.message}~{self.message_to}~{self.message_from}~{self.sent_datetime}~{self.user_id}~{self.psychologist_id}'

class Online(db.Model):
    # columns in the online table
    _id = db.Column(db.Integer,  nullable=False, primary_key=True, unique=True)
    name = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(30), nullable=False)

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f'{self._id}~{self.name}~{self.type}'
# end of database creation and connection
###########################################################################################################################################


# used to listen for the message event then ...
#   -- send the message
#   -- update the message table in the database
@socketio.on('message')
def handle_message(message):
    # split the message to this format ::: [message, name of the person its going to]
    # I used "confidant" to refer someone the person that is logged in is talking to 
    # (if you are a user --> psychologist is confidant)  (if you are a psychologist --> user is confidant)
    rec_message = message.split("~")
    confidant = rec_message[1]

    # print the message and the confidant in the terminal (to check whether or not the messages are received)
    print("Recieved message: " + rec_message[0])
    print("var: " + confidant)

    # the server sends the message to you and the confidant            (????CHECK BROADCAST !!!!) and test it  --------------------------------------------------------------------------------------------------------------- TODO
    send(session['username'] +  "~" + rec_message[0], broadcast=True) #broadcast set to true send the message to everyone on the server chat.

    # if the message is 'joined the chat' ::: don't store it in the database
    if rec_message[0] != 'joined the chat':
        # if the person logged in is a user, we use the code below
        if session['user'] == "user":
            try:
                # query the database and store the message in the database
                with app.app_context():
                    user_row = User.query.filter_by(user_email=session['username']).first()
                    confidant_row = Psychologist.query.filter_by(psychologist_name=confidant).first()

                    message = rec_message[0]

                    message_row = Message(message, confidant_row.psychologist_name, user_row.user_name, datetime.now(), user_row.user_id, confidant_row.psychologist_id)

                    db.session.add(message_row)
                    db.session.commit()
            except:
                # error querying the database
                return "<h2>ERROR QUERYING THE DATABASE</h2>"
                
        # if the person logged in is a psychologist, we use the code below  
        elif session['user'] == "psychologist":
            try:
                # query the database and store the message in the database
                with app.app_context():
                    psychologist_row = Psychologist.query.filter_by(psychologist_email=session['username']).first()
                    confidant_row = User.query.filter_by(user_name=confidant).first()

                    
                    message = rec_message[0]

                    message_row = Message(message, confidant_row.user_name, psychologist_row.psychologist_name, datetime.now(), confidant_row.user_id, psychologist_row.psychologist_id)

                    db.session.add(message_row)
                    db.session.commit()
            except:
                # error with querying the database
                return "<h2>ERROR QUERYING THE DATABASE</h2>"


# pages
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # query the database, log the user in, and update the online table 
            with app.app_context():
                try:
                    # when the person logging in is a user
                    user_row = User.query.filter_by(user_email=username).first()
                    session['user'] = "user"

                    if password == user_row.user_password:
                        session['username'] = user_row.user_name

                        # add the user to the online table after loggin in
                        online_row = Online(user_row.user_name, session['user'])
                        db.session.add(online_row)
                        db.session.commit()

                        return redirect(url_for("home"))
                    else:
                        # wrong password 
                        # flash a message  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- TODO
                        return render_template("login.html")
                except:
                    # when the person logging in is a psychologist
                    psychologist_row = Psychologist.query.filter_by(psychologist_email=username).first()
                    session['user'] = "psychologist"

                    if password == psychologist_row.psychologist_password:
                        session['username'] = psychologist_row.psychologist_name

                        # add the psychologist to the online table after loggin in
                        online_row = Online(psychologist_row.psychologist_name, session['user'])
                        db.session.add(online_row)
                        db.session.commit()

                        return redirect(url_for("home"))
                    else:
                        # wrong password
                        # flash a message  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- TODO
                        return render_template("login.html")                 
        except:
            # user does not exist / error reading the database
            # flash a message  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- TODO
            return render_template("login.html")
        
    return render_template("login.html")


@app.route("/home", methods = ['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/help", methods = ['GET', 'POST'])
def help():
    return render_template("help.html")


@app.route("/chat", methods = ['GET', 'POST'])
def chat():
    # displaying online users on the chat page
    online_users = []

    # if the person logged in is a user it will show online psychologists
    if session['user'] == "user":
        with app.app_context():
            online_rows = Online.query.filter_by(type='psychologist').all()
            
            for user in online_rows:
                online_users.append(user.name)

    # if the person logged in is a psychologist it will show online users
    elif session['user'] == "psychologist":
         with app.app_context():
            online_rows = Online.query.filter_by(type='user').all()
            
            for user in online_rows:
                online_users.append(user.name)

    return render_template("chat.html", online_users=online_users)


@app.route("/chat/<confidant>")
def chat_send(confidant):
    # displaying online users on the chat page
    online_users = []
    message_displayed = ""

    # if the person logged in is a user
    if session['user'] == "user":
        try:
            # query the database
            with app.app_context():
                user_row = User.query.filter_by(user_email=session['username']).first()
                confidant_row = Psychologist.query.filter_by(psychologist_name=confidant).first()

                # quering the database for messages
                message_displayed = Message.query.with_entities(Message.message, Message.message_to, Message.message_from, Message.sent_datetime).filter_by(user_id=user_row.user_id, psychologist_id=confidant_row.psychologist_id).order_by(Message.sent_datetime).all()

                # query and show online psychologists
                online_rows = Online.query.filter_by(type='psychologist').all()
                
                for user in online_rows:
                    online_users.append(user.name)
        except:
            # error querying the database
            return "<h1>ERROR QUERYING THE DATABASE</h1>"
            
            
    elif session['user'] == "psychologist":
        try:
            # query the database
            with app.app_context():
                psychologist_row = Psychologist.query.filter_by(psychologist_email=session['username']).first()
                confidant_row = User.query.filter_by(user_name=confidant).first()

                # quering the database for messages
                message_displayed = Message.query.with_entities(Message.message, Message.message_to, Message.message_from, Message.sent_datetime).filter_by(user_id=confidant_row.user_id, psychologist_id=psychologist_row.psychologist_id).order_by(Message.sent_datetime).all()

                # query and show online psychologists
                online_rows = Online.query.filter_by(type='user').all()
            
                for user in online_rows:
                    online_users.append(user.name)
        except:
            # error with querying the database
            return "<h1>ERROR QUERYING THE DATABASE</h1>"

    return render_template("chatroom.html", confid=confidant, online_users=online_users, messages=message_displayed)
 


@app.route("/logout")
def logout():
    return "logged out"


if __name__ == "__main__":
    socketio.run(app, debug=True)
