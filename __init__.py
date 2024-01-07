from flask import Flask, render_template, request, url_for, redirect, flash
from flask_socketio import SocketIO, emit
from datetime import datetime

users = set()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!fX3_2#@mDcljf@s4ioGhiq@#42d'
socketio = SocketIO(app)

#Get displays home page which has form for username
#Post submits username entered and displays chat page
@app.route("/", methods=['GET','POST'])
def home_page():
    if request.method == "POST":
        user = request.form['username']
        if user in users:
            #flash("User already Exists!")
            return redirect(url_for('home_page'))
        if request.form['username'] == '':
            return render_template("index.html")
        #users.add(user)
        return  redirect(url_for('enterRoom', username = user))
    else:
        return render_template("index.html")

#Once username is entered user is directed to chatroom.
@app.route("/chatroom/<username>",methods=['GET'])
def enterRoom(username):
    if request.method == 'GET':
        return render_template("chatRoom.html", username1 = username)



#Tests to make sure connection is working
@socketio.on('user_connected')
def test_connect(user):
    emit('user_connect',{'user':user}, broadcast=True)

#server recieves message sent from client and emits timestamp and message to all clients
@socketio.on('send_message')
def handle_message(msg, user):
    today = datetime.now()
    message_timestamp = today.strftime("%m/%d %H:%M")
    emit('send_message',{'user':user, 'msg':msg, 'timestamp': message_timestamp},broadcast=True) #send is used to send messages emit is used for other data types

@socketio.on('user_left')
def leaving_message(user):
    users.discard(user)
    emit('user_disconnect', {'user':user}, broadcast=True)

#handles leaving a room
@socketio.on('redirect_to_home_page')
def returnToHome():
    emit('redirect', {'url': url_for('home_page')})


#stats server
def create_app:
    print("running on http://127.0.0.1:5000/ ")
    print()
    socketio.run(app, debug=True)