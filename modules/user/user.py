from libraries.connect_database import connect_database, User
from flask_restful import Resource
from flask import request, jsonify, make_response
from libraries.libraries import get_user_by_id
from sqlalchemy import exc

session = connect_database()


class UserWithoutUserId(Resource):
    def post(self):
        data = request.get_json()
        session_tmp = session()
        if data['function'] == 'sign_in':
            user = session_tmp.query(User).filter_by(username=data['data']['username']).first()

            if user and user.check_password(data['data']['password']):
                return make_response(
                    jsonify(
                        {
                            "message": "done",
                            "data": {
                                "id": user.id,
                                "username": user.username,
                                "is_admin": user.is_admin,
                                "full_name": user.full_name,
                                "phone": user.phone,
                                "email": user.email
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
        else:
            user = session_tmp.query(User).filter_by(username=data['data']['username']).first()
            if not user:
                user = User(data['data']['username'], data['data']['password'], False, data['data']['full_name'],
                            data['data']['phone'], data['data']['email'])
                session_tmp.add(user)
                try:
                    session_tmp.commit()
                    return make_response(
                        jsonify(
                            {
                                "message": "done",
                                "data": {}
                            }
                        ), 200
                    )
                except exc as e:
                    session_tmp.rollback()
                    return make_response(
                        jsonify(
                            {
                                "message": f"{e}",
                                "data": {}
                            }
                        ), 500
                    )
                finally:
                    session_tmp.close()

            else:
                return make_response(
                    jsonify(
                        {
                            "message": "fail",
                            "data": {}
                        }
                    ), 401
                )


class UserWithUserId(Resource):
    def get(self, user_id):
        session_tmp = session()
        try:
            user = get_user_by_id(session_tmp, User, user_id)
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": user
                    }
                ), 200
            )
        except exc as e:
            session_tmp.rollback()
            return make_response(
                jsonify(
                    {
                        "message": f"{e}",
                        "data": {}
                    }
                ), 500
            )
        finally:
            session_tmp.close()

    def put(self, user_id):
        data = request.get_json()
        session_tmp = session()
        session_tmp.query(User).filter_by(id=user_id).update(data)
        try:
            session_tmp.commit()
            user = get_user_by_id(session_tmp, User, user_id)
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": user
                    }
                ), 200
            )
        except exc as e:
            session_tmp.rollback()
            return make_response(
                jsonify(
                    {
                        "message": f"{e}",
                        "data": {}
                    }
                ), 500
            )
        finally:
            session_tmp.close()
