import requests
import csv


class dm_listing:

    def __init__(self):

        self.base_url = "https://www.dm.si"

        self.starting_url= (
            "https://product-search.services.dmtech.com/si/search/static"
            "?allCategories.id=010102"
            "&pageSize=30"
            "&searchType=editorial-search"
            "&sort=editorial_relevance"
            "&type=search-static"
        )

    def parse(self):

        data = requests.get(self.starting_url).json()

        total_pages = data["totalPages"]

        for page in range(total_pages):

            url = self.starting_url + f"&currentPage={page}"

            data = requests.get(url).json()

            for product in data["products"]:

                yield {
                    "product_name": product.get("title", "").strip(),
                    "pdp_url": self.base_url + product["tileData"]["self"],
                    "competitor_name": "dm"
                }
    

spider = dm_listing()

with open("dm_listing.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "product_name",
              "pdp_url",
              "competitor_name"
              ]
    )

    writer.writeheader()

    for item in spider.parse():

        writer.writerow(item)