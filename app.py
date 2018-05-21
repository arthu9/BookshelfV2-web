import requests
import flask
import sys,os
from flask import Flask, render_template, request, flash,session,redirect,url_for, jsonify, make_response, g
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_googlemaps import GoogleMaps, Map, icons
import base64
from base64 import b64encode, b64decode
from datetime import date, datetime
import openlibrary_api
import json, urllib2, io


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
lm = LoginManager()
app = Flask(__name__, template_folder="templates")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAOeYMvF7kPJ7ZcAjOVWiRA8PjCk5E_TsM"
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)
GoogleMaps(app)
app.secret_key = 'supersecretkey'
lm.init_app(app)


def api_login(username, password, response):
    resp_dict = json.loads(response.text)
    url = 'http://localhost:5050/user/info/'+username
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
            'http://localhost:5050/login',
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

@app.route('/getcoordinates', methods=['POST'])
def get_coordinates():
    data = request.get_json()
    requests.post('http://localhost:5050/user/set/coordinates', json={"current_user": session['user'],
                                                                  "latitude": data['latitude'], "longitude": data['longitude']})
    return make_response('Success')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if g.user:
        session.pop('user', None)
        return redirect('/')

@app.route('/signup/1', methods=['POST', 'GET'])
def check_username():
    if request.method == 'POST':
        username =request.form['username']
        response = requests.get(
            'http://localhost:5050/user/info/'+username)
        print(response.text)
        if response.text == 'no user found!':
            return render_template('signup_1.html', username=username, password=request.form['password'])
        else:
            return render_template('error_signup.html', message="Username already taken.",
                                   message2="Please use a different one.")
    else:
        return render_template('signup_1.html')

def calculate_age(born2):
    today = date.today()
    born = datetime.strptime(born2, "%Y-%m-%d")
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def get_bday(born2):
    fmt = "%a, %d %b %Y %H:%M:%S GMT"
    born = datetime.strptime(born2, fmt).strftime('%B, %d %Y')
    return born

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        print('signup')
        username = request.form['username']
        password = request.form['password']
        age = calculate_age(request.form['birth_date'])
        if age <= 18:
            return render_template('error_signup.html', message='Age Requirement:',
                                   message2='You must be 18 or above.')
        address = request.form['address']
        google_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key=AIzaSyAOeYMvF7kPJ7ZcAjOVWiRA8PjCk5E_TsM')
        google_dict = json.loads(google_response.text)
        latitude=google_dict['results'][0]['geometry']['location']['lat']
        longitude=google_dict['results'][0]['geometry']['location']['lng']
        response = requests.post(
            'http://localhost:5050/signup',
            json={"first_name": request.form['first_name'], "last_name": request.form['last_name'],
                     "birth_date": request.form['birth_date'], "gender": request.form['gender'],
                    "contact_number": request.form['contact_number'], "latitude": latitude, "longitude": longitude,
                    "username": username, "password": password},
        )
        resp_dict = json.loads(response.text)
        api_login(username, password, response)

        return redirect('interests')
    else:
        return render_template('signup.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    if g.user:
        url = 'http://localhost:5050/bookshelf/books/latest'
        books = requests.get(url)
        book_dict = json.loads(books.text)
        action = requests.get('http://localhost:5050/interests/view/Action')
        action_dict = json.loads(action.text)
        drama = requests.get('http://localhost:5050/interests/view/Drama')
        drama_dict = json.loads(drama.text)
        horror = requests.get('http://localhost:5050/interests/view/Horror')
        horror_dict = json.loads(horror.text)
        book_dict = json.loads(books.text)
        if not book_dict['book']:
            return render_template('dashboard.html', books={}, none='display', message='No books to display',
                                   message1='No books to display', message2='No books to display', message3='No books to display')
        elif not action_dict['book'] and (not horror_dict['book'] and not drama_dict['book']):
            return render_template('dashboard.html', books=book_dict['book'], none='none',
                                   message1='No books to display', message2='No books to display',
                                   message3='No books to display')
        elif not action_dict['book'] and not drama_dict['book']:
            return render_template('dashboard.html', books=book_dict['book'], none='none',
                                   message1='No books to display', message2='No books to display')
        elif not action_dict['book'] and not horror_dict['book']:
            return render_template('dashboard.html', books=book_dict['book'], none='none',
                                   message1='No books to display', message3='No books to display')
        elif not drama_dict['book'] and not horror_dict['book']:
            return render_template('dashboard.html', books=book_dict['book'], none='none',
                                   message2='No books to display', message3='No books to display')
        elif not action_dict['book']:
            return render_template('dashboard.html', books=book_dict['book'], none='none',
                                   message1='No books to display')
        elif not drama_dict['book']:
            return render_template('dashboard.html', books=book_dict['book'], none='none',
                                   message2='No books to display')
        elif not horror_dict['book']:
            return render_template('dashboard.html', books=book_dict['book'], none='none', message3='No books to display')
        return render_template('dashboard.html', books=book_dict['book'], none='none', horrorbooks=horror_dict['book'],
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
                url = 'http://localhost:5050/interests/'+interests
                requests.post(url, json={"current_user": session['user']})
            else:
                for interest in interests:
                    url='http://localhost:5050/interests/'+interest
                    response = requests.post(url, json={"current_user": session['user']})

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
                'http://localhost:5050/user/addbook',
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
            return render_template('addbook_isbn.html')
    else:
        return redirect('unauthorized')

@app.route('/isbn/search', methods=['POST', 'GET'])
def isbn_search():
    if g.user:
        if request.method == 'POST':
            isbn = request.form['isbn']
            response4 = requests.post('http://localhost:5050/book/isbn', json={"isbn": isbn})
            url3 = "https://openlibrary.org/api/books?bibkeys=ISBN:{0}&jscmd=details&format=json".format(isbn)
            url = "https://openlibrary.org/api/books?bibkeys=ISBN:{0}&jscmd=data&format=json".format(isbn)
            url2 = "https://www.googleapis.com/books/v1/volumes?q=isbn:{0}&key=AIzaSyAOeYMvF7kPJ7ZcAjOVWiRA8PjCk5E_TsM".format(isbn)
            output = []
            book = {}
            response2 = requests.get(url2)
            resp2 = json.loads(response2.text)

            print(resp2['totalItems'])
            if response4.text == 'Book not found':
                response = requests.get(url)
                resp = json.loads(response.text)
                print(resp)
                book['isbn'] = isbn
                if (resp2['totalItems'] == 0) and (not resp):
                    print('ERROR')
                elif not resp:
                    print(response2.text)
                    book['title'] = resp2['items'][0]['volumeInfo']['title']
                    book['publishers'] = resp2['items'][0]['volumeInfo']['publisher']
                    book['book_cover'] = resp2['items'][0]['volumeInfo']['imageLinks']['thumbnail']
                    book['author_name'] = resp2['items'][0]['volumeInfo']['authors'][0]
                    book['description'] = resp2['items'][0]['volumeInfo']['description']
                    book['year'] = resp2['items'][0]['volumeInfo']['publishedDate']
                else:
                    index = "ISBN:{0}".format(isbn)
                    book['title'] = resp[index]['title']
                    book['publishers'] = resp[index]['publishers'][0]['name']
                    book['book_cover'] = resp[index]['cover']['large']
                    book['author_name'] = resp[index]['authors'][0]['name']
                    date1 = resp[index]['publish_date']
                    book['year'] = date1
                    if resp2['totalItems'] != 0:
                        book['title'] = resp2['items'][0]['volumeInfo']['title']
                        book['publishers'] = resp2['items'][0]['volumeInfo']['publisher']
                        book['author_name'] = resp2['items'][0]['volumeInfo']['authors'][0]
                        book['description'] = resp2['items'][0]['volumeInfo']['description']
                        book['year'] = resp2['items'][0]['volumeInfo']['publishedDate']
                output.append(book)
                print(output)
            return render_template('addbook_result.html', book=output[0])
        else:
            return render_template('addbook_result.html', book={})
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/<book_id>/upload/<num>', methods=['POST', 'GET'])
def add_book_pic(book_id, num):
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'], session['user']+"/books")
        response = requests.post('http://localhost:5050/book/picture',
                                 json={"current_user": session['user'], "filename": filename, "book_id": book_id, "num": num})
        message = json.loads(response.text)
        print[message['message']]
        return redirect(url_for('edit_ownbook', book_id=book_id, username=session['user']))
    return redirect(url_for('edit_ownbook', book_id=book_id, username=session['user']))


### PROFILE ###
@app.route('/profile', methods=['GET'])
def profile():
    if g.user:
        url = 'http://localhost:5050/user/info/'+session['user']
        user = requests.get(url)
        print(user.text)
        user_dict = json.loads(user.text)
        bday = get_bday(user_dict['user']['birth_date'])
        map = profilemap(session['user'])
        profilepic = user_dict['user']['profpic']
        book_details = requests.get('http://localhost:5050/user/bookshelf/availability', json={"current_user": session['user']})
        books = requests.get('http://localhost:5050/user/bookshelf', json={"current_user": session['user']})
        if books.text == "no books found":
            return render_template('no_books_profile.html', user=user_dict['user'], bday=bday, map=map,  profilepic=profilepic)
        book_dict=json.loads(books.text)
        book_details_dict=json.loads(book_details.text)
        return render_template('profile.html', books=book_dict['book'], book_details=book_details_dict, user=user_dict['user'], profilepic=profilepic, bday=bday, map=map)
    else:
        return redirect('unauthorized')

def profilemap(username):
    user_details = requests.get('http://localhost:5050/user/coordinates',
                                json={"current_user": username})
    users_details = requests.get('http://localhost:5050/users/coordinates',
                                json={"current_user": username})
    user = json.loads(user_details.text)
    users = json.loads(users_details.text)
    users1 =users['users']
    output = []
    user_1 = {}
    user_1['icon'] = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
    profpic = user['user'][0]['profpic']
    user_1['lat'] = user['user'][0]['latitude']
    user_1['lng'] = user['user'][0]['longitude']
    user_1['infobox'] = """<h6 style="text-align:center;">{0}</h6><img src='data:image;base64, {1}' onerror="this.src='{{url_for('static', 
    filename='images/none.jpeg')}}'" alt="{2}" style="width:80px; height:80px;" alt=" " />""".format(user['user'][0]['username'], profpic, user['user'][0]['username'])
    output.append(user_1)

    for user1 in users1:
        user_data = {}
        profpic2 = user1['other_profpic']
        user_data['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        user_data['lat'] = user1['other_user_lat']
        user_data['lng'] = user1['other_user_lng']
        user_data['infobox'] = """<h6 style="text-align:center;">{0}</h6><img src='data:image;base64, {1}' onerror="this.src='{{url_for('static', 
        filename='images/none.jpeg')}}'" alt="{2}" style="width:80px; height:80px;" alt=" " />""".format(user1['other_username'],profpic2, user1['other_username'])
        output.append(user_data)

    print(output)
    user_lat=user['user'][0]['latitude']
    user_lng = user['user'][0]['longitude']
    profile_map = Map(
        identifier="Booksnearyou",
        lat=user_lat,
        lng=user_lng,
        style="width: 100%; height:500px;",
        circles=[{
            'stroke_color': '#528BE2',
            'stroke_opacity': 1.0,
            'stroke_weight': 7,
            'fill_color': '#528BE2',
            'fill_opacity': 0.2,
            'center': {
                'lat': user_lat,
                'lng': user_lng
            },
            'radius': 1500 * 50,
        }],
        markers=output
    )
    return profile_map

def profilemap_user(username):
    user_details = requests.get('http://localhost:5050/user/coordinates',
                                json={"current_user": username})
    users_details = requests.get('http://localhost:5050/users/coordinates',
                                json={"current_user": username})
    your_details = requests.get('http://localhost:5050/user/coordinates',
                                json={"current_user": session['user']})
    user = json.loads(user_details.text)
    users = json.loads(users_details.text)
    you = json.loads(user_details.text)
    users1 =users['users']
    output = []
    you2 = {}
    you2['icon'] = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
    profpic = you['user'][0]['profpic']
    you2['lat'] = you['user'][0]['latitude']
    you2['lng'] = you['user'][0]['longitude']
    you2['infobox'] = """<h6 style="text-align:center;">Your Location</h6><img src='data:image;base64, {0}' onerror="this.src='{{url_for('static', 
        filename='images/none.jpeg')}}'" alt="{1}" style="width:80px; height:80px;" alt=" " />""".format(profpic, you['user'][0]['username'])
    output.append(you2)
    user_1 = {}
    user_1['icon'] = 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
    profpic = user['user'][0]['profpic']
    user_1['lat'] = user['user'][0]['latitude']
    user_1['lng'] = user['user'][0]['longitude']
    user_1['infobox'] = """<h6 style="text-align:center;">{0}'s Location</h6><img src='data:image;base64, {1}' onerror="this.src='{{url_for('static', 
    filename='images/none.jpeg')}}'" alt="{2}" style="width:80px; height:80px;" alt=" " />""".format(user['user'][0]['username'], profpic, user['user'][0]['username'])
    output.append(user_1)

    for user1 in users1:
        user_data = {}
        profpic2 = user1['other_profpic']
        user_data['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        user_data['lat'] = user1['other_user_lat']
        user_data['lng'] = user1['other_user_lng']
        user_data['infobox'] = """<h6 style="text-align:center;">{0}</h6><img src='data:image;base64, {1}' onerror="this.src='{{url_for('static', 
        filename='images/none.jpeg')}}'" alt="{2}" style="width:80px; height:80px;" alt=" " />""".format(user1['other_username'],profpic2, user1['other_username'])
        output.append(user_data)

    print(output)
    user_lat=user['user'][0]['latitude']
    user_lng = user['user'][0]['longitude']
    profile_map = Map(
        identifier="Booksnearyou",
        lat=user_lat,
        lng=user_lng,
        style="width: 100%; height:500px;",
        circles=[{
            'stroke_color': '#528BE2',
            'stroke_opacity': 1.0,
            'stroke_weight': 7,
            'fill_color': '#528BE2',
            'fill_opacity': 0.2,
            'center': {
                'lat': user_lat,
                'lng': user_lng
            },
            'radius': 1500 * 50,
        }],
        markers=output
    )
    return profile_map


@app.route('/profile/<username>', methods=['GET', 'POST'])
def view_profile(username):
    if g.user:
        if username == session['user']:
            return redirect('profile')
        url = 'http://localhost:5050/user/info/'+username
        user = requests.get(url)
        user_dict = json.loads(user.text)
        bday = get_bday(user_dict['user']['birth_date'])
        profilepic = user_dict['user']['profpic']
        map = profilemap_user(username)
        book_details = requests.get('http://localhost:5050/user/bookshelf/availability', json={"current_user": username})
        books = requests.get('http://localhost:5050/user/bookshelf', json={"current_user": username})
        if books.text == "no books found":
            return render_template('no_books_profile.html', user=user_dict['user'], bday=bday, map=map, profilepic=profilepic)
        book_dict=json.loads(books.text)
        book_details_dict=json.loads(book_details.text)
        print(book_dict['book'])
        print(user_dict['user'])
        return render_template('user_profile.html', books=book_dict['book'], book_details=book_details_dict, user=user_dict['user'], bday=bday, map=map, profilepic=profilepic)
    else:
        return redirect('unauthorized')

@app.route('/image/<username>/profpic')
def user_profpicture(username):
    url = 'http://localhost:5050/user/info/' + username
    user = requests.get(url)
    user_dict = json.loads(user.text)
    profilepic = user_dict['user']['profpic']
    return app.response_class(profilepic, mimetype='application/octet-stream')

@app.route('/profile/edit', methods=['POST', 'GET'])
def edit_profile():
    if g.user:
        url = 'http://localhost:5050/user/info/' + session['user']
        user = requests.get(url)
        user_dict = json.loads(user.text)
        map = profilemap(session['user'])
        profilepic = (user_dict['user']['profpic'])
        bday = get_bday(user_dict['user']['birth_date'])
        book_details = requests.get('http://localhost:5050/user/bookshelf/availability',
                                    json={"current_user": session['user']})
        books = requests.get('http://localhost:5050/user/bookshelf', json={"current_user": session['user']})
        if books.text == "no books found":
            return render_template('no_books_editprofile.html', user=user_dict['user'], bday=bday,map=map, profilepic=profilepic)
        book_dict = json.loads(books.text)
        book_details_dict = json.loads(book_details.text)
        if request.method == 'POST':
            print('HELLO')
        else:
            return render_template('edit_profile.html', user=user_dict['user'], books=book_dict['book'], bday=bday, map=map, profilepic=profilepic)
    else:
        return redirect('unauthorized')

@app.route('/profile/upload', methods=['POST', 'GET'])
def add_profile_pic():
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        response = requests.post('http://localhost:5050/profile/picture', json={"current_user": session['user'], "filename": b64encode(file.read())})
        message = json.loads(response.text)
        return redirect('profile')
    return redirect('profile')



### END PROFILE ###

@app.route('/bookshelf/<username>/<book_id>', methods=['GET'])
def viewbook(book_id, username):
    if g.user:
        book = requests.get('http://localhost:5050/user/bookshelf/'+book_id, json={"current_user": username})
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
        book = requests.get('http://localhost:5050/user/bookshelf/' + book_id, json={"current_user": username})
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
        books = requests.get('http://localhost:5050/interests/view/'+genre_name)
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
        books = requests.get('http://localhost:5050/bookshelf/books')
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
            url = 'http://localhost:5050/bookshelf/wishlist'
            response= requests.post(url, json={"bookshelf_id": bookshelf_id, "username":session['user'], "book_id":book_id})
            book_dict=json.loads(response.text)
            print(response.text)
            url2 = 'http://localhost:5050/bookshelf/wishlist/user'
            books = requests.get(url2, json={"current_user": session['user']})
            book_dict2 = json.loads(books.text)
            if book_dict['message'] == "You can't add your own book to your wishlist":
                if not book_dict2['book']:
                    return render_template('no_books_wishlist.html', message=book_dict['message'], none='block')
                return render_template('wishlist.html', books=book_dict2['book'], message=book_dict['message'],display='block')
            elif book_dict['message'] == 'Book is already in wishlist':
                return render_template('wishlist.html', books=book_dict2['book'], message=book_dict['message'], display='block')
            elif book_dict['message'] == 'Failed to add':
                if not book_dict2['book']:
                    return render_template('no_books_wishlist.html', message=book_dict['message'],display='block')
                return render_template('wishlist.html', books=book_dict2['book'], message=book_dict['message'],display='block')
            else:
                return render_template('wishlist.html', books=book_dict2['book'], display='none')
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/wishlist/remove/<username>/<book_id>', methods=['GET', 'POST'])
def remove_wishlist(username, book_id):
    if g.user:
        url= 'http://localhost:5050/bookshelf/remove_wishlist'
        response = requests.post(url, json={"book_id": book_id, "bookshelf_owner": username, "username": session['user']})
        book_dict = json.loads(response.text)
        return redirect('wishlist')
    else:
        return redirect('unauthorized')

@app.route('/wishlist', methods=['GET'])
def wishlist():
    if g.user:
        url = 'http://localhost:5050/bookshelf/wishlist/user'
        books = requests.get(url, json={"current_user": session['user']})
        book_dict = json.loads(books.text)
        print(book_dict['book'])
        if not book_dict['book']:
            return render_template('no_books_wishlist.html', display='none')
        return render_template('wishlist.html', books=book_dict['book'], display='none')
    else:
        return redirect('unauthorized')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
            r = requests.get('http://localhost:5050/search', json={'item': request.form['info'], 'current_user': session['user']})
            print(r.text)
            book_dict = json.loads(r.text)
            return render_template("result.html", books=book_dict['book'])
    else:
        return "error"


@app.route('/viewresult', methods=['GET'])
def viewresult():
    if g.user:
        book = requests.get('http://localhost:5050/user/bookshelf/', json={'current_user': session['user']})
        if book.text == "no books found":
            return render_template('profile.html', books={})
        book_dict=json.loads(book.text)
        print(book_dict['book'])
        return render_template('single_product.html', books=book_dict['book'])
    else:
        return redirect('unauthorized')

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)