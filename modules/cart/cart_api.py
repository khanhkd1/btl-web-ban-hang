from libraries.connect_database import connect_database, Product, Cart, Bank, BankOfUser, User, Payment
from libraries.libraries import get_carts, get_banks, get_payments
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import exc
import datetime

session = connect_database()


class CartUser(Resource):
    def __init__(self):
        self.session = session()

    def get(self, user_id):
        carts = get_carts(self.session, Cart, Product, user_id)
        self.session.close()
        return {
            "carts": carts,
            "total": sum([x['total_price'] for x in carts])
        }


class CartUserProduct(Resource):
    def __init__(self):
        self.session = session()

    def post(self, user_id, product_id):
        data = request.get_json()
        cart = self.session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
        if not cart:
            self.session.add(Cart(user_id=user_id, product_id=product_id, amount=data['amount'],
                total_price=data['amount'] * self.session.query(Product).filter_by(id=product_id).first().price))
        else:
            self.session.query(Cart).filter_by(user_id=user_id, product_id=product_id).update(
                {
                    'amount': data['amount'] + cart.amount,
                    'total_price': (data['amount'] + cart.amount) * self.session.query(Product).filter_by(
                        id=product_id).first().price
                }
            )
        self.session.commit()
        self.session.close()
        return

    def put(self, user_id, product_id):
        data = request.get_json()
        self.session.query(Cart).filter_by(user_id=user_id, product_id=product_id).update(
            {
                'amount': data['amount'],
                'total_price': data['amount'] * self.session.query(Product).filter_by(
                    id=product_id).first().price
            }
        )
        self.session.commit()
        self.session.close()
        return

    def delete(self, user_id, product_id):
        self.session.query(Cart).filter_by(user_id=user_id, product_id=product_id).delete()
        self.session.commit()
        self.session.close()
        return


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
