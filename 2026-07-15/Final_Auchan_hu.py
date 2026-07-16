import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import csv
import re
from unidecode import unidecode
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from concurrent.futures import ThreadPoolExecutor, as_completed




def create_url(name, product_id):

    clean_name = unidecode(name)
    clean_name = clean_name.lower()
    clean_name = re.sub(r'[^a-zA-Z0-9]+', '-', clean_name)
    clean_name = re.sub(r'-+', '-', clean_name)
    clean_name = clean_name.strip('-')

    return f"https://auchan.hu/shop/{clean_name}.p-{product_id}"


class Auchan_hu:

    def __init__(self):

        self.url = "https://auchan.hu/api/v2/cache/tree/0"

        self.headers  ={
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer ',
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
    'x-aw-request-id': '',
    'x-aw-tab-id': '1',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=
        }
        self.description_url ='https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/description'

        self.allergens_url = "https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/allergensDetailed"

        self.ingredients_url  = "https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/ingredients"

        self.parameter_url = "https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/parameterList"

        self.params = {
            'cacheSegmentationCode': 'DS',
            'hl': 'hu',
        }

        self.header_description  = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer token',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/hajdu-chili-lime-grillsajt-240-g.p-844525',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '',
    'x-aw-tab-id': '',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _oma
    }

        
        self.allergens_headers = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer ',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/hajdu-chili-lime-grillsajt-240-g.p-844525',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '',
    'x-aw-tab-id': '',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _
    }

        
        self.header_parameter = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer ',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/hajdu-chili-lime-grillsajt-240-g.p-844525',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '',
    'x-aw-tab-id': '',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; 
    }
        
        self.ingredient_header  = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer ',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/hajdu-chili-lime-grillsajt-240-g.p-844525',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '',
    'x-aw-tab-id': '',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; 
    }

        self.details_params  = {
    'hl': 'hu',
}


        self.product_url = "https://auchan.hu/api/v2/cache/products"

        self.product_headers   = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer ',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/medence-es-kiegeszitok/medence-strandjatek/medence-es-kiegeszitok/merev-falu-csaladi-medencek.c-7593',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '',
    'x-aw-tab-id': '',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; 
    }



        self.product_params  = {
            'itemsPerPage': '12',
            'page': '1',
            'cacheSegmentationCode': 'DS',
             'hl': 'hu',
        }

        
        # Session with Retry
        
        self.session = requests.Session()

        retry = Retry(
            total=5,
            connect=5,
            read=5,
            backoff_factor=2,
            allowed_methods=["GET"],
        )

        adapter =  HTTPAdapter(
                     max_retries=retry,
                     pool_connections=20,
                     pool_maxsize=20,)


        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)



        self.end_categories_dict = {}

        self.seen_pdp_urls = set()

    def fetch(self, url, headers):
          try:
            return self.session.get(
                url,
                params=self.details_params,
                headers=headers,
                timeout=30,
            )
          except Exception:
            return None


    def get_end_categories_dict(self):

        try:

            response = self.session.get(
                self.url,
                headers=self.headers,
                params=self.params,
                timeout=30
            )

            time.sleep(0.1)

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
    
    def process_product(self, product, cat_name):


        pdp_url_details = product.get('selectedVariant',{}) or product.get('defaultVariant',{}) or {}

        product_name = pdp_url_details.get("name", "")

        sku = pdp_url_details.get("sku", "")

        pdp_url = create_url(product_name, sku)

        if pdp_url in self.seen_pdp_urls:
            return None

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

        discountDisplayPercentage = price_info.get('discountDisplayPercentage')if  is_discounted else ""

        promotion_valid_from = price_info.get("discountValidFrom", "") if is_discounted else ""

        promotion_valid_to = price_info.get('discountValidTo','') if is_discounted else ""

        if promotion_valid_from :
                            promotion_valid_from = datetime.fromisoformat(
                             promotion_valid_from
                             ).strftime("%Y-%m-%d")
        else:
            promotion_valid_from = ""

        if promotion_valid_to :
                              promotion_valid_to = datetime.fromisoformat(
                              promotion_valid_to
                             ).strftime("%Y-%m-%d")
        else :
            promotion_valid_to = ""

        flags = pdp_url_details.get("flags", [])
        promotion_label = ""

        promotion_label = ", ".join(
                                    item.get("name", "")
                                    for item in flags
                                    if item.get('flag') =="flag_discount" and item.get("name")
                                    )
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

        unit_price_raw =  pkg_info.get('unitPrice',{}).get('gross') or ""

        if categories_list:
                             
            sorted_cats = sorted(categories_list, key=lambda x: x.get('level', 0))
            cat_names = [c.get('name') for c in sorted_cats if c.get('name')]
            breadcrumb = " > ".join(["Főoldal", "Online áruház"]+cat_names)
        else:
            breadcrumb = "Főoldal > Online áruház"
        
        varient_id = pdp_url_details.get('id','') or ""

        raw_description = ""
        ingredients = ""
        country = ""
        features = ""
        allergensDetailed = ""

        new = []

        if varient_id and unique_id:

            url = self.description_url.format(unique_id, varient_id)

            in_url = self.ingredients_url.format(unique_id, varient_id)

            feature_url = self.parameter_url.format(unique_id, varient_id)

            allergen_url = self.allergens_url.format(unique_id, varient_id)

            with ThreadPoolExecutor(max_workers=4) as executor:
                descri_future = executor.submit(self.fetch, url, self.header_description)
                ingredient_future = executor.submit(self.fetch, in_url, self.ingredient_header)
                feature_future = executor.submit(self.fetch, feature_url, self.header_parameter)
                allergen_future = executor.submit(self.fetch, allergen_url, self.allergens_headers)

                descri_response = descri_future.result()
                ingredient_response = ingredient_future.result()
                feature_respo = feature_future.result()
                allergens_response = allergen_future.result()
            
            if descri_response and descri_response.status_code == 200:

                json_data = descri_response.json()
                html_description = json_data.get("description", "")
                if html_description:
                    raw_description = BeautifulSoup(
                                         html_description,
                                         "html.parser"
                                        ).get_text(separator=" ", strip=True)
            if ingredient_response and ingredient_response.status_code == 200:

                in_json_data = ingredient_response.json()
                ingredients = in_json_data.get("description", "")

                if ingredients:
                    ingredients = BeautifulSoup(
                                                  ingredients,
                                                  "html.parser"
                                         ).get_text(separator=" ", strip=True)
            if feature_respo and feature_respo.status_code == 200:
                data = feature_respo.json()

                for item in data.get("parameters", []):
                    name = item.get("name")
                    value = item.get("value", "")
                    value = ", ".join(
                                        line.strip()
                                        for line in value.splitlines()
                                        if line.strip()
                                        )
                    if name == "Származási ország":
                        country = value

                    elif name:
                        new.append(f"{name}: {value}")
                features = ", ".join(new)
            
            if allergens_response and allergens_response.status_code == 200:
                all_data = allergens_response.json()
                raw_allergensDetailed = all_data.get("allergensDetailed", [])
                allergensDetailed = ", ".join(
                                    item.get("name", "")
                                    for item in raw_allergensDetailed
                                    if item.get("name")
         
                                    )
        description = " ".join((raw_description or "").split())
        ingredients = " ".join(ingredients.split()) or ""
        country = country or ""

        return {
                            "unique_id": unique_id,
                            "product_name":product_name,
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
                            "discountpercentage":discountDisplayPercentage,
                            "promotion_label":promotion_label,
                            "country":country,
                            "allergens":allergensDetailed,
                            "features":features,
                            "images":images,
                            "rating":rating,
                            "promotion_valid_to":promotion_valid_to,
                            "promotion_valid_from":promotion_valid_from,
                            "review_count":review_count,
                            "descripition":description,
                            "ingredients":ingredients,
                            "part_number": sku or "",
                            "unit_price":unit_price_raw
                        }


        
    
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

            time.sleep(0.1)

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

                time.sleep(0.1)

                if page_response.status_code == 200:

                    page_data = page_response.json()

                    products = page_data.get("results", [])

                    with ThreadPoolExecutor(max_workers=5) as executor:
                         
                         futures = [
                        executor.submit(
                            self.process_product,
                            product,
                            cat_name
                        )
                        for product in products
                    ]
                         for future in as_completed(futures):
                            row = future.result()

                            if row:
                              yield row




if __name__ == "__main__":

    scraper = Auchan_hu()

    with open(
        "auchan_product_data_test.csv",
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
                "promotion_valid_from",
                "promotion_valid_to",
                "discountpercentage",
                "promotion_label",
                "currency",
                "package_size",
                "unit_type",
                "unit_price",
                "availability",
                "images",
                "part_number",
                "country",
                "breadcrumb",
                "pdp_url",
                "features",
                "allergens",
                "ingredients",
                "descripition",
                "rating",
                "review_count",
                "upc",
            ]
        )

        writer.writeheader()

        for row in scraper.parse():

            writer.writerow(row)

    print("CSV saved successfully")


# if we using the mangodb insteda of the csv file 

# from pymongo import MongoClient



#     from pymongo import MongoClient

# class EndCategories:

#     def __init__(self):

#         # Your existing code...

#         self.client = MongoClient("localhost_string wanna give here")

#         self.db = self.client["auchan"] # dastabase name

#         self.collection = self.db["products"]       # the collection name like table name 



# for future in as_completed(futures):

#     row = future.result()

#     if row:
#         self.collection.insert_one(row)




# if __name__ == "__main__":

#     scraper = EndCategories()

#     scraper.parse()

#     print("Data saved successfully.")



# instead of writing too much def we can use a folder and cerated the def function inside diffrent file just call them insteda writing in a  file 

# the upper portion we an write into a another file also the subcatres like that .