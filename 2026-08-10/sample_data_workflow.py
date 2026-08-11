import json
import requests
import csv
from urllib.parse import urljoin
from settings import (
    HEADERS,
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    BASE_URL,
)

collection = client[ MONGO_DB][ MONGO_COLLECTION_CATEGORY]
categories = [
    {
        "url": "https://www.matalanme.com/ae_en/women/dresses/casual-dresses",
        "uid": "MTky"
    },
    {
        "url": "https://www.matalanme.com/ae_en/women/lingerie-and-hosiery/socks-and-hosiery",
        "uid": "MjA0"
    },
    {
        "url": "https://www.matalanme.com/ae_en/women/bottoms/jeans-and-jeggings",
        "uid": "MTg4"
    },
    {"url":"https://www.matalanme.com/bh_en/women/bottoms/shorts",
      "uid": "MTg2"
      }
]

json_data = {
    'operationName': 'GetProductDetailVariants',
    'variables': {
        'url_key': 'rosie-light-wash-pull-on-jeggings',
    },
    'query': 'query GetProductDetailVariants($url_key: String!) {\n  products(filter: {url_key: {eq: $url_key}}) {\n    items {\n      ... on ConfigurableProduct {\n        variants {\n          product {\n            swatch_image\n            id\n            url_key\n            home_delivery\n            store_pickup\n            media_gallery {\n              url\n              label\n              __typename\n            }\n            name\n            sku\n            product_custom_attributes\n            qty_left_in_stock\n            stock_status\n            color_label {\n              color_label\n              background_color_label\n              __typename\n            }\n            product_label\n            is_new\n            is_bestseller\n            is_featured\n            price_range {\n              minimum_price {\n                discount {\n                  amount_off\n                  percent_off\n                  __typename\n                }\n                final_price {\n                  currency\n                  value\n                  __typename\n                }\n                regular_price {\n                  currency\n                  value\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            attribute_set_id\n            __typename\n          }\n          attributes {\n            label\n            code\n            value_index\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
}

json_data_copy = json_data.copy()
API_URL = "https://api.bfab.com/graphql"

headers =  {
    
}


params = {
    "product_version": "2035",
    "query": """query GetProductList(
        $filter: ProductAttributeFilterInput,
        $pageSize: Int,
        $currentPage: Int,
        $sort: ProductAttributeSortInput
    ) {
        products(
            filter: $filter
            pageSize: $pageSize
            currentPage: $currentPage
            sort: $sort
        ) {
            total_count

            page_info {
                current_page
                page_size
                total_pages
            }

            items {
                id
                sku
                name
                url_key
                brand_name
                home_delivery
                store_pickup
                product_label
                stock_status
                is_new
                is_bestseller
                is_featured
                hover_image
                rating_aggregation_value

                thumbnail {
                    url
                    label
                }

                categories {
                    id
                    name
                }

                price_range {
                    minimum_price {
                        regular_price {
                            value
                            currency
                        }
                        final_price {
                            value
                            currency
                        }
                        discount {
                            amount_off
                            percent_off
                        }
                    }
                }
            }
        }
    }""",

    "operationName": "GetProductList",

    "variables": json.dumps({
        "filter": {
            "category_uid": {
                "in": ["MTky"]
            }
        },
        "pageSize": 40,
        "currentPage": 1,
        "sort": {}
    })
}


all_products = []

seen_skus = set()

csv_file = open(
    "products.csv",
    "w",
    newline="",
    encoding="utf-8"
)

writer = csv.writer(csv_file)

writer.writerow([
    "product_id",
    "url",
    "name",
  
])



all_products = []
seen_skus = set()
seen_urls = set()

csv_file = open(
    "products.csv",
    "w",
    newline="",
    encoding="utf-8"
)

writer = csv.writer(csv_file)

writer.writerow([
    "product_id",
    "url",
    "name",
])
from datetime import datetime

extraction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for category in categories:

    print(f"\nProcessing: {category['url']}")
    print(f"UID: {category['uid']}")

    variables = json.loads(params["variables"])
    variables["filter"]["category_uid"]["in"] = [category["uid"]]

    current_page = 1

    while True:
        variables["currentPage"] = current_page
        params["variables"] = json.dumps(variables)

        response = requests.get(
            API_URL,
            params=params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            products_data = data.get("data", {}).get("products", {})
            products = products_data.get("items", [])

            page_info = products_data.get("page_info", {})
            total_pages = page_info.get("total_pages", 0)
            current = page_info.get("current_page", current_page)

            print(
                f"Page {current}/{total_pages} | "
                f"Products: {len(products)}"
            )

            for product in products:
                url_key = product.get('url_key', '')
                product_id = product.get('id', '')

                if not url_key:
                    continue

                check_url = urljoin(BASE_URL, url_key)

                if check_url in seen_urls:
                    print("POST failed | Duplicate URL skipped")
                    continue
                seen_urls.add(check_url)

                categories_list = product.get("categories", [])
                breadcrumb_names = []
                for cat in categories_list:
                    name = cat.get("name", "").strip()
                    if name and name not in breadcrumb_names:
                        breadcrumb_names.append(name)
                
                product_names = product.get("name", "").strip()
                if product_names:
                    breadcrumb_names.append(product_names)
                    breadcrumbs = " > ".join(breadcrumb_names)
                else:
                    breadcrumbs = ""

                json_data_copy = json_data.copy()
                json_data_copy['variables'] = {'url_key': url_key}

                rs = requests.post(API_URL, json=json_data_copy, headers=headers)

                if rs.status_code == 200:
                    data = rs.json()
                    items = data.get("data", {}).get("products", {}).get("items", [])

                    for item in items:
                        variants = item.get("variants", [])
                        if not variants:
                            continue

                        sizes = []
                        colors = []
                        # for variant in variants:
                        #     for attr in variant.get("attributes", []):
                        #         if attr.get("code") == "size" or "size_length":
                        #             sizes.append(attr.get("label"))
                        #         elif attr.get("code") == "color":
                        #             colors.append(attr.get("label"))
                        for variant in variants:
                            for attr in variant.get("attributes", []):
                                if attr.get("code") in ("size", "size_length"):
                                    sizes.append(attr.get("label"))
                                elif attr.get("code") == "color":
                                    colors.append(attr.get("label"))




                        
                        sizes = ",".join(sizes)
                        colors = ",".join(list(dict.fromkeys(colors)))

                        prod_variant = variants[0].get("product", {})
                        name = prod_variant.get("name", "")
                        print(name)
                        quantity = prod_variant.get("qty_left_in_stock",'')
                        stock_status = prod_variant.get("stock_status","")
                        product_id = prod_variant.get("id", "")
                        url = prod_variant.get("url_key", "")
                        full_url = urljoin(BASE_URL, url) if url else check_url

                        selling_price = (
                            prod_variant.get("price_range", {})
                            .get("minimum_price", {})
                            .get("final_price", {})
                            .get("value", "")
                        )

                        currency = (
                            prod_variant.get("price_range", {})
                            .get("minimum_price", {})
                            .get("final_price", {})
                            .get("currency", "")
                        )
                        if not currency:
                            currency = (
                                prod_variant.get("price_range", {})
                                .get("minimum_price", {})
                                .get("regular_price", {})
                                .get("currency", "")
                            )

                        regular_price = (
                            prod_variant.get("price_range", {})
                            .get("minimum_price", {})
                            .get("regular_price", {})
                            .get("value", "")
                        )
                        extraction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                        selling_price = selling_price if selling_price else regular_price
                        media_gallery = prod_variant.get("media_gallery", [])

                        images = []
                        for image in media_gallery:
                            image_url = image.get("url", "")
                            if image_url:
                                images.append(image_url)
                        images = list(dict.fromkeys(images))
                        images_string = ", ".join(images)
                        attrs = json.loads(prod_variant.get("product_custom_attributes", "[]"))

                        gender = ""
                        description = ""
                        details = {}
                        for section in attrs:
                            if section.get("title") == "Specifications":
                                for spec in section.get("children", []):
                                    details[spec["label"]] = spec["value"]
                                    if spec["label"] == "Gender":
                                        gender = spec["value"] or ""
                            elif section.get("title") == "Description":
                                description = section.get("value", "")
                        
                        details_string = ", ".join(
                            f'"{key}": "{value}"'
                            for key, value in details.items()
                        ) or ""

                        if not name:
                            continue

                        db_item = {
                            "product_name": name,
                            "colors": colors,
                            "quantity":quantity,
                            "sizes": sizes,
                            "url": full_url,
                            "images": images_string,
                            "product_id": product_id,
                            "sellings_price": selling_price,
                            "currency": currency,
                            "regular_price": regular_price,
                            "gender": gender or "",
                            "product_details": details_string,
                            "breadcrumb": breadcrumbs,
                            "description": description,
                            "extraction_date" : extraction_date ,

                        }
                        
                        collection.insert_one(db_item)
                        writer.writerow([product_id, full_url, name])
                        print(full_url, name)

        if current_page >= total_pages:
            break

        current_page += 1

csv_file.close()
print("\n====================")
print(f"Total products processed.")