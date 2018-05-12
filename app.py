import requests
import flask
import sys,os
from flask import Flask, render_template, request, flash,session,redirect,url_for, jsonify, make_response, g
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES
import base64
from datetime import datetime
import json, urllib2

app = Flask(__name__)
app.secret_key = 'thisissecretkey'
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)
lm = LoginManager()

lm.init_app(app)


def api_login(username, password, response):
    resp_dict = json.loads(response.text)
    url = 'http://localhost:5000/user/info/'+username
    user = requests.get(url)
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
        if response.text == 'username already used':
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
        book_dict = json.loads(books.text)
        action = requests.get('http://localhost:5000/interests/view/Action')
        action_dict = json.loads(action.text)
        drama = requests.get('http://localhost:5000/interests/view/Drama')
        drama_dict = json.loads(drama.text)
        horror = requests.get('http://localhost:5000/interests/view/Horror')
        horror_dict = json.loads(horror.text)
        print(books.text)
        print(drama.text)
        print('HORROR BOOKS')
        print(horror.text)
        if not book_dict['book']:
            return render_template('dashboard.html', books={}, message='No books to display')
        book_dict = json.loads(books.text)
        return render_template('dashboard.html', books=book_dict['book'], horrorbooks=horror_dict['book'],
                               actionbooks=action_dict['book'], dramabooks=drama_dict['book'], user=session['user'])
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
            filename="default_book.jpeg"
            if 'photo' in request.files:
                filename = photos.save(request.files['photo'], session['user']+"/books")
            response = requests.post(
                'http://localhost:5000/user/addbook',
                json={"current_user": session['user'], 'title': request.form['title'], "edition": request.form['edition'],
                      "year": request.form['year'], "isbn": request.form['isbn'], "types": request.form['types'],
                      "publisher_name": request.form['publisher_name'], "author_fname": request.form['author_fname'],
                      "author_lname": request.form['author_lname'], "category": request.form['category'],
                      "description": request.form['description'], "price": request.form['price'],
                      "genre": request.form['genre'], "quantity": request.form['quantity'], "filename": filename}
            )
            resp = json.loads(response.text)
            print(resp['message'])
            if resp['message'] == 'The book is already in your bookshelf! We suggest editing the book if there are changes.':
                return render_template('addbook.html', message=resp['message'], color='danger', x='&times;')
            return redirect('home')
        else:
            return render_template('addbook.html')
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/<book_id>/upload/<num>', methods=['POST', 'GET'])
def add_book_pic(book_id, num):
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'], session['user']+"/books")
        response = requests.post('http://localhost:5000/book/picture',
                                 json={"current_user": session['user'], "filename": filename, "book_id": book_id, "num": num})
        message = json.loads(response.text)
        print[message['message']]
        return redirect(url_for('edit_ownbook', book_id=book_id, username=session['user']))
    return redirect(url_for('edit_ownbook', book_id=book_id, username=session['user']))


### PROFILE ###
@app.route('/profile', methods=['GET'])
def profile():
    if g.user:
        url = 'http://localhost:5000/user/info/'+session['user']
        user = requests.get(url)
        print(user.text)
        user_dict = json.loads(user.text)
        print(user_dict)
        book_details = requests.get('http://localhost:5000/user/bookshelf/availability', json={"current_user": session['user']})
        books = requests.get('http://localhost:5000/user/bookshelf', json={"current_user": session['user']})
        if books.text == "no books found":
            return render_template('no_books_profile.html', user=user_dict['user'])
        book_dict=json.loads(books.text)
        book_details_dict=json.loads(book_details.text)
        print(book_dict['book'])
        print(user_dict['user'])
        return render_template('profile.html', books=book_dict['book'], book_details=book_details_dict, user=user_dict['user'])
    else:
        return redirect('unauthorized')

@app.route('/profile/<username>', methods=['GET', 'POST'])
def view_profile(username):
    if g.user:
        if username == session['user']:
            return redirect('profile')
        url = 'http://localhost:5000/user/info/'+username
        user = requests.get(url)
        print(user.text)
        user_dict = json.loads(user.text)
        print(user_dict)
        book_details = requests.get('http://localhost:5000/user/bookshelf/availability', json={"current_user": username})
        books = requests.get('http://localhost:5000/user/bookshelf', json={"current_user": username})
        if books.text == "no books found":
            return render_template('no_books_profile.html', user=user_dict['user'])
        book_dict=json.loads(books.text)
        book_details_dict=json.loads(book_details.text)
        print(book_dict['book'])
        print(user_dict['user'])
        return render_template('user_profile.html', books=book_dict['book'], book_details=book_details_dict, user=user_dict['user'])
    else:
        return redirect('unauthorized')

@app.route('/profile/edit', methods=['POST', 'GET'])
def edit_profile():
    if g.user:
        url = 'http://localhost:5000/user/info/' + session['user']
        user = requests.get(url)
        user_dict = json.loads(user.text)
        book_details = requests.get('http://localhost:5000/user/bookshelf/availability',
                                    json={"current_user": session['user']})
        books = requests.get('http://localhost:5000/user/bookshelf', json={"current_user": session['user']})
        if books.text == "no books found":
            return render_template('no_books_editprofile.html', user=user_dict['user'])
        book_dict = json.loads(books.text)
        book_details_dict = json.loads(book_details.text)
        if request.method == 'POST':
            print('HELLO')
        else:
            return render_template('edit_profile.html', user=user_dict['user'], books=book_dict['book'])
    else:
        return redirect('unauthorized')

@app.route('/profile/upload', methods=['POST', 'GET'])
def add_profile_pic():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'], session['user'])
        response = requests.post('http://localhost:5000/profile/picture', json={"current_user": session['user'], "filename": filename})
        message = json.loads(response.text)
        print[message['message']]
        return redirect('profile')
    return redirect('profile')



### END PROFILE ###

@app.route('/bookshelf/<username>/<book_id>', methods=['GET'])
def viewbook(book_id, username):
    if g.user:
        book = requests.get('http://localhost:5000/user/bookshelf/'+book_id, json={"current_user": username})
        book_dict = json.loads(book.text)
        print(username)
        print(session['user'])
        if username == session['user']:
            return render_template('own_product.html', books=book_dict['book'])

        print(book_dict['book'])
        return render_template('single_product.html', books=book_dict['book'])
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/<username>/<book_id>/edit', methods=['POST', 'GET'])
def edit_ownbook(book_id, username):
    if g.user:
        book = requests.get('http://localhost:5000/user/bookshelf/' + book_id, json={"current_user": username})
        book_dict = json.loads(book.text)
        if request.method == 'POST':
            print('HELLO')
        else:
            return render_template('edit_ownbook.html', books=book_dict['book'])
    else:
        return redirect('unauthorized')

@app.route('/genre/<genre_name>', methods=['GET'])
def view_genre(genre_name):
    if g.user:
        books = requests.get('http://localhost:5000/interests/view/'+genre_name)
        print(books.text)
        book_dict = json.loads(books.text)
        if not book_dict['book']:
            return render_template('no_books_genre.html', genre_name=genre_name)
        print(book_dict['book'])
        return render_template('genre.html', books=book_dict['book'], genre_name=genre_name)
    else:
        return redirect('unauthorized')

@app.route('/bookstore', methods=['GET'])
def store():
    if g.user:
        books = requests.get('http://localhost:5000/bookshelf/books')
        book_dict = json.loads(books.text)
        if not book_dict['book']:
            return render_template('no_books_shop.html', books={})
        print(book_dict['book'])
        return render_template('shop2.html', books=book_dict['book'])
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/wishlist/<bookshelf_id>/<book_id>', methods=['POST', 'GET'])
def add_wishlist(bookshelf_id, book_id):
    if g.user:
        if request.method == 'POST':
            url = 'http://localhost:5000/bookshelf/wishlist'
            response= requests.post(url, json={"bookshelf_id": bookshelf_id, "username":session['user'], "book_id":book_id})
            book_dict=json.loads(response.text)
            print(response.text)
            url2 = 'http://localhost:5000/bookshelf/wishlist/user'
            books = requests.get(url2, json={"current_user": session['user']})
            book_dict2 = json.loads(books.text)
            if book_dict['message'] == "You can't add your own book to your wishlist":
                if not book_dict2['book']:
                    message = "No books to display"
                    return render_template('wishlist.html', books=book_dict2['book'], message=book_dict['message'],
                                           color='danger', nodisplay=message)
                return render_template('wishlist.html', books=book_dict2['book'], message=book_dict['message'], color='danger')
            elif book_dict['message'] == '"Book is already in wishlist':
                return render_template('wishlist.html', books=book_dict2['book'], message=book_dict['message'], color='danger')
            elif book_dict['message'] == 'Failed to add':
                if not book_dict2['book']:
                    message = "No books to display"
                    return render_template('wishlist.html', books=book_dict2['book'], message=book_dict['message'],
                                           color='danger', nodisplay=message)
                return render_template('wishlist.html', books=book_dict2['book'], message=book_dict['message'], color='danger')
            else:
                return render_template('wishlist.html', books=book_dict2['book'])
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/wishlist/remove/<username>/<book_id>', methods=['GET', 'POST'])
def remove_wishlist(username, book_id):
    if g.user:
        url= 'http://localhost:5000/bookshelf/remove_wishlist'
        response = requests.post(url, json={"book_id": book_id, "bookshelf_owner": username, "username": session['user']})
        book_dict = json.loads(response.text)
        return redirect('wishlist')
    else:
        return redirect('unauthorized')

@app.route('/wishlist', methods=['GET'])
def wishlist():
    if g.user:
        url = 'http://localhost:5000/bookshelf/wishlist/user'
        books = requests.get(url, json={"current_user": session['user']})
        book_dict = json.loads(books.text)
        print(book_dict['book'])
        if not book_dict['book']:
            message="No books to display"
            return render_template('wishlist.html', books={}, nodisplay=message)
        return render_template('wishlist.html', books=book_dict['book'])
    else:
        return redirect('unauthorized')
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)