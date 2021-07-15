from libraries.connect_database import connect_database, Product, Brand
from libraries.libraries import get_default, get_data_with_page, get_brands, get_products, get_cameras_or_laptops, get_product
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import exc
import requests
from base64 import b64encode

session = connect_database()


class Home(Resource):
	def get(self):
		session_tmp = session()
		parameters = request.args
		limit, page, offset, order = get_default(
			parameters, Product.__table__.columns, Product
		)
		try:
			products, total_count = get_products(session_tmp, parameters, order, offset, limit)

			camera_brands, laptop_brands = get_brands(session_tmp)

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


class ProductWithProductId(Resource):
	def __init__(self):
		self.session = session()

	def get(self, product_id):
		product = get_product(self.session, product_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": product
				}
			), 200
		)

	def put(self, product_id):
		data = request.get_json()
		self.session.query(Product).filter_by(id=product_id).update(date)
		self.session.commit()
		product = get_product(self.session, product_id)
		self.session.close()
		return make_response(
			jsonify(
				{
					"message": "done",
					"data": product
				}
			), 200
		)


class ProductWithoutProductId(Resource):
	def __init__(self):
		self.session = session()

	def post(self):
		img_1 = requests.post(
			'https://api.imgur.com/3/upload',
			headers={'Authorization': 'Bearer ' + 'a87898db9b7f3ef7b996ee0008773554a2fa3fa6',},
			data={
				'image': b64encode(request.files['img_1'].read()),
				'type': 'base64'
			}
		).json()['data']['link']

		img_2 = requests.post(
			'https://api.imgur.com/3/upload',
			headers={'Authorization': 'Bearer ' + 'a87898db9b7f3ef7b996ee0008773554a2fa3fa6',},
			data={
				'image': b64encode(request.files['img_2'].read()),
				'type': 'base64'
			}
		).json()['data']['link']

		try:
			product = Product(
				brand_id=int(request.form['brand_id']),
				productName=request.form['productName'],
				quantity=int(request.form['quantity']),
				price=float(request.form['price']),
				productSummary=request.form['productSummary'],
				warranty=request.form['warranty'],
				images=f'{img_1},{img_2}'
			)
			self.session.add(product)
			self.session.flush()
			product_id = product.id
			self.session.commit()

			return make_response(
				jsonify(
					{
						"message": "done",
						"product_id": product_id
					}
				), 200
			)
		except:
			self.session.rollback()
			return make_response(
				jsonify(
					{
						"message": "fail",
					}
				), 500
			)
		finally:
			self.session.close()



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
