
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
CATEGORY_WORKERS =  2

# Product level parallel workers (Parallel PDP fetches per page)
PRODUCT_WORKERS = 2

# Delays between requests (in seconds)
MIN_DELAY = 0.5
MAX_DELAY = 1.0

MY_HEADERS =  {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'if-modified-since': 'Tue, 21 Jul 2026 10:53:25 GMT',
    'priority': 'u=0, i',
    'referer': 'https://www.webstaurantstore.com/hometown-provisions-dark-vanilla-syrup-1-gallon/999VANLDKGAL.html?__cf_chl_tk=ZX6wSqq6RjhF0OFkS9nYMmLrIeingCqjl0d_GEqjKqo-1784627425-1.0.1.1-7YbEIow3El.W7h_Cu.l.az7q4tnId9qprXb5e1i9sUw',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"148.0.7778.96"',
    'sec-ch-ua-full-version-list': '"Chromium";v="148.0.7778.96", "Google Chrome";v="148.0.7778.96", "Not/A)Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '""',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 'cookie': '_gcl_au=1.1.343074361.1784263975; _ga=GA1.1.157084933.1784263975; DATACENTER_ID=2; SESSION_ID=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; CFID=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; CFTOKEN=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; ajs_anonymous_id=990d3e68-b523-4501-abde-92b640dd5dcf; newVariationId=701:a; _fbp=fb.1.1784263976434.315661878923442003; _pin_unauth=dWlkPU16WmtZMlkyT0RjdE5UZzBPQzAwWkRoa0xUaGhZV1F0WkRVNE5UZ3lOR0kxTkdVNQ; REFERERSOURCE=%7B%22referer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22details%22%3A%7B%7D%2C%22entryDate%22%3A%2207%2F19%2F26%22%2C%22entryTime%22%3A%2223%3A06%22%7D; _cfuvid=9onZNHM6k_H4YgHs.lSAhJzoVixQTjrS.RyjwrpCi6Q-1784596110.6371481-1.0.1.1-l.AIdOoyl8ptvV_1nI.FB9.DkWtdExl5.I3J5PFnnfA; CreditKeyPublicKey=thewebstaurantstoreinc_dcf536bfabb748999f1bf57dda2630c6; CreditKeyPdpMinimumDisplayPrice=500; CSRF_TOKEN=9D78C4DDA9CFF9490516D83985B3F791B37356E2; _clck=1c06vir%5E2%5Eg7x%5E0%5E2389; eligibleABTestLimit=21; cf_clearance=qmiyKMyGtxJ1D9sTgVaLKvA3RWpMLAYwXm5OjmU7svI-1784631205-1.2.1.1-FC.aP7LtIZWXNhhNHmUm3__QhYvoUGwO65Yw__TtgMjD5V1GE1XhtP9CEXIBpHR.W9aT2bAonoJi9bghH.p_dSLr7ps1jMah4rMChF2vvR0vjIAJk0kFph_ACqeS_sibUftDE8cRVKxgJrRvpZTAwGLMAN6yK5LVanppwppMJOd_s8427EGyoVRZqVCHfEJ02JoZ0kwTJKTJTXl5_MMMHb.7FrE7u3wHoF_LA5dg5IxA69alaF8BNKVtZ0yVdM8hd5XNavz9QTiOD1fAzQjaINK.XsVvfrpPb1dKCf_4vjBWkDnIpZw7dXibxIbWbSpevfECE3zjkWmnHKlmwzL_ZiTa2gAESlUC.C_fbxwg9pyzJOSSjwZG9kX7IhtDWkkJpTzKiBwIRrcfXwbqGJevh1k3WfoNhCNT.zWdTY0BS45.3Nqo6zKjWf7a9jQdjbQZ_w1slDKG9Jxg2mwOHbrpco4hnQt_jw1Q3mkYGgkIPpHntMFUP3M9dFEoEa6zQOTj; CFGLOBALS=urltoken%3DCFID%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%26CFTOKEN%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23lastvisit%3D%7Bts%20%272026%2D07%2D21%2006%3A54%3A45%27%7D%23hitcount%3D1%23timecreated%3D%7Bts%20%272026%2D07%2D21%2006%3A54%3A45%27%7D%23cftoken%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23cfid%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23; _ga_ZFM16S3J5F=GS2.1.s1784631285$o14$g0$t1784631285$j60$l0$h452226325; _uetsid=736e9eb083d411f1b043c14401650a85; _uetvid=5fbbe750819b11f1ab46f1dd31c9ba10; _clsk=1mdam27%5E1784633406477%5E1%5E0%5Ef.clarity.ms%2Fcollect',
}



MY_COOKIES  =  {
    '_gcl_au': '1.1.343074361.1784263975',
    '_ga': 'GA1.1.157084933.1784263975',
    'DATACENTER_ID': '2',
    'SESSION_ID': '74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e',
    'CFID': '74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e',
    'CFTOKEN': '74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e',
    'ajs_anonymous_id': '990d3e68-b523-4501-abde-92b640dd5dcf',
    'newVariationId': '701:a',
    '_fbp': 'fb.1.1784263976434.315661878923442003',
    '_pin_unauth': 'dWlkPU16WmtZMlkyT0RjdE5UZzBPQzAwWkRoa0xUaGhZV1F0WkRVNE5UZ3lOR0kxTkdVNQ',
    'REFERERSOURCE': '%7B%22referer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22details%22%3A%7B%7D%2C%22entryDate%22%3A%2207%2F19%2F26%22%2C%22entryTime%22%3A%2223%3A06%22%7D',
    '_clck': '1c06vir%5E2%5Eg7x%5E0%5E2389',
    'eligibleABTestLimit': '21',
    'cf_clearance': 'BN6T.dB1_e8_CvhXS9P4KvWMvcvHxU9fgjSwlzXVUao-1784654073-1.2.1.1-Mje_k1ww9yVXFmjuYjFkMCs8C_zFkBafJ6DzAnyIMjD8CNytJYLf5jg6PPrcmnSJrQqQytRxK7WwJx.1CguKxrybA7ZJ2LK6cF2gldXCGIqoRnlepU6fJZBR2RreX0PMDmxdWJEVvLt9itH6cPebxkPYwDPyonaj4HwBaxYB7QFsqdNH3VIG4EHdKsXHl0KO0zpUDhE3dTk8x8Cg1fuCpBT3e7wKvSdNBoG5hpBe4m2ZFX3B_lIpr8JAkwEILtd63ygLKrZsPyZ8TOJlpe20lLLPPRXeizQ0OQiNuDO.Z_AiZxYXoYw7pNqedVR_..uWzC0XNdFyjUl2tAtEuMeg7sPQekY9z37wL9xI9UUVGh8oYmxreVjcVxv0T4_4kmaPKgmFcGIOuwbRPbkNKv8Bp1C71bykspwU9xxVyHtlSAhHzANjvkbkauGf_3XJGOyegT42NIWnXqr7ERgmOZKnjp3kXHydxv4MSteRev3m9w2qrNLpRWV9dIfO9_mxeH1s',
    '__cf_bm': 'e6V6oKIErf090aeQfej7uTO1O6xs57IswAbSLvUZYpo-1784654073.1191044-1.0.1.1-mNDR1bR9RJqY00KcEzdJHZbGJ1PFpY0gC2zJ3jCIn3NOLwEV3DUD3OflQaiReL_VcZvgbnQ826imxDPjDkpTxju6FdKfOK6FY..6CwFIEDnEZ7UsuOVVaNj_TLBVp6yX',
    '_cfuvid': 'XOBZyoN7tnHPoVoybUjYp8iUA_CBEjgeEdgn7zRYUPs-1784654073.2626238-1.0.1.1-RJ3LjBZvEfD30KLcGebMG7vya0_Oo68DCMPq2FvsWQ0',
    'CSRF_TOKEN': '86E178424A709E2676DE004F2F6A764A9FB4C1E7',
    'CFGLOBALS': 'urltoken%3DCFID%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%26CFTOKEN%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23lastvisit%3D%7Bts%20%272026%2D07%2D21%2001%3A14%3A35%27%7D%23hitcount%3D1%23timecreated%3D%7Bts%20%272026%2D07%2D21%2001%3A14%3A35%27%7D%23cftoken%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23cfid%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23',
    '_uetsid': '736e9eb083d411f1b043c14401650a85',
    '_uetvid': '5fbbe750819b11f1ab46f1dd31c9ba10',
    '_clsk': '1e3qizl%5E1784654076732%5E1%5E1%5Ee.clarity.ms%2Fcollect',
    '_ga_ZFM16S3J5F': 'GS2.1.s1784654075$o17$g0$t1784654084$j51$l0$h647666720',
}






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
        """Helper task for worker threads: Requests PDP page and extracts rating and details."""
        pdp_url = item["pdp_url"]
        productnameof = item["product_name"]
        itemsnumberof = item["item_number"]
        variant_list = ""
        rating =""
        price = ""
        price_unit =""
        brand = ""
        sku = ""
        related_product_skus =""
        faq_json=""
        Features= ""
        models = ""
        intro_headline = ""
        description = ""
        product_details =""
        shipping_info = ""
        upc = ""
        Specifications = ""
        video = ""
        product_documents = ""
        Product_Image_URLs = ""
        sku = ""
        result =""
        Selected_Variant = {}
        configurable_attributes = []

        image_urls = []
        variants = {}

        with self.lock:
            if pdp_url in self.seen_pdp_urls:
                return None
            self.seen_pdp_urls.add(pdp_url)

        try:
            time.sleep(random.uniform(0.5, 1.0))

            response = session.get(pdp_url, timeout=20)

            if response.status_code != 200:
                return None

            selector = Selector(text=response.text)



            

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
            price_container = selector.xpath(
                '//*[@data-testid="price-container"]'
            )

            if price_container:
                raw_unit = price_container.xpath(
                    'normalize-space(.//span[contains(@class,"pr-1")] | .//span/span)'
                ).get() or ""

                price_unit = raw_unit.replace("/", "").strip()

                full_price_text = price_container.xpath(
                    'normalize-space(.)'
                ).get() or ""

                if raw_unit:
                    price = full_price_text.replace(
                        raw_unit, ""
                    ).replace("$", "").strip()
                else:
                    price = full_price_text.replace("$", "").strip()

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
                s.replace("relatedproduct_companion_", "")
                for s in selector.xpath(
                    '//div[contains(@class,"add-to-cart")]//form/@id'
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

            faq_json = json.dumps(
                faqs,
                ensure_ascii=False,
                separators=(",", ":")
            if faqs else '""')

            # ---------------- SKU from JSON LD ----------------
            for script in selector.xpath('//script/text()').getall():
              if "productTemplates" in script:
                    
                try:
                 

                    script = script.strip()

                    script = script.removeprefix("<!--").removesuffix("-->").strip()

                    data = json.loads(script)

                    product = data["productTemplates"][0]

                    sku = str(product.get("itemNumberId", ""))

                    break
                except:

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

                for item in group.get("variationGroupItems", []):
                    skus = str(item.get("itemNumberId", ""))

                    if not skus:
                        continue
                    variants.setdefault(skus, {"sku": skus})
                    variants[skus][attr] = item.get("variationText", "")
            result = list(variants.values())

    
            # ---------------- 3D Models ----------------
            model_list = []

            for script in selector.xpath(
                '//script[@type="application/ld+json"]/text()'
            ).getall():
                try:
                    data = json.loads(script.strip())
                    if data.get("@type") == "3DModel":
                        for obj in data.get("encoding", []):
                            url = obj.get(
                                "contentUrl"
                            )
                            if url:
                                model_list.append(
                                    url.lstrip("/")
                                )
                except json.JSONDecodeError:
                    continue

            models = ",".join(model_list) if model_list else ""

        except Exception as e:
            print(
                f"Error fetching PDP rating for {pdp_url}: {e}"
            )

        return {
            "product_name":productnameof,
            "brand": brand,
            "shipping_info": shipping_info,
            "rating": rating,
            "item_number": itemsnumberof,
            "price": price,
            "price_unit": price_unit,
            "FAQ": faq_json ,
            "Specifications": Specifications,
            "Selected_Variant": Selected_Variant,
            "configurable_attributes": configurable_attributes,
            "Features": Features,
            "Video_URLs": video,
            "upc": upc,
            "pdp_url": pdp_url,
            "sku": sku,
            "Image_URLs":Product_Image_URLs,
            "Configurable Variations":result,
            "related_product_skus": related_product_skus,
            "Product_Documents": product_documents,
            "3D_Asset_URLs": models,
            "description": product_details,
            "Category": breadcrumbs
        }

    def extract_product_items(self, html_content: str, base_url: str) -> list:
        """Extracts product name, item number, and PDP URL directly via HTML DOM XPath."""
        extracted_items = []
        seen_urls_in_page = set()

        selector = Selector(text=html_content)
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
            "Selected_Variant",
            "configurable_attributes",
            "Features",
            "Video_URLs",
            "FAQ",
            "pdp_url",
            "Image_URLs",
            "upc",
            "sku",
            "related_product_skus",
            "Configurable Variations",
            "Product_Documents",
            "3D_Asset_URLs",
            "description",
            "Category"
        ]

        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            outfile.flush()

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






    