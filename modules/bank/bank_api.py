from libraries.connect_database import connect_database, BankOfUser
from libraries.libraries import get_banks_of_user, get_banks
from flask_restful import Resource
from flask import request, make_response, jsonify

session = connect_database()


class BankAPI(Resource):
    def __init__(self):
        self.session = session()

    def get(self):
        banks = get_banks(self.session)
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": 'done',
                    "data": banks
                }
            ), 200
        )    


class BankUserAPI(Resource):
    def __init__(self):
        self.session = session()

    def get(self, user_id):
        banks_info_of_user = get_banks_of_user(self.session, user_id)
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": 'done',
                    "data": banks_info_of_user
                }
            ), 200
        )

    def post(self, user_id):
        data = request.get_json()
        bank_of_user = self.session.query(BankOfUser).filter_by(user_id=user_id, bank_id=data['bank_id']).first()
        if not bank_of_user:
            self.session.add(BankOfUser(user_id=user_id, bank_id=data['bank_id'], bank_number=data['bank_number']))
            self.session.commit()
            message = 'done'
        else:
            message = 'fail'
        banks_info_of_user = get_banks_of_user(self.session, user_id)
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": message,
                    "data": banks_info_of_user,
                    "note": "message = fail có nghĩa là người dùng đã liên kết ngân hàng này rồi"
                }
            ), 200
        )

    def put(self, user_id):
        data = request.get_json()
        self.session.query(BankOfUser).filter_by(user_id=user_id, bank_id=data['bank_id']).update(data)
        self.session.commit()
        banks_info_of_user = get_banks_of_user(self.session, user_id)
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": 'done',
                    "data": banks_info_of_user
                }
            ), 200
        )

    def delete(self, user_id):
        data = request.get_json()
        self.session.query(BankOfUser).filter_by(user_id=user_id, bank_id=data['bank_id']).delete()
        self.session.commit()
        banks_info_of_user = get_banks_of_user(self.session, user_id)
        self.session.close()
        return make_response(
            jsonify(
                {
                    "message": 'done',
                    "data": banks_info_of_user
                }
            ), 200
        )
