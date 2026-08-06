import logging
import json
import requests

from urllib.parse import urljoin, urlparse, parse_qs
from parsel import Selector

from settings import (
    HEADERS,
    COOKIES,
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    BASE_URL
)

from items import ProductCategoryUrlItem


class CategoryCrawler:

    def __init__(self):
        self.collection = client[MONGO_DB][MONGO_COLLECTION_CATEGORY]

        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.cookies.update(COOKIES)

        self.visited = set()
        self.saved = set()


    def start(self):
        try:
            response = self.session.get(BASE_URL, timeout=30)

            if response.status_code != 200:
                logging.error("Homepage failed")
                return

            selector = Selector(response.text)

            script = selector.xpath(
                '//script[@data-hypernova-key="GlobalHeader"]/text()'
            ).get()

            if not script:
                return

            data = json.loads(
                script.replace("<!--", "")
                     .replace("-->", "")
                     .strip()
            )

            for category in data.get("navDataItems", []):
                self.crawl(
                    category["displayName"],
                    urljoin(BASE_URL, category["link"])
                )

        except Exception as e:
            logging.error(e)


    def get_children(self, selector):

        result = {}

        links = selector.xpath(
            '//div[@data-testid="Photo Grid Categories"]//a[@href]'
        )

        for link in links:

            url = urljoin(
                BASE_URL,
                link.xpath("@href").get()
            )

            name = " ".join(
                x.strip()
                for x in link.xpath(".//text()").getall()
                if x.strip() and "Product" not in x
            )

            if name:
                result[url] = {
                    "name": name,
                    "url": url
                }

        return list(result.values())



    def crawl(self, name, url, depth=0):

        if url in self.visited:
            return

        self.visited.add(url)

        logging.info(
            "  " * depth + f"Crawling {name}"
        )

        try:
            response = self.session.get(
                url,
                timeout=30
            )

            if response.status_code != 200:
                return

        except Exception as e:
            logging.error(e)
            return


        selector = Selector(response.text)

        children = self.get_children(selector)


        if not children:
            self.save_category(name, url)
            item = {
                        "category_name": name,
                        "url": url
                    }
            self.saved.add(url)
            
            logging.info(item)
            try:
                self.collection.insert_one(item)
            
                product = ProductCategoryUrlItem(**item)
                product.save()
            
            except Exception as e:
                        logging.error(e)
            
            return


        for child in children:
            self.crawl(
                child["name"],
                child["url"],
                depth + 1
            )



if __name__ == "__main__":

    crawler = CategoryCrawler()
    crawler.start()