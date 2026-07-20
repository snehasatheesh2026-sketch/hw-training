

import csv
import json
import random
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from urllib.parse import urljoin

from curl_cffi import requests
from bs4 import BeautifulSoup
from parsel import Selector

# =====================================================================
# CONFIGURATION
# =====================================================================

INPUT_FILE = "categories.csv"
OUTPUT_FILE = "products.csv"

# Category level parallel workers
CATEGORY_WORKERS = 2  

# Product level parallel workers (Parallel PDP fetches per page)
PRODUCT_WORKERS = 5  

# Delays between requests (in seconds)
MIN_DELAY = 2.0
MAX_DELAY = 4.0

MY_HEADERS ={}
MY_COOKIES =  {}


# =====================================================================
# SCRAPER CLASS
# =====================================================================

class WebstaurantScraper:
    def __init__(self):
        self.seen_pdp_urls = set()
        self.lock = Lock()

    def parse_breadcrumbs(self, soup: BeautifulSoup) -> str:
        """Extracts category breadcrumbs from LD+JSON scripts."""
        for script in soup.find_all("script", type="application/ld+json"):
            if not script.string:
                continue

            try:
                data = json.loads(script.string)
                nodes = data if isinstance(data, list) else data.get("@graph", [data])

                for node in nodes:
                    if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
                        crumbs = [
                            item.get("name")
                            for item in node.get("itemListElement", [])
                            if item.get("name")
                        ]
                        if crumbs:
                            return " > ".join(crumbs)
            except (json.JSONDecodeError, TypeError, AttributeError):
                continue

        return ""

    def clean_item_number(self, raw_str: str) -> str:
        """Strips out unwanted label prefixes like 'Item number#'."""
        if not raw_str:
            return ""
        
        cleaned = raw_str.replace("Item number#", "").replace("Item #", "").replace("Item number:", "").replace("Item:", "")
        return cleaned.strip()

    def fetch_pdp_rating(self, session: requests.Session, item: dict, breadcrumbs: str) -> dict | None:
        """Helper task for worker threads: Requests PDP page and extracts rating only."""
        pdp_url = item["pdp_url"]

        rating, price, price_unit, brand, sku, related_product_skus, faq_json, rating = "","", "", "", "","","",""
        intro_headline, description, product_details, shipping_info, upc, Specifications= "", "", "", "","", ""

    
        # Thread-safe duplicate check across all categories/threads
        with self.lock:
            if pdp_url in self.seen_pdp_urls:
                return None
            self.seen_pdp_urls.add(pdp_url)

        rating = ""

        try:
            time.sleep(random.uniform(0.5, 1.5))  # Brief polite delay
            response = session.get(pdp_url, timeout=20)
            
            if response.status_code == 200:
                selector = Selector(text=response.text)
                
                # Fetch rating from data-testid="zest-ratings-sr" on PDP

                raw_rating = selector.xpath('//span[contains(@aria-label, "star")]/@aria-label').get() or ""

                if not raw_rating:

                    raw_rating = selector.xpath('normalize-space(.//*[@data-testid="zest-ratings-sr"])').get() or ""
                if raw_rating:
                    rating = raw_rating.split(' ')[0].strip()
                else:
                    rating = ""
            

                rating = raw_rating.split(' ')[0].strip()
                price = price_container = selector.xpath('//*[@data-testid="price-container"]')

                if price_container:

                    raw_unit = price_container.xpath('normalize-space(.//span[contains(@class, "pr-1")] | .//span/span)').get() or ""

                    price_unit = raw_unit.replace("/", "").strip()

                    full_price_text = price_container.xpath('normalize-space(.)').get() or ""

                    if raw_unit:

                        price = full_price_text.replace(raw_unit, "").strip()

                    else:
                        price = full_price_text# 

                brand = selector.xpath('normalize-space(//*[@data-testid="brand-side-section"]//a/@title)').get() or ""

                intro_container = selector.xpath('//*[@data-testid="introduction"]')

                if intro_container:

                     intro_headline = intro_container.xpath('normalize-space(.//*[@id="details-group-headline"] | .//h2)').get() or ""

                     description = intro_container.xpath('string(.//div[contains(@class, "template-text")] | .//p)').get() or ""
                if not description:
                    details_group = selector.xpath('//*[@data-testid="details-group"]')

                    if details_group:
                        description = details_group.xpath('string(.//div[@class="padded"])').get() or ""

                product_details = f"{intro_headline} {description}".strip()
                shipping_info = selector.xpath('normalize-space(.//*[@data-testid="highlights-meta-side-section"]//p)').get() or ""

                # --- EXTRACT UPC CODE ---
                upc= selector.xpath('normalize-space(.//*[@data-testid="UPC-Number"])').get() or ""

                Specifications = {
                        key.strip(): " ".join(value.xpath(".//text()").getall()).strip()
                        for key, value in zip(
                        selector.xpath('//dl[@id="tbSpecSheetRows"]/dt/text()').getall(),
                        selector.xpath('//dl[@id="tbSpecSheetRows"]/dd')
                         )
                      }
                
                related_product_skus = ",".join(
                              sku.replace("relatedproduct_companion_", "")
                            for sku in selector.xpath('//div[contains(@class,"add-to-cart")]//form/@id').getall()
                            )
                
                faqs = [
                            {
                               "Question": faq.xpath(".//div[contains(@class,'customer-question')]//span/text()").get(default="").strip(),
                                "Answer": " ".join(
                                 text.strip()
                                 for text in faq.xpath(".//div[contains(@class,'csr-answer')]//text()").getall()
                                 if text.strip()
                                 )
                            }
                        for faq in selector.xpath("//div[@data-testid='expanded-question-answer']//div[contains(@class,'customer-qa')]")
                    ]
                faq_json = json.dumps(faqs, ensure_ascii=False, separators=(",", ":"))


                scripts = selector.xpath('//script[@type="application/ld+json"]//text()').getall()
                for script in scripts:
                    if "hasVariant" in script:
                        try:
                             data = json.loads(script)
            # Access the first variant image URL
                             variants = data.get("hasVariant", [])
                             if variants:
                                 image_url = variants[0].get("image", "")
                # Regex to find the number between 'products/large/' and '/...jpg'
                                 match = re.search(r'products/large/(\d+)/', image_url)
                             if match:
                                sku = match.group(1)
                                break
                        except:
                          continue
                    




        except Exception as e:
            print(f"Error fetching PDP rating for {pdp_url}: {e}")

        return {
            "product_name": item["product_name"],
            "brand":brand,
            "shipping_info":shipping_info,
            "rating": rating,
            "item_number": item["item_number"],
            "price":price,
            "price_unit":price_unit,
            "FAQ":faq_json,
            "Specifications":Specifications,
            "upc":upc,
            "pdp_url": pdp_url,
            "sku":sku,
            "related_product_skus":related_product_skus,
            "description":product_details,
            "breadcrumbs": breadcrumbs
        }

    def extract_product_items(self, html_content: str, base_url: str) -> list:
        """Extracts product name, item number, and PDP URL directly via HTML DOM XPath."""
        extracted_items = []
        seen_urls_in_page = set()

        selector = Selector(text=html_content)

        # WebstaurantStore DOM containers via XPath
        product_list = selector.xpath('//div[@data-testid="productBoxContainer"]')

        for product in product_list:
            try:
                rel_url = product.xpath('.//a[@data-testid="itemLink"]/@href | .//a/@href').get()
                if not rel_url:
                    continue

                full_url = urljoin(base_url, rel_url)
                if full_url in seen_urls_in_page:
                    continue

                raw_item_num = product.xpath(
                    'normalize-space(.//*[@data-testid="itemNumber"] | .//*[contains(@class, "item-number")])'
                ).get() or ""
                
                item_number = self.clean_item_number(raw_item_num)

                name = product.xpath(
                    'normalize-space(.//*[@data-testid="itemDescription"] | .//a[@data-testid="itemLink"])'
                ).get() or ""

                seen_urls_in_page.add(full_url)
                extracted_items.append({
                    "product_name": name,
                    "item_number": item_number,
                    "pdp_url": full_url
                })

            except Exception as e:
                print(f"Error parsing product: {e}")
                continue

        return extracted_items

    def extract_next_page(self, html_content: str, current_url: str) -> str | None:
        """Extracts next page URL using canonical link tags."""
        selector = Selector(text=html_content)
        next_href = selector.xpath('//link[@rel="next"]/@href | //a[@rel="next"]/@href').get()
        if next_href:
            return urljoin(current_url, next_href)
        return None

    def process_category(self, row: dict) -> list:
        category_name = row.get("name", "").strip()
        url = row.get("url", "").strip()

        if not category_name or not url:
            return []

        results = []
        current_url = url
        visited_pages = set()

        session = requests.Session(impersonate="chrome124")
        session.headers.update(MY_HEADERS)
        session.cookies.update(MY_COOKIES)

        print(f"\n====================\nCategory: {category_name}\nStart URL: {url}\n====================")

        while current_url:
            if current_url in visited_pages:
                break
            visited_pages.add(current_url)

            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

            try:
                response = session.get(current_url, timeout=30)
                print(f"[{response.status_code}] {current_url}")

                if response.status_code == 429:
                    print(f"[429 RATE LIMIT] Pausing 30 seconds for {current_url}")
                    time.sleep(30)
                    continue

                if response.status_code == 403:
                    print(f"[403 FORBIDDEN] DataDome cookie expired or IP blocked on {current_url}")
                    break

                if response.status_code != 200:
                    print(f"[ERROR] Failed with status {response.status_code}")
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                breadcrumbs = self.parse_breadcrumbs(soup)
                product_items = self.extract_product_items(response.text, response.url)

                print(f"   --> Found {len(product_items)} items. Requesting PDP ratings with {PRODUCT_WORKERS} product workers...")

                # --- PARALLEL WORKERS FOR PRODUCTS ON THIS PAGE ---
                with ThreadPoolExecutor(max_workers=PRODUCT_WORKERS) as pdp_executor:
                    futures = [
                        pdp_executor.submit(self.fetch_pdp_rating, session, item, breadcrumbs)
                        for item in product_items
                    ]
                    for future in as_completed(futures):
                        res = future.result()
                        if res:
                            results.append(res)

                print(f"Products Processed on Page: {len(results)}")

                current_url = self.extract_next_page(response.text, response.url)

            except Exception as e:
                print(f"Error requesting {current_url}: {e}")
                break

        return results

    def run(self):
        with open(INPUT_FILE, "r", encoding="utf-8") as infile:
            categories = list(csv.DictReader(infile))

        fieldnames = [
            "product_name",
            "brand",
            "shipping_info",
            "rating",
            "item_number",
            "price",
            "price_unit",
            "Specifications",
            "FAQ",
            "pdp_url",
            "upc",
            "sku",
            "related_product_skus",
            "description",
            "breadcrumbs"
        ]

        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            outfile.flush()

            # --- PARALLEL WORKERS FOR CATEGORIES ---
            with ThreadPoolExecutor(max_workers=CATEGORY_WORKERS) as category_executor:
                futures = [
                    category_executor.submit(self.process_category, row)
                    for row in categories
                ]

                for future in as_completed(futures):
                    category_results = future.result()
                    for record in category_results:
                        writer.writerow(record)
                    outfile.flush()

        print("\nAll categories completed! CSV saved successfully.")


if __name__ == "__main__":
    scraper = WebstaurantScraper()
    scraper.run()