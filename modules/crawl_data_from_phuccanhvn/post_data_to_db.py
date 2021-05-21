from libraries.connect_database import connect_database, Camera, CameraBrand, LaptopBrand, Laptop
from sqlalchemy import exc
import json

session = connect_database()


def post_a_camera(data):
    session_tmp = session()
    # check brand da co chua
    camera_brand = session_tmp.query(CameraBrand).filter_by(brand=data['brand']['name']).first()
    if not camera_brand:
        camera_brand = CameraBrand(
            id=int(data['brand']['id']),
            brand=data['brand']['name']
        )
        session_tmp.add(camera_brand)
        try:
            session_tmp.commit()
        except exc as e:
            session_tmp.rollback()

    camera = Camera(
        id=int(data['productId']),
        brand=int(data['brand']['id']),
        productName=data['productName'],
        quantity=int(data['quantity']),
        price=float(data['price']),
        productSummary=data['productSummary'],
        warranty=data['warranty'],
        images=','.join([x['image']['original'] for x in data['imageCollection']])
    )
    session_tmp.add(camera)
    try:
        session_tmp.commit()
    except exc as e:
        session_tmp.rollback()
        return 'error'
    finally:
        session_tmp.close()
    return 'done'


def post_a_laptop(data):
    session_tmp = session()
    # check brand da co chua
    laptop_brand = session_tmp.query(LaptopBrand).filter_by(brand=data['brand']['name']).first()
    if not laptop_brand:
        laptop_brand = LaptopBrand(
            id=int(data['brand']['id']),
            brand=data['brand']['name']
        )
        session_tmp.add(laptop_brand)
        try:
            session_tmp.commit()
        except exc as e:
            session_tmp.rollback()

    laptop = Laptop(
        id=int(data['productId']),
        brand=int(data['brand']['id']),
        productName=data['productName'],
        quantity=int(data['quantity']),
        price=float(data['price']),
        productSummary=data['productSummary'],
        warranty=data['warranty'],
        images=','.join([x['image']['original'] for x in data['imageCollection']])
    )
    session_tmp.add(laptop)
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
        data = json.load(f)
    for i in range(len(data)):
        try:
            print(post_a_laptop(data[i]))
        except:
            print('duplicate key')
