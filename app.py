import requests
import flask
import sys,os
from flask import Flask, render_template, request, flash,session,redirect,url_for, jsonify, make_response
import base64
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(
            'http://localhost:5000/login',
            json={"username": username, "password": password, },
            auth=(username, password),
        )
        print(response.text)
        if response.text == "Could not verify":
            return render_template('error.html')

        return render_template('dashboard.html')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(
            'http://localhost:5000/signup',
            json={"first_name": request.form['first_name'], "last_name": request.form['last_name'],
                     "birth_date": request.form['birth_date'], "gender": request.form['gender'],
                    "contact_number": request.form['contact_number'], "username": username, "password": password, "profpic": "default.jpg"},
        )
        resp_dict = json.loads(response.text)
        if resp_dict['message'] == 'username already created':
            return render_template('error_signup.html')
        else:
            response2 = requests.post(
                'http://localhost:5000/login',
                json={"username": username, "password": password, },
                auth=(username, password),
            )
            resp_dict = json.loads(response2.text)
            print(resp_dict['token'])

        return redirect('interests')
    else:
        return render_template('signup.html')


@app.route('/interests', methods=['POST', 'GET'])
def interests():
    if request.method == 'POST':
        return render_template('dashboard.html')
    else:
        return render_template('interest.html')

@app.route('/addbook', methods=['POST', 'GET'])
def addbook():
    if request.method == 'POST':
        requests.post(
            'http://localhost:5000/addbook',
            json={"title": request.form['title'], "edition": request.form['edition'],
                  "year": request.form['year'], "isbn": request.form['isbn'],
                  "publisher_name": request.form['publisher_name'], "author_fname": request.form['author_fname'],
                  "author_lname": request.form['author_lname']},
        )
        return render_template('profile.html')
    else:
        return render_template('addbook.html')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)