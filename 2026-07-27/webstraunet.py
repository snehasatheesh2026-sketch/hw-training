import csv
import json
import random
import time
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from urllib.parse import urljoin

from curl_cffi import requests
from parsel import Selector

# =====================================================================
# CONFIGURATION
# =====================================================================

INPUT_FILE = "categories.csv"
OUTPUT_FILE = "output_products4.csv"

# Safe concurrency settings to prevent triggering DataDome / 403 blocks
CATEGORY_WORKERS = 1
PRODUCT_WORKERS = 5

# Realistic delays to mimic human traffic safely
MIN_DELAY = 0.1
MAX_DELAY = 0.2

MAX_RETRIES = 5

MY_HEADERS  = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    

}


MY_COOKIES = {
      }

# Thread-local storage to maintain persistent sessions per thread with request counters
thread_local = threading.local()

# Lock and timestamp tracking for rate-limiting global cookie refreshes
cookie_lock = threading.Lock()
last_cookie_refresh = 0
COOKIE_REFRESH_INTERVAL = 60  # seconds


def refresh_cookies():
    """Actively pings the target site to fetch brand-new dynamic anti-bot/session cookies."""
    session = requests.Session(impersonate="chrome124")
    session.headers.update(MY_HEADERS)
    session.cookies.update(MY_COOKIES)

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
    """Thread-safely refreshes and updates the global MY_COOKIES dictionary with cooldown checks and dynamic subset validation."""
    global last_cookie_refresh
    with cookie_lock:
        if time.time() - last_cookie_refresh < COOKIE_REFRESH_INTERVAL:
            print("Cookie refresh skipped (cooldown active).")
            return

        new = refresh_cookies()
        
        # Dynamically ensure all previously established required keys are present
        required = set(MY_COOKIES.keys())
        
        if new and (not required or required.issubset(new.keys())):
            MY_COOKIES.clear()
            MY_COOKIES.update(new)
            last_cookie_refresh = time.time()
            print("Global cookies updated successfully.")
        else:
            print("Cookie refresh failed or missing required session keys - keeping existing cookies.")


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
        self.row_buffer = []
        self.buffer_lock = Lock()
        self.file_initialized = False
        self.file_lock = Lock()

    def clean_item_number(self, raw_str: str) -> str:
        """Strips out unwanted label prefixes like 'Item number#'."""
        if not raw_str:
            return ""
        
        cleaned = raw_str.replace("Item number#", "").replace("Item #", "").replace("Item number:", "").replace("Item:", "")
        return cleaned.strip()

    def flush_buffer_to_csv(self, force=False):
        """Batch writes accumulated rows to CSV using an optimized buffer pattern."""
        with self.buffer_lock:
            if len(self.row_buffer) >= 50 or (force and self.row_buffer):
                rows_to_write = list(self.row_buffer)
                self.row_buffer.clear()
            else:
                return

        if rows_to_write:
            with self.file_lock:
                mode = "a"
                try:
                    with open(OUTPUT_FILE, mode, newline="", encoding="utf-8") as csvfile:
                        fieldnames = list(rows_to_write[0].keys())
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        
                        if csvfile.tell() == 0:
                            writer.writeheader()
                        
                        for row in rows_to_write:
                            formatted_row = {
                                k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                                for k, v in row.items()
                            }
                            writer.writerow(formatted_row)
                    self.file_initialized = True
                except Exception as e:
                    print(f"Error writing to CSV: {e}")

    def fetch_pdp_rating(self, item: dict, breadcrumbs: str) -> dict | None:
        """Helper task for worker threads: Requests PDP page and extracts rating and details using its own thread-safe session."""
        pdp_url = item["pdp_url"]
        
        with self.lock:
            if pdp_url in self.seen_pdp_urls:
                return None
            self.seen_pdp_urls.add(pdp_url)

        product_name = ""
        itemsnumberof = str(item["item_number"])
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
                time.sleep(0.1)
                response = session.get(pdp_url, timeout=20)

                if response.status_code == 429:
                    print(f"[429 RATE LIMIT] PDP Pausing 30 seconds for {pdp_url}")
                    response.close()
                    time.sleep(30)
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
                # documents = selector.xpath(
                #     '//div[@id="resources-group"]//a/@href'
                # ).getall()

                documents = [
                          url for url in selector.xpath(
                    '//div[@id="resources-group"]//a/@href'
                             ).getall()
                             if url.lower().endswith((
                                  ".pdf",
                                   ".doc",
                                    ".docx",
                                     ".xls",
                                      ".xlsx",
                                        ".ppt",
                                     ".pptx",
                                       ".zip"
                                          ))
                                              ]


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

                # # ---------------- Rating ----------------
                raw_rating = selector.xpath('//span[@data-testid="zest-ratings-sr"]/text()').get() or ""

                print("RAW RATING:", repr(raw_rating))

                match = re.search(r'(\d+(?:\.\d+)?)', raw_rating)
                rating = match.group(1) if match else ""

                print("EXTRACTED RATING:", rating)

               # ---------------- Price ----------------
                # price_container = selector.xpath('//*[@data-testid="price-container"]')

                # if price_container:
                #     full_price_text = " ".join(t.strip() for t in price_container.xpath(".//text()").getall() if t.strip())
                
                # price_match = re.search(r"\$?\s*([\d,]+(?:\.\d+)?)", full_price_text)
                # if price_match:
                #     price = price_match.group(1).replace(",", "")
                
                # unit_match = re.search(r"/\s*([A-Za-z0-9 .-]+)", full_price_text)
                # if unit_match:
                #     price_unit = unit_match.group(1).strip()


                price_container = (selector.xpath('//*[@data-testid="price-container"]') or selector.xpath('//div[contains(@class,"map__price")]'))
                
                if price_container:
                    full_price_text = " ".join(t.strip() for t in price_container.xpath(".//text()").getall() if t.strip()
                                            )
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
                upc = str(selector.xpath(
                    'normalize-space(.//*[@data-testid="UPC-Number"])'
                ).get() or "")

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
                related_product_skus =str (",".join(
                    s.split("relatedproduct_companion_")[-1]
                    for s in selector.xpath(
                    '//div[contains(@class,"add-to-cart")]//form[starts-with(@id,"relatedproduct_companion_")]/@id'
                    ).getall()
                ))

                # ---------------- FAQ ----------------
                # faqs = []

                # for faq in selector.xpath(
                #     "//div[@data-testid='expanded-question-answer']"
                #     "//div[contains(@class,'customer-qa')]"
                # ):
                #     faqs.append({
                #         "Question": faq.xpath(
                #             ".//div[contains(@class,'customer-question')]//span/text()"
                #         ).get(default="").strip(),

                #         "Answer": " ".join(
                #             t.strip()
                #             for t in faq.xpath(
                #                 ".//div[contains(@class,'csr-answer')]//text()"
                #             ).getall()
                #             if t.strip()
                #         )
                #     })

                # faqs = []

                # for faq in selector.xpath( "//div[@data-testid='expanded-question-answer']//div[contains(@class,'customer-qa')]"):

                #     question = faq.xpath(".//div[contains(@class,'customer-question')]//span/text()").get(default="").strip()

                #     answer = " ".join(t.strip()for t in faq.xpath(  ".//div[contains(@class,'csr-answer')]//text()" ).getall() if t.strip())

                #     if question and answer:
                #         faqs.append({
                #          "Question": question,
                #              "Answer": answer
                #                      })

                # if faqs:
                #     faq_json = json.dumps(faqs, ensure_ascii=False, separators=(",", ":"))
                # else:
                #     faq_json = ""

                faqs = []
                seen = set()


                for faq in selector.xpath("//div[contains(@class,'customer-qa')]"):
                    question = faq.xpath(
                            "normalize-space(.//div[contains(@class,'customer-question')])"
                              ).get(default="")

                    answer = " ".join(
                                    t.strip()
                                       for t in faq.xpath(
                                        ".//div[contains(@class,'csr-answer')]//text()"
                                       ).getall()
                                        if t.strip()
                                    )
                    
                    if question and answer:
                            key = (question, answer)
                            if key not in seen:
                                seen.add(key)   

                                faqs.append({
                            "Question": question,
                             "Answer": answer
                             })
                faq_json = json.dumps(faqs, ensure_ascii=False, separators=(",", ":")) if faqs else ""


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
                    for href in selector.xpath('//div[@data-testid="main-slider-item"]//img/@src').getall():
                        if f"/products/large/{sku}/" in href:
                            match = re.search(r'(images/products/large/.*)', href)
                            if match:
                                image_urls.append(match.group(1))

                image_urls = list(dict.fromkeys(image_urls))
                Product_Image_URLs = ",".join(image_urls)if image_urls else ""

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
                time.sleep(min(2 ** retry, 0.5))
        
        # itemsnumberof = str(itemsnumberof)
        # upc = str(upc)
        # related_product_skus = str(related_product_skus)
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
                            time.sleep(min(2 ** retry, 30))
                            continue
                        else:
                            break
                    except Exception:
                        if response:
                            response.close()
                            response = None
                        time.sleep(min(2 ** retry, 30))
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
                        with self.buffer_lock:
                            self.row_buffer.append(res)
                        page_processed_count += 1
                        self.flush_buffer_to_csv()

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

        self.flush_buffer_to_csv(force=True)

    def run(self):
        with open(INPUT_FILE, "r", encoding="utf-8") as infile:
            categories = list(csv.DictReader(infile))

        with ThreadPoolExecutor(max_workers=PRODUCT_WORKERS) as pdp_executor:
            with ThreadPoolExecutor(max_workers=CATEGORY_WORKERS) as category_executor:
                futures = [
                    category_executor.submit(self.process_category, row, pdp_executor)
                    for row in categories
                ]

                for future in as_completed(futures):
                    future.result()

        self.flush_buffer_to_csv(force=True)
        print(f"\nAll categories completed! Data saved successfully to {OUTPUT_FILE}.")


if __name__ == "__main__":
    scraper = WebstaurantScraper()
    scraper.run()