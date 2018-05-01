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
                    "contact_number": request.form['contact_number'], "username": username, "password": password, "profpic": "none.jpeg"},
        )
        resp_dict = json.loads(response.text)
        if resp_dict[1]['message'] == 'username already created':
            return render_template('error_signup.html')
        else:
            api_login(username, password, response)

        return redirect('interests')
    else:
        return render_template('signup.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    if g.user:
        url = 'http://localhost:5000/bookshelf/books/latest'
        books = requests.get(url)
        if books.text == "no books found":
            return render_template('dashboard.html', books={})
        book_dict = json.loads(books.text)
        return render_template('dashboard.html', books=book_dict['book'], user=session['user'])
    else:
        return redirect('unauthorized')

@app.route('/unauthorized', methods=['POST', 'GET'])
def unauthorized():
    return render_template('unauthorized.html')

@app.route('/interests', methods=['POST', 'GET'])
def interests():
    if g.user:
        if request.method == 'POST':
            interests = request.form.getlist('interests')
            print(interests)
            if len(interests) == 1:
                interests = request.form.get('interests')
                url = 'http://localhost:5000/interests/'+interests
                requests.post(url, json={"current_user": session['user']})
            else:
                for interest in interests:
                    print(interest)
                    url='http://localhost:5000/interests/'+interest
                    response = requests.post(url, json={"current_user": session['user']})
                    print(response.text)
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
                      "author_lname": request.form['author_lname'], "category": request.form['category'],
                      "description": request.form['description'], "price": request.form['price'],
                      "genre": request.form['genre'],}
            )
            return redirect('home')
        else:
            return render_template('addbook.html')
    else:
        return redirect('unauthorized')

@app.route('/profile', methods=['GET'])
def profile():
    if g.user:
        book_details = requests.get('http://localhost:5000/user/bookshelf/availability', json={"current_user": session['user']})
        books = requests.get('http://localhost:5000/user/bookshelf', json={"current_user": session['user']})
        if books.text == "no books found":
            return render_template('profile.html', books={})
        book_dict=json.loads(books.text)
        book_details_dict=json.loads(book_details.text)
        print(book_dict['book'])
        return render_template('profile.html', books=book_dict['book'], book_details=book_details_dict, user=session['user'])
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/<username>/<book_id>', methods=['GET'])
def viewbook(book_id, username):
    if g.user:
        book = requests.get('http://localhost:5000/user/bookshelf/'+book_id, json={"current_user": username})
        if book.text == "no books found":
            return render_template('profile.html', books={})
        book_dict=json.loads(book.text)
        print(book_dict['book'])
        return render_template('single_product.html', books=book_dict['book'])
    else:
        return redirect('unauthorized')

@app.route('/genre/<genre_name>', methods=['GET'])
def view_genre(genre_name):
    if g.user:
        books = requests.get('http://localhost:5000/interests/view/'+genre_name)
        if books.text == "no books found":
            return render_template('genre.html', books={})
        book_dict = json.loads(books.text)
        print(book_dict['book'])
        return render_template('genre.html', books=book_dict['book'], genre_name=genre_name)
    else:
        return redirect('unauthorized')

@app.route('/bookstore', methods=['GET'])
def store():
    if g.user:
        books = requests.get('http://localhost:5000/bookshelf/books')
        if books.text == "no books found":
            return render_template('shop2.html', books={})
        book_dict = json.loads(books.text)
        print(book_dict['book'])
        return render_template('shop2.html', books=book_dict['book'])
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/wishlist/<bookshelf_id>/<username>/<book_id>', methods=['POST'])
def add_wishlist(bookshelf_id, username, book_id):
    if g.user:
        url = 'http://localhost:5000/bookshelf/wishlist'
        response= requests.post(url, json={"bookshelf_id": bookshelf_id, "username":session['user'], "book_id":book_id})
        book_dict=json.loads(response.text)
        if book_dict['message']== 'failed to add':
            return redirect('store')
        else:
            return redirect(url_for('store'))
    else:
        return redirect('unauthorized')

@app.route('/wishlist', methods=['GET'])
def wishlist():
    if g.user:
        url = 'http://localhost:5000/bookshelf/wishlist/user'
        books = requests.get(url, json={"current_user": session['user']})
        book_dict = json.loads(books.text)
        print(book_dict['book'])
        return render_template('wishlist.html', books=book_dict['book'])
    else:
        return redirect('unauthorized')
if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)