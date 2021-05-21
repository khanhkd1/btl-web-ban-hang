
from libraries.connect_database import connect_database, Laptop, LaptopBrand
from libraries.libraries import get_default, standardized_data
from flask_restful import Resource
from flask import request
from sqlalchemy import or_, exc

session = connect_database()


class LaptopWithoutId(Resource):
    def get(self):
        try:
            session_tmp = session()
            parameters = request.args
            limit, page, offset, order = get_default(
                parameters, Laptop.__table__.columns, Laptop
            )
            query = session_tmp.query(Laptop)
            if "search" in parameters and parameters['search'] != "":
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    query = query.filter(or_(key.like('%' + search_value + '%') for key in Laptop.__table__.columns))
            # total_count = query.count()
            records = query.order_by(order).offset(offset).limit(limit).all()
            for i in range(len(records)):
                records[i] = standardized_data(records[i])
                records[i]['images'] = records[i]['images'].split(',')
                records[i]['brand'] = session_tmp.query(LaptopBrand).filter_by(id=records[i]['brand']).first().brand
            return records
        except exc as e:
            session_tmp.rollback()
            return []
        finally:
            session_tmp.close()
