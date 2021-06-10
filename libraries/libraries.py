from sqlalchemy import or_


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


def standardized_data(obj, del_param=None, param=None):
    data = {}
    try:
        obj = obj.__dict__
    except:
        return None
    try:
        if '_sa_instance_state' in obj:
            del obj["_sa_instance_state"]
    except:
        pass
    if del_param is not None:
        for d in del_param:
            try:
                del obj[d]
            except:
                pass
    if param is not None:
        for p in param:
            data[p] = obj[param[p]]
        return data

    return obj


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


def get_brands(session, brand_obj):
    brands = session.query(brand_obj)
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


def get_products(session, parameters, product_obj, brand_obj, order, offset, limit, brand_id=False):
    if not brand_id:
        products = session.query(product_obj)
    else:
        products = session.query(product_obj).filter_by(brand_id=brand_id)
    products = check_search(products, parameters, product_obj)
    total_count = products.count()
    products = products.order_by(order).offset(offset).limit(limit).all()

    for i in range(len(products)):
        products[i] = process_data(products[i], session, brand_obj, False)
    return products, total_count


def get_product(session, product_obj, brand_obj, product_id):
    product = session.query(product_obj).filter_by(id=product_id).first()
    return process_data(product, session, brand_obj, False)


def get_carts(session, cart_obj, product_obj, user_id):
    carts = session.query(cart_obj).filter_by(user_id=user_id).all()
    for i in range(len(carts)):
        carts[i] = standardized_data(carts[i])
        carts[i]['product'] = session.query(product_obj).filter_by(id=carts[i]['product_id']).first().productName
    return carts


def get_favorites(session, favorite_obj, product_obj, user_id):
    favorites = session.query(favorite_obj).filter_by(user_id=user_id).all()
    for i in range(len(favorites)):
        favorites[i] = standardized_data(favorites[i])
        favorites[i]['product'] = session.query(product_obj).filter_by(id=favorites[i]['product_id']).first().productName
    return favorites


def get_banks_of_user(session, bank_info_obj, user_obj, bank_obj, user_id):
    banks_of_user = session.query(bank_info_obj).filter_by(user_id=user_id).all()
    for i in range(len(banks_of_user)):
        banks_of_user[i] = standardized_data(banks_of_user[i])
        banks_of_user[i]['full_name'] = session.query(user_obj).filter_by(
            id=banks_of_user[i]['user_id']).first().full_name
        banks_of_user[i]['bank_name'] = session.query(bank_obj).filter_by(
            id=banks_of_user[i]['bank_id']).first().bank_name
    return banks_of_user


def get_user_by_id(session, user_obj, user_id):
    user = session.query(user_obj).filter_by(id=user_id).first()
    if user is None:
        return None
    user = standardized_data(user)
    del user['password']
    del user['is_admin']
    del user['id']
    return user


def get_banks(session, bank_obj):
    banks = session.query(bank_obj).all()
    for i in range(len(banks)):
        banks[i] = standardized_data(banks[i])
    return banks


def process_products(products, session, product_obj):
    products = products.split('-')
    for i in range(len(products)):
        products[i] = products[i].replace('[', '').replace(']', '').split(',')
        products[i] = {
            'productName': session.query(product_obj).filter_by(id=int(products[i][0])).first().productName,
            'amount': int(products[i][1]),
            'total_price': float(products[i][2])
        }
    return products


def get_payments(session, payment_obj, product_obj, user_id):
    payments = session.query(payment_obj).filter_by(user_id=user_id).all()
    for i in range(len(payments)):
        payments[i] = standardized_data(payments[i])
        payments[i]['products'] = process_products(payments[i]['products'], session, product_obj)
    return payments


def get_addresses(session, address_obj, user_id):
    addresses = session.query(address_obj).filter_by(user_id=user_id).all()
    for i in range(len(addresses)):
        addresses[i] = standardized_data(addresses[i])
        del addresses[i]['user_id']
    return addresses 


def get_cameras_or_laptops(session, product_obj, brand_obj, is_camera):
    brands = session.query(brand_obj).filter_by(is_camera=is_camera).all()
    for i in range(len(brands)):
        brands[i] = standardized_data(brands[i])
        del brands[i]['is_camera']
        del brands[i]['is_laptop']
        brands[i]['products'] = []
        products = session.query(product_obj).filter_by(brand_id=brands[i]['id']).all()
        for j in range(len(products)):
            brands[i]['products'].append(process_data(products[j], session, brand_obj, False))
    return brands
