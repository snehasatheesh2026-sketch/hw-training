from items import ProductItem
import logging
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

class Crawler:

    def __init__(self):
        self.db = client[MONGO_DB]
        
        self.category_collection = self.db[MONGO_COLLECTION_CATEGORY]
        
        self.data_collection = self.db[  MONGO_COLLECTION_DATA]
        self.data_collection.create_index("product_url", unique=True)

        
    def start(self):


        categories = self.category_collection.find({}, {"category_name": 1, "url": 1})
        
        if not categories:
            logging.warning("No categories found in MongoDB collection.")
            return

        for  cat in categories:
            category_name = cat.get("category_name")
            current_url = cat.get("url")


            if not current_url:
                continue


            while current_url:
                try:
                    response = requests.get(current_url, headers=HEADERS, cookies=COOKIES, timeout=30)
                    
                    
                    if response.status_code == 200:
                        sel = Selector(response.text)
                        
                        is_products_found = self.parse_item(sel, category_name, current_url)
                        if not is_products_found:
                            logging.info(f"No products found on page: {current_url}")

                        next_href = sel.xpath(
                            '//link[@rel="next"]/@href '
                        ).get()
                        
    
                        if next_href:
                            current_url = urljoin(current_url, next_href)
                        else:
                            logging.info("Pagination completed for this category (No more next pages).")
                            break
                    else:
                        logging.warning(f"Failed to fetch {current_url}, status code: {response.status_code}")
                
                        break
                except Exception as e:
                    print(f"DEBUG EXCEPTION: {e}")
                    break

    def parse_item(self, sel, category_name, base_url):
    

        product_list = sel.xpath('//div[@data-testid="productBoxContainer"]')
    
        
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
                    item['product_name'] = name
                    item['category_name'] = category_name
                    item['item_number'] = raw_item_num

                    try:
                
                        product_item = ProductItem(**item)
                        product_item.save()

                        
                        count += 1
                    except Exception as e:
                        logging.error(f"Error inserting into MongoDB: {e}")

                except Exception as e:
                    logging.error(f"Error parsing individual product item: {e}")

            return count > 0
        return False

    def close(self):

       client.close()
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    crawler = Crawler()
    crawler.start()
    crawler.close()