from time import localtime, strftime
from flask import Flask, redirect, render_template, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from models import *
from wtform_fields import *
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.secret_key = 'blabla'


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://sncxlhsjnkdxok:654b2e167c35c8564a055b8ba92c2122e1c2e5ea07061f99c9698c95b8db460a@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/dsc3vl3jpp8vo'
db = SQLAlchemy(app)

socketio = SocketIO(app)
ROOMS = []

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):

    return User.query.get(int(id))

@app.route("/", methods=['GET','POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pass = pbkdf2_sha256.hash(password)
              
        user = User(username=username, password=hashed_pass)
        db.session.add(user)
        db.session.commit()

        flash('Registered succesfully, please login', 'success')

        return redirect(url_for('login'))
        
    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET','POST'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('game'))

    return render_template("login.html", form=login_form)

@app.route("/game", methods=['GET','POST'])
def game():

    # if not current_user.is_authenticated:
    #     flash('Please login', 'danger')
    #     return redirect(url_for('login'))

    return render_template('game.html', username=current_user.username, rooms=ROOMS)

@app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@socketio.on('create-room')
def create_room(data):
    if (data["new_room_name"] in ROOMS): 
        flash('The room already exists', 'danger')
        return redirect(url_for('game'))
    else:   
        print(f"{data}")
        room_name = data["new_room_name"]
        print(room_name)
        ROOMS.append(room_name)   
        emit('new-room-received', data, broadcast=True)
    


@socketio.on('incoming-message')
def message(data):

    username = data["username"]
    msg = data["msg"]
    room = data["room"]

    print(f"\n\n{data}\n\n")
    emit('incoming-message', {'msg': msg, 'username': username, 'time_stamp': strftime('%b-%d %I:%Mp', localtime())}, room=room)


@socketio.on('join')
def join(data):

    username = data["username"]
    room = data["room"]

    join_room(room)
    emit('incoming-message',{'msg': username + " has joined the " + room}, room=room)
   

@socketio.on('leave')
def leave(data):

    username = data["username"]
    room = data["room"]
    
    leave_room(room)
    emit('incoming-message',{'msg': username + " has left the " + room}, room=room)



if __name__ == "__main__":
    socketio.run(app, debug=True)