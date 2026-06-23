import requests
from parsel import Selector
import csv


class lidl_ch_spider:

    def __init__(self):
        self.start_url = "https://sortiment.lidl.ch/de/obst-gemuese"

        self.headers = {
            'user-agent': 'Mozilla/5.0'
        }

    def parse(self, url):

        print(f"Progress: {url}")

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return

        selectors = Selector(text=response.text)

        # S get all links
        links = selectors.xpath(
            "//ul[contains(@class,'items-children')]//a"
        )

        # build child_links using  logic
        child_links = selectors.xpath(
            "//ul[contains(@class,'items-children')]//a/@href"
        ).getall()

        child_links = [
            link for link in child_links
            if "/catalog/category/view" not in link or "items-children" in link
        ]

        # extract name + filter using child_links
        for link in links:

            name = link.xpath(".//span[@class='label']/text()").get()
            sub_url = link.xpath("./@href").get()

            if name and sub_url and sub_url in child_links:

                yield {
                    "main_category_url": url,
                    "sub_category_name": name.strip(),
                    "sub_category_url": sub_url.strip()
                }

    def run(self):
        return self.parse(self.start_url)


spider = lidl_ch_spider()

with open("lidl_categories.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "main_category_url",
            "sub_category_name",
            "sub_category_url"
        ]
    )

    writer.writeheader()

    for item in spider.run():
        writer.writerow(item)

print("Saved successfully")