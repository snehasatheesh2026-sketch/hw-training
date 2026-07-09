from curl_cffi import requests
from lxml import html
from urllib.parse import urljoin
import json
import re
import csv


class NextParser:

    def __init__(self):
        self.base_url = "https://www.next.co.uk"
        self.url = "https://www.next.co.uk/women"
        self.data = None


    def fetch(self):

        response = requests.get(
            self.url,
            impersonate="chrome"
        )

        document = html.fromstring(response.text)

        script = document.xpath(
            "//script[contains(text(),'window.__INITIAL_CONTENT__')]"
        )[0]

        js = script.text

        match = re.search(
            r'window\.__INITIAL_CONTENT__\s*=\s*(\{.*\});',
            js,
            re.DOTALL
        )

        self.data = json.loads(match.group(1))


    def get_categories(self):

        links = self.data[
            "desktop_content"
        ][
            "links_list"
        ][0][
            "external_links"
        ]

        categories = []

        for item in links:

            categories.append(
                {
                    "subcategory": item["title"],
                    "url": urljoin(
                        self.base_url,
                        item["url"]
                    )
                }
            )


        # Move CLOTHING to last position
        categories.sort(
            key=lambda x: x["subcategory"].upper() == "CLOTHING"
        )


        for category in categories:
            yield category



    def parse_category(self, subcategory, category_url):

        seen_urls = set()
        page = 1


        while True:

            response = requests.get(
                category_url,
                impersonate="chrome",
                params={
                    "p": page
                }
            )


            document = html.fromstring(response.text)


            products = document.xpath(
                "//a[@data-testid='product_summary_image_media']"
            )


            if not products:
                break


            new_products = 0


            for product in products:

                name = product.get("title")
                pdp_url = product.get("href")


                if pdp_url and pdp_url not in seen_urls:

                    seen_urls.add(pdp_url)

                    new_products += 1


                    yield {
                        "subcategory": subcategory,
                        "name": name,
                        "pdp_url": pdp_url
                    }


            if new_products == 0:
                break


            page += 1





parser = NextParser()

parser.fetch()


with open(
    "products.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:


    writer = csv.DictWriter(
        file,
        fieldnames=[
            "subcategory",
            "name",
            "pdp_url"
        ]
    )


    writer.writeheader()


    for category in parser.get_categories():

        for product in parser.parse_category(
            category["subcategory"],
            category["url"]
        ):

            writer.writerow(product)



