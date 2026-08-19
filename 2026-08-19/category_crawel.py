
import logging
import requests

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


    def start(self):
        """Request category API."""

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


        categories = self.parse_categories(response)

        logging.info(
            "Found %s categories",
            len(categories)
        )


        # Insert categories into MongoDB

        for category in categories:

            item = {
                "category": category["category"],
                "category_id": category["category_id"],
            }

            try:

                result = self.collection.update_one(
                    {
                        "category_id": item["category_id"]
                    },
                    {
                        "$set": item
                    },
                    upsert=True
                )

                logging.info(
                    "Mongo category saved: %s",
                    item
                )

            except Exception:

                logging.exception(
                    "Mongo insert failed: %s",
                    item
                )


    def parse_categories(self, response):
        """Extract categories from API response."""

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


        categories = []


        for section in data:

            for item in section.get(
                "shopItems",
                []
            ):

                # Only process Category objects

                if item.get("__typename") != "Category":
                    continue


                category_name = item.get("name")

                category_id = item.get("id")


                if not category_name:
                    continue


                if not category_id:
                    continue


                # Only save required main categories

                if category_name not in MAIN_CATEGORIES:
                    continue


                category = {
                    "category": category_name,
                    "category_id": str(category_id),
                }


                categories.append(category)


        return categories


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s"
    )


    crawler = CategoryCrawler()

    crawler.start()