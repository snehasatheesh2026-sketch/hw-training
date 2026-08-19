
import logging
import requests

from settings import (
    API_URL,
    HEADERS,
    CATEGORY_JSON_DATA,
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    MONGO_COLLECTION_DATA,
)


class Crawler:
    """Crawling Product IDs"""

    def __init__(self):

        # Category collection
        self.category_collection = client[
            MONGO_DB
        ][
            MONGO_COLLECTION_CATEGORY
        ]

        # Product ID collection
        self.product_collection = client[
            MONGO_DB
        ][
            MONGO_COLLECTION_DATA
        ]

        self.session = requests.Session()

        self.session.headers.update(
            HEADERS
        )


    def start(self):
        """Read categories from MongoDB and crawl product IDs."""

        categories = list(
            self.category_collection.find({})
        )

        logging.info(
            "Found %s categories",
            len(categories)
        )


        # Process every category

        for category in categories:

            category_name = category.get(
                "category"
            )

            category_id = category.get(
                "category_id"
            )


            if not category_name or not category_id:

                logging.warning(
                    "Invalid category: %s",
                    category
                )

                continue


            logging.info(
                "Starting category: %s | ID: %s",
                category_name,
                category_id
            )


            # Set category ID

            CATEGORY_JSON_DATA[
                "variables"
            ][
                "filters"
            ][0][
                "id"
            ] = str(category_id)


            # Start from page 0

            CATEGORY_JSON_DATA[
                "variables"
            ][
                "page"
            ] = 0


            while True:

                page = CATEGORY_JSON_DATA[
                    "variables"
                ][
                    "page"
                ]


                logging.info(
                    "Category: %s | Page: %s",
                    category_name,
                    page
                )


                try:

                    response = self.session.post(
                        API_URL,
                        headers=HEADERS,
                        json=CATEGORY_JSON_DATA,
                        timeout=30
                    )


                    logging.info(
                        "Response status: %s",
                        response.status_code
                    )


                    response.raise_for_status()


                except requests.RequestException:

                    logging.exception(
                        "Request failed | Category: %s | Page: %s",
                        category_name,
                        page
                    )

                    break


                # Parse response

                is_next = self.parse_item(
                    response,
                    category_name,
                    category_id
                )


                # No products = stop pagination

                if not is_next:

                    logging.info(
                        "Pagination completed: %s",
                        category_name
                    )

                    break


                # Next page

                CATEGORY_JSON_DATA[
                    "variables"
                ][
                    "page"
                ] += 1


    def parse_item(
        self,
        response,
        category_name,
        category_id
    ):
        """Extract product IDs."""

        try:

            response_json = response.json()

        except ValueError:

            logging.exception(
                "Invalid JSON response"
            )

            return False


        data = response_json.get(
            "data",
            {}
        )


        # Get products

        category_products = (
            data.get(
                "categoryProductList",
                {}
            ).get(
                "categoryProducts",
                []
            )
            or
            data.get(
                "products",
                {}
            ).get(
                "items",
                []
            )
        )


        # No products on this page

        if not category_products:

            return False


        # Process products

        for product in category_products:

            product_id = product.get(
                "productID"
            )


            if not product_id:

                continue


            item = {
                "product_id": str(product_id),
                "category": category_name,
                "category_id": str(category_id),
            }


            logging.info(
                "Product ID: %s | Category: %s",
                product_id,
                category_name
            )


            try:
                self.product_collection.insert_one(item)

                # self.product_collection.update_one(
                #     {
                #         "product_id": str(product_id),
                #         "category_id": str(category_id),
                #     },
                #     {
                #         "$set": item
                #     },
                #     upsert=True
                # )

            except Exception:

                logging.exception(
                    "Mongo insert failed: %s",
                    item
                )


        return True


    def close(self):
        """Close function."""

        self.session.close()


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s"
    )


    crawler = Crawler()

    try:

        crawler.start()

    finally:

        crawler.close()