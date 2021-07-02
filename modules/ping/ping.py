from flask_restful import Resource
from flask import jsonify, make_response

class Ping(Resource):
	def get(self):
		return make_response(
			jsonify(
				{
					"message": "ok",
				}
			), 200
		)
