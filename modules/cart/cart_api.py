from libraries.connect_database import connect_database, Product, Cart
from libraries.libraries import get_carts
from flask_restful import Resource
from flask import request

session = connect_database()


class CartUser(Resource):
    def __init__(self):
        self.session = session()

    def get(self, user_id):
        carts = get_carts(self.session, user_id)
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
        self.session.add(Cart(user_id=user_id, product_id=product_id, amount=data['amount'],
                              total_price=data['amount'] * self.session.query(Product).filter_by(
                                  id=product_id).first().price))
        self.session.commit()
        carts = get_carts(self.session, user_id)
        self.session.close()
        return {
            "carts": carts,
            "total": sum([x['total_price'] for x in carts])
        }

    def put(self, user_id, product_id):
        data = request.get_json()
        product = self.session.query(Product).filter_by(id=product_id).first()
        if data['amount'] <= product.quantity:
            self.session.query(Cart).filter_by(user_id=user_id, product_id=product_id).update(
                {
                    'amount': data['amount'],
                    'total_price': data['amount'] * self.session.query(Product).filter_by(
                        id=product_id).first().price
                }
            )
            self.session.commit()
        carts = get_carts(self.session, user_id)
        self.session.close()
        return {
            "carts": carts,
            "total": sum([x['total_price'] for x in carts])
        }

    def delete(self, user_id, product_id):
        self.session.query(Cart).filter_by(user_id=user_id, product_id=product_id).delete()
        self.session.commit()
        carts = get_carts(self.session, user_id)
        self.session.close()
        return {
            "carts": carts,
            "total": sum([x['total_price'] for x in carts])
        }
