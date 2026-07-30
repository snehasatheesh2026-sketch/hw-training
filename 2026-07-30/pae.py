import requests


headers = {
    }

base_url = "https://www.sephora.sg/api/v2.6/products"

page = 1
all_products = []

while True:
    params = {
        "page[number]": page,
        "page[size]": 36,
        "sort": "sales",
        "filter[category]": "makeup",
        "include": "featured_variant,brand,featured_ad",
    }

    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()

    all_products.extend(data["data"])

    
    meta = data["meta"]
    print(meta['total-pages'])
    print(f"Page {meta['current-page']} of {meta['total-pages']}")

    if meta["current-page"] >= meta["total-pages"]:
        break

    page += 1

print(f"Downloaded {len(all_products)} products.")