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
