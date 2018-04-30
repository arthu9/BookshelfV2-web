import requests
import flask
import sys,os
from flask import Flask, render_template, request, flash,session,redirect,url_for, jsonify, make_response, g
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import base64
from datetime import datetime
import json, urllib2

app = Flask(__name__)
app.secret_key = 'thisissecretkey'
lm = LoginManager()

lm.init_app(app)


def api_login(username, password, response):
    print(request.headers)
    resp_dict = json.loads(response.text)
    url = 'http://localhost:5000/user/info/'+username
    user = requests.get(url, headers={'refresh-token': resp_dict[0]['token'],'x-access-token': resp_dict[0]['token']})
    print(user)
    print(user.text)
    resp_dict2 = json.loads(user.text)
    print(resp_dict2['user']['username'])
    session['user'] = resp_dict2['user']['username']
    g.user = session['user']
    return resp_dict[0]['token']


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        username = request.form['username']
        password = request.form['password']
        response = requests.post(
            'http://localhost:5000/login',
            auth=(username, password),
        )
        print(response.text)
        if response.text == "Could not verify":
            return render_template('error.html')
        else:
            token = api_login(username, password, response)
        print(token)
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if g.user:
        session.pop('user', None)
        return redirect('/')

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
        print(resp_dict)
        if resp_dict[0]['message'] == 'username already created':
            return render_template('error_signup.html')
        else:
            api_login(username, password)

        return redirect('interests')
    else:
        return render_template('signup.html')

@app.route('/home', methods=['POST', 'GET'])
def home():


    return render_template('dashboard.html', user=session['user'])

@app.route('/unauthorized', methods=['POST', 'GET'])
def unauthorized():
    return render_template('unauthorized.html')

@app.route('/interests', methods=['POST', 'GET'])
def interests():
    if g.user:
        if request.method == 'POST':
            return redirect('home')

        return render_template('interest.html')

    else:
        return redirect('unauthorized')

@app.route('/addbook', methods=['POST', 'GET'])
def addbook():
    if g.user:
        if request.method == 'POST':
            print(request.form['types'])
            requests.post(
                'http://localhost:5000/user/addbook',
                json={"current_user": session['user'], 'title': request.form['title'], "edition": request.form['edition'],
                      "year": request.form['year'], "isbn": request.form['isbn'], "types": request.form['types'],
                      "publisher_name": request.form['publisher_name'], "author_fname": request.form['author_fname'],
                      "author_lname": request.form['author_lname']},
            )
            return render_template('profile.html')
        else:
            return render_template('addbook.html')
    else:
        return redirect('unauthorized')

@app.route('/profile/bookshelf', methods=['GET'])
def profile():
    if g.user:
        book_details = requests.get('http://localhost:5000/user/bookshelf/availability', json={"current_user": session['user']})
        books = requests.get('http://localhost:5000/user/bookshelf', json={"current_user": session['user']})
        book_dict=json.loads(books.text)
        book_details_dict=json.loads(book_details.text)
        print(book_dict)
        print(book_dict['book'][1]['title'])
        print(book_dict['book'])
        return render_template('profile.html', books=book_dict['book'], book_details=book_details_dict)
    else:
        return redirect('unauthorized')

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)