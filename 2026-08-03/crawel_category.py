
import logging
import json
from urllib.parse import urljoin, urlparse, parse_qs
from parsel import Selector
import requests
from settings import (
    HEADERS,
    COOKIES,
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    BASE_URL
)
from items import ProductCategoryUrlItem

class careiory_crawl:
    """Crawling WebstaurantStore categories and saving links to MongoDB"""

    def __init__(self):
        self.db = client[MONGO_DB]
        self.collection = MONGO_COLLECTION_CATEGORY
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.cookies.update(COOKIES)
        self.visited = set()
        self.saved_urls = set()

    def start(self):
        """Requesting Start url and traversing categories"""
        try:
            response = self.session.get(BASE_URL, timeout=30)
            if response.status_code != 200:
                logging.error(f"Failed to fetch homepage: {response.status_code}")
                return

            sel = Selector(response.text)
            script_content = sel.xpath('//script[@data-hypernova-key="GlobalHeader"]/text()').get()
            
            if script_content:
                cleaned_script = script_content.replace("<!--", "").replace("-->", "").strip()
                data = json.loads(cleaned_script)

                for item in data.get("navDataItems", []):
                    self.crawl(
                        item["displayName"],
                        urljoin(BASE_URL, item["link"])
                    )
        except Exception as e:
            logging.error(f"Error during crawling initialization: {e}")

        logging.info(f"Finished! Processed {len(self.saved_urls)} categories.")

    def get_photo_grid_links(self, sel):
        links = []
        for a in sel.xpath('//div[@data-testid="Photo Grid Categories"]//a[@href]'):
            href = a.xpath("@href").get()
            if not href:
                continue

            href = urljoin(BASE_URL, href)
            texts = [
                t.strip()
                for t in a.xpath(".//text()").getall()
                if t.strip() and "Product" not in t
            ]
            name = " ".join(texts)

            if not name:
                continue

            links.append({
                "name": name,
                "url": href
            })

        unique = {}
        for item in links:
            unique[item["url"]] = item

        return list(unique.values())

    def crawl(self, name, url, depth=0):
        if url in self.visited:
            return

        self.visited.add(url)
        logging.info("  " * depth + f"Crawling: {name}")

        try:
            response = self.session.get(url, timeout=30)
            if response.status_code != 200:
                logging.warning(f"Failed: {response.status_code} for {url}")
                return
        except Exception as e:
            logging.error(f"Error requesting {url}: {e}")
            return

        sel = Selector(response.text)
        photo_grid = sel.xpath('//div[@data-testid="Photo Grid Categories"]')

        def is_valid_new_url(target_url):
            parsed = urlparse(target_url)
            query = parse_qs(parsed.query)

            if "page" in query:
                return False

            if target_url in self.saved_urls:
                return False

            return True

        if not photo_grid:
            if (
                is_valid_new_url(url)
                and "Category" not in name
                and "Categories" not in name
            ):
                self.saved_urls.add(url)
                
                item = {
                    "category_name": name,
                    "url": url
                }
                
                logging.info(item)
                try:
                    self.db[self.collection].insert_one(item)
                    product_item = ProductCategoryUrlItem(**item)
                    product_item.save()
                except Exception:
                    pass

            return

        children = self.get_photo_grid_links(sel)

        if not children:
            if (
                is_valid_new_url(url)
                and "Category" not in name
                and "Categories" not in name
            ):
                self.saved_urls.add(url)
                
                item = {
                    "category_name": name,
                    "url": url
                }
                
                logging.info(item)
                try:
                    self.db[self.collection].insert_one(item)
                    product_item = ProductCategoryUrlItem(**item)
                    product_item.save()
                except Exception:
                    pass

            return

        for child in children:
            self.crawl(
                child["name"],
                child["url"],
                depth=depth + 1
            )

    def close(self):
        """Close function for all module object closing"""
        pass


if __name__ == "__main__":
    crawler = careiory_crawl()
    crawler.start()
    crawler.close()