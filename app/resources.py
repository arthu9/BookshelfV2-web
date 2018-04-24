from flask_restful import Resource, reqparse
#from models import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_jwt_extended import JWTManager
from flask import Flask, render_template
from flask.views import View

app = Flask(__name__)
jwt = JWTManager(app)


parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('first_name')
parser.add_argument('last_name')
parser.add_argument('contact_number')
parser.add_argument('birth_date')
parser.add_argument('gender')



class RenderTemplate(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)





@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklist(jti)



class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}


        new_user = UserModel(
           # 'http://localhost:8080/signup',
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            first_name = data['first_name'],
            last_name = data['last_name'],
            contact_number = data['contact_number'],
            birth_date = data['birth_date'],
            gender = data['gender']
        )
        # data(
        #     'http://localhost:8080/signup',
        #     json={"first_name": first_name, "last_name": last_name,
        #           "birth_date": birth_date, "gender": gender,
        #           "contact_number": contact_number, "username": username, "password": password},
        # )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity= data['username'])
            refresh_token = create_refresh_token(identity= data['username'])
            # # return {
            #     'message': 'User {} was created'.format(data['username']),
            #     'access_token': access_token,
            #     'refresh_token': refresh_token
            # }
            #return render_template('dashboard.html', access_token=access_token, refresh_token=refresh_token)

            return app.add_url_rule('/dashboard', view_func=RenderTemplateView.as_view(
                'dashboard', template_name='dashboard.html', access_token=access_token, refresh_token=refresh_token))
        except:
            return {'message': 'Something went wrong'}, 500




class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_username(data['username'])


        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity= data['username'])
            refresh_token = create_refresh_token(identity= data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500



class UserLogoutRefresh(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }