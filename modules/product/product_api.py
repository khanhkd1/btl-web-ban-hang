from libraries.connect_database import connect_database, Product, Brand
from libraries.libraries import get_default, get_data_with_page, get_brands, get_products, get_cameras_or_laptops, get_product
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import exc

session = connect_database()


class Home(Resource):
	def get(self):
		session_tmp = session()
		parameters = request.args
		limit, page, offset, order = get_default(
			parameters, Product.__table__.columns, Product
		)
		try:
			products, total_count = get_products(session_tmp, parameters, Product, Brand, order, offset, limit)

			camera_brands, laptop_brands = get_brands(session_tmp, Brand)

			return make_response(
				jsonify(
					{
						"message": "done",
						"data": {
							"products": get_data_with_page(products, limit, page, total_count),
							"camera_brands": camera_brands,
							"laptop_brands": laptop_brands
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


class ProductWithBrandId(Resource):
	def get(self, brand_id):
		session_tmp = session()
		parameters = request.args
		limit, page, offset, order = get_default(
			parameters, Product.__table__.columns, Product
		)
		try:
			products, total_count = get_products(session_tmp, parameters, Product, Brand, order, offset, limit, brand_id)

			camera_brands, laptop_brands = get_brands(session_tmp, Brand)

			return make_response(
				jsonify(
					{
						"message": "done",
						"data": {
							"products": get_data_with_page(products, limit, page, total_count),
							"camera_brands": camera_brands,
							"laptop_brands": laptop_brands
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
						"data": []
					}
				), 500
			)
		finally:
			session_tmp.close()


class ProductWithProductId(Resource):
	def get(self, product_id):
		session_tmp = session()
		try:
			return make_response(
				jsonify(
					{
						"message": "done",
						"data": get_product(session_tmp, Product, Brand, product_id)
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


class Camera(Resource):
	def get(self):
		session_tmp = session()
		try:
			brand_with_products = get_cameras_or_laptops(session_tmp, True)
			return make_response(
				jsonify(
					{
						"message": "done",
						"data": brand_with_products
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


class Laptop(Resource):
	def get(self):
		session_tmp = session()
		try:
			brand_with_products = get_cameras_or_laptops(session_tmp, False)
			return make_response(
				jsonify(
					{
						"message": "done",
						"data": brand_with_products
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
