@app.route('/email_info', methods=['POST', 'GET'])
def email_info():
    data = request.get_json()

    user1 = User.query.filter_by(username=data['username']).first()
    user2 = User.query.filter_by(username=data['sender']).first()

    if user1 is None:
        return jsonify({'message': "Email Address not found"})

    user_data = {}
    user_data['sender'] = user2.email_address
    user_data['recipients'] = user1.email_address
    print(user_data['sender'])

    return jsonify({'user': user_data})