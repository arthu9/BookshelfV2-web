import requests
import flask
import sys,os
from flask import Flask, render_template, request, flash,session,redirect,url_for, jsonify, make_response, g
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_googlemaps import GoogleMaps, Map, icons
import base64, django
from werkzeug.contrib.cache import SimpleCache
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
cache = SimpleCache()

def api_login(username, password, response):
    resp_dict = json.loads(response.text)
    url = 'http://localhost:5050/user/info/'+username
    user = requests.get(url)
    print(resp_dict)
    resp_dict2 = json.loads(user.text)
    session['user'] = resp_dict2['user']['username']
    session['token'] = resp_dict['token']
    g.user = session['user']
    g.token = session['token']
    return resp_dict['token']


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.before_request
def before_request():
    g.user = None
    g.token = None
    if 'user' in session and 'token' in session:
        g.user = session['user']
        g.token = session['token']

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
        print(session['token'])
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
        session.pop('token', None)
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
        url2 = 'http://localhost:5050/bookshelf/books/recent'
        url3 = 'http://localhost:5050/bookshelf/books/toprated'
        books = requests.get(url, headers={'x-access-token': session['token']})
        books2 = requests.get(url2, headers={'x-access-token': session['token']})
        books3 = requests.get(url3, headers={'x-access-token': session['token']})
        action = requests.get('http://localhost:5050/interests/view2/Action', headers={'x-access-token': session['token']})
        action_dict = json.loads(action.text)
        drama = requests.get('http://localhost:5050/interests/view2/Drama', headers={'x-access-token': session['token']})
        drama_dict = json.loads(drama.text)
        horror = requests.get('http://localhost:5050/interests/view2/Horror', headers={'x-access-token': session['token']})
        fiction = requests.get('http://localhost:5050/category/view/Fiction', headers={'x-access-token': session['token']})
        nonfiction = requests.get('http://localhost:5050/category/view/Non-Fiction', headers={'x-access-token': session['token']})
        acads = requests.get('http://localhost:5050/category/view/Educational', headers={'x-access-token': session['token']})
        horror_dict = json.loads(horror.text)
        book_dict = json.loads(books.text)
        book2_dict = json.loads(books2.text)
        book3_dict = json.loads(books3.text)
        fict_dict = json.loads(fiction.text)
        nonfict_dict = json.loads(nonfiction.text)
        acad_dict = json.loads(acads.text)
        return render_template('dashboard.html', books2=book2_dict['book'], books=book_dict['book'],\
                               horrorbooks=horror_dict['book'], actionbooks=action_dict['book'], \
                               dramabooks=drama_dict['book'], user=session['user'], acadbooks=acad_dict['book'], \
                               fictionbooks=fict_dict['book'], books3=book3_dict['book'], nonficbooks=nonfict_dict['book'])
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
            fiction = {'Action', 'Adventure', 'Drama', 'Horror', 'Mystery', 'Mythology'}
            non_fiction = {'Biography', 'Essay', 'Journalism', 'Personal Narrative', 'Reference Book', 'Speech'}
            educational = {'English', 'Math', 'History', 'Science'}
            genre = request.form['genre']
            if genre in fiction:
                category = "Fiction"
            elif genre in non_fiction:
                category = "Non-Fiction"
            else:
                category = "Educational"

            print(category)
            response = requests.post(
                'http://localhost:5050/user/addbook', headers={'x-access-token': session['token']},
                json={"current_user": session['user'], 'title': request.form['title'],
                      "year": request.form['year'], "isbn": request.form['isbn'],
                      "publisher_name": request.form['publisher'], "author_name": request.form['author'],
                        "category": category, "book_cover": request.form['book_cover'],
                      "description": request.form['description'], "price": request.form['price'],
                      "genre": genre, "quantity": request.form['quantity'], "method": request.form.get('methods')}
            )
            print(response.text)
            if response.text == 'The book is already in your bookshelf!':
                return render_template('addbook_isbn.html', display='block')
            return redirect('home')
        else:
            return render_template('addbook_isbn.html', display='none')
    else:
        return redirect('unauthorized')



@app.route('/add_unpublishedbook', methods=['POST', 'GET'])
def add_unpublishedbook():
    if g.user:
        if request.method == 'POST':
            print(request.form['types'])
            filename="default_book.jpeg"
            if 'photo' in request.files:
                filename = photos.save(request.files['photo'], session['user']+"/books")
            response = requests.post(
                'http://localhost:5050/user/addbook', headers={'x-access-token': session['token']},
                json={"current_user": session['user'], 'title': request.form['title'], "edition": request.form['edition'],
                      "year": request.form['year'], "isbn": request.form['isbn'], "types": request.form['types'],
                      "publisher_name": request.form['publisher_name'], "author_fname": request.form['author_fname'],
                      "author_lname": request.form['author_lname'], "category": request.form['category'],
                      "description": request.form['description'], "price": request.form['price'],
                      "genre": request.form['genre'], "quantity": request.form['quantity'], "filename": filename},
            )
            resp = json.loads(response.text)
            print(resp['message'])
            if resp['message'] == 'The book is already in your bookshelf! We suggest editing the book if there are changes.':
                return render_template('addbook.html', message=resp['message'], color='danger', x='&times;')
            return redirect('home')
        else:
            return render_template('addbook_isbn.html', display='none')
    else:
        return redirect('unauthorized')

@app.route('/addbook/step-1', methods=['POST', 'GET'])
def addbook_step1():
    if g.user:
        if request.method == 'POST':
            book = {}
            book['title'] = request.form['title']
            book['description'] = request.form['description']
            book['book_cover'] = request.form['book_cover']
            book['author_name'] = request.form['author_name']
            book['publisher'] = request.form['publisher']
            book['year'] = request.form['year']
            book['isbn'] = request.form['isbn']
            print(book)

            return render_template('addbook_step1.html', book=book)
        else:
            book = {}
            book['title'] = request.form['title']
            book['description'] = request.form['description']
            book['book_cover'] = request.form['book_cover']
            book['author_name'] = request.form['author_name']
            book['publisher'] = request.form['publisher']
            book['year'] = request.form['year']
            book['isbn'] = request.form['isbn']
            print(book)

            return render_template('addbook_step1.html', book=book)
    else:
        return redirect('unauthorized')


@app.route('/title/search/<search>', methods=['GET'])
def title_search(search):
    if g.user:
        output = []
        url = "https://www.googleapis.com/books/v1/volumes?q=intitle:{0}&key=AIzaSyAOeYMvF7kPJ7ZcAjOVWiRA8PjCk5E_TsM&maxResults=40".format(search)
        print(url)
        response = requests.get(url)
        resp = json.loads(response.text)
        print(response.text)
        response2 = requests.post('http://localhost:5050/book/title', json={"title": search}, headers={'x-access-token': session['token']})
        print(response2.text)
        print(resp['totalItems'])
        if int(resp['totalItems']) == 0 and response2.text == 'Book not found':
            return render_template('addbook_noresult.html')
        elif int(resp['totalItems']) == 0:
            resp2 = json.loads(response2.text)
            return render_template('addbook_results.html', books={}, dbbooks=resp2['books'])
        else:
            for book_item in resp['items']:
                books = {}
                if((('publisher' in book_item['volumeInfo']) and ('industryIdentifiers' in book_item['volumeInfo']))
                  and (('imageLinks' in book_item['volumeInfo']) and ('authors' in book_item['volumeInfo'])))\
                    and ('description' in book_item['volumeInfo'] and 'publishedDate' in book_item['volumeInfo']):
                    books['title'] = book_item['volumeInfo']['title']
                    books['publishers'] = book_item['volumeInfo']['publisher']
                    books['isbn'] = book_item['volumeInfo']['industryIdentifiers'][0]['identifier']
                    books['book_cover'] = book_item['volumeInfo']['imageLinks']['thumbnail']
                    books['author_name'] = book_item['volumeInfo']['authors'][0]
                    books['description'] = book_item['volumeInfo']['description']
                    books['year'] = book_item['volumeInfo']['publishedDate']
                    output.append(books)
                else:
                    continue
            if response2.text != 'Book not found':
                resp2 = json.loads(response2.text)
                return render_template('addbook_results.html', books=output, dbbooks=resp2['books'])
            return render_template('addbook_results.html', books=output)
    else:
        return redirect('unauthorized')

@app.route('/author/search/<search>', methods=['GET'])
def author_search(search):
    if g.user:
        output = []
        url = "https://www.googleapis.com/books/v1/volumes?q=inauthor:{0}&key=AIzaSyAOeYMvF7kPJ7ZcAjOVWiRA8PjCk5E_TsM&maxResults=40".format(search)
        response = requests.get(url)
        resp = json.loads(response.text)
        print(response.text)
        response2 = requests.post('http://localhost:5050/book/author', json={"author_name": search}, headers={'x-access-token': session['token']})
        print(response2.text)
        if int(resp['totalItems']) == 0 and response2.text == 'Author not found!':
            return render_template('addbook_noresult.html')
        elif int(resp['totalItems']) == 0:
            resp2 = json.loads(response2.text)
            return render_template('addbook_results.html', books={}, dbbooks=resp2['books'])
        for book_item in resp['items']:
            books = {}
            if ((('publisher' in book_item['volumeInfo']) and ('industryIdentifiers' in book_item['volumeInfo']))
                and (('imageLinks' in book_item['volumeInfo']) and ('authors' in book_item['volumeInfo'])))\
                    and ('description' in book_item['volumeInfo'] and 'publishedDate' in book_item['volumeInfo']):
                books['title'] = book_item['volumeInfo']['title']
                books['publishers'] = book_item['volumeInfo']['publisher']
                books['isbn'] = book_item['volumeInfo']['industryIdentifiers'][0]['identifier']
                books['book_cover'] = book_item['volumeInfo']['imageLinks']['thumbnail']
                books['author_name'] = book_item['volumeInfo']['authors'][0]
                books['description'] = book_item['volumeInfo']['description']
                books['year'] = book_item['volumeInfo']['publishedDate']
                output.append(books)
            else:
                continue
        if response2.text != 'Author not found!':
            resp2 = json.loads(response2.text)
            return render_template('addbook_results.html', books=output, dbbooks=resp2['books'])
        else:
            return render_template('addbook_results.html', books=output)
    else:
        return redirect('unauthorized')

@app.route('/isbn/search', methods=['POST', 'GET'])
def isbn_search():
    if g.user:
        if request.method == 'POST':
            filter = request.form['searchfilter']
            search = request.form['search']
            print(filter)
            if filter == 'Title':
                return redirect(url_for('title_search', search=search))
            elif filter == 'Author':
                return redirect(url_for('author_search', search=search))
            else:
                isbn = request.form['search']
                response4 = requests.post('http://localhost:5050/book/isbn', json={"isbn": isbn}, headers={'x-access-token': session['token']})
                url3 = "https://openlibrary.org/api/books?bibkeys=ISBN:{0}&jscmd=details&format=json".format(isbn)
                url = "https://openlibrary.org/api/books?bibkeys=ISBN:{0}&jscmd=data&format=json".format(isbn)
                url2 = "https://www.googleapis.com/books/v1/volumes?q=isbn:{0}&key=AIzaSyAOeYMvF7kPJ7ZcAjOVWiRA8PjCk5E_TsM".format(isbn)
                output = []
                book = {}
                response2 = requests.get(url2)
                resp2 = json.loads(response2.text)
                print(resp2['totalItems'])
                print(response4.text)
                if response4.text == 'Book not found':
                    response = requests.get(url)
                    resp = json.loads(response.text)
                    print(resp)
                    book['isbn'] = isbn
                    if (resp2['totalItems'] == 0) and (not resp):
                        return render_template('addbook_noresult.html')
                    elif not resp:
                        print(response2.text)
                        book['title'] = resp2['items'][0]['volumeInfo']['title']
                        if 'publisher' in resp2['items'][0]['volumeInfo']:
                            book['publishers'] = resp2['items'][0]['volumeInfo']['publisher']
                        else:
                            book['publishers'] = ''
                        book['book_cover'] = resp2['items'][0]['volumeInfo']['imageLinks']['thumbnail']
                        book['author_name'] = resp2['items'][0]['volumeInfo']['authors'][0]
                        book['description'] = resp2['items'][0]['volumeInfo']['description']
                        book['year'] = resp2['items'][0]['volumeInfo']['publishedDate']
                    else:
                        index = "ISBN:{0}".format(isbn)
                        book['title'] = resp[index]['title']
                        book['publishers'] = resp[index]['publishers'][0]['name']
                        if 'cover' in resp[index]:
                            book['book_cover'] = resp[index]['cover']['large']
                        else:
                            book['cover'] = '#'
                        book['author_name'] = resp[index]['authors'][0]['name']
                        date1 = resp[index]['publish_date']
                        book['year'] = date1
                        if resp2['totalItems'] != 0:
                            book['title'] = resp2['items'][0]['volumeInfo']['title']
                            if 'publisher' in resp2['items'][0]['volumeInfo']:
                                book['publishers'] = resp2['items'][0]['volumeInfo']['publisher']
                            else:
                                book['publishers'] = ''
                            if 'authors' in resp2['items'][0]['volumeInfo']:
                                book['author_name'] = resp2['items'][0]['volumeInfo']['authors'][0]
                            book['description'] = resp2['items'][0]['volumeInfo']['description']
                            book['year'] = resp2['items'][0]['volumeInfo']['publishedDate']
                    output.append(book)
                    return render_template('addbook_result.html', book=output[0])
                else:
                    resp4 = json.loads(response4.text)
                    print(resp4)
                    return render_template('addbook_result.html', book=resp4['book'][0])

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
        book_details = requests.get('http://localhost:5050/user/bookshelf/availability', headers={'x-access-token': session['token']}, json={"current_user": session['user']})
        books = requests.get('http://localhost:5050/user/bookshelf', headers={'x-access-token': session['token']}, json={"current_user": session['user']})
        if books.text == "no books found":
            return render_template('profile.html', books={}, user=user_dict['user'], bday=bday, map=map,  profilepic=profilepic)
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
    filename='images/none.jpeg')}}'" alt="{2}" style="width:80px; height:80px;" alt=" " />""".format('My Current Location', profpic, user['user'][0]['username'])
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
        book_details = requests.get('http://localhost:5050/user/bookshelf/availability', headers={'x-access-token': session['token']}, json={"current_user": username} )
        books = requests.get('http://localhost:5050/user/bookshelf', headers={'x-access-token': session['token']}, json={"current_user": username})
        if books.text == "no books found":
            return render_template('user_profile.html', books={}, user=user_dict['user'], bday=bday, map=map, profilepic=profilepic)
        book_dict=json.loads(books.text)
        book_details_dict=json.loads(book_details.text)
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
        bday = get_bday(user_dict['user']['birth_date'])
        profilepic = (user_dict['user']['profpic'])
        book_details = requests.get('http://localhost:5050/user/bookshelf/availability', headers={'x-access-token': session['token']},
                                    json={"current_user": session['user']})
        books = requests.get('http://localhost:5050/user/bookshelf', headers={'x-access-token': session['token']}, json={"current_user": session['user']})
        if books.text == "no books found":
            return render_template('edit_profile.html', books={}, user=user_dict['user'], bday=bday,map=map, profilepic=profilepic, display='none')
        book_dict = json.loads(books.text)
        book_details_dict = json.loads(book_details.text)
        if request.method == 'POST':
            firstname = request.form['first_name']
            lastname = request.form['last_name']
            gender = request.form['gender']
            bdate = request.form['birth_date']
            age = calculate_age(bdate)
            if age < 18:
                books = requests.get('http://localhost:5050/user/bookshelf', headers={'x-access-token': session['token']}, json={"current_user": session['user']})
                if books.text == "no books found":
                    return render_template('edit_profile.html', user=user_dict['user'], bday=bday, map=map,
                                           profilepic=profilepic, display='block')
                return render_template('edit_profile.html', user=user_dict['user'], books=book_dict['book'], bday=bday,
                                       map=map, profilepic=profilepic, display='block')

            contact_num = request.form['contact_number']
            response = requests.post('http://localhost:5050/user/edit', json={"username": session['user'], "first_name": firstname,
                                                                              "last_name": lastname, "birth_date": bdate, "gender": gender,
                                                                              "contact_num":contact_num}, headers={'x-access-token': session['token']})
            print(response.text)
            return redirect('profile')
        else:
            return render_template('edit_profile.html', user=user_dict['user'], books=book_dict['book'], bday=bday, map=map, profilepic=profilepic, display='none')
    else:
        return redirect('unauthorized')

@app.route('/profile/upload', methods=['POST', 'GET'])
def add_profile_pic():
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        response = requests.post('http://localhost:5050/profile/picture', json={"current_user": session['user'], "filename": b64encode(file.read())}, headers={'x-access-token': session['token']})
        message = json.loads(response.text)
        return redirect('profile')
    return redirect('profile')



### END PROFILE ###
@app.route('/book/rate/<contains_id>/<book_id>/<username>', methods=['POST'])
def rate_book(contains_id, book_id, username):
    if g.user:
        ratings = request.form['stars']
        print(ratings)
        response = requests.post('http://localhost:5050/rate-book', json={"ratings":ratings, "username":session['user'], "contains_id":contains_id}, headers={'x-access-token': session['token']})
        print(response.text)
        return redirect(url_for('viewbook', book_id=book_id, username=username))
    else:
        return redirect('unauthorized')

@app.route('/book/comment/<contains_id>/<book_id>/<username>', methods=['POST'])
def comment_book(contains_id, book_id, username):
    if g.user:
        comment = request.form['comment']
        response = requests.post('http://localhost:5050/comment-book', json={"comment":comment, "username":session['user'], "contains_id":contains_id}, headers={'x-access-token': session['token']})
        print(response.text)
        return redirect(url_for('viewbook', book_id=book_id, username=username))
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/<username>/<book_id>', methods=['GET'])
def viewbook(book_id, username):
    if g.user:
        book = requests.get('http://localhost:5050/user/bookshelf/'+book_id, json={"username": username, "current_user": session['user']}, headers={'x-access-token': session['token']})
        book_dict = json.loads(book.text)
        comments = requests.get('http://localhost:5050/bookshelf/comments/book', json={"username": username, "book_id":book_id}, headers={'x-access-token': session['token']})
        comments_dict = json.loads(comments.text)
        print(len(comments_dict['comments']))
        if username == session['user']:
            return render_template('own_product.html', books=book_dict['book'], comments=comments_dict['comments'][0:5], total=len(comments_dict['comments']), comments2=comments_dict['comments'])

        print(book_dict['book'])
        return render_template('single_product.html', books=book_dict['book'], comments=comments_dict['comments'][0:5], total=len(comments_dict['comments']), comments2=comments_dict['comments'])
    else:
        return redirect('unauthorized')

@app.route('/bookshelf/edit/<book_id>', methods=['GET', 'POST'])
def editbook(book_id):
    if g.user:
        book = requests.get('http://localhost:5050/user/bookshelf/'+book_id, json={"current_user": session['user']}, headers={'x-access-token': session['token']})
        book_dict = json.loads(book.text)
        if request.method == 'POST':
            quantity = request.form['quantity']
            methods = request.form['methods']
            price = request.form['price']
            book = requests.post('http://localhost:5050/user/edit/book', json={"username": session['user'], "quantity":quantity,
                            "methods": methods, "price": price, "book_id": book_id}, headers={'x-access-token': session['token']})
            print(book.text)
            return redirect(url_for('viewbook', book_id=book_id, username=session['user']))
        else:
            return render_template('edit_ownbook.html', username=session['user'], books=book_dict['book'])

    else:
        return redirect('unauthorized')

@app.route('/bookshelf/remove/<book_id>', methods=['POST', 'GET'])
def remove_book(book_id):
    if g.user:
        book = requests.post('http://localhost:5050/user/bookshelf/remove/book', json={"book_id":book_id, "username":session['user']}, headers={'x-access-token': session['token']})
        print(book.text)
        return redirect('home')
    else:
        return redirect('unauthorized')

@app.route('/genre/<genre_name>', methods=['GET'])
def view_genre(genre_name):
    if g.user:
        books = requests.get('http://localhost:5050/interests/view/'+genre_name, headers={'x-access-token': session['token']})
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
        books = requests.get('http://localhost:5050/bookshelf/books', headers={'x-access-token': session['token']})
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
            response= requests.post(url, json={"bookshelf_id": bookshelf_id, "username":session['user'], "book_id":book_id}, headers={'x-access-token': session['token']})
            book_dict=json.loads(response.text)
            print(response.text)
            url2 = 'http://localhost:5050/bookshelf/wishlist/user'
            books = requests.get(url2, json={"current_user": session['user']}, headers={'x-access-token': session['token']})
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
        response = requests.post(url, json={"book_id": book_id, "bookshelf_owner": username, "username": session['user']}, headers={'x-access-token': session['token']})
        book_dict = json.loads(response.text)
        return redirect('wishlist')
    else:
        return redirect('unauthorized')

@app.route('/wishlist', methods=['GET'])
def wishlist():
    if g.user:
        url = 'http://localhost:5050/bookshelf/wishlist/user'
        books = requests.get(url, json={"current_user": session['user']}, headers={'x-access-token': session['token']})
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