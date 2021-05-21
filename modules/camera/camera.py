
from libraries.connect_database import connect_database, Camera, CameraBrand
from libraries.libraries import get_default, standardized_data
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import or_, exc

session = connect_database()


class CameraWithoutId(Resource):
    def get(self):
        session_tmp = session()
        parameters = request.args
        limit, page, offset, order = get_default(
            parameters, Camera.__table__.columns, Camera
        )
        try:
            query = session_tmp.query(Camera)
            if "search" in parameters and parameters['search'] != "":
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    query = query.filter(or_(key.like('%' + search_value + '%') for key in Camera.__table__.columns))
            # total_count = query.count()
            records = query.order_by(order).offset(offset).limit(limit).all()
            for i in range(len(records)):
                records[i] = standardized_data(records[i])
                records[i]['images'] = records[i]['images'].split(',')
                records[i]['brand'] = session_tmp.query(CameraBrand).filter_by(id=records[i]['brand']).first().brand
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": records
                    }
                ), 200
            )
        except exc as e:
            session_tmp.rollback()
            return make_response(
                jsonify(
                    {
                        "message": "fail",
                        "data": []
                    }
                ), 500
            )
        finally:
            session_tmp.close()


class CameraBrandWithoutId(Resource):
    def get(self):
        session_tmp = session()
        try:
            query = session_tmp.query(CameraBrand)
            records = query.all()
            for i in range(len(records)):
                records[i] = standardized_data(records[i])
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": records
                    }
                ), 200
            )
        except exc as e:
            session_tmp.rollback()
            return make_response(
                jsonify(
                    {
                        "message": "fail",
                        "data": []
                    }
                ), 500
            )
        finally:
            session_tmp.close()


class CameraWithBrandId(Resource):
    def get(self, brand_id):
        session_tmp = session()
        try:
            query = session_tmp.query(Camera).filter_by(brand=brand_id)
            records = query.all()
            for i in range(len(records)):
                records[i] = standardized_data(records[i])
            return make_response(
                jsonify(
                    {
                        "message": "done",
                        "data": records
                    }
                ), 200
            )
        except exc as e:
            session_tmp.rollback()
            return make_response(
                jsonify(
                    {
                        "message": "fail",
                        "data": []
                    }
                ), 500
            )
        finally:
            session_tmp.close()
