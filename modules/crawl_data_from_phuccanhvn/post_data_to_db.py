from libraries.connect_database import connect_database, Brand, Product
from sqlalchemy import exc
import json

session = connect_database()


def post_a_product(data, is_laptop, is_camera):
    session_tmp = session()
    # check brand da co chua
    brand = session_tmp.query(Brand).filter_by(brand=data['brand']['name']).first()
    if not brand:
        brand = Brand(
            id=int(data['brand']['id']),
            brand=data['brand']['name'],
            is_laptop=is_laptop,
            is_camera=is_camera
        )
        session_tmp.add(brand)
        try:
            session_tmp.commit()
        except exc as e:
            session_tmp.rollback()

    product = Product(
        id=int(data['productId']),
        brand=int(data['brand']['id']),
        productName=data['productName'],
        quantity=int(data['quantity']),
        price=float(data['price']),
        productSummary=data['productSummary'],
        warranty=data['warranty'],
        images=','.join([x['image']['original'] for x in data['imageCollection']])
    )
    session_tmp.add(product)
    try:
        session_tmp.commit()
    except exc as e:
        session_tmp.rollback()
        return 'error'
    finally:
        session_tmp.close()
    return 'done'


if __name__ == '__main__':
    with open('data_laptop.json') as f:
        laptops = json.load(f)
    with open('data_camera.json') as f:
        cameras = json.load(f)

    for i in range(len(laptops)):
        try:
            print(post_a_product(laptops[i], is_laptop=True, is_camera=False))
        except Exception as e:
            print(e)

    for i in range(len(cameras)):
        try:
            print(post_a_product(cameras[i], is_laptop=False, is_camera=True))
        except Exception as e:
            print(e)
