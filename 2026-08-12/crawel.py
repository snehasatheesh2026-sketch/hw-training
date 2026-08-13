from bs4 import BeautifulSoup
import logging
import json
import base64
import requests
from parsel import Selector
from urllib.parse import urljoin
from settings import (
    HEADERS,
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    MONGO_COLLECTION_DATA,
    API_URL,
    params,
    JOIN_URL
)

# print(params)

# variables = json.loads(params["variables"])

# variables["filter"]["category_uid"]["in"] = "MTkz"

# params["variables"] = json.dumps(variables)

# print(params)




class Crawler:

    def __init__(self):
        self.db = client[MONGO_DB]
        

        self.category_collection = self.db[MONGO_COLLECTION_CATEGORY]
        

        self.collection = MONGO_COLLECTION_DATA



        self.seen_urls = set()
        

        
        self.data_collection = self.db[self.collection]
    
    def start(self):
        """Requesting Start url"""
        categories = list(self.category_collection.find({}))
        print(f"DEBUG: Found {len(categories)} categories in MongoDB.")
        if not categories:
           logging.warning("No categories found in MongoDB collection.")
           return
        for  cat in categories:
            category_name = cat.get("category",'')
            start_url = cat.get("url",'')
            cat_id = cat.get("category_id",'')
            cat_link = cat.get('url','')
            id = cat.get('id','')

            if not cat_id:

              cat_id = base64.b64encode(id.encode()).decode()

            variables = json.loads(params["variables"])

            variables["filter"]["category_uid"]["in"] = cat_id

            current_page = 1

            while True:
              variables["currentPage"] = current_page

              params["variables"] = json.dumps(variables)

              try:

                response = requests.get(
                            API_URL,
                            params=params,
                            headers=HEADERS,
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
                    
                    

                    is_next = self.parse_item(
                            response,category_name)
                    if not is_next:

                       logging.info(
                        "Pagination completed"
                    )
                       break

                    if current_page >= total_pages:
                        break

                    current_page += 1
              except Exception as e:
                 logging.error(
                    f"Error processing "
                    f"{category_name}: {e}"
                )
                 break
    def parse_item(self, response,category_name):
       data = response.json()
       category = category_name

           
       products_data = (
        data
        .get("data", {})
        .get("products", {})
    )
       products = products_data.get("items", [])
       if not products:
         return False
       for product in products:
        try:
          url_key = product.get('url_key', '')
          product_id = product.get('id', '')

          if not url_key:
             continue
          full_url = urljoin(JOIN_URL,url_key)
          if full_url in self.seen_urls:
            print(
                f"Duplicate URL skipped: {full_url}"
            )
            continue
          print("yes")
          self.seen_urls.add(
            full_url)
          print(full_url)
          item = {}
          item['product_url'] = full_url
    
          item['category'] = category
          logging.info(item)
          try:
             self.data_collection.insert_one(item)
          except Exception as e:
             logging.error(f"Error inserting into MongoDB: {e}")
        except Exception as e:
           logging.error(f"Error parsing individual product item: {e}")
       return True
    def close(self):
       
        try:
            client.close()
        except Exception:
            pass
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    crawler = Crawler()
    crawler.start()
    crawler.close
     
        
             
          


          
          



          








 
                            

                    
                



                

