
import logging
import json
import requests
import base64
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

        self.collection = client[ MONGO_DB][ MONGO_COLLECTION_CATEGORY]
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.visited = set()
        self.saved = set()

    def start(self):
        """Requesting Start URL."""

        response = self.session.get(
            BASE_URL,
            timeout=30
        )

        logging.info("Response status: %s", response.status_code )

        response.raise_for_status()

        categories = self.parse_categories(response)

        logging.info(
            "Found %s end categories",
            len(categories)
        )

        # Insert every category into MongoDB
        for category in categories:

            item = {
                "id": category["id"],
                "encoded_id": category["encoded_id"],
                "name": category["name"],
                "full":category["full"],
                "link": category["link"],
            }

            try:

                result = self.collection.insert_one(item)

                logging.info("Mongo inserted: %s", result.inserted_id
                )

            except Exception:

                logging.exception(
                    "Mongo insert failed: %s", item)

    def parse_categories(self, response):

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        script_text = next(
            (
                script.string or script.get_text()
                for script in soup.find_all("script")
                if "topmenuparsedData" in (
                    script.string or script.get_text()
                )
            ),
            None,
        )

        if not script_text:
            raise Exception(
                "topmenuparsedData not found"
            )

        decoded = script_text.encode().decode(
            "unicode_escape"
        )

        marker = 'topmenuparsedData":{'

        start = decoded.find(marker)

        if start == -1:
            raise Exception(
                "topmenuparsedData JSON start not found"
            )

        start = decoded.find(
            "{",
            start
        )

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
                "Could not find JSON end"
            )

        menu = json.loads(decoded[start:end + 1] )

        end_categories = []

        for root in menu.get( "content", []):

            end_categories.extend(
                self.get_leaf_categories(root)
            )

        return end_categories

    def get_leaf_categories(self, node):
        """Recursively extract leaf categories."""

        children = node.get(
            "children",
            {}
        ).get(
            "content",
            []
        )

        # No children = leaf/end category
        if not children:

            category_id = str( node["id"])


            return [{
                "id": category_id,
                "encoded_id": base64.b64encode( category_id.encode()).decode(),
                "name": node["name"],
                "full":urljoin(BASE_URL,node['link']),
                "link": node["link"],
            }]

        # Has children -> recursively process them
        result = []

        for child in children:

            result.extend(
                self.get_leaf_categories(child)
            )

        return result


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s"
    )

    crawler = CategoryCrawler()

    crawler.start()




