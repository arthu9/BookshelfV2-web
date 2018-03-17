from app import db, datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

userInterests = db.Table('userInterests',
                            db.Column('genreid', db.ForeignKey('genre.genre_id')),
                            db.Column('userid', db.ForeignKey('user.id'))
                            )

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.String(11))
    birth_date = db.Column(db.DATE, nullable=False)
    sex = db.Column(db.String(6), nullable=False)
    profpic = db.Column(db.TEXT)
    bookshelf_user = db.relationship('Bookshelf', uselist=False, backref='user_bookshelf')
    borrow_bookshelfs = db.relationship('BorrowsAssociation', backref='user_borrow')
    userRateBooks = db.relationship('BookRateAssociation', backref='user_raterBooks')
    interests = db.relationship('Genre', secondary=userInterests, backref=db.backref('user_interest', lazy='dynamic'))

    def __init__(self, username='', password='', first_name='', last_name='', contact_number='', birth_date='', sex=''):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')
        self.first_name = first_name
        self.last_name = last_name
        self.contact_number = contact_number
        self.birth_date = birth_date
        self.sex = sex


class Bookshelf(db.Model):
    __tablename__ = 'bookshelf'
    bookshelf_id = db.Column(db.Integer, primary_key=True)
    bookshef_owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='bookshelf_owner')
    booksContain = db.relationship('ContainsAsscociation', backref=db.backref('bookshelf_contains'))
    borrow_users = db.relationship('BorrowsAssociation', backref='bookshelfBooks')

    def __init__(self, bookshelf_id='', bookshef_owner=''):
        self.bookshelf_id = bookshelf_id
        self.bookshef_owner = bookshef_owner


class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT, nullable=False)
    edition = db.Column(db.Integer)
    year_published = db.Column(db.String(4))
    isbn = db.Column(db.String(20))
    types = db.Column(db.String(20))
    genre = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.publisher_id'))
    bookshelfBooks = db.relationship('ContainsAsscociation', backref='books_contains')
    booksAuthor = db.relationship('WrittenByAssociation', backref='books_author')
    publisher = db.relationship('Publisher', backref='bookPublish')
    rateBooks = db.relationship('BookRateAssociation', backref='books_rateBooks')
    borrowcount = db.Column(db.Integer, default=0)

    def __init__(self, title='', edition='', year_published='', isbn='', types='', publisher_id=''):
        self.title = title
        self.edition = edition
        self.year_published = year_published
        self.isbn = isbn
        self.types = types
        self.publisher_id = publisher_id


class ContainsAsscociation(db.Model):
    __tablename__ = 'contains'
    quantity = db.Column(db.Integer)
    availability = db.Column(db.String(3))
    shelf_id = db.Column(db.Integer, db.ForeignKey('bookshelf.bookshelf_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    bookshelfcontain = db.relationship('Bookshelf', backref='containingbooks')
    containsbooks = db.relationship('Books', backref='booksBookshelf')

    def __init__(self, shelf_id='', book_id='', quantity='', availability=''):
        self.shelf_id = shelf_id
        self.book_id = book_id
        self.quantity = quantity
        self.availability = availability


class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    categories = db.Column(db.String(30))
    books = db.relationship('Books', backref='books_cat')


class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True)
    author_first_name = db.Column(db.String(50))
    author_last_name = db.Column(db.String(50))
    authorBooks = db.relationship('WrittenByAssociation', backref="author_books")

    def __init__(self, author_first_name='', author_last_name=''):
        self.author_first_name = author_first_name
        self.author_last_name = author_last_name


class WrittenByAssociation(db.Model):
    __tablename__ = 'writtenBy'
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), primary_key=True)
    author = db.relationship('Author', backref='author_writtenby')
    books = db.relationship('Books', backref='booksAuthor_writtenby')

    def __init__(self, author_id='', book_id=''):
        self.author_id = author_id
        self.book_id = book_id


class Publisher(db.Model):
    __tablename__ = 'publisher'
    publisher_id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(50))
    publishBooks = db.relationship('Books', backref='publisher_books')

    def __init__(self, publisher_name=''):
        self.publisher_name = publisher_name


class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, genre_name):
        self.genre_name = genre_name




class BorrowsAssociation(db.Model):
    __tablename__ = 'borrows'
    borrowed = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shelf_id = db.Column(db.Integer, db.ForeignKey('bookshelf.bookshelf_id'))
    date = db.Column(db.DateTime, default=datetime.datetime.today)
    status = db.Column(db.Integer)
    bookid = db.Column(db.Integer)
    seen = db.Column(db.Integer)
    otherUserReturn = db.Column(db.Integer)
    curUserReturn = db.Column(db.Integer)
    returnDate = db.Column(db.TEXT)
    user = db.relationship('User', backref='borrowBookshelfs')
    bookshelf = db.relationship('Bookshelf', backref='borrowUsers')

    def __init__(self, user_id='', shelf_id='', status='', bookid='', seen='', otherUserReturn='',curUserReturn='',returnDate=''):
        self.user_id = user_id
        self.shelf_id = shelf_id
        self.status = status
        self.bookid = bookid
        self.seen = seen
        self.otherUserReturn = otherUserReturn
        self.curUserReturn = curUserReturn
        self.returnDate = returnDate


class BookRateAssociation(db.Model):
    __tablename__ = 'bookRate'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.TEXT)
    user = db.relationship('User', backref='user_booksRate')
    books = db.relationship('Books', backref='bookRate')

    def __init__(self, user_id='', book_id='', rating='', comment=''):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
        self.comment = comment


class BookRateTotal(db.Model):
    __tablename__ = 'bookrateTotal'
    numRate = db.Column(db.Integer, primary_key=True)
    userRater = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookRated = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    totalRate = db.Column(db.Float, default=0)

    def __init__(self, userRater='', bookRated='', totalRate=''):
        self.userRater = userRater
        self.bookRated = bookRated
        self.totalRate = totalRate


class UserRateAssociation(db.Model):
    __tablename__ = 'userRate'
    user_idRater = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    user_idRatee = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key= True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.TEXT)

    def __init__(self, user_idRater='', user_idRatee='', rating='', comment=''):
        self.user_idRater = user_idRater
        self.user_idRatee = user_idRatee
        self.rating = rating
        self.comment = comment


class UserRateTotal(db.Model):
    __tablename__ = 'userRateTotal'
    numOfRate = db.Column(db.Integer, primary_key=True)
    userRatee = db.Column(db.Integer, db.ForeignKey('user.id'))
    userRater = db.Column(db.Integer, db.ForeignKey('user.id'))
    totalRate = db.Column(db.Float)

    def __init__(self, userRatee='', userRater='', totalRate=''):
        self.userRatee = userRatee
        self.userRater = userRater
        self.totalRate = totalRate

class ActLogs(db.Model):
    __tablename__ = 'actlogs'
    logs = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shelf_id = db.Column(db.Integer, db.ForeignKey('bookshelf.bookshelf_id'))
    date = db.Column(db.DateTime, default=datetime.datetime.today)
    status = db.Column(db.Integer)
    bookid = db.Column(db.Integer)
    def __init__(self, user_id='', shelf_id='', status='', bookid=''):
        self.user_id = user_id
        self.shelf_id = shelf_id
        self.status = status
        self.bookid = bookid

