
##############################CRAWLER##############################

import requests
import json
import re
from bs4 import BeautifulSoup

import requests
cookies = {
    }

headers = {
    }

params = {
    'rows': '50',
    'o': '949',
    'plaEnabled': 'true',
    'xdEnabled': 'false',
    'isFacet': 'true',
    'p': '20',
    'pincode': '',
}

response = requests.get(
    'https://www.myntra.com/gateway/v4/search/women-ethnic-wear',
    params=params,
    cookies=cookies,
    headers=headers,
)

data = response.json()

products = data.get("products", []) + data.get("plaProducts", [])

print(len(products))
for product in products:
    product_id = product.get("productId")
    # print(product_id)
    # url = product.get("landingPageUrl", "")
    # print(url)

##############################PARSER##############################
         


import json
from bs4 import BeautifulSoup
response = requests.get(
    # 'https://www.myntra.com/shirts/glitchez/glitchez-textured-slim-fit-casual-shirt/40842650/buy',
    'https://www.myntra.com/sarees/anouk/anouk-embellished-floral-sequinned-organza-saree/31819129/buy',
    
    headers=headers,
)
print(response.status_code)

page_html = response.text
soup = BeautifulSoup(page_html, "html.parser")

# ---------------------------
# JSON-LD Data
# ---------------------------
breadcrumb = ""
category = ""
mpn = ""

for script in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(script.string)

        if data.get("@type") == "Product":
            mpn = data.get("mpn", "")

        elif data.get("@type") == "BreadcrumbList":
            breadcrumb = " > ".join(
                item["item"]["name"]
                for item in data.get("itemListElement", [])
            )

            if data.get("itemListElement"):
                category = data["itemListElement"][0]["item"]["name"]

    except Exception:
        continue

print("Breadcrumb:", breadcrumb)
print("Category:", category)
print("MPN:", mpn)

# ---------------------------
# window.__myx JSON
# ---------------------------
marker = "window.__myx = "

start = page_html.find(marker)

if start != -1:

    start = page_html.find("{", start)
    end = page_html.find("</script>", start)

    json_text = page_html[start:end].strip()

    if json_text.endswith(";"):
        json_text = json_text[:-1]

    data = json.loads(json_text)

    pdp = data["pdpData"]

    title = pdp.get("name", "")

    
    mrp = pdp.get("mrp", "")

    
    manufacturer = pdp.get("manufacturer", "")

    
    item_number = pdp.get("id", "")


    price_raw  = pdp.get("price", {}) or ""

    discounted = price_raw.get("discounted")

    price = discounted if discounted else  mrp

    discount = pdp.get('discounts',[{}])[0].get('label','')

    print(discount)
    

    occasion = pdp.get("articleAttributes", {}).get("Occasions", "")

    sizes = [
        size.get("label")
        for size in pdp.get("sizes", [])
    ]

    colours = [
        colour.get("label")
        for colour in pdp.get("colours", [])
    ]

    selected_colour = pdp.get("baseColour", "")

    # Images
    images = []

    for album in pdp.get("media", {}).get("albums", []):
        for image in album.get("images", []):
            if image.get("src"):
                images.append(image["src"])

    brand = pdp.get("brand", "")

    print(brand)

    sku = (
        pdp.get("buyButtonSellerOrder", [{}])[0]
        .get("skuId", "")
    )

    print(sku)

    ratings = pdp.get("ratings", {})

    average_rating = ratings.get("averageRating", "")
    rating_count = ratings.get("totalCount", "")

    review_count = (
        pdp.get("reviewInfo", {})
        .get("reviewsCount", "")
    )

    sub_category = (
        pdp.get("analytics", {})
        .get("subCategory", "")
    )

    gender = pdp.get("analytics", {}).get("gender", "")
    print(gender)

    
    description = {}

    for item in pdp.get("descriptors", []):

        title_key = item.get("title", "")
        desc_html = item.get("description", "")

        text = BeautifulSoup(
            desc_html,
            "html.parser"
        ).get_text("\n", strip=True)

        description[title_key] = text

    print(description)

    print(images)
    print(sizes)

    from datetime import datetime

    scraped_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    