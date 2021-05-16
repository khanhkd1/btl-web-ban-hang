from libraries.connect_database import connect_database, Camera
from libraries.libraries import get_default, standardized_data
from flask_restful import Resource
from flask import request
from sqlalchemy import or_

session = connect_database()


class CameraWithoutId(Resource):
    def get(self):
        session_tmp = session()
        parameters = request.args
        limit, page, offset, order = get_default(
            parameters, Camera.__table__.columns, Camera
        )
        query = session_tmp.query(Camera)
        if "search" in parameters and parameters['search'] != "":
            search_values = parameters['search'].split(",")
            for search_value in search_values:
                query = query.filter(or_(key.like('%' + search_value + '%') \
                                         for key in Camera.__table__.columns))
        total_count = query.count()
        records = query.order_by(order).offset(offset).limit(limit).all()
        for i in range(len(records)):
            records[i] = standardized_data(records[i])
        return records
