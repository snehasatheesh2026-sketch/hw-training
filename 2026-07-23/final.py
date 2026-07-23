# import csv
# import json
# import random
# import time
# import re
# import threading
# import queue
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from threading import Lock
# from urllib.parse import urljoin

# from curl_cffi import requests
# from parsel import Selector
# from pymongo import MongoClient, UpdateOne

# # =====================================================================
# # CONFIGURATION
# # =====================================================================

# INPUT_FILE = "categories.csv"

# # MongoDB Configuration
# MONGO_URI = "mongodb://localhost:27017"
# DB_NAME = "webstaurant_db"
# COLLECTION_NAME = "products"

# # Concurrency settings optimized for higher throughput
# CATEGORY_WORKERS = 2
# PRODUCT_WORKERS = 2
# # Realistic delays to mimic human traffic safely
# MIN_DELAY = 0.1
# MAX_DELAY = 0.2

# MAX_RETRIES = 5

# MY_HEADERS ={}
# MY_COOKIES ={}




# # Thread-local storage to maintain persistent sessions per thread with request counters
# thread_local = threading.local()

# # Lock and timestamp tracking for rate-limiting global cookie refreshes
# cookie_lock = threading.Lock()
# last_cookie_refresh = 0
# COOKIE_REFRESH_INTERVAL = 8 # seconds


# def refresh_cookies():
#     """Actively pings the target site to fetch brand-new dynamic anti-bot/session cookies."""
#     session = requests.Session(impersonate="chrome124")
#     session.headers.update(MY_HEADERS)

#     try:
#         response = session.get(
#             "https://www.webstaurantstore.com/",
#             timeout=30
#         )
#         print("Refresh status:", response.status_code)
#         cookies = session.cookies.get_dict()
#         print("Refreshed cookies received:", cookies)

#         if response.status_code == 200:
#             return cookies

#         return None
#     except Exception as e:
#         print("Cookie refresh error:", e)
#         return None
#     finally:
#         session.close()


# def refresh_global_cookies():
#     """Thread-safely refreshes and updates the global MY_COOKIES dictionary with cooldown checks and dynamic subset validation."""
#     global last_cookie_refresh
#     with cookie_lock:
#         if time.time() - last_cookie_refresh < COOKIE_REFRESH_INTERVAL:
#             print("Cookie refresh skipped (cooldown active).")
#             return

#         new = refresh_cookies()
        
#         # Dynamically ensure all previously established required keys are present
#         required = set(MY_COOKIES.keys())
        
#         if new and (not required or required.issubset(new.keys())):
#             MY_COOKIES.clear()
#             MY_COOKIES.update(new)
#             last_cookie_refresh = time.time()
#             print("Global cookies updated successfully.")
#         else:
#             print("Cookie refresh failed or missing required session keys - keeping existing cookies.")


# def get_thread_session():
#     """Returns a thread-local curl_cffi Session, refreshing it periodically or if closed to avoid stale connections."""
#     session_is_valid = True
#     if not hasattr(thread_local, "session") or not hasattr(thread_local, "request_count"):
#         session_is_valid = False
#     else:
#         try:
#             if getattr(thread_local.session, "_closed", False):
#                 session_is_valid = False
#         except Exception:
#             session_is_valid = False

#     if not session_is_valid:
#         try:
#             if hasattr(thread_local, "session"):
#                 thread_local.session.close()
#         except Exception:
#             pass
#         session = requests.Session(impersonate="chrome124")
#         session.headers.update(MY_HEADERS)
#         session.cookies.update(MY_COOKIES)
#         thread_local.session = session
#         thread_local.request_count = 0
    
#     # Refresh session every 300 requests to prevent stale keep-alive / transport errors
#     thread_local.request_count += 1
#     if thread_local.request_count >= 300:
#         try:
#             thread_local.session.close()
#         except Exception:
#             pass
#         session = requests.Session(impersonate="chrome124")
#         session.headers.update(MY_HEADERS)
#         session.cookies.update(MY_COOKIES)
#         thread_local.session = session
#         thread_local.request_count = 1

#     return thread_local.session


# def reset_thread_session():
#     """Forces recreation of the thread-local session cleanly via central management."""
#     if hasattr(thread_local, "session"):
#         try:
#             thread_local.session.close()
#         except Exception:
#             pass
#         del thread_local.session
#     if hasattr(thread_local, "request_count"):
#         del thread_local.request_count
#     return get_thread_session()


# class WebstaurantScraper:
#     def __init__(self):
#         self.seen_pdp_urls = set()
#         self.lock = Lock()
        
#         # Dedicated thread-safe queue for asynchronous database writing
#         self.mongo_queue = queue.Queue()
#         self.is_scraping_done = threading.Event()
        
#         # Initialize MongoDB Client and Collection
#         self.mongo_client = MongoClient(MONGO_URI)
#         self.db = self.mongo_client[DB_NAME]
#         self.collection = self.db[COLLECTION_NAME]
        
#         # Ensure unique index on pdp_url to prevent duplicates
#         self.collection.create_index("pdp_url", unique=True)
        
#         # Start the background database writer thread
#         self.writer_thread = threading.Thread(target=self._mongo_writer_worker, daemon=True)
#         self.writer_thread.start()

#     def clean_item_number(self, raw_str: str) -> str:
#         """Strips out unwanted label prefixes like 'Item number#'."""
#         if not raw_str:
#             return ""
        
#         cleaned = raw_str.replace("Item number#", "").replace("Item #", "").replace("Item number:", "").replace("Item:", "")
#         return cleaned.strip()

#     def _flush_batch(self, batch, tasks_count):
#         """Helper method to execute bulk_write upserts and acknowledge tasks safely using integer counts."""
#         if not batch:
#             return
        
#         try:
#             operations = [
#                 UpdateOne(
#                     {"pdp_url": doc["pdp_url"]},
#                     {"$set": doc},
#                     upsert=True
#                 )
#                 for doc in batch
#             ]
#             result = self.collection.bulk_write(operations, ordered=False)
#             print(f"[Mongo] Upserted batch: {len(batch)} documents processed (Modified: {result.modified_count}, Upserted: {len(result.upserted_ids)})")
#         except Exception as e:
#             print(f"[Mongo Error] Bulk write failed: {e}")
#         finally:
#             batch.clear()
#             for _ in range(tasks_count):
#                 self.mongo_queue.task_done()

#     def _mongo_writer_worker(self):
#         """Dedicated background worker thread that flushes items from the queue into MongoDB in larger optimized batches."""
#         batch = []
#         tasks_count = 0
#         batch_size = 300
#         flush_interval = 5.0  # seconds

#         while not self.is_scraping_done.is_set() or not self.mongo_queue.empty():
#             try:
#                 try:
#                     item = self.mongo_queue.get(timeout=flush_interval)
#                     batch.append(item)
#                     tasks_count += 1

#                     if len(batch) >= batch_size:
#                         self._flush_batch(batch, tasks_count)
#                         tasks_count = 0
#                 except queue.Empty:
#                     if batch:
#                         self._flush_batch(batch, tasks_count)
#                         tasks_count = 0

#             except Exception as e:
#                 print(f"[MongoDB Writer Error]: {e}")

#         # Final safety flush for any remaining items left in queue
#         while not self.mongo_queue.empty():
#             try:
#                 item = self.mongo_queue.get_nowait()
#                 batch.append(item)
#                 tasks_count += 1
#             except queue.Empty:
#                 break

#         if batch:
#             self._flush_batch(batch, tasks_count)

#     def fetch_pdp_rating(self, item: dict, breadcrumbs: str) -> dict | None:
#         """Helper task for worker threads: Requests PDP page and extracts rating and details using its own thread-safe session."""
#         pdp_url = item["pdp_url"]
        
#         with self.lock:
#             if pdp_url in self.seen_pdp_urls:
#                 return None
#             self.seen_pdp_urls.add(pdp_url)

#         product_name = ""
#         itemsnumberof = item["item_number"]
#         rating = ""
#         price = ""
#         price_unit = ""
#         brand = ""
#         sku = ""
#         related_product_skus = ""
#         faq_json = ""
#         Features = ""
#         models = ""
#         intro_headline = ""
#         description = ""
#         product_details = ""
#         shipping_info = ""
#         upc = ""
#         full_price_text = ""

#         Specifications = ""
#         video = ""
#         product_documents = ""
#         Product_Image_URLs = ""
#         result = ""
#         Selected_Variant = {}
#         configurable_attributes = []

#         image_urls = []
#         variants = {}

#         for retry in range(MAX_RETRIES):
#             session = get_thread_session()
#             try:
#                 time.sleep(0.1)
#                 response = session.get(pdp_url, timeout=20)

#                 if response.status_code == 429:
#                     print(f"[429 RATE LIMIT] PDP Pausing 30 seconds for {pdp_url}")
#                     response.close()
#                     time.sleep(10)
#                     continue
#                 elif response.status_code == 403:
#                     response.close()
#                     refresh_global_cookies()
#                     reset_thread_session()
#                     continue
#                 elif response.status_code != 200:
#                     response.close()
#                     return None

#                 selector = Selector(text=response.text)
#                 response.close()

#                 product_name = selector.xpath('normalize-space(//h1[@data-testid="product-detail-heading"])').get() or ""

#                 # ---------------- Product Documents ----------------
#                 documents = selector.xpath(
#                     '//div[@id="resources-group"]//a/@href'
#                 ).getall()

#                 documents = list(dict.fromkeys(documents))
#                 product_documents = ",".join(documents) if documents else ""

#                 # ---------------- Video ----------------
#                 video = selector.xpath(
#                     '//source[contains(@src, "_4.mp4")]/@src'
#                 ).get("")

#                 # ---------------- Selected Variant + Config Attributes ----------------
#                 for heading in selector.xpath(
#                     '//h2[@data-testid="productVariationsHeading"]'
#                 ):
#                     s_name = heading.xpath(
#                         'normalize-space(text())'
#                     ).get("").replace(":", "").strip()

#                     s_value = heading.xpath(
#                         './span/text()'
#                     ).get("").strip()

#                     if s_name and s_value:
#                         Selected_Variant[s_name] = s_value

#                         if s_name not in configurable_attributes:
#                             configurable_attributes.append(s_name)
                
#                 if not Selected_Variant:
#                     Selected_Variant = ""

#                 configurable_attributes = (
#                     ",".join(configurable_attributes)
#                     if configurable_attributes else ""
#                 )

#                 # ---------------- Product Features ----------------
#                 product_overview = selector.xpath(
#                     '//h3[normalize-space()="Product Overview"]'
#                     '/following-sibling::ul[1]/li/span/text()'
#                 ).getall()

#                 product_overview = [
#                     x.strip()
#                     for x in product_overview
#                     if x.strip()
#                 ]

#                 Features = ",".join(product_overview) if product_overview else ""

#                 # ---------------- Rating ----------------
#                 raw_rating = selector.xpath('//span[@data-testid="zest-ratings-sr"]/text()').get() or ""
#                 match = re.search(r'(\d+(?:\.\d+)?)', raw_rating)
#                 rating = match.group(1) if match else ""

#                 # ---------------- Price ----------------
#                 price_container = selector.xpath('//*[@data-testid="price-container"]')

#                 if price_container:
#                     full_price_text = " ".join(t.strip() for t in price_container.xpath(".//text()").getall() if t.strip())
                
#                 price_match = re.search(r"\$?\s*([\d,]+(?:\.\d+)?)", full_price_text)

#                 if price_match:
#                     price = price_match.group(1).replace(",", "")
                
#                 unit_match = re.search(r"/\s*([A-Za-z0-9 .-]+)", full_price_text)

#                 if unit_match:
#                     price_unit = unit_match.group(1).strip()

#                 # ---------------- Brand ----------------
#                 brand = selector.xpath(
#                     'normalize-space(//*[@data-testid="brand-side-section"]//a/@title)'
#                 ).get() or ""

#                 # ---------------- Description ----------------
#                 intro_container = selector.xpath(
#                     '//*[@data-testid="introduction"]'
#                 )

#                 if intro_container:
#                     intro_headline = intro_container.xpath(
#                         'normalize-space(.//*[@id="details-group-headline"] | .//h2)'
#                     ).get() or ""

#                     description = intro_container.xpath(
#                         'string(.//div[contains(@class,"template-text")] | .//p)'
#                     ).get() or ""

#                 if not description:
#                     details_group = selector.xpath(
#                         '//*[@data-testid="details-group"]'
#                     )

#                     if details_group:
#                         description = details_group.xpath(
#                             'string(.//div[@class="padded"])'
#                         ).get() or ""

#                 product_details = f"{intro_headline} {description}".strip()

#                 # ---------------- Shipping ----------------
#                 shipping_info = selector.xpath(
#                     'normalize-space(.//*[@data-testid="highlights-meta-side-section"]//p)'
#                 ).get() or ""

#                 # ---------------- UPC ----------------
#                 upc = selector.xpath(
#                     'normalize-space(.//*[@data-testid="UPC-Number"])'
#                 ).get() or ""

#                 # ---------------- Specifications ----------------
#                 Specifications = {
#                     key.strip(): " ".join(value.xpath(".//text()").getall()).strip()
#                     for key, value in zip(
#                         selector.xpath('//dl[@id="tbSpecSheetRows"]/dt/text()').getall(),
#                         selector.xpath('//dl[@id="tbSpecSheetRows"]/dd')
#                     )
#                 }

#                 Specifications = Specifications if Specifications else ""

#                 # ---------------- Related Products ----------------
#                 related_product_skus = ",".join(
#                     s.split("relatedproduct_companion_")[-1]
#                     for s in selector.xpath(
#                     '//div[contains(@class,"add-to-cart")]//form[starts-with(@id,"relatedproduct_companion_")]/@id'
#                     ).getall()
#                 )

#                 # ---------------- FAQ ----------------
#                 faqs = []

#                 for faq in selector.xpath(
#                     "//div[@data-testid='expanded-question-answer']"
#                     "//div[contains(@class,'customer-qa')]"
#                 ):
#                     faqs.append({
#                         "Question": faq.xpath(
#                             ".//div[contains(@class,'customer-question')]//span/text()"
#                         ).get(default="").strip(),

#                         "Answer": " ".join(
#                             t.strip()
#                             for t in faq.xpath(
#                                 ".//div[contains(@class,'csr-answer')]//text()"
#                             ).getall()
#                             if t.strip()
#                         )
#                     })

#                 if faqs:
#                     faq_json = json.dumps(faqs, ensure_ascii=False, separators=(",", ":"))
#                 else:
#                     faq_json = ""

#                 # ---------------- SKU from JSON LD ----------------
#                 product = {}
#                 for script in selector.xpath('//script/text()').getall():
#                     if "productTemplates" in script:
#                         try:
#                             script = script.strip()
#                             script = script.removeprefix("<!--").removesuffix("-->").strip()
#                             data = json.loads(script)
#                             product = data["productTemplates"][0]
#                             sku = str(product.get("itemNumberId", ""))
#                             break
#                         except Exception:
#                             pass
                
#                 if sku:
#                     for href in selector.xpath('//link[@rel="preload" and @as="image"]/@href').getall():
#                         if f"/products/large/{sku}/" in href:
#                             match = re.search(r'(images/products/large/.*)', href)
#                             if match:
#                                 image_urls.append(match.group(1))

#                 image_urls = list(dict.fromkeys(image_urls))
#                 Product_Image_URLs = ",".join(image_urls)

#                 for group in product.get("variationMembership", {}).get("variationGroups", []):
#                     attr = group.get("optionName", "")
#                     if attr == "Height Style":
#                         attr = "Height"

#                     for item_var in group.get("variationGroupItems", []):
#                         skus = str(item_var.get("itemNumberId", ""))

#                         if not skus:
#                             continue
#                         variants.setdefault(skus, {"sku": skus})
#                         variants[skus][attr] = item_var.get("variationText", "")
#                 result = list(variants.values()) if variants else ""

#                 # ---------------- 3D Models ----------------
#                 model_list = []

#                 for script in selector.xpath(
#                     '//script[@type="application/ld+json"]/text()'
#                 ).getall():
#                     try:
#                         data = json.loads(script.strip())
#                         nodes = data if isinstance(data, list) else data.get("@graph", [data])
#                         for node in nodes:
#                             if isinstance(node, dict) and node.get("@type") == "3DModel":
#                                 for obj in node.get("encoding", []):
#                                     url = obj.get("contentUrl")
#                                     if url:
#                                         model_list.append(url.lstrip("/"))
#                     except json.JSONDecodeError:
#                         continue

#                 models = ",".join(model_list) if model_list else ""

#                 # ---------------- Breadcrumbs Extraction (with Fallback) ----------------
#                 page_breadcrumbs = ""
#                 bc_script = selector.xpath('//script[contains(text(),"BreadcrumbList")]/text()').get()
#                 if bc_script:
#                     try:
#                         data = json.loads(bc_script.strip())
#                         nodes = data if isinstance(data, list) else data.get("@graph", [data])
#                         for node in nodes:
#                             if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
#                                 crumbs = [
#                                     cb.get("name")
#                                     for cb in node.get("itemListElement", [])
#                                     if cb.get("name")
#                                 ]
#                                 if crumbs:
#                                     page_breadcrumbs = " > ".join(crumbs[:-1])
#                                     break
#                     except Exception:
#                         pass

#                 if not page_breadcrumbs:
#                     fallback_crumbs = selector.xpath('//ul[contains(@class,"breadcrumb")]//li/a/text() | //nav[@aria-label="Breadcrumb"]//a/text()').getall()
#                     fallback_crumbs = [c.strip() for c in fallback_crumbs if c.strip()]
#                     if fallback_crumbs:
#                         page_breadcrumbs = " > ".join(fallback_crumbs)

#                 if page_breadcrumbs:
#                     breadcrumbs = page_breadcrumbs

#                 break  # Successful execution, break retry loop

#             except Exception as e:
#                 print(f"Error fetching PDP rating for {pdp_url} (Attempt {retry + 1}/{MAX_RETRIES}): {e}")
#                 reset_thread_session()
#                 time.sleep(min(2 ** retry, 0.2))
        
#         itemsnumberof = str(itemsnumberof)
#         upc = str(upc)
#         related_product_skus = str(related_product_skus)
#         return {
#             "product_name": product_name,
#             "brand": brand,
#             "shipping_info": shipping_info,
#             "rating": rating,
#             "item_number": itemsnumberof,
#             "price": price,
#             "price_unit": price_unit,
#             "FAQ": faq_json,
#             "Specifications": Specifications,
#             "Selected_Variant": Selected_Variant,
#             "configurable_attributes": configurable_attributes,
#             "Features": Features,
#             "Video_URLs": video,
#             "upc": upc,
#             "pdp_url": pdp_url,
#             "sku": sku,
#             "Image_URLs": Product_Image_URLs,
#             "Configurable Variations": result,
#             "related_product_skus": related_product_skus,
#             "Product_Documents": product_documents,
#             "3D_Asset_URLs": models,
#             "description": product_details,
#             "Category": breadcrumbs
#         }

#     def extract_product_items(self, selector: Selector, base_url: str) -> list:
#         """Extracts product name, item number, and PDP URL via parsed Selector."""
#         extracted_items = []
#         seen_urls_in_page = set()

#         product_list = selector.xpath('//div[@data-testid="productBoxContainer"]')

#         for product in product_list:
#             try:
#                 rel_url = product.xpath('.//a[@data-testid="itemLink"]/@href | .//a/@href').get()
#                 if not rel_url:
#                     continue

#                 full_url = urljoin(base_url, rel_url)
#                 if full_url not in seen_urls_in_page:
#                     seen_urls_in_page.add(full_url)

#                     raw_item_num = product.xpath(
#                         'normalize-space(.//*[@data-testid="itemNumber"] | .//*[contains(@class, "item-number")])'
#                     ).get() or ""
                    
#                     item_number = self.clean_item_number(raw_item_num)

#                     name = product.xpath(
#                         'normalize-space(.//*[@data-testid="itemDescription"] | .//a[@data-testid="itemLink"])'
#                     ).get() or ""

#                     extracted_items.append({
#                         "product_name": name,
#                         "item_number": item_number,
#                         "pdp_url": full_url
#                     })

#             except Exception as e:
#                 print(f"Error parsing product: {e}")
#                 continue

#         return extracted_items

#     def extract_next_page(self, selector: Selector, current_url: str) -> str | None:
#         """Extracts next page URL using canonical link tags from parsed Selector."""
#         next_href = selector.xpath('//link[@rel="next"]/@href | //a[@rel="next"]/@href').get()
#         if next_href:
#             return urljoin(current_url, next_href)
#         return None

#     def process_category(self, row: dict, pdp_executor) -> None:
#         category_name = row.get("name", "").strip()
#         url = row.get("url", "").strip()

#         if not category_name or not url:
#             return

#         current_url = url
#         visited_pages = set()

#         print(f"\n====================\nCategory: {category_name}\nStart URL: {url}\n====================")

#         while current_url:
#             if current_url in visited_pages:
#                 break
#             visited_pages.add(current_url)

#             time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

#             response = None
#             try:
#                 for retry in range(MAX_RETRIES):
#                     session = get_thread_session()
#                     try:
#                         response = session.get(
#                             current_url,
#                             timeout=(10, 20)
#                         )
#                         if response.status_code == 200:
#                             break
#                         elif response.status_code == 429:
#                             print(f"[429 RATE LIMIT] Pausing 30 seconds for {current_url}")
#                             if response:
#                                 response.close()
#                                 response = None
#                             time.sleep(0.8)
#                             continue
#                         elif response.status_code == 403:
#                             if response:
#                                 response.close()
#                                 response = None
#                             refresh_global_cookies()
#                             reset_thread_session()
#                             continue
#                         elif response.status_code in [500, 502, 503, 504]:
#                             if response:
#                                 response.close()
#                                 response = None
#                             time.sleep(min(2 ** retry, 30))
#                             continue
#                         else:
#                             break
#                     except Exception:
#                         if response:
#                             response.close()
#                             response = None
#                         time.sleep(min(2 ** retry, 0.3))
#                         reset_thread_session()

#                 if response is None:
#                     break

#                 print(f"[{response.status_code}] {current_url}")

#                 if response.status_code != 200:
#                     print(f"[ERROR] Failed with status {response.status_code}")
#                     response.close()
#                     break

#                 selector = Selector(text=response.text)
#                 response.close()
#                 response = None

#                 product_items = self.extract_product_items(selector, current_url)
#                 print(f"   --> Found {len(product_items)} items. Requesting PDP ratings with shared executor...")

#                 futures = [
#                     pdp_executor.submit(self.fetch_pdp_rating, item, category_name)
#                     for item in product_items
#                 ]
                
#                 page_processed_count = 0
#                 for future in as_completed(futures):
#                     res = future.result()
#                     if res:
#                         self.mongo_queue.put(res)
#                         page_processed_count += 1

#                 print(f"Products Processed on Page: {page_processed_count}")
#                 current_url = self.extract_next_page(selector, current_url)

#             except Exception as e:
#                 print(f"Error requesting {current_url}: {e}")
#                 if response:
#                     try:
#                         response.close()
#                     except Exception:
#                         pass
#                 break

#     def run(self):
#         with open(INPUT_FILE, "r", encoding="utf-8") as infile:
#             categories = list(csv.DictReader(infile))

#         # Global shared ThreadPoolExecutor for PDP requests to prevent socket/thread starvation
#         with ThreadPoolExecutor(max_workers=PRODUCT_WORKERS) as pdp_executor:
#             with ThreadPoolExecutor(max_workers=CATEGORY_WORKERS) as category_executor:
#                 futures = [
#                     category_executor.submit(self.process_category, row, pdp_executor)
#                     for row in categories
#                 ]

#                 for future in as_completed(futures):
#                     future.result()

#         # Signal background writer that scraping is done and wait for queue to empty
#         self.is_scraping_done.set()
#         self.writer_thread.join()
        
#         # Close MongoDB connection cleanly
#         self.mongo_client.close()

#         print("\nAll categories completed! Data saved successfully to MongoDB.")


# if __name__ == "__main__":
#     scraper = WebstaurantScraper()
#     scraper.run()









import csv
import json
import random
import time
import re
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from urllib.parse import urljoin

from curl_cffi import requests
from parsel import Selector
from pymongo import MongoClient, UpdateOne

# =====================================================================
# CONFIGURATION
# =====================================================================

INPUT_FILE = "categories.csv"

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "webstaurant_db"
COLLECTION_NAME = "products"

# Concurrency settings optimized for higher throughput
CATEGORY_WORKERS = 2
PRODUCT_WORKERS = 5
# Realistic delays to mimic human traffic safely
MIN_DELAY = 0.1
MAX_DELAY = 0.3

MAX_RETRIES = 5

MY_HEADERS = {
    }

MY_COOKIES = {
}



# Thread-local storage to maintain persistent sessions per thread with request counters
thread_local = threading.local()

# Lock and timestamp tracking for rate-limiting global cookie refreshes
cookie_lock = threading.Lock()
last_cookie_refresh = 0
COOKIE_REFRESH_INTERVAL = 8  # seconds


def refresh_cookies():
    """Actively pings the target site to fetch brand-new dynamic anti-bot/session cookies."""
    session = requests.Session(impersonate="chrome124")
    session.headers.update(MY_HEADERS)

    try:
        response = session.get(
            "https://www.webstaurantstore.com/",
            timeout=30
        )
        print("Refresh status:", response.status_code)
        cookies = session.cookies.get_dict()
        print("Refreshed cookies received:", cookies)

        if response.status_code == 200:
            return cookies

        return None
    except Exception as e:
        print("Cookie refresh error:", e)
        return None
    finally:
        session.close()


def refresh_global_cookies():
    """Thread-safely refreshes and updates the global MY_COOKIES dictionary with cooldown checks."""
    global last_cookie_refresh
    with cookie_lock:
        if time.time() - last_cookie_refresh < COOKIE_REFRESH_INTERVAL:
            print("Cookie refresh skipped (cooldown active).")
            return

        new = refresh_cookies()
        
        if new:
            MY_COOKIES.clear()
            MY_COOKIES.update(new)
            last_cookie_refresh = time.time()
            print("Global cookies updated successfully.")
        else:
            print("Cookie refresh failed.")


def get_thread_session():
    """Returns a thread-local curl_cffi Session, refreshing it periodically or if closed to avoid stale connections."""
    session_is_valid = True
    if not hasattr(thread_local, "session") or not hasattr(thread_local, "request_count"):
        session_is_valid = False
    else:
        try:
            if getattr(thread_local.session, "_closed", False):
                session_is_valid = False
        except Exception:
            session_is_valid = False

    if not session_is_valid:
        try:
            if hasattr(thread_local, "session"):
                thread_local.session.close()
        except Exception:
            pass
        session = requests.Session(impersonate="chrome124")
        session.headers.update(MY_HEADERS)
        session.cookies.update(MY_COOKIES)
        thread_local.session = session
        thread_local.request_count = 0
    
    # Refresh session every 300 requests to prevent stale keep-alive / transport errors
    thread_local.request_count += 1
    if thread_local.request_count >= 300:
        try:
            thread_local.session.close()
        except Exception:
            pass
        session = requests.Session(impersonate="chrome124")
        session.headers.update(MY_HEADERS)
        session.cookies.update(MY_COOKIES)
        thread_local.session = session
        thread_local.request_count = 1

    return thread_local.session


def reset_thread_session():
    """Forces recreation of the thread-local session cleanly via central management."""
    if hasattr(thread_local, "session"):
        try:
            thread_local.session.close()
        except Exception:
            pass
        del thread_local.session
    if hasattr(thread_local, "request_count"):
        del thread_local.request_count
    return get_thread_session()


class WebstaurantScraper:
    def __init__(self):
        self.seen_pdp_urls = set()
        self.lock = Lock()
        
        # Dedicated thread-safe queue for asynchronous database writing
        self.mongo_queue = queue.Queue()
        self.is_scraping_done = threading.Event()
        
        # Initialize MongoDB Client with connection pool configuration and Collection
        self.mongo_client = MongoClient(
            MONGO_URI,
            maxPoolSize=50
        )
        self.db = self.mongo_client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]
        
        # Ensure unique index on pdp_url to prevent duplicates
        self.collection.create_index("pdp_url", unique=True)
        
        # Start the background database writer thread
        self.writer_thread = threading.Thread(target=self._mongo_writer_worker, daemon=True)
        self.writer_thread.start()

    def clean_item_number(self, raw_str: str) -> str:
        """Strips out unwanted label prefixes like 'Item number#'."""
        if not raw_str:
            return ""
        
        cleaned = raw_str.replace("Item number#", "").replace("Item #", "").replace("Item number:", "").replace("Item:", "")
        return cleaned.strip()

    def _flush_batch(self, batch, tasks_count):
        """Helper method to execute bulk_write upserts and acknowledge tasks safely using integer counts."""
        if not batch:
            return
        
        try:
            operations = [
                UpdateOne(
                    {"pdp_url": doc["pdp_url"]},
                    {"$set": doc},
                    upsert=True
                )
                for doc in batch
            ]
            result = self.collection.bulk_write(operations, ordered=False)
            print(f"[Mongo] Upserted batch: {len(batch)} documents processed (Modified: {result.modified_count}, Upserted: {len(result.upserted_ids)})")
        except Exception as e:
            print(f"[Mongo Error] Bulk write failed: {e}")
        finally:
            batch.clear()
            for _ in range(tasks_count):
                self.mongo_queue.task_done()

    def _mongo_writer_worker(self):
        """Dedicated background worker thread that flushes items from the queue into MongoDB in larger optimized batches."""
        batch = []
        tasks_count = 0
        batch_size = 300
        flush_interval = 5.0  # seconds

        while not self.is_scraping_done.is_set() or not self.mongo_queue.empty():
            try:
                try:
                    item = self.mongo_queue.get(timeout=flush_interval)
                    batch.append(item)
                    tasks_count += 1

                    if len(batch) >= batch_size:
                        self._flush_batch(batch, tasks_count)
                        tasks_count = 0
                except queue.Empty:
                    if batch:
                        self._flush_batch(batch, tasks_count)
                        tasks_count = 0

            except Exception as e:
                print(f"[MongoDB Writer Error]: {e}")

        # Final safety flush for any remaining items left in queue
        while not self.mongo_queue.empty():
            try:
                item = self.mongo_queue.get_nowait()
                batch.append(item)
                tasks_count += 1
            except queue.Empty:
                break

        if batch:
            self._flush_batch(batch, tasks_count)

    def fetch_pdp_rating(self, item: dict, breadcrumbs: str) -> dict | None:
        """Helper task for worker threads: Requests PDP page and extracts rating and details using its own thread-safe session."""
        pdp_url = item["pdp_url"]
        
        with self.lock:
            if pdp_url in self.seen_pdp_urls:
                return None
            self.seen_pdp_urls.add(pdp_url)

        product_name = ""
        itemsnumberof = item["item_number"]
        rating = ""
        price = ""
        price_unit = ""
        brand = ""
        sku = ""
        related_product_skus = ""
        faq_json = ""
        Features = ""
        models = ""
        intro_headline = ""
        description = ""
        product_details = ""
        shipping_info = ""
        upc = ""
        full_price_text = ""

        Specifications = ""
        video = ""
        product_documents = ""
        Product_Image_URLs = ""
        result = ""
        Selected_Variant = {}
        configurable_attributes = []

        image_urls = []
        variants = {}

        for retry in range(MAX_RETRIES):
            session = get_thread_session()
            try:
                time.sleep(random.uniform(0.2, 0.5))
                response = session.get(pdp_url, timeout=20)

                if response.status_code == 429:
                    print(f"[429 RATE LIMIT] PDP Pausing 30 seconds for {pdp_url}")
                    response.close()
                    time.sleep(10)
                    continue
                elif response.status_code == 403:
                    response.close()
                    refresh_global_cookies()
                    reset_thread_session()
                    continue
                elif response.status_code != 200:
                    response.close()
                    return None

                selector = Selector(text=response.text)
                response.close()

                product_name = selector.xpath('normalize-space(//h1[@data-testid="product-detail-heading"])').get() or ""

                # ---------------- Product Documents ----------------
                documents = selector.xpath(
                    '//div[@id="resources-group"]//a/@href'
                ).getall()

                documents = list(dict.fromkeys(documents))
                product_documents = ",".join(documents) if documents else ""

                # ---------------- Video ----------------
                video = selector.xpath(
                    '//source[contains(@src, "_4.mp4")]/@src'
                ).get("")

                # ---------------- Selected Variant + Config Attributes ----------------
                for heading in selector.xpath(
                    '//h2[@data-testid="productVariationsHeading"]'
                ):
                    s_name = heading.xpath(
                        'normalize-space(text())'
                    ).get("").replace(":", "").strip()

                    s_value = heading.xpath(
                        './span/text()'
                    ).get("").strip()

                    if s_name and s_value:
                        Selected_Variant[s_name] = s_value

                        if s_name not in configurable_attributes:
                            configurable_attributes.append(s_name)
                
                if not Selected_Variant:
                    Selected_Variant = ""

                configurable_attributes = (
                    ",".join(configurable_attributes)
                    if configurable_attributes else ""
                )

                # ---------------- Product Features ----------------
                product_overview = selector.xpath(
                    '//h3[normalize-space()="Product Overview"]'
                    '/following-sibling::ul[1]/li/span/text()'
                ).getall()

                product_overview = [
                    x.strip()
                    for x in product_overview
                    if x.strip()
                ]

                Features = ",".join(product_overview) if product_overview else ""

                # ---------------- Rating ----------------
                raw_rating = selector.xpath('//span[@data-testid="zest-ratings-sr"]/text()').get() or ""
                match = re.search(r'(\d+(?:\.\d+)?)', raw_rating)
                rating = match.group(1) if match else ""

                # ---------------- Price ----------------
                price_container = selector.xpath('//*[@data-testid="price-container"]')

                if price_container:
                    full_price_text = " ".join(t.strip() for t in price_container.xpath(".//text()").getall() if t.strip())
                
                price_match = re.search(r"\$?\s*([\d,]+(?:\.\d+)?)", full_price_text)

                if price_match:
                    price = price_match.group(1).replace(",", "")
                
                unit_match = re.search(r"/\s*([A-Za-z0-9 .-]+)", full_price_text)

                if unit_match:
                    price_unit = unit_match.group(1).strip()

                # ---------------- Brand ----------------
                brand = selector.xpath(
                    'normalize-space(//*[@data-testid="brand-side-section"]//a/@title)'
                ).get() or ""

                # ---------------- Description ----------------
                intro_container = selector.xpath(
                    '//*[@data-testid="introduction"]'
                )

                if intro_container:
                    intro_headline = intro_container.xpath(
                        'normalize-space(.//*[@id="details-group-headline"] | .//h2)'
                    ).get() or ""

                    description = intro_container.xpath(
                        'string(.//div[contains(@class,"template-text")] | .//p)'
                    ).get() or ""

                if not description:
                    details_group = selector.xpath(
                        '//*[@data-testid="details-group"]'
                    )

                    if details_group:
                        description = details_group.xpath(
                            'string(.//div[@class="padded"])'
                        ).get() or ""

                product_details = f"{intro_headline} {description}".strip()

                # ---------------- Shipping ----------------
                shipping_info = selector.xpath(
                    'normalize-space(.//*[@data-testid="highlights-meta-side-section"]//p)'
                ).get() or ""

                # ---------------- UPC ----------------
                upc = selector.xpath(
                    'normalize-space(.//*[@data-testid="UPC-Number"])'
                ).get() or ""

                # ---------------- Specifications ----------------
                Specifications = {
                    key.strip(): " ".join(value.xpath(".//text()").getall()).strip()
                    for key, value in zip(
                        selector.xpath('//dl[@id="tbSpecSheetRows"]/dt/text()').getall(),
                        selector.xpath('//dl[@id="tbSpecSheetRows"]/dd')
                    )
                }

                Specifications = Specifications if Specifications else ""

                # ---------------- Related Products ----------------
                related_product_skus = ",".join(
                    s.split("relatedproduct_companion_")[-1]
                    for s in selector.xpath(
                    '//div[contains(@class,"add-to-cart")]//form[starts-with(@id,"relatedproduct_companion_")]/@id'
                    ).getall()
                )

                # ---------------- FAQ ----------------
                faqs = []

                for faq in selector.xpath(
                    "//div[@data-testid='expanded-question-answer']"
                    "//div[contains(@class,'customer-qa')]"
                ):
                    faqs.append({
                        "Question": faq.xpath(
                            ".//div[contains(@class,'customer-question')]//span/text()"
                        ).get(default="").strip(),

                        "Answer": " ".join(
                            t.strip()
                            for t in faq.xpath(
                                ".//div[contains(@class,'csr-answer')]//text()"
                            ).getall()
                            if t.strip()
                        )
                    })

                if faqs:
                    faq_json = json.dumps(faqs, ensure_ascii=False, separators=(",", ":"))
                else:
                    faq_json = ""

                # ---------------- SKU from JSON LD ----------------
                product = {}
                for script in selector.xpath('//script/text()').getall():
                    if "productTemplates" in script:
                        try:
                            script = script.strip()
                            script = script.removeprefix("<!--").removesuffix("-->").strip()
                            data = json.loads(script)
                            product = data["productTemplates"][0]
                            sku = str(product.get("itemNumberId", ""))
                            break
                        except Exception:
                            pass
                
                if sku:
                    for href in selector.xpath('//link[@rel="preload" and @as="image"]/@href').getall():
                        if f"/products/large/{sku}/" in href:
                            match = re.search(r'(images/products/large/.*)', href)
                            if match:
                                image_urls.append(match.group(1))

                image_urls = list(dict.fromkeys(image_urls))
                Product_Image_URLs = ",".join(image_urls)

                for group in product.get("variationMembership", {}).get("variationGroups", []):
                    attr = group.get("optionName", "")
                    if attr == "Height Style":
                        attr = "Height"

                    for item_var in group.get("variationGroupItems", []):
                        skus = str(item_var.get("itemNumberId", ""))

                        if not skus:
                            continue
                        variants.setdefault(skus, {"sku": skus})
                        variants[skus][attr] = item_var.get("variationText", "")
                result = list(variants.values()) if variants else ""

                # ---------------- 3D Models ----------------
                model_list = []

                for script in selector.xpath(
                    '//script[@type="application/ld+json"]/text()'
                ).getall():
                    try:
                        data = json.loads(script.strip())
                        nodes = data if isinstance(data, list) else data.get("@graph", [data])
                        for node in nodes:
                            if isinstance(node, dict) and node.get("@type") == "3DModel":
                                for obj in node.get("encoding", []):
                                    url = obj.get("contentUrl")
                                    if url:
                                        model_list.append(url.lstrip("/"))
                    except json.JSONDecodeError:
                        continue

                models = ",".join(model_list) if model_list else ""

                # ---------------- Breadcrumbs Extraction (with Fallback) ----------------
                page_breadcrumbs = ""
                bc_script = selector.xpath('//script[contains(text(),"BreadcrumbList")]/text()').get()
                if bc_script:
                    try:
                        data = json.loads(bc_script.strip())
                        nodes = data if isinstance(data, list) else data.get("@graph", [data])
                        for node in nodes:
                            if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
                                crumbs = [
                                    cb.get("name")
                                    for cb in node.get("itemListElement", [])
                                    if cb.get("name")
                                ]
                                if crumbs:
                                    page_breadcrumbs = " > ".join(crumbs[:-1])
                                    break
                    except Exception:
                        pass

                if not page_breadcrumbs:
                    fallback_crumbs = selector.xpath('//ul[contains(@class,"breadcrumb")]//li/a/text() | //nav[@aria-label="Breadcrumb"]//a/text()').getall()
                    fallback_crumbs = [c.strip() for c in fallback_crumbs if c.strip()]
                    if fallback_crumbs:
                        page_breadcrumbs = " > ".join(fallback_crumbs)

                if page_breadcrumbs:
                    breadcrumbs = page_breadcrumbs

                break  # Successful execution, break retry loop

            except Exception as e:
                print(f"Error fetching PDP rating for {pdp_url} (Attempt {retry + 1}/{MAX_RETRIES}): {e}")
                reset_thread_session()
                time.sleep(min(2 ** retry, 0.2))
        
        itemsnumberof = str(itemsnumberof)
        upc = str(upc)
        related_product_skus = str(related_product_skus)
        return {
            "product_name": product_name,
            "brand": brand,
            "shipping_info": shipping_info,
            "rating": rating,
            "item_number": itemsnumberof,
            "price": price,
            "price_unit": price_unit,
            "FAQ": faq_json,
            "Specifications": Specifications,
            "Selected_Variant": Selected_Variant,
            "configurable_attributes": configurable_attributes,
            "Features": Features,
            "Video_URLs": video,
            "upc": upc,
            "pdp_url": pdp_url,
            "sku": sku,
            "Image_URLs": Product_Image_URLs,
            "Configurable Variations": result,
            "related_product_skus": related_product_skus,
            "Product_Documents": product_documents,
            "3D_Asset_URLs": models,
            "description": product_details,
            "Category": breadcrumbs
        }

    def extract_product_items(self, selector: Selector, base_url: str) -> list:
        """Extracts product name, item number, and PDP URL via parsed Selector."""
        extracted_items = []
        seen_urls_in_page = set()

        product_list = selector.xpath('//div[@data-testid="productBoxContainer"]')

        for product in product_list:
            try:
                rel_url = product.xpath('.//a[@data-testid="itemLink"]/@href | .//a/@href').get()
                if not rel_url:
                    continue

                full_url = urljoin(base_url, rel_url)
                if full_url not in seen_urls_in_page:
                    seen_urls_in_page.add(full_url)

                    raw_item_num = product.xpath(
                        'normalize-space(.//*[@data-testid="itemNumber"] | .//*[contains(@class, "item-number")])'
                    ).get() or ""
                    
                    item_number = self.clean_item_number(raw_item_num)

                    name = product.xpath(
                        'normalize-space(.//*[@data-testid="itemDescription"] | .//a[@data-testid="itemLink"])'
                    ).get() or ""

                    extracted_items.append({
                        "product_name": name,
                        "item_number": item_number,
                        "pdp_url": full_url
                    })

            except Exception as e:
                print(f"Error parsing product: {e}")
                continue

        return extracted_items

    def extract_next_page(self, selector: Selector, current_url: str) -> str | None:
        """Extracts next page URL using canonical link tags from parsed Selector."""
        next_href = selector.xpath('//link[@rel="next"]/@href | //a[@rel="next"]/@href').get()
        if next_href:
            return urljoin(current_url, next_href)
        return None

    def process_category(self, row: dict, pdp_executor) -> None:
        category_name = row.get("name", "").strip()
        url = row.get("url", "").strip()

        if not category_name or not url:
            return

        current_url = url
        visited_pages = set()

        print(f"\n====================\nCategory: {category_name}\nStart URL: {url}\n====================")

        while current_url:
            if current_url in visited_pages:
                break
            visited_pages.add(current_url)

            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

            response = None
            try:
                for retry in range(MAX_RETRIES):
                    session = get_thread_session()
                    try:
                        response = session.get(
                            current_url,
                            timeout=(10, 20)
                        )
                        if response.status_code == 200:
                            break
                        elif response.status_code == 429:
                            print(f"[429 RATE LIMIT] Pausing 30 seconds for {current_url}")
                            if response:
                                response.close()
                                response = None
                            time.sleep(0.8)
                            continue
                        elif response.status_code == 403:
                            if response:
                                response.close()
                                response = None
                            refresh_global_cookies()
                            reset_thread_session()
                            continue
                        elif response.status_code in [500, 502, 503, 504]:
                            if response:
                                response.close()
                                response = None
                            time.sleep(min(2 ** retry, 20))
                            continue
                        else:
                            break
                    except Exception:
                        if response:
                            response.close()
                            response = None
                        time.sleep(min(2 ** retry, 0.3))
                        reset_thread_session()

                if response is None:
                    break

                print(f"[{response.status_code}] {current_url}")

                if response.status_code != 200:
                    print(f"[ERROR] Failed with status {response.status_code}")
                    response.close()
                    break

                selector = Selector(text=response.text)
                response.close()
                response = None

                product_items = self.extract_product_items(selector, current_url)
                print(f"   --> Found {len(product_items)} items. Requesting PDP ratings with shared executor...")

                futures = [
                    pdp_executor.submit(self.fetch_pdp_rating, item, category_name)
                    for item in product_items
                ]
                
                page_processed_count = 0
                for future in as_completed(futures):
                    res = future.result()
                    if res:
                        self.mongo_queue.put(res)
                        page_processed_count += 1

                print(f"Products Processed on Page: {page_processed_count}")
                current_url = self.extract_next_page(selector, current_url)

            except Exception as e:
                print(f"Error requesting {current_url}: {e}")
                if response:
                    try:
                        response.close()
                    except Exception:
                        pass
                break

    def run(self):
        with open(INPUT_FILE, "r", encoding="utf-8") as infile:
            categories = list(csv.DictReader(infile))

        # Global shared ThreadPoolExecutor for PDP requests to prevent socket/thread starvation
        with ThreadPoolExecutor(max_workers=PRODUCT_WORKERS) as pdp_executor:
            with ThreadPoolExecutor(max_workers=CATEGORY_WORKERS) as category_executor:
                futures = [
                    category_executor.submit(self.process_category, row, pdp_executor)
                    for row in categories
                ]

                for future in as_completed(futures):
                    future.result()

        # Signal background writer that scraping is done and wait for queue to empty
        self.is_scraping_done.set()
        self.writer_thread.join()
        
        # Close MongoDB connection cleanly
        self.mongo_client.close()

        print("\nAll categories completed! Data saved successfully to MongoDB.")


if __name__ == "__main__":
    scraper = WebstaurantScraper()
    scraper.run()