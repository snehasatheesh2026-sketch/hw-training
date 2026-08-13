import requests
from datetime import datetime
import re
from urllib.parse import urljoin

##############################CRAWLER##############################
headers = {
}
base_url ='https://www.dm.hu/'
params = {
    'allCategories.id': '110306',
    'pageSize': '30',
    'searchType': 'editorial-search',
    'sort': 'editorial_relevance',
    'type': 'search-static',
}

response = requests.get('https://product-search.services.dmtech.com/hu/search/static', params=params, headers=headers)

page_data =  response.json()


for product in page_data.get("products", []):
  unique_id = product.get("gtin") or ""
                    
                    
                        
  tile_data = product.get("tileData", {})
  pdp_url = tile_data.get("self", "")
  part_number  = product.get("dan",'')

  unique_id = product.get('gtin','')

  product_name = product.get('title','')

  brand_name = product.get('brandName','')
                          
  tile_data = product.get("tileData", {})
  pdp_url = urljoin(base_url,tile_data.get("self", ""))


  raw_price = tile_data.get("price", {}).get("price", {}).get("current", {}).get("value")
  selling_price = raw_price.replace("€", "").replace("$", "").strip() if raw_price else ""

  images = raw_images = tile_data.get("images", [])



##############################PARSER##############################



response = requests.get('https://products.dm.de/product/products/detail/HU/dan/'+ str(part_number), headers=headers)


json_response = response.json()

metadata =json_response.get('metadata','')

dan = json_response.get('dan','')

product_name = json_response.get('title','').get('headline')

brand =  json_response.get('seoInformation','').get('structuredData','').get('brand','')

category =json_response.get('breadcrumbs','')

breadcrumb = " > ".join(["Kezdőlap"] + category) if category else "Kezdőlap"

unique_id =  json_response.get("gtin") or ""

extraction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

competitor_name = "dm"

levels =["Kezdőlap"] + category or ""

producthierarchy_level1 = levels[0] if len(levels) > 0 else ""
producthierarchy_level2 = levels[1] if len(levels) > 1 else ""
producthierarchy_level3 = levels[2] if len(levels) > 2 else ""
producthierarchy_level4 = levels[3] if len(levels) > 3 else ""
producthierarchy_level5 = levels[4] if len(levels) > 4 else ""
producthierarchy_level6 = levels[5] if len(levels) > 5 else ""

currency = json_response.get('metadata','').get('currency')

price =json_response.get('price','').get('price','').get('current','').get('value','')
price_value = float(re.sub(r"[^\d,.-]", "", price).replace(",", "."))
selling_price = f"{price_value:.2f}"

regular_price  =json_response.get('metadata','').get('price') or selling_price
regular_price  = f"{regular_price:.2f}"

price_field = json_response.get('price','').get('infos', '')
if price_field:
    r_text = price_field[0] 
    c_text = r_text.split('(')[0].strip()

site_shown_uom = c_text

grammage_quantity = c_text.split()[0] if len(c_text.split()) > 0 else ""

grammage_unit = c_text.split()[-1] if len(c_text.split()) > 0 else ""

match = re.search(r'(\d+[,.]?\d*)\s*Ft.*?(\d+)\s*ml', r_text)
price_per_unit = f"{float(match.group(1).replace(',', '.')):.2f} Ft {match.group(2)} ml-enként" if match else ""

pills = json_response.get('pills','')

organictype = "organic" if "Boi" in pills else "non-organic"

pdp_url = metadata.get('canonical','')

barcode =   json_response.get("gtin") or ""

product_unique_key = unique_id+"p" if unique_id else ""

description_groups = json_response.get('descriptionGroups', [])

traget = "  ".join(
                description_groups[0].get('contentBlock', [{}])[0].get('bulletpoints', [])
                if len(description_groups) > 0 else []
                    )
target_text = ""
content_blocks = description_groups[0].get('contentBlock', []) if len(description_groups) > 0 else []

if len(content_blocks) > 1:
             target_text = content_blocks[1].get('texts', [""])[0]

product_description = traget + " " + target_text if traget else target_text

raw_instructionforuse = next((g for g in description_groups if g.get('header') == 'Használati információk'), {})
instructionforuse = raw_instructionforuse.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_instructionforuse else ""

ingredients_text = next((g for g in description_groups if g.get('header') == 'Összetevők'), {})
ingredients = ingredients_text.get('contentBlock', [{}])[0].get('texts', [""])[0] if ingredients_text else ""


product_feature = next((g for g in description_groups if g.get('header') == 'Termékjellemzők'), {})

raw_product_features = "\n".join(
    f"**{x.get('title', '')}:**\n{x.get('description', '')}"
    for x in product_feature.get('contentBlock', [{}])[0].get('descriptionList', [])
)

features = raw_product_features.replace('**','').replace('\n','').replace('\xa0', ' ') if raw_product_features else ""

match_age = re.search(
    r'Ajánlott életkor:\s*(.*?)(?=\s*(?:):|$)',
    features
)

material = re.search(
    r'Anyag:\s*(.*?)(?=\s*(?:):|$)',
    features
)





age_recommendations = match_age .group(1).strip() if match else ''

raw_product_warning = next((g for g in description_groups if g.get('header') == 'Figyelmeztető adat'), {})

warning = raw_product_features.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_product_warning else ""

if not warning:

      raw_product_warning =  next((g for g in description_groups if g.get('header') == 'Opozorilo o nevarnosti'), {})
      warning = raw_product_features.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_product_warning else ""




storage_instructions_raw = next((g for g in description_groups if g.get('header') == 'Tárolási információk'), {})


storage_instructions = storage_instructions_raw.get('contentBlock', [{}])[0].get('texts', [""])[0] if storage_instructions_raw else ""


manufacturer_address_raw = next((g for g in description_groups if g.get('header') == 'Gyártás helye'), {})

country_of_origin = manufacturer_address_raw.get('contentBlock', [{}])[0].get('texts', [""])[0] if  manufacturer_address_raw else ""



preparationinstructions_raw = next((g for g in description_groups if g.get('header') == 'Elkészítés'), {})

preparationinstructions = preparationinstructions_raw.get('contentBlock', [{}])[0].get('texts', [""])[0] if preparationinstructions_raw else ""

raw_allergens = next((g for g in description_groups if g.get('header') == 'Allergének'), {})


allergens = raw_allergens.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_allergens else ""


nutritional_information_raw = next((g for g in description_groups if g.get('header') == 'Tápérték'), {})


content_block = nutritional_information_raw.get('contentBlock', [{}])[0] if nutritional_information_raw else ""

nutrition_table = content_block.get('table','') if  content_block.get('table','') else ""

raw_ingredients_text = content_block.get('texts', [''])[0] if  content_block.get('texts', [''])[0] else ""

nutritional_information =  f"{nutrition_table }, {raw_ingredients_text}"


special_information_raw =  next((g for g in description_groups if g.get('header').strip() == 'Információ a fenntartható termékekről'), {})
special_information_s = special_information_raw.get('contentBlock', [{}])[0].get('texts', [""])[0] if special_information_raw else ""

Required_information_raw = next((g for g in description_groups if g.get('header').strip() == 'Kötelező információk'), {})
Required_information = Required_information_raw.get('contentBlock', [{}])[0].get('texts', [""])[0] if Required_information_raw else ""




# also considered as special filed

Additives = next((g for g in description_groups if g.get('header').strip() == 'Adalékanyagok'), {})
Additives_s= Additives.get('contentBlock', [{}])[0].get('texts', [""])[0] if Additives else ""

special_information = f"{special_information_s}, {Required_information}, {Additives_s}"



variants_data = (
    json_response
    .get('variants', {})
    .get('colors', [{}])[0]
    .get('options', [])
)
color_list = [
    variant.get('label', '').strip()
    for variant in variants_data
    if variant.get('label')
]

selected_label = next(
    (
        variant.get('label', '')
        for variant in variants_data
        if variant.get('isSelected') is True
    ),
    ''
)
matchs = re.search(r'.\s*\d+\s+(.+)$', selected_label)

color = color_name = matchs.group(1).strip() if matchs else ''



size_list = []

for group in json_response.get('variants', {}).get('texts', []):
    heading = group.get('heading', '').strip().lower()

    if 'méret' in heading:  # Hungarian for "size"
        size_list = [
            option.get('label', '').strip()
            for option in group.get('options', [])
            if option.get('label')
        ]
        break

variants = {
    'color': color_list,
    'size': size_list
}


raw_feeding_recommendation=  next((g for g in description_groups if g.get('header','').strip() == 'Etetési javaslat'), {})

feeding_recommendation = raw_feeding_recommendation.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_feeding_recommendation else ""


images = json_response.get('images','')


image_urls = list(dict.fromkeys(
    img.get('src', '')
    for img in response.json().get('images', [])
    if img.get('src')
))


image_url_1, image_url_2, image_url_3, image_url_4, image_url_5, image_url_6 = (
    image_urls + [''] * 6
)[:6]


price_data = json_response.get('price', {})
not_increased_text = price_data.get('notIncreasedSince', {}).get('text', '')

matchss= re.search(r'\d{4}\.\d{2}\.\d{2}', not_increased_text)

price_valid_from =  matchss.group(0) if match else ''









# additional request area
# ----------------------------------------------------------------

# the availablilty of product 

rs  = requests.get('https://products.dm.de/availability/api/v2/tiles/HU/'+str(dan), headers=headers)

availability = rs.json()

rows = response.json().get(dan,'').get('rows','')  #  1460866 =  dan here

if not rows:
      rows = response.json().get('rows','')

raw_retail_limit = rs.json().get('quantitySelection','')

retail_limit = max(raw_retail_limit)

available = any(row.get('text') == 'Rendelhető' for row in rows)
instock = available

# additional request for the review and rating

ratingreview_request  = requests.get(f'https://stars.services.dmtech.com/api/HU/v1/ratings/{dan}/summary', headers=headers)

data = response.json()

rating = f"{data[0].get('ratingAvg', ''):.2f}"

review = data[0].get('ratingCount', '')



##############################CATEGORY_CRAWLER##############################

response = requests.get('https://products.dm.de/categories/v1/categories-tree/hu-HU', headers=headers)



