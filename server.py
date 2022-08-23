from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#Get displays home page which has form for username
#Post submits username entered and displays chat page
@app.route("/", methods=['GET','POST'])
def home_page():
    if request.method == "POST":
        user = request.form['username']
        if request.form['username'] == '':
            return render_template("index.html")
        return  redirect(url_for('enterRoom', username = user))
    else:
        return render_template("index.html")

#Once username is entered user is directed to chatroom.
@app.route("/chatroom/<username>",methods=['GET'])
def enterRoom(username):
    if request.method == 'GET':
        return render_template("chatRoom.html", username1 = username)

#Tests to make sure connection is working
@socketio.on('connect')
def test_connect():
    print('User has connected')

#server recieves message sent from client and emits timestamp and message to all clients
@socketio.on('send_message')
def handle_message(msg, user):
    today = datetime.now()
    message_timestamp = today.strftime("%m/%d %H:%M")
    print()
    print('received message from: ' + user + ' -- message: ' + msg + 'at timestamp: ' + message_timestamp)
    print()
    emit('send_message',{'user':user, 'msg':msg, 'timestamp': message_timestamp},broadcast=True) #send is used to send messages emit is used for other data types
    return redirect(url_for('home_page'))

#handles leaving a room
@socketio.on('redirect_to_home_page')
def returnToHome():
    emit('redirect', {'url': url_for('home_page')})


#stats server
if __name__ == "__main__":
    print("running on http://127.0.0.1:5000/ ")
    print()
    socketio.run(app, debug=True)