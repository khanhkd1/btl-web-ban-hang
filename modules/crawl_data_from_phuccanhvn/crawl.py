import requests as requests
import json


def get_items(curl):
    res = requests.get(curl)
    return res.json()['list']


if __name__ == '__main__':
    camera_curls = ["https://www.phucanh.vn/ajax/get_json.php?action=product&action_type=product-list&type=&collection"
                    "=81sort=order&show=10", "https://www.phucanh.vn/ajax/get_json.php?action=product&action_type"
                    "=product-list&category=736&type=&sort=order&show=6",
                    "https://www.phucanh.vn/ajax/get_json.php"
                    "?action=product&action_type=product-list&category=737&type=&sort=order&show=6", "https://www"
                    ".phucanh.vn/ajax/get_json.php?action=product&action_type=product-list&category=738&type=&sort"
                                                                                                     "=order&show=6",
                    "https://www.phucanh.vn/ajax/get_json.php?action=product&action_type=product"
                    "-list&category=224&type=&sort=order&show=6", "https://www.phucanh.vn/ajax/get_json.php?action"
                    "=product&action_type=product-list&category=890&type=&sort=order&show=6",
                    "https://www.phucanh.vn"
                    "/ajax/get_json.php?action=product&action_type=product-list&category=895&type=&sort=order&show=6",
                    "https://www.phucanh.vn/ajax/get_json.php?action=product&action_type=product-list&category=169"
                    "&type=&sort=order&show=6"]

    laptop_curls = ["https://www.phucanh.vn/ajax/get_json.php?action=deal&action_type=list&type=started&show=10",
                    "https://www.phucanh.vn/ajax/get_json.php?action=product&action_type=product-list&type"
                    "=&collection=160sort=order&show=10", "https://www.phucanh.vn/ajax/get_json.php?action=product"
                    "&action_type=product-list&category=375&type=&sort=order&show=6", "https://www.phucanh.vn/ajax"
                    "/get_json.php?action=product&action_type=product-list&category=945&type=&sort=order&show=6",
                    "https://www.phucanh.vn/ajax/get_json.php?action=product&action_type=product-list&category=652"
                    "&type=&sort=order&show=6", "https://www.phucanh.vn/ajax/get_json.php?action=product&action_type"
                    "=product-list&category=651&type=&sort=order&show=6", "https://www.phucanh.vn/ajax/get_json.php"
                    "?action=product&action_type=product-list&category=814&type=&sort=order&show=6", "https://www"
                    ".phucanh.vn/ajax/get_json.php?action=product&action_type=product-list&category=815&type=&sort"
                    "=order&show=6", "https://www.phucanh.vn/ajax/get_json.php?action=product&action_type=product"
                    "-list&category=726&type=&sort=order&show=6", "https://www.phucanh.vn/ajax/get_json.php?action"
                    "=product&action_type=product-list&category=629&type=&sort=order&show=6", "https://www.phucanh.vn"
                    "/ajax/get_json.php?action=product&action_type=product-list&category=1126&type=&sort=order&show=6"]

    cameras = []
    laptops = []
    for curl in camera_curls:
        print(len(get_items(curl)))
        cameras += get_items(curl)

    with open('data_camera.json', 'w') as outfile:
        json.dump(cameras, outfile)

    for curl in laptop_curls:
        print(len(get_items(curl)))
        laptops += get_items(curl)

    with open('data_laptop.json', 'w') as outfile:
        json.dump(laptops, outfile)
