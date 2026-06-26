import time
import csv
import requests


class dm_listing:

    def __init__(self):
        self.base_url = "https://www.dm.si"
        self.starting_url = (
            "https://product-search.services.dmtech.com/si/search/static"
        )

        self.headers = {
            "sec-ch-ua-platform": '"Linux"',
            "x-dm-product-search-token": "48126215296179",
            "Referer": "https://www.dm.si/",
            "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "x-dm-product-search-tags": "presentation:grid;search-type:editorial;channel:web;editorial-type:brand",
        }

        self.params = {
            "brandName": [
                "PHILIPS",
                "PHILIPS AVENT",
                "PHILIPS OneBlade",
                "Philips Sonicare",
            ],
            "pageSize": "50",
            "sort": "new",
            "currentPage": "0",
            "categoryNames": "Nega za moške",  # തു
            "searchType": "editorial-search",
            "type": "search-static",
        }

    def parse(self):
        params = self.params.copy()

        
        try:
            res_json = requests.get(
                self.starting_url, params=params, headers=self.headers
            ).json()

            subcategories = []
            facets = res_json.get("facets", [])
            for facet in facets:
                if facet.get("key") == "categoryNames":
                    subcategories = [
                        v["name"] for v in facet.get("values", []) if "name" in v
                    ]

            print(f"{subcategories}\n")

        except Exception as e:
            print(f"Error reading initial JSON: {e}")
            return

        
        for sub_cat in subcategories:
            params["categoryNames"] = sub_cat  

            try:
                data = requests.get(
                    self.starting_url, params=params, headers=self.headers
                ).json()

                for product in data.get("products", []):
                    tile_data = product.get("tileData", {})
                    breadcrumbs_list = product.get("categoryNames", [])
                    breadcrumb_string = " > ".join(breadcrumbs_list)  # Result: "Nega za moške > Depilacija in britje > Električni brivniki"

                 
                    yield {
                        "sub_category": sub_cat,
                        "brand_name": product.get("brandName", "").strip(),
                        "unique_id": product.get("dan") or "",
                        "product_id": product.get("gtin") or "",
                        "product_name": tile_data.get("title", {})
                        .get("tileHeadline", "")
                        .strip(),
                        "breadcrumb": breadcrumb_string,
                        "price": tile_data.get("price", {}).get("price", {}).get("current", {}).get("value", "") or "",
                        "pdp_url": self.base_url + tile_data.get("self", ""),
                        "competitor_name": "dm",
                    }
            except Exception as e:
                print(f"Error parsing products in {sub_cat}: {e}")

            time.sleep(1) 



spider = dm_listing()

with open("dm_all_details.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "unique_id",
            "sub_category",
            "brand_name",
            "product_name",
            "price",
            "breadcrumb",
            "pdp_url",
            "product_id",
            "competitor_name",
        ],
    )

    writer.writeheader()


    for item in spider.parse():
        writer.writerow(item)

print( "data saved ."
)