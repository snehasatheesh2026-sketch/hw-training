

##############################CRAWLER##############################

from urllib.parse import urlsplit, urlunsplit
import requests
from pprint import pprint

headers = {
    }


base_url = "https://www.sephora.sg/api/v2.6/products"

params = {
        "page[number]": 1,
        "page[size]": 36,
        "sort": "sales",
        "filter[category]": "makeup/face/contour",
        "include": "featured_variant,brand,featured_ad",
    }
response = requests.get(base_url, headers=headers, params=params)

data = response.json()

# print(data['meta'])
# # print(data['data'])

# for product in data.get('data',[]):

#     print(product.get("attributes", {}).get("slug-url", ""))
#     print(product.get("attributes",{}).get('name',''))
#     break



##############################PARSER##############################
import requests
from pprint import pprint

params = {
    "include": (
        "variants.filter_values,"
        "variants.ingredient_preference,"
        "featured_ad.virtual_bundle.bundle_elements,"
        "product_articles,"
        "filter_types"
    )
}



slug = "haus-labs-by-lady-gaga-precision-sculpt-shaping-balm"
url = f"https://www.sephora.sg/api/v2.6/products/{slug}"

response = requests.get(
        url,
        params = params,
       headers=headers
)



data = response.json()
product = data.get('data')
attributes = product.get("attributes", {})
relationships = product.get("relationships", {})
included = data.get("included", [])
heading =attributes.get("heading","") or ""
product_name = f"{attributes.get('name', '')}{heading}" # 1
# 1

price = attributes.get("original-price")  # 2

availbity = "Out of Stock" if attributes.get("sold-out","") else "In Stock" or ""  # 3

unique_id = product.get("id", "")  # 4

description = f"{attributes.get('benefits', '')}{attributes.get('description', '')}"# 5

ingredients =  attributes.get("ingredients","")  # 6

how_to_use = attributes.get('how-to-text','') # 7

available_shades = []

for item in data.get("included", []):
    if (
        item.get("type") == "variants"
        and item.get("attributes", {}).get("available")
    ):
        available_shades.append(
            item.get("attributes", {}).get("shade",'')
        )
available_shades  = ','.join(available_shades) or ""# 8

available_size = []

for item in data.get("included", []):
    if (
        item.get("type") == "variants"
        and item.get("attributes", {}).get("available")
    ):
        available_size.append(
            item.get("attributes", {}).get("size") or ""
        )

available_size = ",".join(size for size in available_size if size)  # 17

brand = attributes.get('brand-name','') or ""   # 16
 
all_images = []
seen = set()

def add_image(url):
    url = (url or "").split("?")[0]

    if url and url not in seen:
        seen.add(url)
        all_images.append(url)



for image in attributes.get("zoom-image-urls", [])  :
    add_image(image)


for item in data.get("included", []):

    if item.get("type") != "product-articles":
        continue

    attr = item.get("attributes", {})

    if attr.get("article-type") != "image":
        continue

    add_image(attr.get("image"))

print(f"Total Images: {len(all_images)}")
print(all_images)         # 9




selected_shade= ""

variant_id = str(attributes.get("featured-variant-id"))

for item in data.get("included", []):
  try:
    if (
        item.get("type") == "variants"
        and item.get("id") == variant_id
    ):
        selected_shade = item.get("attributes", {}).get('shade','')
        break
  except:
    pass
selected_shade # 10

variant_id # 11,
selected_size= ""

variant_id = str(attributes.get("featured-variant-id"))

for item in data.get("included", []):
  try:
    if (
        item.get("type") == "variants"
        and item.get("id") == variant_id
    ):
        selected_size = item.get("attributes", {}).get('size','')
        break
  except:
    pass
selected_size # 10

variant_id  # 15


params = {
    'productid': f'default-{product-id}-{variant_id}',
    'contentType': 'reviews,questions',
    'reviewDistribution': 'primaryRating,recommended',
    'rev': '0',
}

response = requests.get(
    'https://apps.bazaarvoice.com/bfd/v1/clients/sephora-au/api-products/cv2/resources/data/display/0.2alpha/product/summary',
    params=params,
    headers=headers,
)

summary = response.json() #rating

review_summary = summary.get("response", {}).get("reviewSummary", {})

rating = round(review_summary.get("primaryRating", {}).get("average"),2) # 12

review_count = review_summary.get("numReviews") # 13


variant_ids = list({
    item.get("id")
    for item in data.get("included", [])
    if item.get("type") == "variants"
})

print(variant_ids)  # 14