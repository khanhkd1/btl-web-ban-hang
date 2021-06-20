from libraries.connect_database import connect_database, User
from flask_restful import Resource
from flask import request, jsonify, make_response
from libraries.libraries import get_user_by_id
from werkzeug.security import generate_password_hash

session = connect_database()


class SignIn(Resource):
    def __init__(self):
        self.session = session()

    def post(self):
        data = request.get_json()
        user = self.session.query(User).filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            user = get_user_by_id(self.session, user.id)
            message = 'done'
            data = user
            code = 200
        else:
            message = 'fail'
            data = None
            code = 401
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": message,
                    "data": data
                }
            ), code
        )


class SignUp(Resource):
    def __init__(self):
        self.session = session()

    def post(self):
        data = request.get_json()
        user = self.session.query(User).filter_by(username=data['username']).first()
        if not user:
            user = User(data['username'], data['password'])
            self.session.add(user)
            self.session.commit()
            message = 'done'
            code = 200
        else:
            message = 'fail'
            code = 401
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": message,
                    "data": {}
                }
            ), code
        )


class UserAPI(Resource):
    def __init__(self):
        self.session = session()

    def get(self, user_id):
        user = get_user_by_id(self.session, user_id)
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": "done",
                    "user": user
                }
            ), 200
        )

    def put(self, user_id):
        data = request.get_json()
        if 'current_password' in data and 'new_password' in data:
            user = self.session.query(User).filter_by(id=user_id).first()
            if user.check_password(data['current_password']):
                self.session.query(User).filter_by(id=user_id).update(
                    {
                        'password': generate_password_hash(data['new_password'])
                    }
                )
                self.session.commit()
                user = get_user_by_id(self.session, user_id)
                message = 'done'
                code = 200
            else:
                message = 'fail'
                user = None
                code = 401
        else:
            self.session.query(User).filter_by(id=user_id).update(data)
            self.session.commit()
            user = get_user_by_id(self.session, user_id)
            message = 'done'
            code = 200
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": message,
                    "user": user
                }
            ), code
        )

    def delete(self, user_id):
        data = request.get_json()
        user = self.session.query(User).filter_by(id=user_id).first()
        if user.check_password(data['password']):
            self.session.query(User).filter_by(id=user_id).delete()
            self.session.commit()
            message = 'done'
            code = 200
        else:
            message = 'fail'
            code = 401
            self.session.close()
            
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": message,
                    "data": None
                }
            ), code
        )
