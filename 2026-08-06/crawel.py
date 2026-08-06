
import logging
import json
import requests
from parsel import Selector
from urllib.parse import urljoin
from settings import (
    HEADERS,
    COOKIES,
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    MONGO_COLLECTION_DATA
)
from items import ProductItem


class Crawler:

    def __init__(self):
        self.db = client[MONGO_DB]
        

        self.category_collection = self.db[MONGO_COLLECTION_CATEGORY]
        

        self.collection = MONGO_COLLECTION_DATA
        

        
        self.data_collection = self.db[self.collection]
        
    def start(self):
        """Requesting Start url"""

        categories = list(self.category_collection.find({}, {"category_name": 1, "url": 1}))
        print(f"DEBUG: Found {len(categories)} categories in MongoDB.")
        
        if not categories:
            logging.warning("No categories found in MongoDB collection.")
            return

        for  cat in categories:
            category_name = cat.get("category_name")
            start_url = cat.get("url")

            print(f"{category_name} : {start_url}")

            if not start_url:
                print(f"DEBUG: Skipping category due to missing name or URL.")
                continue

            current_url = start_url
            visited_pages = set()

            while current_url:
                if current_url in visited_pages:
                    break
                visited_pages.add(current_url)


                try:
                    response = requests.get(current_url, headers=HEADERS, cookies=COOKIES, timeout=30)
                    
                    print(f"DEBUG: URL -> {current_url} | Status Code -> {response.status_code}")
                    
                    if response.status_code == 200:
                        sel = Selector(response.text)
                        
                        is_products_found = self.parse_item(sel, category_name, current_url)
                        if not is_products_found:
                            logging.info(f"No products found on page: {current_url}")

                        next_href = sel.xpath(
                            '//link[@rel="next"]/@href '
                        ).extract_first()
                        
                        response.close()

                        if next_href:
                            current_url = urljoin(current_url, next_href)
                        else:
                            logging.info("Pagination completed for this category (No more next pages).")
                            break
                    else:
                        logging.warning(f"Failed to fetch {current_url}, status code: {response.status_code}")
                        response.close()
                        break
                except Exception as e:
                    print(f"DEBUG EXCEPTION: {e}")
                    break

    def parse_item(self, sel, meta, base_url):
    

        product_list = sel.xpath('//div[@data-testid="productBoxContainer"]')
    
        category_name = meta
        if not category_name:
            return False

        if product_list:
            count = 0
            for product in product_list:
                try:
                    rel_url = product.xpath(
                        './/a[@data-testid="itemLink"]/@href | .//a/@href'
                    ).get()  
                    
                    if not rel_url:
                        continue

                    url = urljoin(base_url, rel_url)

            
                    raw_item_num = product.xpath(
                        'normalize-space(.//*[@data-testid="itemNumber"] | .//*[contains(@class, "item-number")])'
                    ).get() or ""

                    if raw_item_num:
                         raw_item_num = raw_item_num.replace("Item number#", "").strip()
                    else:
                        raw_item_num = ""

                    name = product.xpath(
                        'normalize-space(.//*[@data-testid="itemDescription"] | .//a[@data-testid="itemLink"] | .//a[contains(@class, "name")])'
                    ).get() or ""

                    
                    item = {}
                    item['product_url'] = url
                    item['name'] = name
                    item['category'] = category_name
                    item['item_number'] = raw_item_num
                    
                    logging.info(item)
                    try:
                
                        self.data_collection.insert_one(item)
                        #product_item = ProductItem(**item)
                        # self.mongo.process(product_item)  
                        count += 1
                    except Exception as e:
                        logging.error(f"Error inserting into MongoDB: {e}")

                except Exception as e:
                    logging.error(f"Error parsing individual product item: {e}")

            return count > 0
        return False

    def close(self):
        """Close function for all module object closing"""
        try:
            client.close()
        except Exception:
            pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    crawler = Crawler()
    crawler.start()
    crawler.close()