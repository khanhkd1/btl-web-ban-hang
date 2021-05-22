from libraries.connect_database import connect_database, Product, Cart
from libraries.libraries import get_default, get_data_with_page, get_carts
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import exc

session = connect_database()


class CartWithUserId(Resource):
	def get(self, user_id):
		session_tmp = session()
		parameters = request.args
		limit, page, offset, order = get_default(
			parameters, Cart.__table__.columns, Cart
		)
		try:
			carts, total_count = get_carts(session_tmp, parameters, Cart, Product, order, offset, limit, user_id)

			return make_response(
				jsonify(
					{
						"message": "done",
						"data": {
							"carts": get_data_with_page(carts, limit, page, total_count)
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
					'total_price': (data['amount'] + exist_cart.amount) * session_tmp.query(Product).filter_by(id=data['product_id']).first().price
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
				'total_price': data['amount'] * session_tmp.query(Product).filter_by(id=data['product_id']).first().price
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
