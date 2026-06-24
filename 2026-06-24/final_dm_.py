
import requests
import csv


class dm_listing:

    def __init__(self):

        self.base_url = "https://www.dm.si"

        self.starting_url = (
            "https://product-search.services.dmtech.com/si/search/static"
            "?allCategories.id=010102"
            "&pageSize=30"
            "&searchType=editorial-search"
            "&sort=editorial_relevance"
            "&type=search-static"
        )

    def parse(self):

        data = requests.get(self.starting_url).json()
        total_pages = data.get("totalPages", 1)  # if total page is missing → default is 1

        for page in range(total_pages):

            url = self.starting_url + f"&currentPage={page}"
            data = requests.get(url).json()

            for product in data.get("products", []):

                tile = product.get("tileData", {})

                
                raw_price = tile.get("price", {}).get("price", {}).get("current", {}).get("value")
                selling_price = raw_price.replace("€", "").replace("$", "").strip() if raw_price else ""

                
                images = tile.get("images", [])

                
                rating = product.get("tileData", {}).get("rating", {}).get("ratingValue")#

                yield {
                    "unique_id": product.get("gtin") or "",
                    "product_name": product.get("title", "") or "",
                    "brand_name":product.get('brandName',{}) or "",
                    "competitor_name": "dm",

                    "currency": product.get("tileData",{}).get("trackingData", {}).get("currency") or "",

                    "selling_price": selling_price.replace(',','.'),

                    "image_1": images[0]["tileSrc"] if len(images) > 0 else "",
                    "image_2": images[1]["tileSrc"] if len(images) > 1 else "",
                    "image_3": images[2]["tileSrc"] if len(images) > 2 else "",

                    "pdp_url": self.base_url + tile.get("self", "") ,

                    "rating": round(float(rating),2) if rating else ""
                }


spider = dm_listing()

with open("dm_product_data.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "unique_id",
            "competitor_name",
            "product_name",
            "brand_name",
            "selling_price",
            "currency",
            "image_1",
            "image_2",
            "image_3",
            "rating",
            "pdp_url",
        ]
    )

    writer.writeheader()

    for item in spider.parse():
        writer.writerow(item)