from app import app
from flask import jsonify


@app.route('/')
def index():
    return jsonify({'message': 'Hello World!'})

@app.route('/registration', methods=['POST'])
def registration():

    new_user = UserModels(username=data['username'], password=data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created'})
