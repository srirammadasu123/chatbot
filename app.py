from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask.typing import ResponseValue
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import hashlib

import os

import pyttsx3

from pydub import AudioSegment
from pydub.playback import play

app = Flask(__name__)


#app.secret_key = os.urandom(24)

@app.route('/')
def initial():
    return render_template('initial.html')

@app.route('/index')
def index():
    return render_template('index.html') #redirect(url_for('initial'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return "Username and password are required."
        register_user( username, password )
        
        return redirect(url_for('success')),redirect(url_for('index'))
    return render_template('register.html')

@app.route('/success')
def success():
    return "Registration successful!"
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if verify_password(username, password):
            return redirect(url_for('dashboarda', username=username))
        else:
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/dashboarda/<username>')
def dashboard(username):
    print(f'Welcome, {username}!')
    return redirect(url_for('login'))

user_data = {
    #'user1': {'hashed_password': '123','salt': '456'},
    # Add more user data here
}
def verify_password(username, password):
    if username in user_data:
        stored_hashed_password = user_data[username]['hashed_password']
        stored_salt = user_data[username]['salt']
        input_hashed_password = hashlib.sha256((password + stored_salt).encode()).hexdigest()
        return input_hashed_password == stored_hashed_password
    return False
def register_user(username, password):
    salt = "somerandomsalt"  # You should generate a unique salt for each user
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    user_data[username] = {'hashed_password': hashed_password, 'salt': salt}

if __name__ == '__main__':
    app.run(debug=True)
