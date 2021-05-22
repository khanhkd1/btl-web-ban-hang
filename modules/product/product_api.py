
from libraries.connect_database import connect_database, Product, Brand
from libraries.libraries import get_default, process_data, get_data_with_page
from flask_restful import Resource
from flask import request, jsonify, make_response
from sqlalchemy import or_, exc

session = connect_database()


class AllProduct(Resource):
    def get(self):
        session_tmp = session()
        parameters = request.args
        limit, page, offset, order = get_default(
            parameters, Product.__table__.columns, Product
        )
        try:
            products = session_tmp.query(Product)
            if "search" in parameters and parameters['search'] != "":
                search_values = parameters['search'].split(",")
                for search_value in search_values:
                    products = products.filter(or_(key.like('%' + search_value + '%') for key in Product.__table__.columns))
            total_count = products.count()
            products = products.order_by(order).offset(offset).limit(limit).all()

            for i in range(len(products)):
                products[i] = process_data(products[i], session_tmp, Brand, False)

            brands = session_tmp.query(Brand)
            brands = brands.all()

            camera_brands = []
            laptop_brands = []
            for i in range(len(brands)):
                brands[i] = process_data(brands[i], None, None, True)
                if brands[i]['is_laptop']:
                    laptop_brands.append(brands[i])
                else:
                    camera_brands.append(brands[i])

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
                        "message": "fail",
                        "data": []
                    }
                ), 500
            )
        finally:
            session_tmp.close()


# class AllCamera(Resource):
#     def get(self):
#         session_tmp = session()
#         parameters = request.args
#         limit, page, offset, order = get_default(
#             parameters, Product.__table__.columns, Product
#         )
#         try:
#             query = session_tmp.query(Product)
#             if "search" in parameters and parameters['search'] != "":
#                 search_values = parameters['search'].split(",")
#                 for search_value in search_values:
#                     query = query.filter(or_(key.like('%' + search_value + '%') for key in Product.__table__.columns))
#             # total_count = query.count()
#             records = query.order_by(order).offset(offset).limit(limit).all()
#             for i in range(len(records)):
#                 records[i] = process_data(records[i], session_tmp, Brand, False)
#             return make_response(
#                 jsonify(
#                     {
#                         "message": "done",
#                         "data": records
#                     }
#                 ), 200
#             )
#         except exc as e:
#             session_tmp.rollback()
#             return make_response(
#                 jsonify(
#                     {
#                         "message": "fail",
#                         "data": []
#                     }
#                 ), 500
#             )
#         finally:
#             session_tmp.close()
