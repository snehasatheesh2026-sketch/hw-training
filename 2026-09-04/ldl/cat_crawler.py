import logging
import requests
from parsel import Selector

from settings import (
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    CATGORY_URL,
    HEADERS
)

from items import ProductCategoryUrlItem
class Crawler:
    """Crawling Lidl category URLs"""

    def __init__(self):

        # MongoDB connection
        self.collection = client[MONGO_DB][MONGO_COLLECTION_CATEGORY]
        self.collection.create_index("end_category_url", unique=True)
           

        self.start_url = CATGORY_URL

        self.headers = HEADERS

    def start(self):
        

        if self.start_url:
            response = requests.get(
                self.start_url,
                headers=self.headers
            )

            if response.status_code == 200:

                end_categories = self.parse_categories(response)

                for category in end_categories:

                    item = {
                        "end_category_name": category["end_category_name"],
                        "end_category_url": category["end_category_url"]
                    }

                    logging.info(item)
                    try:
                      product = ProductCategoryUrlItem(**item)
                      print("yes")
                      product.save()
                    except Exception as e:
                        logging.exception("Error while saving item: %s", e)


                    

            else:

                logging.error(
                    f"Request failed: {response.status_code}"
                )

    def parse_categories(self, response):
        """Extract end categories"""

        selector = Selector(text=response.text)

        end_categories = []

        categories = selector.xpath(
            "//ul[contains(@class,'items') and "
            "not(ancestor::ul[contains(@class,'items-children')])]"
            "/li"
        )

        for category in categories:

            # Check if category has children
            children = category.xpath(
                "./ul[contains(@class,'items-children')]/li/a"
            )

            if children:

                # Has children -> children are end categories
                for child in children:

                    name = child.xpath(
                        "normalize-space(.//span[@class='label']/text())"
                    ).get()

                    child_url = child.xpath(
                        "./@href"
                    ).get()

                    if name and child_url:

                        end_categories.append({
                            "end_category_name": name.strip(),
                            "end_category_url": child_url.strip()
                        })

            else:

                # No children -> current category is end category
                link = category.xpath(
                    "./a[contains(@class,'no-childs')]"
                )

                name = link.xpath(
                    "normalize-space(text())"
                ).get()

                category_url = link.xpath(
                    "./@href"
                ).get()

                if name and category_url:

                    name = name.strip()

                    # Skip Alle Kategorien
                    if name == "Alle Kategorien":
                        continue

                    end_categories.append({
                        "end_category_name": name,
                        "end_category_url": category_url.strip()
                    })

        return end_categories

    def close(self):
        

        client.close()


if __name__ == "__main__":

    crawler = Crawler()

    try:
        crawler.start()
    finally:
        crawler.close()