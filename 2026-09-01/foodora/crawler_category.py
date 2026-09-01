
import logging
import requests
from items import ProductCategoryUrlItem
from settings import (
    API_URL,
    HEADERS,
    JSON_DATA,
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    MAIN_CATEGORIES,
)


class CategoryCrawler:

    def __init__(self):

        self.collection = client[MONGO_DB][MONGO_COLLECTION_CATEGORY]

        self.session = requests.Session()

        self.session.headers.update(HEADERS)

        self.collection.create_index("category_id",unique=True)

    def start(self):


        try:

            response = self.session.post(
                API_URL,
                headers=HEADERS,
                json=JSON_DATA,
                timeout=30
            )

            logging.info(
                "Response status: %s",
                response.status_code
            )

            response.raise_for_status()

        except requests.RequestException:

            logging.exception(
                "API request failed"
            )

            return


        self.parse_categories(response)

        
            
    def parse_categories(self, response):


        try:

            response_json = response.json()

        except ValueError:

            logging.exception(
                "Invalid JSON response"
            )

            return []


        data = (
            response_json
            .get("data", {})
            .get("shopDetails", {})
            .get("shopItemsResponse", {})
            .get("shopItemsList", [])
        )

        for section in data:

            for item in section.get(
                "shopItems",
                []
            ):

                if item.get("__typename") != "Category":
                    continue

                category_name = item.get("name")

                category_id = item.get("id")


                if not category_name:
                    continue

                if not category_id:
                    continue

                if category_name not in MAIN_CATEGORIES:
                    continue


                items = {
                    "category": category_name,
                    "category_id": category_id,
                }

                try:
                
                  product = ProductCategoryUrlItem(**items)
                  product.save()

                  logging.info( "Mongo category saved: %s",items)
                
                except Exception:
                
                  logging.exception( "Mongo insert failed: %s",items)
                
                
if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s"
    )


    crawler = CategoryCrawler()

    crawler.start()