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
        limit = 10
    else:
        try:
            limit = int(parameters['limit'])
        except:
            limit = 10
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
    if is_brand:
        return standardized_data(data)
    data = standardized_data(data)
    data['images'] = data['images'].split(',')
    data['brand'] = session_tmp.query(obj).filter_by(id=data['brand']).first().brand
    return data
