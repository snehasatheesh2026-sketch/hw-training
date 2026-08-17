from datetime import datetime
import json
import random
import re
import time
from urllib.parse import urljoin
import csv
import requests


class Dm_makeup_listing:

    def __init__(self):
        self.base_url = "https://www.dm.hu/"
        self.tree_url = "https://products.dm.de/categories/v1/categories-tree/de-DE"
        self.strating_url = "https://product-search.services.dmtech.com/hu/search/static"
        self.details = "https://products.dm.de/product/products/detail/HU/dan/"

        self.output_csv = "DataHUT_Hu_FullDump_20260817.csv"

        self.headers = {
}
        self.details_header  = {
    }
        self.headerss = {
    }

        self.paramss = {
            "allCategories.id": "010109",
            "pageSize": "30",
            "searchType": "editorial-search",
            "sort": "editorial_relevance",
            "type": "search-static",
        }

        self.params = {
            "pageSize": "30",
            "searchType": "editorial-search",
            "sort": "editorial_relevance",
            "type": "search-static",
        }

    def leaf_categories(self, nodes):
        leaves = {}
        for node in nodes:
            subcategories = node.get("subcategories", [])
            if subcategories:
                leaves.update(self.leaf_categories(subcategories))
            else:
                name = node.get("name")
                code = node.get("code")
                if name and code:
                    leaves[name] = code
        return leaves

    def sub_categories(self):
        response = requests.get(self.tree_url, headers=self.headers)
        if response.status_code == 200:
            all_leaves = {}
            for root_node in response.json():
                all_leaves.update(self.leaf_categories([root_node]))
            return all_leaves
        return {}

    def parse(self):
        categories = self.sub_categories()
        seen_ids = set()
        seen_urlss= set()

        seen_gtins = set()
        seen_dans = set()
        seen_urls = set()

        print(f"Total end categories: {len(categories)}")

        for cat_name, cat_id in categories.items():
            print(f"Category: {cat_name} | ID: {cat_id}")

            current_category_param = self.params.copy()
            current_category_param["allCategories.id"] = cat_id

            response = requests.get(
                self.strating_url,
                headers=self.headerss,
                params=current_category_param,
            )
            time.sleep(random.uniform(2, 3))

            if response.status_code == 429:
                print(f"{cat_id} -> 429 Rate Limited")
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    time.sleep(int(retry_after))
                else:
                    time.sleep(10)
                continue

            if response.status_code != 200:
                print(f"{cat_id} statuscode == {response.status_code}")
                continue

            data = response.json()
            total_pages = data.get("totalPages", 1)
            
            for page in range(total_pages):
                current_params = current_category_param.copy()
                current_params["currentPage"] = page
                page_res = requests.get(
                    self.strating_url, headers=self.headerss, params=current_params
                )
                if page_res.status_code != 200:
                    print(f"{page} == {page_res.status_code}")
                    continue
                
                page_data = page_res.json()
                for product in page_data.get("products", []):
                    unique = product.get("gtin",'') or ""

                    if unique and unique in seen_ids:
                        continue
                    listing_gtin = product.get("gtin", "") or ""
                    tile_data = product.get("tileData", {})
                    dan = tile_data.get("dan", "") or ""
                    listing_url = tile_data.get("self", "") or ""

                    
                    # pdp_urls = tile_data.get("self", "")
                    # dan = tile_data.get("dan",'')
                    # if pdp_urls and pdp_urls in seen_urls:
                    #     continue

                    if listing_gtin and listing_gtin in seen_gtins:
                      continue
                    if dan and dan in seen_dans:
                       continue
                    if listing_url and listing_url in seen_urls:
                        continue

                    

                    # Initialize variables
                    product_name = ""
                    brand = ""
                    category = []
                    breadcrumb = ""
                    levels = []
                    producthierarchy_level1 = ""
                    producthierarchy_level2 = ""
                    producthierarchy_level3 = ""
                    producthierarchy_level4 = ""
                    producthierarchy_level5 = ""
                    producthierarchy_level6 = ""
                    selling_price = ""
                    regular_price = ""
                    site_shown_uom = ""
                    grammage_quantity = ""
                    grammage_unit = ""
                    product_unique_key = ""
                    barcode = ""
                    price_per_unit = ""
                    product_description = ""
                    ingredients = ""
                    instructionforuse = ""
                    raw_product_features = ""
                    features = ""
                    age_recommendations = ""
                    warning = ""
                    storage_instructions = ""
                    country_of_origin = ""
                    preparationinstructions = ""
                    raw_ingredients_text = ""
                    nutritional_information = ""
                    allergens = ""
                    nutrition_table = ""
                    special_information_s = ""
                    Required_information = ""
                    Additives_s = ""
                    special_information = ""
                    color = ""
                    size = ""
                    image_urls = []
                    image_url_1 = ""
                    image_url_2 = ""
                    image_url_3 = ""
                    image_url_4 = ""
                    image_url_5 = ""
                    image_url_6 = ""
                    price_valid_from = ""
                    not_increased_text = ""
                    variants = ""
                    material = ""
                    organictype = "non-organic"
                    currency = ""
                    extraction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    rating =""
                    review =""
                    instock =""
                    retail_limit =""
                    required_information =""
                    pdp_url =""

                    if dan:
                        try:
                            if dan and dan in seen_dans:
                              continue
                            details_url = self.details + str(dan)
                            det_response = requests.get(details_url, headers=self.details_header)

                            if det_response.status_code == 200:
                                json_response = det_response.json()
                                metadata = json_response.get("metadata", "")

                                unique_id = json_response.get("gtin",'') or ""
                                product_name = json_response.get("title", "").get("headline")
                                brand = json_response.get("seoInformation", "").get("structuredData", "").get("brand", "")
                                category = json_response.get("breadcrumbs", "")
                                breadcrumb = " > ".join(["Kezdőlap"] + category) if category else "Kezdőlap"
                                levels = ["Kezdőlap"] + category or ""

                                producthierarchy_level1 = levels[0] if len(levels) > 0 else ""
                                producthierarchy_level2 = levels[1] if len(levels) > 1 else ""
                                producthierarchy_level3 = levels[2] if len(levels) > 2 else ""
                                producthierarchy_level4 = levels[3] if len(levels) > 3 else ""
                                producthierarchy_level5 = levels[4] if len(levels) > 4 else ""
                                producthierarchy_level6 = levels[5] if len(levels) > 5 else ""
                                currency = json_response.get("metadata", "").get("currency")

                                price = json_response.get("price", "").get("price", "").get("current", "").get("value", "")
                                if price:
                                    price_value = float(re.sub(r"[^\d,.-]", "", str(price)).replace(",", "."))
                                    selling_price = f"{price_value:.2f}"
                                    
                                reg_price_raw = json_response.get("metadata", "").get("price") or selling_price
                                try:
                                    regular_price = f"{float(reg_price_raw):.2f}"
                                except (ValueError, TypeError):
                                    regular_price = str(reg_price_raw)

                                price_field = json_response.get("price", "").get("infos", "")
                                r_text = price_field[0] if price_field else ""
                                c_text = r_text.split("(")[0].strip() if r_text else ""
                                
                                site_shown_uom = c_text.replace(',','.')
                                grammage_quantity = c_text.split()[0] if len(c_text.split()) > 0 else ""

                                grammage_quantity = grammage_quantity.replace(',','.')
                    
                                grammage_unit = c_text.split()[-1] if len(c_text.split()) > 0 else ""
                                
                                # match = re.search(r"(\d+[,.]?\d*)\s*Ft.*?(\d+)\s*ml", r_text)
                                
                                # price_per_unit = f"{float(match.group(1).replace(',', '.')):.2f} Ft {match.group(2)} ml-enként" if match else ""

                                parts = r_text.split('(', 1)
                                inside = parts[1].rstrip(')').strip() if len(parts) > 1 else ''

                                text = re.sub(
                                     r'\[/\]\([^)]*\)\s*',
                                         '',
                                       inside
                                    )
                                text = text.replace(r'\xa0', ' ').replace(' / ',' ')

                                text = re.sub(r'\[/\]\([^)]*\)', '', text)


                                price_per_unit = re.sub(r'\s+', ' ', text).strip()


                                if price_per_unit:

                                   price_per_unit = text+" enként"
                                else:
                                    price_per_unit =""

                                
                                pdp_url = metadata.get("canonical", "")
                                

                                if pdp_url and pdp_url in seen_urlss:
                                    continue

                                barcode = unique_id
                                product_unique_key = str(unique_id) + "P"

                                description_groups = json_response.get("descriptionGroups", [])
                                traget = "  ".join(
                                    description_groups[0].get("contentBlock", [{}])[0].get("bulletpoints", [])
                                    if len(description_groups) > 0 else []
                                )
                                target_text = ""
                                content_blocks = description_groups[0].get("contentBlock", []) if len(description_groups) > 0 else []
                                if len(content_blocks) > 1:
                                    target_text = content_blocks[1].get("texts", [""])[0]

                                product_description = traget + " " + target_text if traget else target_text
                                
                                raw_instructionforuse = next((g for g in description_groups if g.get("header") == "Használati információk"), {})
                                instructionforuse = raw_instructionforuse.get("contentBlock", [{}])[0].get("texts", [""])[0] if raw_instructionforuse else ""

                                instructionforuse = instructionforuse.replace('!','').replace('-','')

                                ingredients_text = next((g for g in description_groups if g.get("header") == "Összetevők"), {})
                                ingredients = ingredients_text.get("contentBlock", [{}])[0].get("texts", [""])[0] if ingredients_text else ""

                                ingredients = ingredients.replace('•','').replace('\n','').replace('(','').replace(')','').replace('*','').replace('|','').replace('/','').replace('●','').replace('[','').replace(']','').replace('+','')

                                raw_product_warning = next((g for g in description_groups if g.get("header") == "Figyelmeztető adat"), {})
                                warning = raw_product_warning.get("contentBlock", [{}])[0].get("texts", [""])[0] if raw_product_warning else ""
                                if not warning:

                                    raw_product_warning =  next((g for g in description_groups if g.get('header') == 'Opozorilo o nevarnosti'), {})
                                    warning = raw_product_features.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_product_warning else ""
                                warning = warning.replace('/',' ').replace('\n','').replace('(','').replace(')','')

                                storage_instructions_raw = next((g for g in description_groups if g.get("header") == "Tárolási információk"), {})
                                storage_instructions = storage_instructions_raw.get("contentBlock", [{}])[0].get("texts", [""])[0] if storage_instructions_raw else ""

                                manufacturer_address_raw = next((g for g in description_groups if g.get("header") == "Gyártás helye"), {})
                                country_of_origin = manufacturer_address_raw.get("contentBlock", [{}])[0].get("texts", [""])[0] if manufacturer_address_raw else ""

                                preparationinstructions_raw = next((g for g in description_groups if g.get("header") == "Elkészítés"), {})
                                preparationinstructions = preparationinstructions_raw.get("contentBlock", [{}])[0].get("texts", [""])[0] if preparationinstructions_raw else ""

                                raw_allergens = next((g for g in description_groups if g.get("header") == "Allergének"), {})
                                allergens = raw_allergens.get("contentBlock", [{}])[0].get("texts", [""])[0] if raw_allergens else ""

                                price_data = json_response.get("price", {})
                                not_increased_text = price_data.get("notIncreasedSince", {}).get("text", "")
                                matchss = re.search(r"\d{4}\.\d{2}\.\d{2}", not_increased_text)
                                price_valid_from = matchss.group(0) if matchss else ""

                                # Fixed pills definition order
                                pills = json_response.get("pills", [])
                                print("PILLS:", repr(pills))
                                organictype = "organic" if any("bio" in str(pill).strip().casefold() for pill in pills) else "non-organic"
                                print("am originic typprrr", organictype)

                                nutritional_information_raw = next((g for g in description_groups if g.get("header", "").strip() == "Tápérték"), {})
                                nutr_content_blocks = nutritional_information_raw.get("contentBlock", [])
                                nutr_content_block = nutr_content_blocks[0] if nutr_content_blocks else {}
                                nutrition_table = nutr_content_block.get("table", "") or ""
                                texts = nutr_content_block.get("texts", [])
                                raw_ingredients_text = texts[0] if texts else ""
                                nutrition_dict = {
                                               f"{key}_na {unit}": value
                                                for key, value in nutrition_table

                                                 }  
                                nutrition_dicts= nutrition_dict if nutrition_dict else ""        
                                nutritional_information = f"{nutrition_dicts} {raw_ingredients_text}".strip()

                                image_urls = list(dict.fromkeys(
                                    img.get("src", "") for img in json_response.get("images", []) if img.get("src")
                                ))
                                image_url_1, image_url_2, image_url_3, image_url_4, image_url_5, image_url_6 = (image_urls + [""] * 6)[:6]

                                product_feature = next((g for g in description_groups if g.get("header") == "Termékjellemzők"), {})
                                raw_product_features = "\n".join(
                                    f"**{x.get('title', '')}:**\n{x.get('description', '')}"
                                    for x in product_feature.get("contentBlock", [{}])[0].get("descriptionList", [])
                                )
                                features = raw_product_features.replace("**", "").replace("\n", "").replace("\xa0", " ").replace("/","") if raw_product_features else ""

                                match_age = re.search(r"Ajánlott életkor:\s*(.*?)(?=\s*\w+\s*:|$)", features)
                                age_recommendations = match_age.group(1).strip() if match_age else ""

                                match_material = re.search(r"Anyag:\s*(.*?)(?=\s*\w+\s*:|$)", features)
                                material = match_material.group(1).strip() if match_material else ""

                                special_information_raw = next((g for g in description_groups if g.get("header", "").strip() == "Információ a fenntartható termékekről"), {})
                                special_information_s = special_information_raw.get("contentBlock", [{}])[0].get("texts", [""])[0] if special_information_raw else ""
                                special_information_s = special_information_s.replace('(','').replace(')','').replace('|','').replace('-','').replace('*','')

                                Required_information_raw = next((g for g in description_groups if g.get("header", "").strip() == "Kötelező információk"), {})
                                Required_information = Required_information_raw.get("contentBlock", [{}])[0].get("texts", [""])[0] if Required_information_raw else ""
                                required_information =required_information.replace('(','').replace(')','').replace('|','').replace('-','').replace('*','')

                                Additives = next((g for g in description_groups if g.get("header", "").strip() == "Adalékanyagok"), {})
                                Additives_s = Additives.get("contentBlock", [{}])[0].get("texts", [""])[0] if Additives else ""
                                Additives_s = Additives_s.replace('(','').replace(')','').replace('|','').replace('-','').replace('*','')

                                special_information = " ".join(
                                    x for x in [
                                        f"Információ a fenntartható termékekről: {special_information_s}" if special_information_s else "",
                                        f"Kötelező információk: {Required_information}" if Required_information else "",
                                        f"Adalékanyagok: {Additives_s}" if Additives_s else "",
                                    ] if x
                                )

                                variants_data = json_response.get("variants", {}).get("colors", [{}])[0].get("options", [])
                                color_list = [variant.get("label", "").strip() for variant in variants_data if variant.get("label")]
                                selected_label = next((variant.get("label", "") for variant in variants_data if variant.get("isSelected") is True), "")
                                print("selectedlabel",selected_label)
                                # matchs = re.search(r".\s*\d+\s+(.+)$", selected_label)
                                # color = matchs.group(1).strip() if matchs else ""
                                color = re.split(r",|-", selected_label)[-1].strip()
                                matchs = re.match(r"^(?:Nr\.\s*)?\d+\s+(.+)$", color)
                                if matchs:
                                    color = matchs.group(1).strip()
                                

                                print('color ====',color)

                                size_list = []
                                for group in json_response.get("variants", {}).get("texts", []):
                                    heading = group.get("heading", "").strip().lower()
                                    if "méret" in heading:
                                        size_options = group.get("options", [])
                                        size_list = [option.get("label", "").strip() for option in size_options if option.get("label")]
                                        selected_size = next((option.get("label", "").strip() for option in size_options if option.get("isSelected") is True), "")
                                        size = selected_size
                                        break
    
                                variants = " ".join(
                                    x for x in [
                                        f"color: {', '.join(color_list)}" if color_list else "",
                                        f"size: {', '.join(size_list)}" if size_list else "",
                                    ] if x
                                )

        
                                dan = json_response.get('dan','')

                                try:


                                   rating_response = requests.get(f'https://stars.services.dmtech.com/api/HU/v1/ratings/{dan}/summary', headers= self.headers)

                                   if rating_response.status_code == 200:

                                       data = rating_response.json()

                                       rating = f"{data[0].get('ratingAvg', ''):.2f}" if data[0].get('ratingAvg', '') else""

                                       review = data[0].get('ratingCount', '') if  data[0].get('ratingCount', '') else ""

                                   rs_instock  = requests.get(f'https://products.dm.de/availability/api/v2/detail/HU/{dan}', headers=self.headers)

                                 
                                   if rs_instock.status_code == 200:

                                       print("ratelimit not")


                                       instock_response = rs_instock.json()

                                       print(instock_response)
                                       rows = instock_response.get('rows','')  

                                       raw_retail_limit = instock_response.get('quantitySelection','')
                                       if raw_retail_limit:

                                          retail_limit = max(raw_retail_limit)

                                       available = any(row.get('text') == 'Rendelhető' for row in rows)
                                       instock = available
                                    


                  
                                except Exception as e:
                                    pass

                                



                        except Exception as e:
                            print(f"Error parsing product details: {e}")
                    # if pdp_urls:
                    #     seen_urls.add(pdp_urls)
                    if listing_gtin:
                       seen_gtins.add(listing_gtin)
                    if dan:
                       seen_dans.add(dan)

                    if pdp_url:
                        seen_urlss.add(pdp_url)
                

                    if unique:
                        seen_ids.add(unique)
                    if len(seen_ids) >101:
                        break

                    yield {
                        "unique_id": unique_id,
                        "competitor_name": "dm",
                        "store_name": "",
                        "store_addressline1": "",
                        "store_addressline2": "",
                        "store_suburb": "",
                        "store_state": "",
                        "store_postcode": "",
                        "store_addressid": "",
                        "extraction_date": extraction_date,
                        "product_name": product_name,
                        "brand": brand,
                        "brand_type": "",
                        "grammage_quantity": grammage_quantity,
                        "grammage_unit": grammage_unit,
                        "drained_weight": "",
                        "producthierarchy_level1": producthierarchy_level1,
                        "producthierarchy_level2": producthierarchy_level2,
                        "producthierarchy_level3": producthierarchy_level3,
                        "producthierarchy_level4": producthierarchy_level4,
                        "producthierarchy_level5": producthierarchy_level5,
                        "producthierarchy_level6": producthierarchy_level6,
                        "regular_price": regular_price,
                        "selling_price": selling_price,
                        "price_was": "",
                        "promotion_price": "",
                        "promotion_valid_from": "",
                        "promotion_valid_upto": "",
                        "promotion_type": "",
                        "percentage_discount": "",
                        "promotion_description": "",
                        "package_sizeof_sellingprice": "",
                        "per_unit_sizedescription": "",
                        "price_valid_from": price_valid_from,
                        "price_per_unit": price_per_unit,
                        "multi_buy_item_count": "",
                        "multi_buy_items_price_total": "",
                        "currency": currency,
                        "breadcrumb": breadcrumb,
                        "pdp_url": pdp_url,
                        "variants": variants,
                        "product_description": product_description,
                        "instructions": "",
                        "storage_instructions": storage_instructions,
                        "preparationinstructions": preparationinstructions,
                        "instructionforuse": instructionforuse,
                        "country_of_origin": country_of_origin,
                        "allergens": allergens,
                        "age_of_the_product": "",
                        "age_recommendations": age_recommendations,
                        "flavour": "",
                        "nutritions": "",
                        "nutritional_information": nutritional_information,
                        "vitamins": "",
                        "labelling": "",
                        "grade": "",
                        "region": "",
                        "packaging": "",
                        "receipies": "",
                        "processed_food": "",
                        "barcode": barcode,
                        "frozen": "",
                        "chilled": "",
                        "organictype": organictype,
                        "cooking_part": "",
                        "Handmade": "",
                        "max_heating_temperature": "",
                        "special_information": special_information,
                        "label_information": "",
                        "dimensions": "",
                        "special_nutrition_purpose": "",
                        "feeding_recommendation": "",
                        "warranty": "",
                        "color": color,
                        "model_number": "",
                        "material": material,
                        "usp": "",
                        "dosage_recommendation": "",
                        "tasting_note": "",
                        "food_preservation": "",
                        "size": size,
                        "rating": rating,
                        "review": review,
                        "file_name_1": "",
                        "image_url_1": image_url_1,
                        "file_name_2": "",
                        "image_url_2": image_url_2,
                        "file_name_3": "",
                        "image_url_3": image_url_3,
                        "file_name_4": "",
                        "image_url_4": image_url_4,
                        "file_name_5": "",
                        "image_url_5": image_url_5,
                        "file_name_6": "",
                        "image_url_6": image_url_6,
                        "competitor_product_key": "",
                        "fit_guide": "",
                        "occasion": "",
                        "material_composition": "",
                        "style": "",
                        "care_instructions": "",
                        "heel_type": "",
                        "heel_height": "",
                        "upc": "",
                        "features": features,
                        "dietary_lifestyle": "",
                        "manufacturer_address": "",
                        "importer_address": "",
                        "distributor_address": "",
                        "vinification_details": "",
                        "recycling_information": "",
                        "return_address": "",
                        "alchol_by_volume": "",
                        "beer_deg": "",
                        "netcontent": "",
                        "netweight": "",
                        "site_shown_uom": site_shown_uom,
                        "ingredients": ingredients,
                        "random_weight_flag": "",
                        "instock": instock,
                        "promo_limit": "",
                        "product_unique_key": product_unique_key,
                        "multibuy_items_pricesingle": "",
                        "perfect_match": "",
                        "servings_per_pack": "",
                        "Warning": warning,
                        "suitable_for": "",
                        "standard_drinks": "",
                        "environmental": "",
                        "grape_variety": "",
                        "retail_limit": retail_limit,
                    }
                time.sleep(0.5)


if __name__ == "__main__":
    spider = Dm_makeup_listing()
    
    with open(spider.output_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "unique_id",
                "competitor_name",
                "store_name",
                "store_addressline1",
                "store_addressline2",
                "store_suburb",
                "store_state",
                "store_postcode",
                "store_addressid",
                "extraction_date",
                "product_name",
                "brand",
                "brand_type",
                "grammage_quantity",
                "grammage_unit",
                "drained_weight",
                "producthierarchy_level1",
                "producthierarchy_level2",
                "producthierarchy_level3",
                "producthierarchy_level4",
                "producthierarchy_level5",
                "producthierarchy_level6",
                "regular_price",
                "selling_price",
                "price_was",
                "promotion_price",
                "promotion_valid_from",
                "promotion_valid_upto",
                "promotion_type",
                "percentage_discount",
                "promotion_description",
                "package_sizeof_sellingprice",
                "per_unit_sizedescription",
                "price_valid_from",
                "price_per_unit",
                "multi_buy_item_count",
                "multi_buy_items_price_total",
                "currency",
                "breadcrumb",
                "pdp_url",
                "variants",
                "product_description",
                "instructions",
                "storage_instructions",
                "preparationinstructions",
                "instructionforuse",
                "country_of_origin",
                "allergens",
                "age_of_the_product",
                "age_recommendations",
                "flavour",
                "nutritions",
                "nutritional_information",
                "vitamins",
                "labelling",
                "grade",
                "region",
                "packaging",
                "receipies",
                "processed_food",
                "barcode",
                "frozen",
                "chilled",
                "organictype",
                "cooking_part",
                "Handmade",
                "max_heating_temperature",
                "special_information",
                "label_information",
                "dimensions",
                "special_nutrition_purpose",
                "feeding_recommendation",
                "warranty",
                "color",
                "model_number",
                "material",
                "usp",
                "dosage_recommendation",
                "tasting_note",
                "food_preservation",
                "size",
                "rating",
                "review",
                "file_name_1",
                "image_url_1",
                "file_name_2",
                "image_url_2",
                "file_name_3",
                "image_url_3",
                "file_name_4",
                "image_url_4",
                "file_name_5",
                "image_url_5",
                "file_name_6",
                "image_url_6",
                "competitor_product_key",
                "fit_guide",
                "occasion",
                "material_composition",
                "style",
                "care_instructions",
                "heel_type",
                "heel_height",
                "upc",
                "features",
                "dietary_lifestyle",
                "manufacturer_address",
                "importer_address",
                "distributor_address",
                "vinification_details",
                "recycling_information",
                "return_address",
                "alchol_by_volume",
                "beer_deg",
                "netcontent",
                "netweight",
                "site_shown_uom",
                "ingredients",
                "random_weight_flag",
                "instock",
                "promo_limit",
                "product_unique_key",
                "multibuy_items_pricesingle",
                "perfect_match",
                "servings_per_pack",
                "Warning",
                "suitable_for",
                "standard_drinks",
                "environmental",
                "grape_variety",
                "retail_limit",
            ],
        )
        writer.writeheader()

        total_count = 0
        for item in spider.parse():
            writer.writerow(item)
            total_count += 1

    print(f" Total links collected == {total_count}")