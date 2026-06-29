
import csv

import time

import requests

import json

class Dm_makeup_listing:


    def __init__(self):
# basic_url to connect to the pdp_url
        self.base_url = "https://www.dm.si"

# tree_url = for get the all sub_catreis url
        self.tree_url = (
            "https://products.dm.de/categories/v1/categories-tree/sl-SI"

        )

        self.strating_url = (
            "https://product-search.services.dmtech.com/si/search/static"
        )

        self.output_csv = "dm_makeup.csv"
# headers for the tree url
        self.headers = {
            "sec-ch-ua-platform": '"Linux"',
            "Referer": "https://www.dm.si/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            
        }
# herades for the sub_cateries
        self.headerss = {

                        'sec-ch-ua-platform': '"Linux"',

                        'x-dm-product-search-token': '48130558781589',

                        'Referer': 'https://www.dm.si/',

                        'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',

                        'sec-ch-ua-mobile': '?0',

                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',

                        'Accept': 'application/json, text/plain, */*',

                        'x-dm-product-search-tags': 'presentation:grid;search-type:editorial;channel:web;editorial-type:category',

        }

        self.params = {
            "pageSize": "30",
            "searchType": "editorial-search",     
            "sort": "editorial_relevance",
            "type": "search-static",
        }    # for the sub_category change the allsub_catreis = we will get specfic sub_cateogry
    
    def leaf_categories(self, nodes): # leaf cateries

        leaves = {}

        for node in nodes:

            subcategories = node.get("subcategories", [])

            if subcategories:

                leaves.update(self.leaf_categories(subcategories))
            else:

                leaves[node.get("name")] = node.get("code")

        return leaves
    
    def sub_categories(self):  # subacteries

        response = requests.get(self.tree_url, headers= self.headers)

        if response.status_code == 200:

            for root_node in response.json():

                if root_node.get("name") == "Ličila":

                    return self.leaf_categories([root_node])
        return {}
    
    def parse(self):  # pdp_url

        categories = self.sub_categories()

        for cat_name, cat_id in categories.items():

            current_category_param = self.params.copy()

            current_category_param['allCategories.id'] = cat_id

            response = requests.get(self.strating_url, headers= self.headerss, params= current_category_param)

            if response.status_code != 200:

                print(f"{cat_id} statuscode == {response.status_code}")

                continue

            data = response.json()

            total_pages = data.get('totalPages', 1)

            for page in range(total_pages):

                current_params = current_category_param.copy()

                current_params['currentPage'] = page

                page_res = requests.get(self.strating_url, headers= self.headerss, params= current_params)

                if page_res.status_code != 200:

                    print(f"{page} == {page_res.status_code}")

                    continue

                page_data = page_res.json()

                for product in page_data.get("products", []):

                    tile_data = product.get("tileData",{})

                    pdp_url = tile_data.get("self", "")

                    if pdp_url:

                        yield {
                            "sub_category_name": cat_name,
                            "product_name": product.get("title", "").strip(),
                            "pdp_url": self.base_url + pdp_url,
                            "competitor_name": "dm",

                        }
                    
                time.sleep(0.5)
if __name__ == "__main__":
    spider = Dm_makeup_listing()

    with open(spider.output_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["sub_category_name", "product_name", "pdp_url", "competitor_name"]
        )
        writer.writeheader()

        total_count = 0
        for item in spider.parse():
            writer.writerow(item)
            total_count += 1

    print(f" Total links collected == {total_count}")







    











