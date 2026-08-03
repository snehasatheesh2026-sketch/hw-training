


# import logging
# import json
# import requests
# from parsel import Selector
# from urllib.parse import urljoin
# from settings import (
#     HEADERS,
#     COOKIES,
#     client,
#     MONGO_DB,
#     MONGO_COLLECTION_CATEGORY,
#     MONGO_COLLECTION_DATA
# )


# class Crawler:
#     """Crawling Urls"""

#     def __init__(self):
#         self.db = client[MONGO_DB]
        
#         # Read categories from this collection
#         self.category_collection = self.db[MONGO_COLLECTION_CATEGORY]
        
#         # Save products into this collection
#         self.data_collection = self.db[MONGO_COLLECTION_DATA]
        
#         self.queue = ''  # connect queue if needed

#     def clean_item_number(self, raw_str: str) -> str:
#         """Strips out unwanted label prefixes like 'Item number#'."""
#         if not raw_str:
#             return ""
#         cleaned = raw_str.replace("Item number#", "").replace("Item #", "").replace("Item number:", "").replace("Item:", "")
#         return cleaned.strip()

#     def start(self):
#         """Requesting Start url"""

#         categories = list(self.category_collection.find({}, {"category_name": 1, "url": 1}))
#         print(f"DEBUG: Found {len(categories)} categories in MongoDB.")
        
#         if not categories:
#             logging.warning("No categories found in MongoDB collection.")
#             return

#         for i, cat in enumerate(categories):
#             category_name = cat.get("category_name")
#             start_url = cat.get("url")

#             print(f"DEBUG: Processing [{i+1}/{len(categories)}] -> {category_name} : {start_url}")

#             if not start_url or not category_name:
#                 print(f"DEBUG: Skipping category due to missing name or URL.")
#                 continue

#             meta = {}
#             meta['category'] = category_name.strip()
#             current_url = start_url
#             visited_pages = set()

#             # Loop through all available pagination pages
#             while current_url:
#                 if current_url in visited_pages:
#                     break
#                 visited_pages.add(current_url)

#                 HEADERS['referer'] = start_url
#                 try:
#                     response = requests.get(current_url, headers=HEADERS, cookies=COOKIES, timeout=30)
                    
#                     print(f"DEBUG: URL -> {current_url} | Status Code -> {response.status_code}")
                    
#                     if response.status_code == 200:
#                         sel = Selector(response.text)
                        
#                         # 1. Parse products on the current page
#                         is_products_found = self.parse_item(sel, meta, current_url)
#                         if not is_products_found:
#                             logging.info(f"No products found on page: {current_url}")

#                         # 2. Extract the 'Next Page' link dynamically using expanded selectors
#                         next_href = sel.xpath(
#                             '//link[@rel="next"]/@href | '
#                             '//a[@rel="next"]/@href | '
#                             '//a[contains(@class,"pagination-next")]/@href | '
#                             '//a[contains(@aria-label, "Next")]/@href | '
#                             '//li[contains(@class, "pagination__item--next")]/a/@href'
#                         ).extract_first()
                        
#                         response.close()

#                         if next_href:
#                             current_url = urljoin(current_url, next_href)
#                         else:
#                             logging.info("Pagination completed for this category (No more next pages).")
#                             break
#                     else:
#                         logging.warning(f"Failed to fetch {current_url}, status code: {response.status_code}")
#                         response.close()
#                         break
#                 except Exception as e:
#                     print(f"DEBUG EXCEPTION: {e}")
#                     break

#     def parse_item(self, sel, meta, base_url):
#         """Extracts products and saves their URLs using your requested schema."""
        
#         # Expanded XPaths to catch products across different template layouts
#         product_list = sel.xpath('//div[@data-testid="productBoxContainer"]')
#         if not product_list:
#             product_list = sel.xpath('//div[contains(@class,"b-product-tile__bottom b-product-tile")]')
#         if not product_list:
#             # Generic fallback to target product cards directly
#             product_list = sel.xpath('//div[contains(@class, "product-box") or contains(@class, "cell") or contains(@data-automation, "product")]')

#         category_name = meta.get('category')
#         if not category_name:
#             return False

#         if product_list:
#             count = 0
#             for product in product_list:
#                 try:
#                     # Broadened URL extraction
#                     rel_url = product.xpath(
#                         './/a[@data-testid="itemLink"]/@href | '
#                         './/a[@class="b-product-name__link js-name-link"]/@href | '
#                         './/a[contains(@class, "description")]/@href | '
#                         './/a/@href'
#                     ).extract_first()
                    
#                     if not rel_url:
#                         continue

#                     url = urljoin(base_url, rel_url)

#                     # Optional fields extraction with fallback safe-guards
#                     raw_item_num = product.xpath(
#                         'normalize-space(.//*[@data-testid="itemNumber"] | .//*[contains(@class, "item-number")])'
#                     ).get() or ""
#                     item_number = self.clean_item_number(raw_item_num)

#                     name = product.xpath(
#                         'normalize-space(.//*[@data-testid="itemDescription"] | .//a[@data-testid="itemLink"] | .//a[contains(@class, "name")])'
#                     ).get() or ""

#                     # Construct item payload using your specific format
#                     item = {}
#                     item['product_url'] = url
#                     item['name'] = name
#                     item['category'] = meta.get('category')
#                     if item_number:
#                         item['item_number'] = item_number
                    
#                     logging.info(item)
#                     try:
#                         self.db[self.collection].insert_one(item)
#                         product_item = product_item(**item)
#                         product_item.save()
#                         # self.data_collection.insert_one(item)
#                         # count += 1
#                     except Exception:
#                         pass

#                 except Exception as e:
#                     logging.error(f"Error parsing individual product item: {e}")

#             return count > 0
#         return False

#     def close(self):
#         """Close function for all module object closing"""
#         try:
#             client.close()
#         except Exception:
#             pass


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     crawler = Crawler()
#     crawler.start()
#     crawler.close()


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
    """Crawling Urls"""

    def __init__(self):
        self.db = client[MONGO_DB]
        
        # Read categories from this collection
        self.category_collection = self.db[MONGO_COLLECTION_CATEGORY]
        
        # Save products collection name reference
        self.collection = MONGO_COLLECTION_DATA
        
        # Keep data_collection just in case
        self.data_collection = self.db[self.collection]
        
        self.queue = ''  # connect queue if needed

    def clean_item_number(self, raw_str: str) -> str:
        """Strips out unwanted label prefixes like 'Item number#'."""
        if not raw_str:
            return ""
        cleaned = raw_str.replace("Item number#", "").replace("Item #", "").replace("Item number:", "").replace("Item:", "")
        return cleaned.strip()

    def start(self):
        """Requesting Start url"""

        categories = list(self.category_collection.find({}, {"category_name": 1, "url": 1}))
        print(f"DEBUG: Found {len(categories)} categories in MongoDB.")
        
        if not categories:
            logging.warning("No categories found in MongoDB collection.")
            return

        for i, cat in enumerate(categories):
            category_name = cat.get("category_name")
            start_url = cat.get("url")

            print(f"DEBUG: Processing [{i+1}/{len(categories)}] -> {category_name} : {start_url}")

            if not start_url or not category_name:
                print(f"DEBUG: Skipping category due to missing name or URL.")
                continue

            meta = {}
            meta['category'] = category_name.strip()
            current_url = start_url
            visited_pages = set()

            # Loop through all available pagination pages
            while current_url:
                if current_url in visited_pages:
                    break
                visited_pages.add(current_url)

                HEADERS['referer'] = start_url
                try:
                    response = requests.get(current_url, headers=HEADERS, cookies=COOKIES, timeout=30)
                    
                    print(f"DEBUG: URL -> {current_url} | Status Code -> {response.status_code}")
                    
                    if response.status_code == 200:
                        sel = Selector(response.text)
                        
                        # 1. Parse products on the current page
                        is_products_found = self.parse_item(sel, meta, current_url)
                        if not is_products_found:
                            logging.info(f"No products found on page: {current_url}")

                        # 2. Extract the 'Next Page' link dynamically using expanded selectors
                        next_href = sel.xpath(
                            '//link[@rel="next"]/@href | '
                            '//a[@rel="next"]/@href | '
                            '//a[contains(@class,"pagination-next")]/@href | '
                            '//a[contains(@aria-label, "Next")]/@href | '
                            '//li[contains(@class, "pagination__item--next")]/a/@href'
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
        """Extracts products and saves their URLs using your requested schema and database flow."""
        
        # Expanded XPaths to catch products across different template layouts
        product_list = sel.xpath('//div[@data-testid="productBoxContainer"]')
        if not product_list:
            product_list = sel.xpath('//div[contains(@class,"b-product-tile__bottom b-product-tile")]')
        if not product_list:
            # Generic fallback to target product cards directly
            product_list = sel.xpath('//div[contains(@class, "product-box") or contains(@class, "cell") or contains(@data-automation, "product")]')

        category_name = meta.get('category')
        if not category_name:
            return False

        if product_list:
            count = 0
            for product in product_list:
                try:
                    # Broadened URL extraction
                    rel_url = product.xpath(
                        './/a[@data-testid="itemLink"]/@href | '
                        './/a[@class="b-product-name__link js-name-link"]/@href | '
                        './/a[contains(@class, "description")]/@href | '
                        './/a/@href'
                    ).extract_first()
                    
                    if not rel_url:
                        continue

                    url = urljoin(base_url, rel_url)

                    # Optional fields extraction with fallback safe-guards
                    raw_item_num = product.xpath(
                        'normalize-space(.//*[@data-testid="itemNumber"] | .//*[contains(@class, "item-number")])'
                    ).get() or ""
                    item_number = self.clean_item_number(raw_item_num)

                    name = product.xpath(
                        'normalize-space(.//*[@data-testid="itemDescription"] | .//a[@data-testid="itemLink"] | .//a[contains(@class, "name")])'
                    ).get() or ""

                    # Construct item payload using your specific format
                    item = {}
                    item['product_url'] = url
                    item['name'] = name
                    item['category'] = category_name
                    if item_number:
                        item['item_number'] = item_number
                    
                    logging.info(item)
                    try:
                        collection = self.collection
                        self.db[collection].insert_one(item)
                        product_item = ProductItem(**item)
                        # Uncomment if self.mongo pipeline/processor exists in your project framework:
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