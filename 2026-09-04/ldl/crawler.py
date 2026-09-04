

# ------------------------------------------------------------------------------------------------------------------------------
# import logging
# import requests

# from parsel import Selector

# from settings import (
#     client,
#     MONGO_DB,
#     MONGO_COLLECTION_CATEGORY,
#     MONGO_COLLECTION_DATA,
#     HEADERS,
# )


# class Crawler:
#     """Crawling Lidl Products"""

#     def __init__(self):

#         # --------------------------------
#         # MONGODB
#         # --------------------------------

#         self.db = client[MONGO_DB]

#         self.category_collection = self.db[
#             MONGO_COLLECTION_CATEGORY
#         ]

#         self.data_collection = self.db[
#             MONGO_COLLECTION_DATA
#         ]

#         # --------------------------------
#         # UNIQUE PRODUCT URL
#         # --------------------------------

#         self.data_collection.create_index(
#             "product_url",
#             unique=True
#         )

#         # --------------------------------
#         # HEADERS
#         # --------------------------------

#         self.headers = HEADERS.copy()

#     # ==========================================================
#     # START
#     # ==========================================================

#     def start(self):
#         """Request category URLs and handle pagination"""

#         # --------------------------------
#         # GET END CATEGORIES FROM MONGODB
#         # --------------------------------

#         categories = self.category_collection.find(
#             {},
#             {
#                 "end_category_name": 1,
#                 "end_category_url": 1
#             }
#         )

#         # --------------------------------
#         # LOOP CATEGORIES
#         # --------------------------------

#         for category in categories:

#             category_name = category.get(
#                 "end_category_name"
#             )

#             category_url = category.get(
#                 "end_category_url"
#             )

#             if not category_url:
#                 continue

#             # --------------------------------
#             # CATEGORY META
#             # --------------------------------

#             meta = {}

#             meta["category"] = category_name
#             meta["category_url"] = category_url

#             # --------------------------------
#             # FIRST URL
#             # --------------------------------

#             current_url = category_url

#             logging.info("")
#             logging.info(
#                 "############################################"
#             )
#             logging.info(
#                 f"START CATEGORY : {category_name}"
#             )
#             logging.info(
#                 f"START URL      : {category_url}"
#             )
#             logging.info(
#                 "############################################"
#             )

#             # --------------------------------
#             # PAGINATION
#             # --------------------------------

#             while current_url:

#                 logging.info("")
#                 logging.info(
#                     "============================================"
#                 )
#                 logging.info(
#                     f"PROCESSING CATEGORY : {category_name}"
#                 )
#                 logging.info(
#                     f"PROCESSING URL      : {current_url}"
#                 )
#                 logging.info(
#                     "============================================"
#                 )

#                 # --------------------------------
#                 # REFERER
#                 # --------------------------------

#                 self.headers["referer"] = category_url

#                 # --------------------------------
#                 # REQUEST
#                 # --------------------------------

#                 try:

#                     response = requests.get(
#                         current_url,
#                         headers=self.headers,
#                         timeout=30
#                     )

#                 except Exception as e:

#                     logging.error(
#                         f"Request error: {e}"
#                     )

#                     break

#                 # --------------------------------
#                 # RESPONSE CHECK
#                 # --------------------------------

#                 if response.status_code != 200:

#                     logging.error(
#                         f"Request failed: "
#                         f"{response.status_code}"
#                     )

#                     logging.error(
#                         f"URL: {current_url}"
#                     )

#                     break

#                 # --------------------------------
#                 # PARSE CURRENT PAGE
#                 # --------------------------------

#                 next_page = self.parse_item(
#                     response,
#                     meta
#                 )

#                 # --------------------------------
#                 # NO NEXT PAGE
#                 # --------------------------------

#                 if not next_page:

#                     logging.info("")
#                     logging.info(
#                         "Pagination completed"
#                     )

#                     logging.info(
#                         f"Category: {category_name}"
#                     )

#                     logging.info(
#                         f"Last URL: {current_url}"
#                     )

#                     break

#                 # --------------------------------
#                 # NEXT PAGE
#                 # --------------------------------

#                 logging.info("")
#                 logging.info(
#                     f"NEXT PAGE: {next_page}"
#                 )

#                 current_url = next_page

#     # ==========================================================
#     # PARSE ITEM
#     # ==========================================================

#     def parse_item(self, response, meta):
#         """
#         Extract products from current page.

#         Also finds the next page URL.

#         Pagination request itself is handled
#         inside start().
#         """

#         selectors = Selector(
#             text=response.text
#         )

#         # --------------------------------
#         # PRODUCT LIST
#         # --------------------------------

#         product_list = selectors.xpath(
#             '//div[@class="product-item-info"]'
#         )

#         # --------------------------------
#         # NO PRODUCTS
#         # --------------------------------

#         if not product_list:

#             logging.info(
#                 "No products found on this page"
#             )

#             return None

#         logging.info(
#             f"Found {len(product_list)} products"
#         )

#         # --------------------------------
#         # LOOP PRODUCTS
#         # --------------------------------

#         for product in product_list:

#             try:

#                 # --------------------------------
#                 # IMAGES
#                 # --------------------------------

#                 images = product.xpath(
#                     './/img/@data-lazy'
#                 ).getall()

#                 images = [
#                     image.strip()
#                     for image in images
#                     if image and image.strip()
#                 ]

#                 # --------------------------------
#                 # PRODUCT NAME
#                 # --------------------------------

#                 product_name = product.xpath(
#                     'normalize-space('
#                     './/strong['
#                     '@class="product name '
#                     'product-item-name"'
#                     '])'
#                 ).get()

#                 # --------------------------------
#                 # PRODUCT PRICE
#                 # --------------------------------

#                 product_price = product.xpath(
#                     './/strong['
#                     '@itemprop="price"'
#                     ']/@content'
#                 ).get()

#                 # --------------------------------
#                 # DESCRIPTION
#                 # --------------------------------

#                 description = product.xpath(
#                     './/div['
#                     'contains('
#                     '@class,'
#                     '"product-item-description"'
#                     ')]/text()'
#                 ).get(
#                     default=""
#                 )

#                 description = (
#                     description
#                     .strip()
#                     .replace(
#                         ":",
#                         ","
#                     )
#                 )

#                 # --------------------------------
#                 # PRODUCT URL
#                 # --------------------------------

#                 product_url = product.xpath(
#                     './/a['
#                     'contains('
#                     '@class,'
#                     '"product-item-link"'
#                     ')]/@href'
#                 ).get()

#                 # --------------------------------
#                 # ITEM
#                 # --------------------------------

#                 item = {

#                     "end_category_name":
#                         meta.get(
#                             "category"
#                         ),

#                     "end_category_url":
#                         meta.get(
#                             "category_url"
#                         ),

#                     "product_name":
#                         product_name,

#                     "website":
#                         "lidl.ch",

#                     "product_price":
#                         product_price,

#                     "image1":
#                         images[0]
#                         if len(images) > 0
#                         else "",

#                     "image2":
#                         images[1]
#                         if len(images) > 1
#                         else "",

#                     "image3":
#                         images[2]
#                         if len(images) > 2
#                         else "",

#                     "description":
#                         description,

#                     "product_url":
#                         product_url
#                 }

#                 # --------------------------------
#                 # LOG PRODUCT
#                 # --------------------------------

#                 logging.info(
#                     f"PRODUCT NAME : {product_name}"
#                 )

#                 logging.info(
#                     f"PRODUCT URL  : {product_url}"
#                 )

#                 logging.info(
#                     f"PRICE        : {product_price}"
#                 )

#                 # --------------------------------
#                 # CHECK PRODUCT URL
#                 # --------------------------------

#                 if not product_url:

#                     logging.warning(
#                         "Product URL missing. "
#                         "Skipping product."
#                     )

#                     continue

#                 # --------------------------------
#                 # MONGODB INSERT
#                 # --------------------------------

#                 try:

#                     result = (
#                         self.data_collection.insert_one(
#                             item
#                         )
#                     )

#                     logging.info(
#                         f"INSERTED: {product_name}"
#                     )

#                 except Exception as e:

#                     # --------------------------------
#                     # DUPLICATE
#                     # --------------------------------

#                     if (
#                         "duplicate key"
#                         in str(e).lower()
#                     ):

#                         logging.info(
#                             f"ALREADY EXISTS: "
#                             f"{product_url}"
#                         )

#                     else:

#                         logging.error(
#                             f"MongoDB error: {e}"
#                         )

#             except Exception as e:

#                 logging.error(
#                     f"Product Error: {e}"
#                 )

#         # ==================================================
#         # NEXT PAGE
#         # ==================================================

#         next_page = selectors.xpath(
#             '//a[contains(@class,"next")]/@href'
#         ).get()

#         # --------------------------------
#         # NEXT PAGE EXISTS
#         # --------------------------------

#         if next_page:

#             next_page = next_page.strip()

#             logging.info(
#                 f"NEXT PAGE FOUND: {next_page}"
#             )

#             return next_page

#         # --------------------------------
#         # NO NEXT PAGE
#         # --------------------------------

#         logging.info(
#             "NO NEXT PAGE FOUND"
#         )

#         return None

#     # ==========================================================
#     # CLOSE
#     # ==========================================================

#     def close(self):
#         """Close MongoDB connection"""

#         client.close()


# # ==============================================================
# # MAIN
# # ==============================================================

# if __name__ == "__main__":

#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s %(levelname)s: %(message)s"
#     )

#     crawler = Crawler()

#     try:

#         crawler.start()

#     finally:

#         crawler.close()
# ----------------------------------------------------------------------------------------------------------------------


import logging
import requests

from parsel import Selector

from settings import (
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    MONGO_COLLECTION_DATA,
    HEADERS,
)


class Crawler:
    """Crawling Lidl Products"""

    def __init__(self):

        # MongoDB connection
        self.db = client[MONGO_DB]

        self.category_collection = self.db[
            MONGO_COLLECTION_CATEGORY
        ]

        self.data_collection = self.db[
            MONGO_COLLECTION_DATA
        ]

        # Unique product URL
        self.data_collection.create_index(
            "product_url",
            unique=True
        )

        self.headers = HEADERS.copy()

    def start(self):
        """Request category URLs and handle pagination"""

        # -----------------------------------------
        # GET END CATEGORIES FROM MONGODB
        # -----------------------------------------

        categories = self.category_collection.find(
            {},
            {
                "end_category_name": 1,
                "end_category_url": 1
            }
        )

        # -----------------------------------------
        # LOOP THROUGH CATEGORIES
        # -----------------------------------------

        for category in categories:

            category_name = category.get(
                "end_category_name"
            )

            category_url = category.get(
                "end_category_url"
            )

            if not category_url:
                continue

            # -----------------------------------------
            # META
            # -----------------------------------------

            meta = {}

            meta["category"] = category_name
            meta["category_url"] = category_url

            # -----------------------------------------
            # FIRST PAGE
            # -----------------------------------------

            api_url = category_url

            logging.info(
                f"Starting category: {category_name}"
            )

            logging.info(
                f"URL: {api_url}"
            )

            # -----------------------------------------
            # PAGINATION
            # ALL PAGINATION IS HERE
            # -----------------------------------------

            while True:

                logging.info(
                    f"Processing page URL: {api_url}"
                )

                self.headers["referer"] = category_url

                # -----------------------------------------
                # REQUEST
                # -----------------------------------------

                try:

                    response = requests.get(
                        api_url,
                        headers=self.headers,
                        timeout=30
                    )

                except Exception as e:

                    logging.error(
                        f"Request error: {e}"
                    )

                    break

                # -----------------------------------------
                # RESPONSE CHECK
                # -----------------------------------------

                if response.status_code != 200:

                    logging.error(
                        f"Request failed: "
                        f"{response.status_code}"
                    )

                    break

                # -----------------------------------------
                # PRODUCT EXTRACTION ONLY
                # -----------------------------------------

                self.parse_item(
                    response,
                    meta
                )

                # -----------------------------------------
                # NEXT PAGE
                # PAGINATION IS HANDLED ONLY HERE
                # -----------------------------------------

                selectors = Selector(
                    text=response.text
                )

                next_page = selectors.xpath(
                    '//a[contains(@class,"next")]/@href'
                ).get()

                # -----------------------------------------
                # NO NEXT PAGE
                # -----------------------------------------

                if not next_page:

                    logging.info(
                        "Pagination completed"
                    )

                    logging.info(
                        f"Category completed: "
                        f"{category_name}"
                    )

                    break

                # -----------------------------------------
                # NEXT PAGE FOUND
                # -----------------------------------------

                next_page = next_page.strip()

                logging.info(
                    f"Next page found: {next_page}"
                )

                # Move to next page
                api_url = next_page

    def parse_item(self, response, meta):
        """
        Extract products ONLY.

        No pagination is performed here.
        """

        selectors = Selector(
            text=response.text
        )

        # -----------------------------------------
        # PRODUCT XPATH
        # -----------------------------------------

        product_list = selectors.xpath(
            '//div[@class="product-item-info"]'
        )

        if not product_list:

            logging.info(
                "No products found on current page"
            )

            return

        logging.info(
            f"Found {len(product_list)} products"
        )

        # -----------------------------------------
        # PRODUCT LOOP
        # -----------------------------------------

        for product in product_list:

            try:

                # -----------------------------------------
                # IMAGES
                # -----------------------------------------

                images = product.xpath(
                    './/img/@data-lazy'
                ).getall()

                images = [
                    image.strip()
                    for image in images
                    if image and image.strip()
                ]

                # -----------------------------------------
                # PRODUCT NAME
                # -----------------------------------------

                product_name = product.xpath(
                    'normalize-space('
                    './/strong['
                    '@class="product name '
                    'product-item-name"'
                    '])'
                ).get()

                # -----------------------------------------
                # PRODUCT PRICE
                # -----------------------------------------

                product_price = product.xpath(
                    './/strong['
                    '@itemprop="price"'
                    ']/@content'
                ).get()

                # -----------------------------------------
                # DESCRIPTION
                # -----------------------------------------

                description = product.xpath(
                    './/div['
                    'contains('
                    '@class,'
                    '"product-item-description"'
                    ')]/text()'
                ).get(
                    default=""
                )

                description = (
                    description
                    .strip()
                    .replace(
                        ":",
                        ","
                    )
                )

                # -----------------------------------------
                # PRODUCT URL
                # -----------------------------------------

                product_url = product.xpath(
                    './/a['
                    'contains('
                    '@class,'
                    '"product-item-link"'
                    ')]/@href'
                ).get()

                # -----------------------------------------
                # ITEM
                # -----------------------------------------

                item = {}

                item["end_category_name"] = (
                    meta.get("category")
                )

                item["end_category_url"] = (
                    meta.get("category_url")
                )

                item["product_name"] = (
                    product_name
                )

                item["website"] = (
                    "lidl.ch"
                )

                item["product_price"] = (
                    product_price
                )

                item["image1"] = (
                    images[0]
                    if len(images) > 0
                    else ""
                )

                item["image2"] = (
                    images[1]
                    if len(images) > 1
                    else ""
                )

                item["image3"] = (
                    images[2]
                    if len(images) > 2
                    else ""
                )

                item["description"] = (
                    description
                )

                item["product_url"] = (
                    product_url
                )

                # -----------------------------------------
                # LOG PRODUCT
                # -----------------------------------------

                logging.info(
                    f"Product: {product_name}"
                )

                logging.info(
                    f"Product URL: {product_url}"
                )

                # -----------------------------------------
                # CHECK URL
                # -----------------------------------------

                if not product_url:

                    logging.warning(
                        "Product URL missing, skipping"
                    )

                    continue

                # -----------------------------------------
                # INSERT MONGODB
                # -----------------------------------------

                try:

                    self.data_collection.insert_one(
                        item
                    )

                    logging.info(
                        f"Inserted: {product_name}"
                    )

                except Exception as e:

                    # Duplicate product
                    if (
                        "duplicate key"
                        in str(e).lower()
                    ):

                        logging.info(
                            f"Already exists: "
                            f"{product_url}"
                        )

                    else:

                        logging.error(
                            f"MongoDB error: {e}"
                        )

            except Exception as e:

                logging.error(
                    f"Product Error: {e}"
                )

    def close(self):
        """Close MongoDB connection"""

        client.close()


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s: "
            "%(message)s"
        )
    )

    crawler = Crawler()

    try:

        crawler.start()

    finally:

        crawler.close()