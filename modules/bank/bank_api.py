from libraries.connect_database import connect_database, BankOfUser
from libraries.libraries import get_banks_of_user, get_banks
from flask_restful import Resource
from flask import request

session = connect_database()


class BankAPI(Resource):
    def __init__(self):
        self.session = session()

    def get(self):
        banks = get_banks(self.session)
        self.session.close()
        return banks


class BankUserAPI(Resource):
    def __init__(self):
        self.session = session()

    def get(self, user_id):
        banks_info_of_user = get_banks_of_user(self.session, user_id)
        self.session.close()
        return banks_info_of_user


class BankUserBankAPI(Resource):
    def __init__(self):
        self.session = session()

    def post(self, user_id, bank_id):
        data = request.get_json()
        bank_of_user = self.session.query(BankOfUser).filter_by(user_id=user_id, bank_id=bank_id).first()
        if not bank_of_user:
            self.session.add(BankOfUser(user_id=user_id, bank_id=bank_id, bank_number=data['bank_number']))
        else:
            self.session.query(BankOfUser).filter_by(user_id=user_id, bank_id=bank_id).update(data)
        self.session.commit()
        self.session.close()
        return

    def put(self, user_id, bank_id):
        data = request.get_json()
        self.session.query(BankOfUser).filter_by(user_id=user_id, bank_id=bank_id).update(data)
        self.session.commit()
        self.session.close()
        return

    def delete(self, user_id, bank_id):
        self.session.query(BankOfUser).filter_by(user_id=user_id, bank_id=bank_id).delete()
        self.session.commit()
        self.session.close()
        return
