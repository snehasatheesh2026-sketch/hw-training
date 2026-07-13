import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import csv
import re
from unidecode import unidecode


def create_url(name, product_id):

    clean_name = unidecode(name)
    clean_name = clean_name.lower()
    clean_name = re.sub(r'[^a-zA-Z0-9]+', '-', clean_name)
    clean_name = re.sub(r'-+', '-', clean_name)
    clean_name = clean_name.strip('-')

    return f"https://auchan.hu/shop/{clean_name}.p-{product_id}"


class EndCategories:

    def __init__(self):

        self.url = "https://auchan.hu/api/v2/cache/tree/0"

        self.headers  ={
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImI5ZTQxMDkyZDcxOTc5MjU3MmI5MjM0Njg3NTJkMjMwNzQ2ZWFkNjcyOGUxOGFkYWE0N2VjOTFhNGEwYWY1MDkzNjM5ZDczNjFiODNiM2Y4IiwiaWF0IjoxNzgzOTA0NDQ1LjU0MjE5NCwibmJmIjoxNzgzOTA0NDQ1LjU0MjE5NiwiZXhwIjoxNzgzOTkwODQ1LjUxMjc2Mywic3ViIjoiYW5vbl82YzQxYmVkYy0zYTU1LTRlOGQtYjBmNy1lMzk5OTk2YjljYTEiLCJzY29wZXMiOltdfQ.X7GZ_-E4gjss8lDYRDO7rWszxTP8E9Iy1um1zudHZ9h3KfGkyphzOPwpvaps3_807fXgyTBwsqnwrvWHYI9nNv5lMcrlosIUeio7cJG7-IASkfHeAs4NGxN-dPi1eWF7opaWIY-ohLWxUs_zVHMbaMsjCfVKW6ChgufvJcQxbeGkjdHvLoEr1YTfFN5fGe_7SNDqIHO4HKlnUUgbRuDtvLM4OL7wQUoWB1AZgpUXqiKTy8t21lASceaMRwl5CKPeLQsqir-Q5b4KhBixDfVVkmqA1Ll6GF3pdTv7qLKs2PdC506frvi3t-df9WLCieQPhvOepUlz1NSG9YAziua6_w',
    'if-none-match': 'W/"744f5a5060ffe8c07d3fbfb3605b61b1"',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1783904443822_0_3045430_c_75',
    'x-aw-tab-id': '1783904443822_0_3045430',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=8rTeayInSlShC7FBppi2lqxCsBANOUDnNdgHDmVoMUs14RXFwr0YAuHGORPl4aiXuz3kvSWhJVKYnHvIu8iS3x6Q8zZynEll; optiMonkClientId=1b96fb7c-4a6a-2df3-709b-df593b31fbf0; AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; login_type=anon; aw_notification_info=%7B%7D; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImI5ZTQxMDkyZDcxOTc5MjU3MmI5MjM0Njg3NTJkMjMwNzQ2ZWFkNjcyOGUxOGFkYWE0N2VjOTFhNGEwYWY1MDkzNjM5ZDczNjFiODNiM2Y4IiwiaWF0IjoxNzgzOTA0NDQ1LjU0MjE5NCwibmJmIjoxNzgzOTA0NDQ1LjU0MjE5NiwiZXhwIjoxNzgzOTkwODQ1LjUxMjc2Mywic3ViIjoiYW5vbl82YzQxYmVkYy0zYTU1LTRlOGQtYjBmNy1lMzk5OTk2YjljYTEiLCJzY29wZXMiOltdfQ.X7GZ_-E4gjss8lDYRDO7rWszxTP8E9Iy1um1zudHZ9h3KfGkyphzOPwpvaps3_807fXgyTBwsqnwrvWHYI9nNv5lMcrlosIUeio7cJG7-IASkfHeAs4NGxN-dPi1eWF7opaWIY-ohLWxUs_zVHMbaMsjCfVKW6ChgufvJcQxbeGkjdHvLoEr1YTfFN5fGe_7SNDqIHO4HKlnUUgbRuDtvLM4OL7wQUoWB1AZgpUXqiKTy8t21lASceaMRwl5CKPeLQsqir-Q5b4KhBixDfVVkmqA1Ll6GF3pdTv7qLKs2PdC506frvi3t-df9WLCieQPhvOepUlz1NSG9YAziua6_w; refresh_token=def50200e342edc3a8152a98088bc4916b34d0326cb3afc6dd3c881b8558b2db93a638f69bca26525ff5ee5d9820b697b709354af99b3aab7e62d5539edcd9a544166b3e49a16f5e7f3e3b38804700e568dca94748df5f90e71e96c7afd9fbbadd25c3c7031ceb693cdd833841910fef4fe814ffb026ffd69e2664bfebbde758ee52fa7c0e4ad121d6a4426dc1cc32ea1de3b939e44d6f421c168fede9c892ba9f0005482394e1d7b8740e8a762d11d28b46b59bd4460397f30aa809dbd4d9f6a7b3a5b223f33f9ea90cd63744706f38da6f00ac4b802a23bfae1e36b685e0d09cdb24fa2ce4dae706ef0796bdb38c0ba1e03f09f017ffd130a8014c6f04de0bbd25126054a0a50006da3c8e1258776a5d178af8e13f9a9c89be30ad55ee4c85e06fa9f716ec087a3df439ea878930f5acd06218cb6d870faff6355a0342d5f1f809e53a95f9cd7f7fb31779361acd5e5cb3c3aab11b5c8223d8c15a203191b7238b9cb7e4017b94f4dcb8f31ffee0c7c5f1ad13dd5095d993cef817a5a58cf12ed5c42241b2f55b3b814fcf47d3675de6fd315b47bf8c36ee37d7ca98b8b486e68a83840bf3608c75b4; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAbJaWAAxj4A2JS5MAnHQCy+UB0YKIxAA7APYAHVtzDZsQA===; OptanonAlertBoxClosed=2026-07-13T01:02:34.271Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jul+13+2026+06%3A32%3A34+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=88c448d3-d75e-49df-b4c3-52f45c368585&interactionCount=3&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&AwaitingReconsent=false&geolocation=US%3BTX',
}


        self.params = {
            'cacheSegmentationCode': 'DS',
            'hl': 'hu',
        }

        self.product_url = "https://auchan.hu/api/v2/cache/products"

        self.product_headers  ={
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImI5ZTQxMDkyZDcxOTc5MjU3MmI5MjM0Njg3NTJkMjMwNzQ2ZWFkNjcyOGUxOGFkYWE0N2VjOTFhNGEwYWY1MDkzNjM5ZDczNjFiODNiM2Y4IiwiaWF0IjoxNzgzOTA0NDQ1LjU0MjE5NCwibmJmIjoxNzgzOTA0NDQ1LjU0MjE5NiwiZXhwIjoxNzgzOTkwODQ1LjUxMjc2Mywic3ViIjoiYW5vbl82YzQxYmVkYy0zYTU1LTRlOGQtYjBmNy1lMzk5OTk2YjljYTEiLCJzY29wZXMiOltdfQ.X7GZ_-E4gjss8lDYRDO7rWszxTP8E9Iy1um1zudHZ9h3KfGkyphzOPwpvaps3_807fXgyTBwsqnwrvWHYI9nNv5lMcrlosIUeio7cJG7-IASkfHeAs4NGxN-dPi1eWF7opaWIY-ohLWxUs_zVHMbaMsjCfVKW6ChgufvJcQxbeGkjdHvLoEr1YTfFN5fGe_7SNDqIHO4HKlnUUgbRuDtvLM4OL7wQUoWB1AZgpUXqiKTy8t21lASceaMRwl5CKPeLQsqir-Q5b4KhBixDfVVkmqA1Ll6GF3pdTv7qLKs2PdC506frvi3t-df9WLCieQPhvOepUlz1NSG9YAziua6_w',
    'if-none-match': 'W/"744f5a5060ffe8c07d3fbfb3605b61b1"',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1783904443822_0_3045430_c_75',
    'x-aw-tab-id': '1783904443822_0_3045430',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=8rTeayInSlShC7FBppi2lqxCsBANOUDnNdgHDmVoMUs14RXFwr0YAuHGORPl4aiXuz3kvSWhJVKYnHvIu8iS3x6Q8zZynEll; optiMonkClientId=1b96fb7c-4a6a-2df3-709b-df593b31fbf0; AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; login_type=anon; aw_notification_info=%7B%7D; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImI5ZTQxMDkyZDcxOTc5MjU3MmI5MjM0Njg3NTJkMjMwNzQ2ZWFkNjcyOGUxOGFkYWE0N2VjOTFhNGEwYWY1MDkzNjM5ZDczNjFiODNiM2Y4IiwiaWF0IjoxNzgzOTA0NDQ1LjU0MjE5NCwibmJmIjoxNzgzOTA0NDQ1LjU0MjE5NiwiZXhwIjoxNzgzOTkwODQ1LjUxMjc2Mywic3ViIjoiYW5vbl82YzQxYmVkYy0zYTU1LTRlOGQtYjBmNy1lMzk5OTk2YjljYTEiLCJzY29wZXMiOltdfQ.X7GZ_-E4gjss8lDYRDO7rWszxTP8E9Iy1um1zudHZ9h3KfGkyphzOPwpvaps3_807fXgyTBwsqnwrvWHYI9nNv5lMcrlosIUeio7cJG7-IASkfHeAs4NGxN-dPi1eWF7opaWIY-ohLWxUs_zVHMbaMsjCfVKW6ChgufvJcQxbeGkjdHvLoEr1YTfFN5fGe_7SNDqIHO4HKlnUUgbRuDtvLM4OL7wQUoWB1AZgpUXqiKTy8t21lASceaMRwl5CKPeLQsqir-Q5b4KhBixDfVVkmqA1Ll6GF3pdTv7qLKs2PdC506frvi3t-df9WLCieQPhvOepUlz1NSG9YAziua6_w; refresh_token=def50200e342edc3a8152a98088bc4916b34d0326cb3afc6dd3c881b8558b2db93a638f69bca26525ff5ee5d9820b697b709354af99b3aab7e62d5539edcd9a544166b3e49a16f5e7f3e3b38804700e568dca94748df5f90e71e96c7afd9fbbadd25c3c7031ceb693cdd833841910fef4fe814ffb026ffd69e2664bfebbde758ee52fa7c0e4ad121d6a4426dc1cc32ea1de3b939e44d6f421c168fede9c892ba9f0005482394e1d7b8740e8a762d11d28b46b59bd4460397f30aa809dbd4d9f6a7b3a5b223f33f9ea90cd63744706f38da6f00ac4b802a23bfae1e36b685e0d09cdb24fa2ce4dae706ef0796bdb38c0ba1e03f09f017ffd130a8014c6f04de0bbd25126054a0a50006da3c8e1258776a5d178af8e13f9a9c89be30ad55ee4c85e06fa9f716ec087a3df439ea878930f5acd06218cb6d870faff6355a0342d5f1f809e53a95f9cd7f7fb31779361acd5e5cb3c3aab11b5c8223d8c15a203191b7238b9cb7e4017b94f4dcb8f31ffee0c7c5f1ad13dd5095d993cef817a5a58cf12ed5c42241b2f55b3b814fcf47d3675de6fd315b47bf8c36ee37d7ca98b8b486e68a83840bf3608c75b4; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAbJaWAAxj4A2JS5MAnHQCy+UB0YKIxAA7APYAHVtzDZsQA===; OptanonAlertBoxClosed=2026-07-13T01:02:34.271Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jul+13+2026+06%3A32%3A34+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=88c448d3-d75e-49df-b4c3-52f45c368585&interactionCount=3&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&AwaitingReconsent=false&geolocation=US%3BTX',
}



        self.product_params  = {
            'itemsPerPage': '12',
            'page': '1',
            'cacheSegmentationCode': 'DS',
             'hl': 'hu',
        }

        # -------------------------
        # Session with Retry
        # -------------------------
        self.session = requests.Session()

        retry = Retry(
            total=5,
            connect=5,
            read=5,
            backoff_factor=2,
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        # -------------------------

        self.end_categories_dict = {}

        self.seen_pdp_urls = set()

    def get_end_categories_dict(self):

        try:

            response = self.session.get(
                self.url,
                headers=self.headers,
                params=self.params,
                timeout=30
            )

            time.sleep(1)

            if response.status_code == 200:

                all_data = response.json()

                def extract(node):

                    if isinstance(node, dict):

                        children = node.get("children", [])

                        if not children and "id" in node:

                            cat_id = node.get("id")
                            cat_name = node.get("name")

                            self.end_categories_dict[cat_id] = cat_name

                        else:

                            for child in children:
                                extract(child)

                if isinstance(all_data, list):

                    for item in all_data:
                        extract(item)

                elif isinstance(all_data, dict):

                    extract(all_data)

        except Exception as e:

            print(f"Error: {e}")

        return self.end_categories_dict

    def parse(self):

        categories = self.get_end_categories_dict()

        for cat_id, cat_name in categories.items():


            print("Category:", cat_name)
            print("ID:", cat_id)
            print("====================")

            current_category_params = self.product_params.copy()

            current_category_params["categoryId"] = cat_id

            response = self.session.get(
                self.product_url,
                headers=self.product_headers,
                params=current_category_params,
                timeout=30
            )

            time.sleep(1)

            if response.status_code != 200:

                print(f"{cat_id} statuscode == {response.status_code}")
                continue

            data = response.json()

            total_pages = int(data.get("pageCount", 0))

            print("Total Pages:", total_pages)

            for page in range(1, total_pages + 1):

                current_params = current_category_params.copy()

                current_params["page"] = page

                page_response = self.session.get(
                    self.product_url,
                    headers=self.product_headers,
                    params=current_params,
                    timeout=30
                )

                time.sleep(1)

                if page_response.status_code == 200:

                    page_data = page_response.json()

                    products = page_data.get("results", [])

                    print(
                        "Page:",
                        page,
                        "Products:",
                        len(products)
                    )

                    for product in products:

                        pdp_url_details = product.get('selectedVariant',{}) or product.get('defaultVariant',{}) or {}

                        name = pdp_url_details.get("name", "")

                        sku = pdp_url_details.get("sku", "")

                        pdp_url = create_url(name, sku)

                        if pdp_url in self.seen_pdp_urls:
                            continue

                        self.seen_pdp_urls.add(pdp_url)

                        cart_info = pdp_url_details.get('cartInfo', {}) or {}
                        categories_list = product.get('categories', []) or []

                        unique_id =  pdp_url_details.get("productId",'') or ""

                        upc = pdp_url_details.get('eanCode','') or ""

                        brand_name = pdp_url_details.get('brandName','')

                        price_info = pdp_url_details.get('price', {}) or {}

                        regular_price = price_info.get("gross") or ""

                        is_discounted = price_info.get('isDiscounted', False)

                        discounted_price =  price_info.get('grossDiscounted')

                        selling_price = discounted_price if discounted_price else regular_price

                        promotion_price = discounted_price if is_discounted else ""

                        review_count = product.get('reviewSum',{}).get('sumCount') or ""

                        rating = product.get('reviewSum',{}).get('average') or ""

                        currency = price_info.get('currency','')

                        media_data = pdp_url_details.get('media',{}).get('images',[]) or  ""

                        images = ','.join(set(media_data))

                        raw_availability = cart_info.get('availability','')

                        if raw_availability == 'available':

                            availability_status = "In Stock"
                        else:
                            availability_status = "Out of Stock"

                        

                        pkg_info = pdp_url_details.get('packageInfo',{}) or {}

                        raw_unit = pkg_info.get('packageUnit','')

                        raw_size = pkg_info.get('packageSize','')

                        

                        #pack_unit



                        if categories_list:
                             
                             sorted_cats = sorted(categories_list, key=lambda x: x.get('level', 0))
                             cat_names = [c.get('name') for c in sorted_cats if c.get('name')]
                             breadcrumb = " > ".join(cat_names)
                        else:
                            breadcrumb = "Főoldal"
        




                        


                        yield {
                            "unique_id": unique_id,
                            "product_name":name,
                            "unit_type":raw_unit or "",
                            "package_size":raw_size or "",
                            "sub_category_name": cat_name or "",
                            "regular_price":regular_price,
                            "promotion_price":promotion_price or "",
                            "selling_price":selling_price,
                            "currency":currency,
                            "brand_name":brand_name,
                            "breadcrumb":breadcrumb,
                            "availability":availability_status,
                            "pdp_url": pdp_url or "",
                            "upc":upc,
                            "images":images,
                            "rating":rating,
                            "review_count":review_count,
                            "part_number": sku or ""
                        }

                else:

                    print(
                        "Page:",
                        page,
                        "Status:",
                        page_response.status_code
                    )


if __name__ == "__main__":

    scraper = EndCategories()

    with open(
        "auchan_prpducts_data.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "unique_id",
                "sub_category_name",
                "product_name",
                "brand_name",
                "regular_price",
                "selling_price",
                "promotion_price",
                "currency",
                "package_size",
                "unit_type",
                "availability",
                "images",
                "part_number",
                "breadcrumb",
                "pdp_url",
                "rating",
                "review_count",
                "upc",
            ]
        )

        writer.writeheader()

        for row in scraper.parse():

            writer.writerow(row)

    print("CSV saved successfully")