from flask_wtf import FlaskForm
from wtforms import StringField,  PasswordField, RadioField, ValidationError, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, InputRequired, EqualTo, DataRequired
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm = PasswordField('Repeat password', validators=[DataRequired(),
                                                           EqualTo('password', message='Passwords must match.')])
    first_name = StringField('First name', validators=[InputRequired(), Length(min=3, max=25)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=2, max=25)])
    contact = StringField('Contact', validators=[InputRequired(), Length(11)])
    sex = RadioField('Sex', validators=[InputRequired()], choices=[('Male', 'Male'), ('Female', 'Female')], default='M')
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired(), InputRequired()])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired(message='Username is invalid'), Length(min=3, max=25)])
    password = PasswordField('Password', [InputRequired(message='Password is invalid'), Length(min=6, max=80)])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is None:
            raise ValidationError('Username is not registered')


class Search(FlaskForm):
    search = StringField(validators=[InputRequired()])


class EditProfile(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=3, max=25)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=2, max=25)])
    contact = StringField('Contact', validators=[InputRequired(), Length(11)])
    sex = RadioField('Sex', validators=[InputRequired()], choices=[('Male', 'Male'), ('Female', 'Female')], default='M')
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired(), InputRequired()])


class Addbook(FlaskForm):
    title = StringField('Title', validators=[Length(min=1, max=100)])
    year = StringField('Year Published', validators=[Length(min=1, max=10)])
    author_firstname = StringField('Author\'s first name', validators=[Length(min=1, max=40)])
    author_lastname = StringField('Author\'s last name', validators=[Length(min=1, max=40)])
    publisher = StringField('Publisher', validators=[Length(min=1, max=40)])
    edition = StringField('Edition', validators=[Length(min=1, max=20)])
    isbn = StringField('ISBN', validators=[Length(min=1, max=13)])
    type = SelectField('Type', validators=[InputRequired()], choices=[('', 'Types'), ('Hard bound', 'Hard bound'),
                                                                      ('Soft bound', 'Soft bound')])
    genre = SelectField('Genre', validators=[InputRequired()], choices=[('', 'Genre'),
                                                                                  ('Academics', 'Academics'), ('Fantasy', 'Fantasy'), ('Mystery', 'Mystery'),
                                                                                  ('Science Fiction', 'Science Fiction'), ('Classic', 'Classic'),
                                                                                  ('Action and Adventure', 'Action and Adventure'), ('Health', 'Health'),
                                                                                  ('History', 'History'), ('Math', 'Math'), ('Horror', 'Horror'),
                                                                                  ("Children's","Children's" ), ('Science', 'Science'), ('Poetry', 'Poetry'),
                                                                                  ('Comics', 'Comics'), ('Art', 'Art'), ('Cookbooks', 'Cookbooks'), ('Religion', 'Religion'),
                                                                                  ('Biographies', 'Biographies'), ('Autobiographies', 'Autobiographies'),
                                                                                  ('Fiction', 'Fiction'), ('Nonfiction', 'Nonfiction'), ('Young Adult','Young Adult'),
                                                                                  ('Satire', 'Satire'), ('Drama', 'Drama'), ('Romance', 'Romance')])

