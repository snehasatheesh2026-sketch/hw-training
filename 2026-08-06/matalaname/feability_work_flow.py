##############################CRAWLER##############################

params = {'product_version': '2035',
 'query': 'query GetProductList($filter: ProductAttributeFilterInput, $pageSize: Int, $currentPage: Int, $sort: ProductAttributeSortInput) {\n  products(\n    filter: $filter\n    pageSize: $pageSize\n    currentPage: $currentPage\n    sort: $sort\n  ) {\n    total_count\n    aggregations {\n      count\n      attribute_code\n      label\n      __typename\n      options {\n        count\n        label\n        value\n        color_code\n        __typename\n      }\n    }\n    page_info {\n      current_page\n      page_size\n      total_pages\n      __typename\n    }\n    items {\n      id\n      sku\n      name\n      url_key\n      brand_name\n      home_delivery\n      store_pickup\n      color_label {\n        color_label\n        background_color_label\n        __typename\n      }\n      product_label\n      stock_status\n      is_new\n      is_bestseller\n      is_featured\n      __typename\n      hover_image\n      rating_aggregation_value\n      image {\n        label\n        __typename\n      }\n      thumbnail {\n        url\n        label\n        __typename\n      }\n      categories {\n        id\n        name\n        __typename\n      }\n      price_range {\n        minimum_price {\n          regular_price {\n            value\n            currency\n            __typename\n          }\n          final_price {\n            value\n            currency\n            __typename\n          }\n          discount {\n            amount_off\n            percent_off\n            __typename\n          }\n          __typename\n        }\n        maximum_price {\n          regular_price {\n            value\n            currency\n            __typename\n          }\n          final_price {\n            value\n            currency\n            __typename\n          }\n          discount {\n            amount_off\n            percent_off\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n}',
 'operationName': 'GetProductList',
 'variables': '{"filter":{"category_uid":{"in":["MTk2NA=="]}},"pageSize":40,"currentPage":3,"sort":{}}'}

headers = {
}

# import json
import requests

import json

url = "https://api.bfab.com/graphql"

params = params


# Convert JSON string to Python dict
variables = json.loads(params["variables"])

# Change category ID
# variables["filter"]["category_uid"]["in"] = ["NEW_CATEGORY_UID"]

# Change page number
variables["currentPage"] = 3

#
# Convert back to JSON string
params["variables"] = json.dumps(variables)


response = requests.get(url, params=params, headers= headers)

data = response.json()

products = data.get('data',"").get('products',"").get("items","")

print(len(products))


for product in products:

    name = product.get('name')

    brand_name = product.get('brand_name','')

    sku = product.get('sku','')

    product_id = product.get("id","")

    url = product.get('url_key','')

    product_availibity = product.get("stock_status","")

    bread_crambes = product.get('categories','')

    print(url)

##############################PARSER##############################


import requests



params = {
    'product_version': '2035',
}

json_data = {
    'operationName': 'GetProductDetailVariants',
    'variables': {
        'url_key': 'papaya-crinkle-jumpsuit',
    },
    'query': 'query GetProductDetailVariants($url_key: String!) {\n  products(filter: {url_key: {eq: $url_key}}) {\n    items {\n      ... on ConfigurableProduct {\n        variants {\n          product {\n            swatch_image\n            id\n            url_key\n            home_delivery\n            store_pickup\n            media_gallery {\n              url\n              label\n              __typename\n            }\n            name\n            sku\n            product_custom_attributes\n            qty_left_in_stock\n            stock_status\n            color_label {\n              color_label\n              background_color_label\n              __typename\n            }\n            product_label\n            is_new\n            is_bestseller\n            is_featured\n            price_range {\n              minimum_price {\n                discount {\n                  amount_off\n                  percent_off\n                  __typename\n                }\n                final_price {\n                  currency\n                  value\n                  __typename\n                }\n                regular_price {\n                  currency\n                  value\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            attribute_set_id\n            __typename\n          }\n          attributes {\n            label\n            code\n            value_index\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
}

# json_data['variables']['url_key'] = url
response = requests.post('https://api.bfab.com/graphql', params=params, headers=headers, json=json_data)

data = response.json()


items = data.get("data", {}).get("products", {}).get("items", [])

for item in items:

    variants = item.get("variants", [])

    sizes = []
    colors = []

    # Collect all sizes and colors
    for variant in variants:

        for attr in variant.get("attributes", []):

            if attr.get("code") == "size":
                sizes.append(attr.get("label"))

            elif attr.get("code") == "color":
                colors.append(attr.get("label"))

    # Remove duplicate colors
    colors = list(dict.fromkeys(colors))

    # Use the first variant for product details
    product = variants[0].get("product", {})

    url = product.get("url_key", "")
    product_id = product.get("id", "")
    images = product.get("media_gallery", [])
    name = product.get("name", "")

    selling_price = (
        product.get("price_range", {})
        .get("minimum_price", {})
        .get("final_price", {})
        .get("value", "")
    )

    currency = (
        product.get("price_range", {})
        .get("minimum_price", {})
        .get("final_price", {})
        .get("currency", "")
    )

    regular_price = (
        product.get("price_range", {})
        .get("minimum_price", {})
        .get("regular_price", {})
        .get("value", "")
    )

    attrs = json.loads(product.get("product_custom_attributes", "[]"))

    gender = ""
    description = ""
    details = {}

    for section in attrs:

        if section.get("title") == "Specifications":

            for spec in section.get("children", []):

                details[spec["label"]] = spec["value"]

                if spec["label"] == "Gender":
                    gender = spec["value"]

        elif section.get("title") == "Description":

            description = section.get("value", "")











