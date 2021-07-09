from libraries.connect_database import connect_database, User, Product, Cart, Favorite, Bank, BankOfUser, Address, \
    Payment, PaymentType, Brand, VisitsLog
from sqlalchemy import or_, func
from sqlalchemy.ext.declarative import DeclarativeMeta
import random
import json
from datetime import date, timedelta


def get_default(parameters, metadata, obj):
    if ('orderBy' or 'orderType') not in parameters:
        order = obj.id.asc()
    else:
        try:
            if parameters['orderType'] == 'desc':
                order = metadata[parameters['orderBy']].desc()
            else:
                order = metadata[parameters['orderBy']].asc()
        except:
            order = obj.id.asc()
    if 'limit' not in parameters:
        limit = 20
    else:
        try:
            limit = int(parameters['limit'])
        except:
            limit = 20
    if 'page' not in parameters:
        page = 1
    else:
        try:
            page = int(parameters['page'])
        except:
            page = 1
    offset = (page - 1) * limit

    return limit, page, offset, order


def standardized_data(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                json.dumps(data)  # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields
    return json.JSONEncoder.default(obj)


def process_data(data, session_tmp, obj, is_brand):
    if data is None:
        return None
    if is_brand:
        return standardized_data(data)
    data = standardized_data(data)
    data['images'] = data['images'].split(',')
    data['brand'] = session_tmp.query(obj).filter_by(id=data['brand_id']).first().brand
    return data


def get_data_with_page(data, page_limit, current_page, total):
    result = {'data': data, 'paging': {'total_count': total}}

    if int(result['paging']['total_count']) % int(page_limit) == 0:
        total_page = int(result['paging']['total_count']) // int(page_limit)
    else:
        total_page = (int(result['paging']['total_count']) // int(page_limit)) + 1

    if current_page < int(total_page):
        result['paging']['records_in_page'] = page_limit
    else:
        result['paging']['records_in_page'] = int(result['paging']['total_count']) - (
                int(current_page) - 1) * page_limit

    result['paging']['total_page'] = total_page
    result['paging']['current_page'] = int(current_page)

    return result


def check_search(query, parameters, obj):
    if "search" in parameters and parameters['search'] != "":
        search_values = parameters['search'].split(",")
        for search_value in search_values:
            query = query.filter(or_(key.like('%' + search_value + '%') for key in obj.__table__.columns))
    return query


def get_brands(session):
    brands = session.query(Brand)
    brands = brands.all()

    camera_brands = []
    laptop_brands = []

    for i in range(len(brands)):
        brands[i] = process_data(brands[i], None, None, True)
        if brands[i]['is_laptop']:
            laptop_brands.append(brands[i])
        else:
            camera_brands.append(brands[i])
    return camera_brands, laptop_brands


def get_products(session, parameters, order, offset, limit, brand_id=False):
    if not brand_id:
        products = session.query(Product)
    else:
        products = session.query(Product).filter_by(brand_id=brand_id)
    products = check_search(products, parameters, Product)
    total_count = products.count()
    products = products.order_by(order).offset(offset).limit(limit).all()

    for i in range(len(products)):
        products[i] = process_data(products[i], session, Brand, False)
    return products, total_count


def get_product(session, product_id):
    product = session.query(Product).filter_by(id=product_id).first()
    return process_data(product, session, Brand, False)


def get_carts_or_favorites(session, obj, user_id):
    objs = session.query(obj).filter_by(user_id=user_id).all()
    for i in range(len(objs)):
        objs[i] = standardized_data(objs[i])
        objs[i]['product'] = {}
        product = session.query(Product).filter_by(id=objs[i]['product_id']).first()
        objs[i]['product']['name'] = product.productName
        objs[i]['product']['image'] = random.choice(product.images.split(','))
        objs[i]['product']['price'] = product.price
        del objs[i]['registry']
    return objs


def get_carts(session, user_id):
    return get_carts_or_favorites(session, Cart, user_id)


def get_favorites(session, user_id):
    return get_carts_or_favorites(session, Favorite, user_id)


def get_banks_of_user(session, user_id):
    banks_of_user = session.query(BankOfUser).filter_by(user_id=user_id).all()
    for i in range(len(banks_of_user)):
        banks_of_user[i] = standardized_data(banks_of_user[i])
        banks_of_user[i]['full_name'] = session.query(User).filter_by(
            id=banks_of_user[i]['user_id']).first().full_name
        banks_of_user[i]['bank_name'] = session.query(Bank).filter_by(
            id=banks_of_user[i]['bank_id']).first().bank_name
        del banks_of_user[i]['registry']
    return banks_of_user


def get_user_by_id(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        return None
    user = standardized_data(user)
    user['carts'] = get_carts(session, user_id)
    user['favorites'] = get_favorites(session, user_id)
    user['banks'] = get_banks_of_user(session, user_id)
    user['addresses'] = get_addresses(session, user_id)
    user['payments'] = get_payments(session, user_id)
    for field_name in ['bank', 'check_password', 'set_password', 'registry', 'product', 'password']:
        try:
            del user[field_name]
        except:
            continue
    return user


def get_banks(session):
    banks = session.query(Bank).all()
    for i in range(len(banks)):
        banks[i] = standardized_data(banks[i])
        del banks[i]['registry'], banks[i]['user']
    return banks


def process_products(products, session):
    products = products.split('-')
    for i in range(len(products)):
        products[i] = products[i].replace('[', '').replace(']', '').split(',')
        if products[i][0] == '':
            continue
        products[i] = {
            'productName': session.query(Product).filter_by(id=int(products[i][0])).first().productName.strip(),
            'amount': int(products[i][1].strip()),
            'total_price': float(products[i][2].strip())
        }
    return products


def get_payments(session, user_id):
    payments = session.query(Payment).filter_by(user_id=user_id).all()
    for i in range(len(payments)):
        payments[i] = standardized_data(payments[i])
        payments[i]['products'] = process_products(payments[i]['products'], session)
        payments[i]['payment_type'] = session.query(PaymentType).filter_by(
            id=payments[i]['payment_type_id']).first().name
        address = standardized_data(session.query(Address).filter_by(id=payments[i]['address_id']).first())
        del address['registry']
        payments[i]['address'] = address
        del payments[i]['registry']
    return payments


def get_addresses(session, user_id):
    addresses = session.query(Address).filter_by(user_id=user_id).all()
    for i in range(len(addresses)):
        addresses[i] = standardized_data(addresses[i])
        del addresses[i]['registry']
    return addresses


def get_cameras_or_laptops(session, is_camera):
    brands = session.query(Brand).filter_by(is_camera=is_camera).all()
    for i in range(len(brands)):
        brands[i] = standardized_data(brands[i])
        del brands[i]['is_camera']
        del brands[i]['is_laptop']
        brands[i]['products'] = []
        products = session.query(Product).filter_by(brand_id=brands[i]['id']).all()
        for j in range(len(products)):
            brands[i]['products'].append(process_data(products[j], session, Brand, False))
    return brands


def get_payment_types(session):
    payment_types = session.query(PaymentType).all()
    for i in range(len(payment_types)):
        payment_types[i] = standardized_data(payment_types[i])
        del payment_types[i]['registry']
    return payment_types


def get_visitors(session):
    visitors = {}
    for i in range(5):
        visitors[str(date.today() - timedelta(days=i))] = session.query(VisitsLog).filter_by(
            date=str(date.today() - timedelta(days=i))).all()
    for key in visitors.keys():
        for i in range(len(visitors[key])):
            visitors[key][i] = standardized_data(visitors[key][i])
            del visitors[key][i]['registry']
    return visitors
