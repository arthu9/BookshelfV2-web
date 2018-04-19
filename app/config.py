SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123samsamsam@localhost/booksnew'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'Thisissecret'
JWT_SECRET_KEY = 'jwt-secret-string'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']