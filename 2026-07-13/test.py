import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import csv
import re
from unidecode import unidecode
from bs4 import BeautifulSoup



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
    'authorization': 'Bearer  {Token}',
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
    'x-aw-tab-id': '',
}
        self.description_url ='https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/description'

        self.allergens_url = "https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/allergensDetailed"

        self.ingredients_url  = "https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/ingredients"

        self.params = {
            'cacheSegmentationCode': 'DS',
            'hl': 'hu',
        }

        self.details_params  = {
    'hl': 'hu',
}


        self.product_url = "https://auchan.hu/api/v2/cache/products"

        self.product_headers  ={
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer {token}',
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
    'x-aw-tab-id': '',
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

                        
                        varient_id = pdp_url_details.get('id','') or ""

                        raw_description= ""

                        ingredients = ""

                        if varient_id and unique_id:

                            url = self.description_url.format(unique_id,varient_id)

                            descri_response = self.session.get(url, params= self.details_params, headers= self.headers)

                            if descri_response.status_code == 200:

                                

                                json_data =descri_response.json()

                            
                                html_description = json_data.get("description", "")

                                if html_description:
                                    raw_description = BeautifulSoup(
                                            html_description,
                                            "html.parser"
                                    ).get_text(separator=" ", strip=True)
                            
                            in_url = self.ingredients_url.format(unique_id,varient_id)

                            ingredient_response = self.session.get(in_url, params= self.details_params, headers= self.headers)

                            if ingredient_response.status_code == 200:

                                in_json_data = ingredient_response.json()

                                ingredients = in_json_data.get('description','')

                        description = raw_description or ""  

                        description = " ".join(description.split())   

                        ingredients = ingredients or ""



        




                        


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
                            "descripition":description,
                            "ingredients":ingredients,
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