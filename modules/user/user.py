from libraries.connect_database import connect_database, User
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import exc

session = connect_database()


class UserApi(Resource):
    def post(self):
        data = request.get_json()
        session_tmp = session()
        if data['function'] == 'sign_in':
            user = session_tmp.query(User).filter_by(username=data['username']).first()

            if user and user.check_password(data['password']):
                return make_response(
                    jsonify(
                        {
                            "message": "login done",
                            "username": user.username,
                            "is_admin": user.is_admin
                        }
                    ), 200
                )
            else:
                return make_response(
                    jsonify(
                        {
                            "message": "login fail"
                        }
                    ), 401
                )
        else:
            user = session_tmp.query(User).filter_by(username=data['username']).first()
            if not user:
                user = User(data['username'], data['password'], False)
                session_tmp.add(user)
                try:
                    session_tmp.commit()
                except exc as e:
                    session_tmp.rollback()
                finally:
                    session_tmp.close()
                return make_response(
                    jsonify(
                        {
                            "message": "success"
                        }
                    ), 200
                )
            else:
                return make_response(
                    jsonify(
                        {
                            "message": "username is exist"
                        }
                    ), 401
                )
