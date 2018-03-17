from app import app, User, Search, LoginForm, RegistrationForm, db, Author, Bookshelf, BookRateAssociation, Books, \
    WrittenByAssociation, ContainsAsscociation, Addbook, Publisher, BookRateTotal, BorrowsAssociation, EditProfile, \
    UserRateTotal, UserRateAssociation, datetime, ActLogs, Genre
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from sqlalchemy import desc


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/book/<int:book_id>/<int:page_num>', methods=['GET', 'POST'])
def indexind(book_id, page_num):
    form = Search()
    book = ContainsAsscociation.query.filter_by(book_id=book_id).paginate(page_num, 12)
    rate = BookRateTotal.query.filter_by(bookRated=book_id).first()
    yx = []
    comment = BookRateAssociation.query.filter_by(book_id=book_id).all()
    for id in comment:
        s = User.query.filter_by(id=id.user_id).first()
        yx.append(s.first_name + ' ' + s.last_name)

    x = []
    y = []
    z = []
    t = ContainsAsscociation.query.filter_by(book_id=book_id).first()
    title = t.containsbooks.title
    for bok in book.items:
        s = User.query.filter_by(id=bok.shelf_id).first()
        x.append(s.first_name)
        y.append(s.last_name)
        z.append(s.id)
    return render_template('indexind.html', yx=yx, book=book, title=title, comment=comment, rate=rate, form=form,
                           book_id=book_id, x=x, y=y, z=z)


@app.route('/result/<string:item>/<int:page_num>', methods=['GET', 'POST'])
def tosearch(page_num, item):
    form = Search()
    search1 = item
    if form.validate_on_submit():
        book = ContainsAsscociation.query.join(Books).filter(((Books.title.like(search1)) | (
            Books.year_published.like(search1)) | (Books.types.like(search1)) | (Books.edition.like(search1)) | (
                                                              Books.isbn.like(search1)))).paginate(page_num, 12)
        x = []
        y = []
        for bok in book.items:
            s = ContainsAsscociation.query.filter_by(book_id=bok.book_id).first()
            d = WrittenByAssociation.query.filter_by(book_id=s.book_id).first()
            x.append(s.quantity)
            y.append(d.author.author_first_name + ' ' + d.author.author_last_name)
        return render_template('indexres.html', book=book, page_num=page_num, item=item, form=form, x=x, y=y)
    book = ContainsAsscociation.query.join(Books).filter(((Books.title.like(search1)) | (
        Books.year_published.like(search1)) | (Books.types.like(search1)) | (Books.edition.like(search1)) | (
                                                              Books.isbn.like(search1)))).paginate(page_num, 12)
    x = []
    y = []

    for bok in book.items:
        s = ContainsAsscociation.query.filter_by(book_id=bok.book_id).first()
        d = WrittenByAssociation.query.filter_by(book_id=s.book_id).first()
        x.append(s.quantity)
        y.append(d.author.author_first_name + ' ' + d.author.author_last_name)
    return render_template('indexres.html', book=book, page_num=page_num, item=item, form=form, x=x, y=y)


@app.route('/', methods=['GET', 'POST'])
def index():

    check = Genre.query.filter_by(genre_id=1).first()
    check2 = Genre.query.filter_by(genre_id=25).first()
    print(check)
    print(check2)
    if check is None and check2 is None:
        fill_genre()

    form = Search()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    else:
        if form.validate_on_submit():
            search = '%'+form.search.data+'%'
            return redirect(url_for('tosearch', item=search, page_num=1))
        else:
            top = BookRateTotal.query.join(Books).order_by(BookRateTotal.totalRate.desc()).limit(3).all()
            x = []
            y = []
            books = []
            comm = []
            ids = []
            for bok in top:
                s = WrittenByAssociation.query.filter_by(book_id=bok.bookRated).first()
                ss = Books.query.filter_by(book_id=bok.bookRated).first()
                author = Author.query.filter_by(author_id=s.author_id).first()
                comments = BookRateAssociation.query.filter_by(book_id=bok.bookRated).first()
                comm.append(comments.comment)
                books.append(ss.title)
                ids.append(ss.book_id)
                x.append(author.author_first_name)
                y.append(author.author_last_name)
            return render_template('index.html', ids=ids, top=top, books=books, form=form, x=x, y=y, comm=comm)

def fill_genre():
    genre1 = Genre('Academics')
    db.session.add(genre1)
    genre2 = Genre('Action and Adventure')
    db.session.add(genre2)
    genre3 = Genre('Art')
    db.session.add(genre3)
    genre4 = Genre('Autobiography')
    db.session.add(genre4)
    genre5 = Genre('Biography')
    db.session.add(genre5)
    genre6 = Genre("Children's")
    db.session.add(genre6)
    genre7 = Genre('Classic')
    db.session.add(genre7)
    genre8 = Genre('Comics')
    db.session.add(genre8)
    genre9 = Genre('CookBook')
    db.session.add(genre9)
    genre10 = Genre('Drama')
    db.session.add(genre10)
    genre11 = Genre('Fantasy')
    db.session.add(genre11)
    genre12 = Genre('Fiction')
    db.session.add(genre12)
    genre13 = Genre('Health')
    db.session.add(genre13)
    genre14 = Genre('History')
    db.session.add(genre14)
    genre15 = Genre('Horror')
    db.session.add(genre15)
    genre16 = Genre('Math')
    db.session.add(genre16)
    genre17 = Genre('Mystery')
    db.session.add(genre17)
    genre18 = Genre('Nonfiction')
    db.session.add(genre18)
    genre19 = Genre('Poetry')
    db.session.add(genre19)
    genre20 = Genre('Religion')
    db.session.add(genre20)
    genre21 = Genre('Romance')
    db.session.add(genre21)
    genre22 = Genre('Satire')
    db.session.add(genre22)
    genre23 = Genre('Science')
    db.session.add(genre23)
    genre24 = Genre('Sci-Fi')
    db.session.add(genre24)
    genre25 = Genre('Young Adult')
    db.session.add(genre25)
    db.session.commit()



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated is True:
        return redirect(url_for('home'))
    elif form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password')
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if current_user.is_authenticated is True:
        return redirect(url_for('interest'))
    elif form.validate_on_submit():
        new_user = User(form.username.data, form.password.data, form.first_name.data,
                        form.last_name.data, form.contact.data, form.birth_date.data, form.sex.data)
        db.session.add(new_user)
        db.session.commit()
        bookshelf = Bookshelf(new_user.id, new_user.id)
        db.session.add(bookshelf)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('interest'))
    return render_template('register.html', form=form)

@app.route('/interest', methods=['GET', 'POST'])
@login_required
def interest():
    all_genres = Genre.query.order_by().all()
    userid = current_user.id
    user = User.query.filter_by(id=userid).first()
    if request.method == 'POST':
        interests = request.form.getlist('interests')
        print(interests)
        if interests is not None:
            for i in interests:
                genre_selected = Genre.query.filter_by(genre_name=i).first()
                user.interests.append(genre_selected)
                db.session.commit()
        return redirect(url_for('home'))
    return render_template('interest.html', genres=all_genres)

@app.route('/home', defaults={'page_num': 1}, methods=['GET', 'POST'])
@app.route('/home/<int:page_num>', methods=['GET', 'POST'])
@login_required
def home(page_num):
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower

    form = Search()
    if form.validate_on_submit():
        search1 = '%'+form.search.data+'%'
        book = ContainsAsscociation.query.join(Books).filter(((Books.title.like(search1)) | (
                Books.year_published.like(search1)) | (Books.types.like(search1)) | (Books.edition.like(search1)) | (
                                                                      Books.isbn.like(search1)))).paginate(page_num, 8)
        x = []
        y = []
        for bok in book.items:
            s = ContainsAsscociation.query.filter_by(book_id=bok.book_id).first()
            d = WrittenByAssociation.query.filter_by(book_id=s.book_id).first()
            x.append(s.quantity)
            y.append(d.author.author_first_name + ' ' + d.author.author_last_name)
        return render_template('homepage1.html', page_num=page_num, book=book, current_user=current_user, form=form, x=x, y=y, count=count)
    top = BookRateTotal.query.join(Books).order_by(BookRateTotal.totalRate.desc()).limit(4).all()
    authors = []
    bookqnt = []
    ids = []
    book = []
    edition = []
    totrate = []
    most = Books.query.order_by(Books.borrowcount.desc()).limit(4).all()
    mostauth = []
    mostqnt = []
    most1 = Books.query.order_by(Books.book_id.desc()).paginate(page_num, 8)
    mostauth1 = []
    mostqnt1 = []
    for bok in top:
        s = WrittenByAssociation.query.filter_by(book_id=bok.bookRated).first()
        ss = Books.query.filter_by(book_id=bok.bookRated).first()
        qnty = ContainsAsscociation.query.filter_by(book_id=bok.bookRated).all()
        quantity = 0
        for q in qnty:
            quantity = quantity + q.quantity
        bookqnt.append(quantity)
        book.append(ss.title)
        edition.append(ss.edition)
        ids.append(ss.book_id)
        author = Author.query.filter_by(author_id=s.author_id).first()
        authors.append(author.author_first_name + ' ' + author.author_last_name)

    for mst in most:
        s = WrittenByAssociation.query.filter_by(book_id=mst.book_id).first()
        author = Author.query.filter_by(author_id=s.author_id).first()
        mostauth.append(author.author_first_name + ' ' + author.author_last_name)
        qnty = ContainsAsscociation.query.filter_by(book_id=mst.book_id).all()
        quantity = 0
        for q in qnty:
            quantity = quantity + q.quantity
        mostqnt.append(quantity)

    for mst in most1.items:
        s = WrittenByAssociation.query.filter_by(book_id=mst.book_id).first()
        author = Author.query.filter_by(author_id=s.author_id).first()
        mostauth1.append(author.author_first_name + ' ' + author.author_last_name)
        qnty = ContainsAsscociation.query.filter_by(book_id=mst.book_id).all()
        quantity = 0
        for q in qnty:
            quantity = quantity + q.quantity
        mostqnt1.append(quantity)
    return render_template('homepage.html', page_num=page_num, top=top, current_user=current_user, form=form, most=most,
                           count=count, authors=authors, bookqnt=bookqnt, ids=ids, book=book, edition=edition,
                           mostauth=mostauth, mostqnt=mostqnt, most1=most1, mostauth1=mostauth1, mostqnt1=mostqnt1)


@app.route('/profile/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower
    form = Search()
    if user_id == current_user.id:
        return render_template('profile.html', form=form, count=count)
    else:
        user = User.query.filter_by(id=user_id).first()
        return render_template('diffprofile.html', form=form, user=user, count=count)


@app.route('/profile/edit/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def editprof(user_id):
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower
    form = Search()
    form1 = EditProfile()
    info = User.query.filter_by(id=user_id).first()
    if form1.validate_on_submit():
        info.first_name = form1.first_name.data
        info.last_name = form1.last_name.data
        info.sex = form1.sex.data
        info.contact_number = form1.contact.data
        info.birth_date = form1.birth_date.data
        db.session.commit()
        return redirect(url_for('profile', user_id=current_user.id, count=count))
    return render_template('editprofile.html', form1=form1, form=form, info=info, user_id=user_id, count=count)


@app.route('/home/book/<int:book_id>/<int:page_num>', methods=['GET', 'POST'])
@login_required
def indibook(book_id, page_num):
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower
    form = Search()
    book = ContainsAsscociation.query.filter_by(book_id=book_id).paginate(page_num, 12)
    rate = BookRateTotal.query.filter_by(bookRated=book_id).first()
    yx = []
    comment = BookRateAssociation.query.filter_by(book_id=book_id).all()
    for id in comment:
        s = User.query.filter_by(id=id.user_id).first()
        yx.append(s.first_name + ' ' + s.last_name)

    t = ContainsAsscociation.query.filter_by(book_id=book_id).first()
    title = t.containsbooks.title
    id = t.containsbooks.book_id
    x = []
    y = []
    z = []
    for bok in book.items:
        s = User.query.filter_by(id=bok.shelf_id).first()
        x.append(s.first_name)
        y.append(s.last_name)
        z.append(s.id)
    return render_template('individualbook.html', yx=yx, id=id, title=title, book=book, comment=comment, rate=rate, form=form,
                           book_id=book_id, x=x, y=y, z=z, count=count, current_user=current_user)


@app.route('/profile/bookshelf/<int:user_id>/<int:page_num>', methods=['GET', 'POST'])
@login_required
def bookshelf(user_id, page_num):
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower
    form = Search()
    booksearch = Search()
    if current_user.id == user_id:
        if booksearch.validate_on_submit():
            return redirect(url_for('bookshelfsearch', user_id=current_user.id, page_num=1, searchid=booksearch.search.data, count=count))
        books = ContainsAsscociation.query.filter_by(shelf_id=user_id).paginate(page_num, 6)
        x = []
        y = []
        for bok in books.items:
            s = WrittenByAssociation.query.filter_by(book_id=bok.book_id).first()
            author = Author.query.filter_by(author_id=s.author_id).first()
            x.append(author.author_first_name)
            y.append(author.author_last_name)
        return render_template('bookshelf.html', current_user=current_user, form=form, booksearch=booksearch, books=books, x=x, y=y, count=count)
    else:

        if booksearch.validate_on_submit():
            if booksearch.validate_on_submit():
                return redirect(url_for('bookshelfsearch', user_id=user_id, page_num=1, searchid=booksearch.search.data, count=count))
        books = ContainsAsscociation.query.filter_by(shelf_id=user_id).paginate(page_num, 6)
        x = []
        y = []
        z = []
        for bok in books.items:
            s = WrittenByAssociation.query.filter_by(book_id=bok.book_id).first()
            author = Author.query.filter_by(author_id=s.author_id).first()
            bookId = BorrowsAssociation.query.filter_by(bookid = bok.book_id).first()
            x.append(author.author_first_name)
            y.append(author.author_last_name)
            if bookId is not None:
                z.append(bookId.user_id)
            else:
                z.append('None')

        return render_template('diffbookshelf.html', current_user=current_user, form=form, books=books, booksearch=booksearch, user_id=user_id, x=x, y=y, count=count,z=z)


@app.route('/profile/bookshelf/<int:user_id>/<int:page_num>/<string:searchid>', methods=['GET', 'POST'])
@login_required
def bookshelfsearch(user_id, page_num, searchid):
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower
    form = Search()
    booksearch = Search()
    if current_user.id == user_id:
        search1 = '%'+searchid+'%'
        books = ContainsAsscociation.query.join(Books).filter(
            (ContainsAsscociation.shelf_id == current_user.id) & ((Books.title.like(search1)) | (
             Books.year_published.like(search1)) | (Books.types.like(search1)) | (Books.edition.like(search1)) | (
             Books.isbn.like(search1)))).paginate(page_num, 6)
        x = []
        y = []
        for p in books.items:
            s = WrittenByAssociation.query.filter_by(book_id=p.book_id).first()
            author = Author.query.filter_by(author_id=s.author_id).first()
            x.append(author.author_first_name)
            y.append(author.author_last_name)
        return render_template('bookshelfresult.html', current_user=current_user, form=form, search1=search1,
                               books=books, x=x, y=y, booksearch=booksearch, count=count)
    else:
        search1 = '%' + searchid + '%'
        books = ContainsAsscociation.query.join(Books).filter(
            (ContainsAsscociation.shelf_id == user_id) & ((Books.title.like(search1)) | (
                Books.year_published.like(search1)) | (Books.types.like(search1)) | (Books.edition.like(search1)) | (
                                                                      Books.isbn.like(search1)))).paginate(page_num, 6)
        x = []
        y = []
        z = []
        for bok in books.items:
            s = WrittenByAssociation.query.filter_by(book_id=bok.book_id).first()
            author = Author.query.filter_by(author_id=s.author_id).first()
            bookId = BorrowsAssociation.query.filter_by(bookid = bok.book_id).first()
            x.append(author.author_first_name)
            y.append(author.author_last_name)
            if bookId is not None:
                z.append(bookId.user_id)
            else:
                z.append('None')
        return render_template('diffbookshelfresult.html', current_user=current_user, form=form, search1=search1,
                               books=books, x=x, y=y, booksearch=booksearch, user_id=user_id, count=count,z=z)


@app.route('/profile/rate_and_comment/<int:user_id>', methods=['GET', 'POST'])
@login_required
def ratencomm(user_id):
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower
    form = Search()
    if user_id == current_user.id:
        rating = UserRateTotal.query.filter_by(userRatee=user_id).first()
        rates = UserRateAssociation.query.filter((UserRateAssociation.user_idRatee == current_user.id))
        x = []
        for r in rates:
            s = User.query.filter_by(id=r.user_idRater).first()
            x.append(s.first_name + ' ' + s.last_name)
        return render_template('commNrating.html', form=form, rating=rating, rates=rates, x=x, count=count,current_user=current_user)
    else:
        user = User.query.filter_by(id=user_id).first()
        otheruserId = user_id
        rating = UserRateTotal.query.filter_by(userRatee=user_id).first()
        rates = UserRateAssociation.query.filter((UserRateAssociation.user_idRatee == user_id))
        xs = []
        for r in rates:
            s = User.query.filter_by(id=r.user_idRater).first()
            xs.append(s.first_name + ' ' + s.last_name)
        if request.method == 'POST':
            rateNew = request.form['rateUser']
            comment = request.form['comment']
            rateOld = UserRateAssociation.query.filter((UserRateAssociation.user_idRatee == otheruserId) & (
                UserRateAssociation.user_idRater == current_user.id)).first()

            if rateOld is not None:
                rateOld.rating = rateNew
                rateOld.comment = comment
                db.session.commit()

                totOld = UserRateTotal.query.filter(UserRateTotal.userRatee == otheruserId).first()
                if totOld is not None:
                    rateTot = UserRateAssociation.query.filter(
                        UserRateAssociation.user_idRatee == otheruserId).paginate(1, 6)

                    x = 0
                    count = 0
                    for p in rateTot.items:
                        r = int(p.rating)
                        x = float(x + r)
                        count = float(count + 1)

                    totRate = float(x / count)
                    totOld.totalRate = totRate
                    db.session.commit()
                else:
                    rateTot = UserRateAssociation.query.filter(
                        UserRateAssociation.user_idRatee == otheruserId).paginate(1, 6)

                    x = 0
                    count = 0
                    for p in rateTot.items:
                        r = int(p.rating)
                        x = float(x + r)
                        count = float(count + 1)

                    totRate = float(x / count)

                    newRateTot = UserRateTotal(otheruserId, current_user.id, totRate)
                    db.session.add(newRateTot)
                    db.session.commit()
            else:

                newRater = UserRateAssociation(current_user.id, otheruserId, rateNew, comment)
                db.session.add(newRater)
                db.session.commit()

                totOld = UserRateTotal.query.filter(UserRateTotal.userRatee == otheruserId).first()
                if totOld is not None:
                    rateTot = UserRateAssociation.query.filter(
                        UserRateAssociation.user_idRatee == otheruserId).paginate(1, 6)

                    x = 0
                    count = 0
                    for p in rateTot.items:
                        r = int(p.rating)
                        x = float(x + r)
                        count = float(count + 1)

                    totRate = float(x / count)
                    totOld.totalRate = totRate
                    db.session.commit()
                else:
                    rateTot = UserRateAssociation.query.filter(
                        UserRateAssociation.user_idRatee == otheruserId).paginate(1, 6)

                    x = 0
                    count = 0
                    for p in rateTot.items:
                        r = int(p.rating)
                        x = float(x + r)
                        count = float(count + 1)

                    totRate = float(x / count)

                    newRateTot = UserRateTotal(otheruserId, current_user.id, totRate)
                    db.session.add(newRateTot)
                    db.session.commit()
                return redirect(url_for('ratencomm', user_id=user_id))
        return render_template('diffcommNrating.html', form=form, user=user, rating=rating, rates=rates, xs=xs,
                               count=count,current_user=current_user)


@app.route('/notification', methods=['GET', 'POST'])
@login_required
def notif():
    now = datetime.datetime.now().date()

    curId = current_user.id
    form = Search()
    unseen = BorrowsAssociation.query.filter(
        (((BorrowsAssociation.shelf_id == current_user.id) & ((BorrowsAssociation.status == 1)|(BorrowsAssociation.status==3)))) | (
            (BorrowsAssociation.user_id == current_user.id) & ((BorrowsAssociation.status == 2) | (BorrowsAssociation.status==5))) | ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 2) & (BorrowsAssociation.otherUserReturn==1)))

    unseenOtherUserReturn = BorrowsAssociation.query.filter(
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.otherUserReturn==0) & (BorrowsAssociation.status == 2))

    unseenCurUserReturn = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.curUserReturn==1) & (BorrowsAssociation.status==2))

    for q in unseen:
        q.seen = 1
        db.session.commit()

    for r in unseenOtherUserReturn:
        if (date(r.returnDate)[2]<=date(datetime.datetime.now())[2]) and (date(r.returnDate)[1]<=date(datetime.datetime.now())[1]):
            r.otherUserReturn = 1
            r.seen=0
            db.session.commit()

    for j in unseenCurUserReturn:
        if (date(j.returnDate)[2]<=date(datetime.datetime.now())[2]) and (date(j.returnDate)[1]<=date(datetime.datetime.now())[1]):
            j.curUserReturn = 0
            db.session.commit()



    pags = BorrowsAssociation.query.filter((BorrowsAssociation.status == 1) &
                                           (BorrowsAssociation.shelf_id == current_user.id) |
                                           (((BorrowsAssociation.status == 2) | (BorrowsAssociation.status == 3) | (BorrowsAssociation.status == 4) | (BorrowsAssociation.status == 5))&
                                           (BorrowsAssociation.user_id == current_user.id))
                                           ).order_by(desc(BorrowsAssociation.borrowed)).paginate(1, 8)

    pags2 = BorrowsAssociation.query.filter((((BorrowsAssociation.status == 1) | (BorrowsAssociation.otherUserReturn==1)) &
                                           (BorrowsAssociation.shelf_id == current_user.id)) |
                                           (((BorrowsAssociation.status == 2) | (BorrowsAssociation.status==5) )&
                                           (BorrowsAssociation.user_id == current_user.id)) |
                                            ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)) |
                                            ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3)) ).order_by(desc(BorrowsAssociation.borrowed)).paginate(1, 8)

    x = []
    y = []
    i = []
    b = []
    for p in pags.items:
        book = Books.query.filter(Books.book_id == p.bookid).first()
        s = User.query.filter(User.id == p.shelf_id).first()
        x.append(book.title)
        i.append(s.id)
        y.append(s.first_name + ' ' + s.last_name)
        b.append(s.username)

    l = []
    m = []
    n = []
    o = []
    for q in pags2.items:
        book = Books.query.filter(Books.book_id == q.bookid).first()
        t = User.query.filter(User.id == q.user_id).first()
        l.append(book.title)
        n.append(t.id)
        m.append(t.first_name + ' ' + t.last_name)
        o.append(t.username)

    if request.method == 'POST':
        app = request.form['app']
        borrowerId = request.form['borrower']
        borrowedId = request.form['borrowed']
        book = request.form['book']

        approved = BorrowsAssociation.query.filter(
            (BorrowsAssociation.user_id == borrowerId) & (BorrowsAssociation.shelf_id == borrowedId) & (
            BorrowsAssociation.bookid == book)).first()



        if app == "YES":
            approved.seen = 0
            approved.status = 2
            approved.otherUserReturn = 0
            db.session.commit()
            log = ActLogs(approved.user_id,current_user.id,2,approved.bookid)
            db.session.add(log)
            db.session.commit()
            delbook(book)
        else:
            approved.seen = 1
            approved.status = 0
            db.session.commit()

        pags = BorrowsAssociation.query.filter((BorrowsAssociation.status == 1) &
                                               (BorrowsAssociation.shelf_id == current_user.id) |
                                               ((BorrowsAssociation.status == 2) | (BorrowsAssociation.status == 3) | (BorrowsAssociation.status == 4) | (BorrowsAssociation.status == 5)) &
                                               (BorrowsAssociation.user_id == current_user.id)
                                               ).order_by(desc(BorrowsAssociation.borrowed)).paginate(1, 8)

        pags2 = BorrowsAssociation.query.filter((((BorrowsAssociation.status == 1) | (BorrowsAssociation.otherUserReturn==1)) &
                                           (BorrowsAssociation.shelf_id == current_user.id)) |
                                           (((BorrowsAssociation.status == 2) | (BorrowsAssociation.status==5) )&
                                           (BorrowsAssociation.user_id == current_user.id)) |
                                            ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)) |
                                            ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3)) ).order_by(desc(BorrowsAssociation.borrowed)).paginate(1, 8)

        x = []
        for p in pags.items:
            book = Books.query.filter(Books.book_id == p.bookid).first()
            x.append(book.title)

        l = []
        for q in pags2.items:
            book = Books.query.filter(Books.book_id == q.bookid).first()
            l.append(book.title)

        return render_template('notif.html', form=form, pags=pags, x=x, y=y, i=i, now=now, curId = curId,l=l,m=m,n=n,pags2=pags2,o=o,b=b,current_user=current_user)
    return render_template('notif.html', form=form, pags=pags, x=x, y=y, i=i,now=now, curId=curId,l=l,m=m,n=n,pags2=pags2,o=o,b=b,current_user=current_user)
def date(now):
    year, month, day = "", "", ""
    for i in range(0,10):
        if i<4:
            year = year + str(now)[i]
        elif i>=5 and i<7:
            month = month + str(now)[i]
        elif i>=8 and i<10:
            day = day + str(now)[i]
    return year, month, day

@app.route('/profile/bookshelf/delete/<int:book_id>', methods=['GET', 'POST'])
@login_required
def delbook(book_id):
        avail = ContainsAsscociation.query.filter(ContainsAsscociation.book_id == book_id).first()
        availDelete = int(avail.quantity)
        avail.quantity = availDelete - 1
        db.session.commit()
        if avail.quantity <= 0:
            avail.availability = 'NO'
            db.session.commit()
        return redirect(url_for('bookshelf', user_id=current_user.id, page_num=1))


@app.route('/profile/bookshelf/add', methods=['GET', 'POST'])
@login_required
def addbook():
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower
    form = Addbook()
    form1 = Search()
    if form.validate_on_submit():
        titleNew = form.title.data
        yearNew = form.year.data
        typeNew = form.type.data
        editionNew = form.edition.data
        isbnNew = form.isbn.data
        publisherNew = form.publisher.data
        authorFirstNew = form.author_firstname.data
        authorLastNew = form.author_lastname.data
        pub = '%' + str(publisherNew) + '%'
        books = Books.query.filter((Books.title == titleNew) & (Books.edition == editionNew) & (Books.year_published == yearNew) & (
            Books.isbn == isbnNew)).first()
        publishers = Publisher.query.filter((Publisher.publisher_name.like(pub))).first()
        author = Author.query.filter((Author.author_first_name == authorFirstNew) & (Author.author_last_name == authorLastNew)).first()
        if (books is None) or (publishers is None) or (author is None):
            if publishers is None:
                pubbook = Publisher(publisherNew)
                db.session.add(pubbook)
                db.session.commit()
                pub_id = Publisher.query.filter((Publisher.publisher_name == publisherNew)).first()
                if author is None:
                    authbook = Author(authorFirstNew, authorLastNew)
                    db.session.add(authbook)
                    db.session.commit()
                elif author is not None:
                    auth_id = Author.query.filter((Author.author_first_name == authorFirstNew) and (Author.author_last_name == authorLastNew)).first()
            elif publishers is not None:
                pub_id = Publisher.query.filter((Publisher.publisher_name == publisherNew)).first()
                if author is None:
                    authbook = Author(authorFirstNew, authorLastNew)
                    db.session.add(authbook)
                    db.session.commit()
                elif author is not None:
                    auth_id = Author.query.filter((Author.author_first_name == authorFirstNew) and (
                    Author.author_last_name == authorLastNew)).first()

            auth_id = Author.query.filter((Author.author_first_name == authorFirstNew) and (Author.author_last_name == authorLastNew)).first()

            book = Books(titleNew, editionNew, yearNew, isbnNew, typeNew, pub_id.publisher_id)
            db.session.add(book)
            db.session.commit()
            contain = ContainsAsscociation(current_user.id, book.book_id, 1, 'YES')
            db.session.add(contain)
            db.session.commit()
            written = WrittenByAssociation(auth_id.author_id, book.book_id)
            db.session.add(written)
            db.session.commit()
            return redirect(url_for('bookshelf', user_id=current_user.id, page_num=1, count=count))
        else:
            bookquantity = ContainsAsscociation.query.filter((ContainsAsscociation.shelf_id == current_user.id) & (
                                                              ContainsAsscociation.book_id == books.book_id)).first()
            if bookquantity is None:
                contain = ContainsAsscociation(current_user.id, books.book_id, 1, 'YES')
                db.session.add(contain)
                db.session.commit()
            else:
                curQuant = bookquantity.quantity
                bookquantity.quantity = int(curQuant + 1)
                db.session.commit()
            return redirect(url_for('bookshelf', user_id=current_user.id, page_num=1, count=count))
    return render_template('addbook.html', form=form,form1=form1, count=count, current_user=current_user)



@app.route('/rateBook/<int:book_id>', methods=['POST', 'GET'])
@login_required
def ratebook(book_id):
    rate = request.form['rateUser']
    comment = request.form['comment']
    rateOld = BookRateAssociation.query.filter((BookRateAssociation.user_id == current_user.id) & (BookRateAssociation.book_id == book_id)).first()
    if rateOld is not None:
        rateOld.rating = rate
        rateOld.comment = comment
        db.session.commit()

        totOld = BookRateTotal.query.filter(BookRateTotal.bookRated == book_id).first()
        if totOld is not None:
            rateTot = BookRateAssociation.query.filter(BookRateAssociation.book_id == book_id)
            x = 0
            count = 0
            for p in rateTot:
                r = int(p.rating)
                x = float(x + r)
                count = float(count + 1)

            totRate = float(x / count)
            totOld.totalRate = totRate
            db.session.commit()
        else:
            rateTot = BookRateAssociation.query.filter(BookRateAssociation.book_id == book_id)

            x = 0
            count = 0
            for p in rateTot:
                r = int(p.rating)
                x = float(x + r)
                count = float(count + 1)

            totRate = float(x / count)

            newRateTot = BookRateTotal(current_user.id, book_id, totRate)
            db.session.add(newRateTot)
            db.session.commit()
        return redirect(url_for('indibook', book_id=book_id, page_num=1))
    else:
        newRater = BookRateAssociation(current_user.id, book_id, rate, comment)
        db.session.add(newRater)
        db.session.commit()

        totOld = BookRateTotal.query.filter(BookRateTotal.bookRated == book_id).first()
        if totOld is not None:
            rateTot = BookRateAssociation.query.filter(BookRateAssociation.book_id == book_id)

            x = 0
            count = 0
            for p in rateTot:
                r = int(p.rating)
                x = float(x + r)
                count = float(count + 1)

            totRate = float(x / count)
            totOld.totalRate = totRate
            db.session.commit()
        else:
            rateTot = BookRateAssociation.query.filter(BookRateAssociation.book_id == book_id)

            x = 0
            count = 0
            for p in rateTot:
                r = int(p.rating)
                x = float(x + r)
                count = float(count + 1)

            totRate = float(x / count)

            newRateTot = BookRateTotal(current_user.id, book_id, totRate)
            db.session.add(newRateTot)
            db.session.commit()
    return redirect(url_for('indibook', book_id=book_id, page_num=1))


@app.route('/borrow/<int:owner_id>/<int:book_id>', methods = ['POST', 'GET'])
@login_required
def borrow(owner_id, book_id):
    otheruserId = owner_id
    bookid = book_id
    date = request.form['returndate']
    print otheruserId, bookid, date
    pags = ContainsAsscociation.query.filter(ContainsAsscociation.shelf_id == otheruserId).first()
    bookBorrow = BorrowsAssociation.query.filter(
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.shelf_id == otheruserId) & (
            BorrowsAssociation.bookid == bookid)).first()
    quant = int(pags.quantity)
    if quant <= 0:
        return redirect(url_for('bookshelf', user_id=owner_id, page_num=1))
    elif bookBorrow is None:
        borrows = Books.query.filter_by(book_id=book_id).first()
        t = int(borrows.borrowcount) + 1
        borrows.borrowcount = t
        borrowBook = BorrowsAssociation(current_user.id, otheruserId, 1, bookid, 0, 1,1,date)
        db.session.add(borrowBook)
        db.session.commit()
        return redirect(url_for('bookshelf', user_id=owner_id, page_num=1))
    elif bookBorrow is not None:
        return redirect(url_for('bookshelf', user_id=owner_id, page_num=1))
    

@app.route('/borrowInd/<int:owner_id>/<int:book_id>', methods = ['POST', 'GET'])
@login_required
def borrowInd(owner_id, book_id):
    otheruserId = owner_id
    bookid = book_id
    date = request.form['returndate']
    pags = ContainsAsscociation.query.filter(ContainsAsscociation.shelf_id == otheruserId).first()
    bookBorrow = BorrowsAssociation.query.filter(
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.shelf_id == otheruserId) & (
            BorrowsAssociation.bookid == bookid)).first()
    quant = int(pags.quantity)
    if bookBorrow is None:
        borrows = Books.query.filter_by(book_id=book_id).first()
        t = int(borrows.borrowcount) + 1
        borrows.borrowcount = t
        borrowBook = BorrowsAssociation(current_user.id, otheruserId, 1, bookid, 0, 1,1,date)
        db.session.add(borrowBook)
        db.session.commit()
        return redirect(url_for('indibook',book_id=bookid, page_num=1))
    elif bookBorrow is not None:
        return redirect(url_for('indibook',book_id=bookid, page_num=1))
    elif quant == 0:
        return redirect(url_for('indibook',book_id=bookid, page_num=1))


@app.route('/returnBook/<int:owner_id>/<int:book_id>', methods = ['POST', 'GET'])
@login_required
def returnBook(owner_id,book_id):
    otheruserId = owner_id
    bookid = book_id
    confirmation = request.form['app']
    borrower = request.form['borrower']
    pags = ContainsAsscociation.query.filter(ContainsAsscociation.shelf_id == otheruserId).first()
    bookBorrow = BorrowsAssociation.query.filter(
            (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.shelf_id == otheruserId) & (
            BorrowsAssociation.bookid == bookid)).first()
    if owner_id != current_user.id and bookBorrow is not None:

        bookBorrow.status = 3
        bookBorrow.seen = 0
        db.session.commit()
        return redirect(url_for('notif'))
    else:
        bookBorrow = BorrowsAssociation.query.filter(
         (BorrowsAssociation.shelf_id == current_user.id) & (
            BorrowsAssociation.bookid == bookid) & (BorrowsAssociation.user_id==borrower)).first()

        if confirmation == 'YES':
            bookBorrow.status=4
            db.session.commit()
            quant = ContainsAsscociation.query.filter((ContainsAsscociation.shelf_id==otheruserId) & (ContainsAsscociation.book_id==bookid)).first()
            totquant = int(quant.quantity)
            finalTot = totquant+1
            quant.quantity = finalTot
            quant.availability = 'YES'
            db.session.commit()
            log = ActLogs(bookBorrow.user_id,current_user.id,4,bookBorrow.bookid)
            db.session.add(log)
            db.session.commit()

        else:
            bookBorrow.status= 5
            bookBorrow.seen= 0
            db.session.commit()

    return redirect(url_for('notif'))

@app.route('/returnBookDiff/<int:owner_id>/<int:book_id>', methods = ['POST', 'GET'])
@login_required
def returnBookDiff(owner_id,book_id):
    otheruserId = owner_id
    bookid = book_id
    borrower = request.form['borrower']
    pags = ContainsAsscociation.query.filter(ContainsAsscociation.shelf_id == otheruserId).first()
    bookBorrow = BorrowsAssociation.query.filter(
            (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.shelf_id == otheruserId) & (
            BorrowsAssociation.bookid == bookid)).first()
    if owner_id != current_user.id and bookBorrow is not None:

        bookBorrow.status = 3
        bookBorrow.seen = 0
        db.session.commit()
        return redirect(url_for('bookshelf',user_id=owner_id,page_num=1))
    else:
        bookBorrow = BorrowsAssociation.query.filter(
         (BorrowsAssociation.shelf_id == current_user.id) & (
            BorrowsAssociation.bookid == bookid) & (BorrowsAssociation.user_id==borrower)).first()
        confirmation = request.form['app']
        if confirmation == 'YES':
            bookBorrow.status=4
            db.session.commit()
            quant = ContainsAsscociation.query.filter((ContainsAsscociation.shelf_id==otheruserId) & (ContainsAsscociation.book_id==bookid)).first()
            totquant = int(quant.quantity)
            finalTot = totquant+1
            quant.quantity = finalTot
            quant.availability = 'YES'
            db.session.commit()
            log = ActLogs(bookBorrow.user_id,current_user.id,4,bookBorrow.bookid)
            db.session.add(log)
            db.session.commit()

        else:
            bookBorrow.status= 5
            bookBorrow.seen= 0
            db.session.commit()

    return redirect(url_for('bookshelf',user_id=owner_id,page_num=1))

@app.route('/actLogs', defaults={'page_num': 1}, methods=['GET', 'POST'])
@app.route('/actLogs/<int:page_num>', methods=['GET', 'POST'])
@login_required
def actLogs(page_num):
    form = Search()
    notSeen = BorrowsAssociation.query.filter(
        ((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.status == 1) & (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==1)) | (
        (BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.status == 2) &
        (BorrowsAssociation.seen == 0) & (BorrowsAssociation.otherUserReturn==0)) |
        ((BorrowsAssociation.shelf_id==current_user.id) & (BorrowsAssociation.status==3) & (BorrowsAssociation.seen==0)) |
        ((BorrowsAssociation.user_id==current_user.id) & (BorrowsAssociation.status==5) & (BorrowsAssociation.seen==0))).paginate(1, 8)

    seenBorrower = BorrowsAssociation.query.filter((BorrowsAssociation.user_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn==0)).paginate(1,8)
    seenOwner = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.curUserReturn==1)).paginate(1,8)

    returnSeen = BorrowsAssociation.query.filter((BorrowsAssociation.shelf_id == current_user.id) & (BorrowsAssociation.returnDate == datetime.datetime.now().date()) & (BorrowsAssociation.status==2) & (BorrowsAssociation.otherUserReturn == 0))
    for q in returnSeen:
        q.seen = 0
        db.session.commit()


    countBorrower = 0
    for s in seenBorrower.items:
        countBorrower=countBorrower+1

    countOwner = 0
    for q in seenOwner.items:
        countOwner=countOwner+1

    count = 0
    for r in notSeen.items:
        count = count + 1

    count = count+countOwner+countBorrower

    pags = ActLogs.query.filter((ActLogs.shelf_id==current_user.id) | (ActLogs.user_id==current_user.id)).order_by(desc(ActLogs.logs)).paginate(page_num,8)

    l = []
    m = []
    n = []
    o = []
    p = []
    v = []
    for q in pags.items:
        book = Books.query.filter(Books.book_id == q.bookid).first()
        t = User.query.filter(User.id == q.user_id).first()
        s = User.query.filter(User.id == q.shelf_id).first()
        l.append(book.title)
        n.append(t.id)
        m.append(t.first_name + ' ' + t.last_name)
        o.append(t.username)
        p.append(s.first_name + ' ' + s.last_name)
        v.append(s.id)
    return render_template('activitylogs.html', count=count,pags=pags,l=l,m=m,n=n,o=o,p=p,current_user=current_user,form=form)


@app.route('/home/top_rated', defaults={'page_num': 1}, methods=['GET', 'POST'])
@app.route('/home/top_rated/<int:page_num>', methods=['GET', 'POST'])
@login_required
def topbooks(page_num):
    form = Search()
    top = BookRateTotal.query.join(Books).order_by(BookRateTotal.totalRate.desc()).paginate(page_num, 8)
    authors = []
    bookqnt = []
    ids = []
    book = []
    edition = []
    for bok in top.items:
        s = WrittenByAssociation.query.filter_by(book_id=bok.bookRated).first()
        ss = Books.query.filter_by(book_id=bok.bookRated).first()
        qnty = ContainsAsscociation.query.filter_by(book_id=bok.bookRated).all()
        quantity = 0
        for q in qnty:
            quantity = quantity + q.quantity
        bookqnt.append(quantity)
        book.append(ss.title)
        edition.append(ss.edition)
        ids.append(ss.book_id)
        author = Author.query.filter_by(author_id=s.author_id).first()
        authors.append(author.author_first_name + ' ' + author.author_last_name)
    return render_template('topbooks.html', form=form, page_num=page_num, authors=authors, bookqnt=bookqnt, ids=ids,
                           book=book, edition=edition, top=top,current_user=current_user)


@app.route('/home/most_borrowed', defaults={'page_num': 1}, methods=['GET', 'POST'])
@app.route('/home/most_borrowed<int:page_num>', methods=['GET', 'POST'])
@login_required
def mostborrow(page_num):
    form = Search()
    most = Books.query.order_by(Books.borrowcount.desc()).paginate(page_num, 8)
    mostauth = []
    mostqnt = []
    for mst in most.items:
        s = WrittenByAssociation.query.filter_by(book_id=mst.book_id).first()
        author = Author.query.filter_by(author_id=s.author_id).first()
        mostauth.append(author.author_first_name + ' ' + author.author_last_name)
        qnty = ContainsAsscociation.query.filter_by(book_id=mst.book_id).all()
        quantity = 0
        for q in qnty:
            quantity = quantity + q.quantity
        mostqnt.append(quantity)
    return render_template('mostborrow.html', form=form, most=most, page_num=page_num, mostauth=mostauth,
                           mostqnt=mostqnt,current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
