from libraries.connect_database import connect_database, User, Product, Cart, Favorite
from flask_restful import Resource
from flask import request, jsonify, make_response
from libraries.libraries import get_user_by_id, get_carts, get_favorites
from sqlalchemy import exc

session = connect_database()


class SignIn(Resource):
    def __init__(self):
        self.session = session()

    def post(self):
        data = request.get_json()
        user = self.session.query(User).filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": {
                            "id": user.id,
                            "username": user.username,
                            "is_admin": user.is_admin,
                            "carts": get_carts(self.session, Cart, Product, user.id),
                            "favorites": get_favorites(self.session, Favorite, Product, user.id)
                        }
                    }
                ), 200
            )
        else:
            return make_response(
                jsonify(
                    {
                        "message": "fail",
                        "data": {}
                    }
                ), 401
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
            self.session.close()
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": {}
                    }
                ), 200
            )
        else:
            self.session.close()
            return make_response(
                jsonify(
                    {
                        "message": "fail",
                        "data": {}
                    }
                ), 401
            )


class UserAPI(Resource):
    def __init__(self):
        self.session = session()

    def get(self, user_id):
        user = get_user_by_id(self.session, User, user_id)
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
        self.session.query(User).filter_by(id=user_id).update(data)
        self.session.commit()
        user = get_user_by_id(self.session, User, user_id)
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": "done",
                    "user": user
                }
            ), 200
        )            

    def delete(self, user_id):
        self.session.query(User).filter_by(id=user_id).delete()
        self.session.commit()
        return make_response(
            jsonify(
                {
                    "message": "done",
                    "data": None
                }
            ), 200
        )
