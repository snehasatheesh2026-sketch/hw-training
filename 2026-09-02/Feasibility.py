import requests
from parsel import Selector
import json
import re


headers = {
    }

response = requests.get('https://www.zomato.com/kolkata/dominos-pizza-2-bara-bazar/order', headers=headers)


selector = Selector(response.text)
script = selector.xpath(
    '//script[contains(text(), "window.__PRELOADED_STATE__")]/text()'
).get()


match = re.search(
        r'window\.__PRELOADED_STATE__\s*=\s*JSON\.parse\("(.*?)"\);',
        script,
        re.DOTALL
    )

json_string = json.loads('"' + match.group(1) + '"')
data = json.loads(json_string)

products = []

def find_items(data):

    if isinstance(data, dict):

        # Skip modifierGroups completely
        if "modifierGroups" in data:
            data = {
                key: value
                for key, value in data.items()
                if key != "modifierGroups"
            }

        if "item" in data:
            products.append(data["item"])

        for value in data.values():
            find_items(value)

    elif isinstance(data, list):

        for value in data:
            find_items(value)


find_items(data)

print(len(products))

for product in products:
    
    
    unique_id =  product.get('id','')
    
    item_name = product.get('name','')

    product_description = product.get('desc','')

    product_image = product.get('item_image_url','')

    dietary_type = product.get('dietary_slugs','')

    service_availability = product.get('service_slugs','')

