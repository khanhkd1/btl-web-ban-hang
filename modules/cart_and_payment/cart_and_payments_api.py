from libraries.connect_database import connect_database, Product, Cart, Bank, BankOfUser, User, Payment
from libraries.libraries import get_carts, get_banks_info_of_user, get_banks, get_payments
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import exc
import datetime

session = connect_database()


class CartWithUserId(Resource):
    def get(self, user_id):
        session_tmp = session()
        try:
            carts = get_carts(session_tmp, Cart, Product, user_id)
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": {
                            "carts": carts,
                            "total": sum([x['total_price'] for x in carts])
                        }
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

    def post(self, user_id):
        data = request.get_json()
        session_tmp = session()

        if not session_tmp.query(Cart).filter_by(user_id=user_id, product_id=data['product_id']).first():
            cart = Cart(
                user_id=user_id,
                product_id=data['product_id'],
                amount=data['amount'],
                total_price=data['amount'] * session_tmp.query(Product).filter_by(id=data['product_id']).first().price
            )
            session_tmp.add(cart)
        else:
            exist_cart = session_tmp.query(Cart).filter_by(user_id=user_id, product_id=data['product_id']).first()
            session_tmp.query(Cart).filter_by(user_id=user_id, product_id=data['product_id']).update(
                {
                    'amount': data['amount'] + exist_cart.amount,
                    'total_price': (data['amount'] + exist_cart.amount) * session_tmp.query(Product).filter_by(
                        id=data['product_id']).first().price
                }
            )
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
                        "data": []
                    }
                ), 500
            )
        finally:
            session_tmp.close()

    def put(self, user_id):
        data = request.get_json()
        session_tmp = session()
        session_tmp.query(Cart).filter_by(user_id=user_id, product_id=data['product_id']).update(
            {
                'amount': data['amount'],
                'total_price': data['amount'] * session_tmp.query(Product).filter_by(
                    id=data['product_id']).first().price
            }
        )
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
                        "data": []
                    }
                ), 500
            )
        finally:
            session_tmp.close()

    def delete(self, user_id):
        data = request.get_json()
        session_tmp = session()
        session_tmp.query(Cart).filter_by(user_id=user_id, product_id=data['product_id']).delete()
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
                        "data": []
                    }
                ), 500
            )
        finally:
            session_tmp.close()


class BankWithUserId(Resource):
    def get(self, user_id):
        session_tmp = session()
        try:
            banks_info_of_user = get_banks_info_of_user(session_tmp, BankInfoOfUser, User, Bank, user_id)
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": {
                            "banks_info_of_user": banks_info_of_user
                        }
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


class BankWithoutUserId(Resource):
    def get(self):
        session_tmp = session()
        try:
            banks = get_banks(session_tmp, Bank)
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": {
                            "banks": banks
                        }
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


class PaymentAPI(Resource):
    def get(self, user_id):
        session_tmp = session()
        try:
            payments = get_payments(session_tmp, Payment, Product, user_id)
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": {
                            'payments': payments
                        }
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

    def post(self, user_id):
        session_tmp = session()
        carts = get_carts(session_tmp, Cart, Product, user_id)
        products = '-'.join([str([x['product_id'], x['amount'], x['total_price']]) for x in carts])

        payment = Payment(
            user_id=user_id,
            products=products,
            total=sum([x['total_price'] for x in carts]),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            cancel=False,
            admin_confirm=False,
            status='Chờ xác nhận'
        )
        session_tmp.add(payment)
        try:
            session_tmp.commit()
            for id_tmp in [x['id'] for x in carts]:
                session_tmp.query(Cart).filter_by(id=id_tmp).delete()
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