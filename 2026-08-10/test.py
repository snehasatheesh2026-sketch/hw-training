import logging
import json
import requests

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from settings import (
    HEADERS,
    client,
    MONGO_DB,
    MONGO_COLLECTION_CATEGORY,
    BASE_URL,
)


class CategoryCrawler:

    def __init__(self):

        self.collection = client[
            MONGO_DB
        ][
            MONGO_COLLECTION_CATEGORY
        ]

        self.session = requests.Session()
        self.session.headers.update(HEADERS)

        self.visited = set()
        self.saved = set()

    def start(self):
        """Request the start URL and crawl categories."""

        logging.info(
            "Requesting start URL: %s",
            BASE_URL
        )

        response = self.session.get(
            BASE_URL,
            timeout=30
        )

        logging.info(
            "Response status: %s",
            response.status_code
        )

        response.raise_for_status()

        categories = self.parse_categories(
            response
        )

        logging.info(
            "Found %s end categories",
            len(categories)
        )

        # Insert every category into MongoDB
        for category in categories:

            item = {
                "id": category["id"],
                "encoded_id": category["encoded_id"],
                "full_link": category['full_link'],
                "name": category["name"],
                "link": category["link"],
            }

            try:

                result = self.collection.insert_one(
                    item
                )

                print(item)

                logging.info(
                    "Mongo inserted: %s",
                    result.inserted_id
                )

            except Exception:

                logging.exception(
                    "Mongo insert failed: %s",
                    item
                )

    def parse_categories(self, response):
        """
        Extract topmenuparsedData from the page
        and recursively find leaf categories.
        """

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        script_text = next(
            (
                script.string or script.get_text()
                for script in soup.find_all("script")
                if "topmenuparsedData" in (
                    script.string
                    or script.get_text()
                )
            ),
            None,
        )

        if not script_text:

            raise Exception(
                "topmenuparsedData not found"
            )

        # Decode escaped JavaScript string
        decoded = (
            script_text
            .encode()
            .decode("unicode_escape")
        )

        marker = "topmenuparsedData\":{"

        start = decoded.find(
            marker
        )

        if start == -1:

            raise Exception(
                "topmenuparsedData JSON start not found"
            )

        # Find opening {
        start = decoded.find(
            "{",
            start
        )

        if start == -1:

            raise Exception(
                "Could not find topmenuparsedData opening brace"
            )

        # Find matching closing }
        count = 0
        end = None

        for position in range(
            start,
            len(decoded)
        ):

            if decoded[position] == "{":

                count += 1

            elif decoded[position] == "}":

                count -= 1

                if count == 0:

                    end = position
                    break

        if end is None:

            raise Exception(
                "Could not find topmenuparsedData JSON end"
            )

        json_text = decoded[
            start:end + 1
        ]

        try:

            menu = json.loads(
                json_text
            )

        except json.JSONDecodeError:

            logging.exception(
                "Could not decode topmenuparsedData"
            )

            raise

        end_categories = []

        for root in menu.get(
            "content",
            []
        ):

            end_categories.extend(
                self.get_leaf_categories(
                    root
                )
            )

        return end_categories

    def get_leaf_categories(
        self,
        node
    ):
        """
        Recursively extract leaf/end categories.
        """

        children = node.get(
            "children",
            {}
        ).get(
            "content",
            []
        )

        # --------------------------------------------------
        # LEAF CATEGORY
        # --------------------------------------------------

        if not children:

            category_id = str(
                node["id"]
            )

            relative_link = node.get(
                "link"
            )

            if not relative_link:

                logging.warning(
                    "Category has no link: %s",
                    node
                )

                return []

            full_url = urljoin(
                BASE_URL,
                relative_link
            )

            logging.info(
                "Processing leaf category: %s",
                full_url
            )

            category_data = None

            try:

                response = self.session.get(
                    full_url,
                    timeout=30
                )

                response.raise_for_status()

                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )

                # ------------------------------------------
                # Find categoryData inside Next.js script
                # ------------------------------------------

                for script in soup.find_all(
                    "script"
                ):

                    text = script.get_text()

                    if r'\"categoryData\"' not in text:

                        continue

                    start = text.find(
                        r'{\"__typename\":\"CategoryTree\"'
                    )

                    if start == -1:

                        continue

                    try:

                        # Decode:
                        #
                        # \" → "
                        # \u0026 → &
                        #
                        decoded = (
                            text[start:]
                            .encode()
                            .decode(
                                "unicode_escape"
                            )
                        )

                        decoder = (
                            json.JSONDecoder()
                        )

                        category_data, _ = (
                            decoder.raw_decode(
                                decoded
                            )
                        )

                        logging.info(
                            "CategoryTree found: %s",
                            category_data
                        )

                        break

                    except (
                        UnicodeDecodeError,
                        json.JSONDecodeError
                    ):

                        logging.exception(
                            "Could not decode "
                            "CategoryTree: %s",
                            full_url
                        )

            except requests.RequestException:

                logging.exception(
                    "Request failed: %s",
                    full_url
                )

            # ------------------------------------------
            # Build final category
            # ------------------------------------------

            if category_data:

                encoded_id = (
                    category_data.get(
                        "uid"
                    )
                )

                name = (
                    category_data.get(
                        "name"
                    )
                    or node.get(
                        "name"
                    )
                )

            else:

                encoded_id = None

                name = node.get(
                    "name"
                )

                logging.warning(
                    "---------------------------------------------------------------CategoryTree not found: %s",
                    full_url
                )

            return [
                {
                    "id": category_id,
                    "encoded_id": encoded_id,
                    "name": name,
                    "full_link": full_url,
                    "link": relative_link,
                }
            ]

        # --------------------------------------------------
        # HAS CHILDREN
        # --------------------------------------------------

        result = []

        for child in children:

            result.extend(
                self.get_leaf_categories(
                    child
                )
            )

        return result


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s: "
            "%(message)s"
        )
    )

    crawler = CategoryCrawler()

    crawler.start()