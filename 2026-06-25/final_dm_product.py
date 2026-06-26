import csv
import requests


class dm_spider:

    def __init__(self):
        self.base_url = "https://www.dm.si"
        self.details_base_url = "https://products.dm.de/product/products/detail/SI/dan/"

        self.starting_url = (
            "https://product-search.services.dmtech.com/si/search/static"
            "?allCategories.id=010102"
            "&pageSize=30"
            "&searchType=editorial-search"
            "&sort=editorial_relevance"
            "&type=search-static"
        )

        self.details_headers = {
            'accept': '*/*',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.dm.si',
            'referer': 'https://www.dm.si/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            'x-dm-version': '2026.624.73333-1',
        }

    def parse(self):
        data = requests.get(self.starting_url).json()
        total_pages = data.get("totalPages", 1)

        for page in range(total_pages):
            url = self.starting_url + f"&currentPage={page}"
            data = requests.get(url).json()

            for product in data.get("products", []):
                tile = product.get("tileData", {})

                raw_price = tile.get("price", {}).get("price", {}).get("current", {}).get("value")
                selling_price = raw_price.replace("€", "").replace("$", "").strip() if raw_price else ""

                raw_images = tile.get("images", [])
                image_url_list = []
                
                for img in raw_images:
                    src = img.get("tileSrc", "")
                    if src and src not in image_url_list:
                        image_url_list.append(src)
                
                all_images_combined = ", ".join(image_url_list)
                rating = tile.get("rating", {}).get("ratingValue")
                review_count = tile.get("rating", {}).get("ratingCount") or ""
                
                dan = tile.get("dan")
                
                description_text = ""
                breadcrumbs = ""
                raw_ingredients_text = ""
                raw_warning_text = ""
                c_company_address = ""
                color_variant = ""
                features_string = ""
                raw_usage_text = ""
                raw_site_shown = ""
                raw_unit = ""
                raw_quantity = ""
                manufacture = ""
                product_durability =""
            
                if dan:
                    details_url = self.details_base_url + str(dan)
                    try:
                        response = requests.get(details_url, headers=self.details_headers)
                        if response.status_code == 200:
                            datas = response.json()
                            description_groups = datas.get('descriptionGroups', [])

                            # 1. Extract and join description bulletpoints
                            traget = "  ".join(
                                description_groups[0].get('contentBlock', [{}])[0].get('bulletpoints', [])
                                if len(description_groups) > 0 else []
                            )
                            #descripition
                            target_text = ""
                            content_blocks = description_groups[0].get('contentBlock', []) if len(description_groups) > 0 else []
                            if len(content_blocks) > 1:
                                target_text = content_blocks[1].get('texts', [""])[0]

                            if traget:
                                description_text = traget + " " + target_text
                            else:
                                description_text = target_text

                            # Breadcrumbs
                            raw_breadcrumbs = datas.get("breadcrumbs", [])
                            breadcrumbs = " > ".join(raw_breadcrumbs) if raw_breadcrumbs else ""

        
                            features_group = next((g for g in description_groups if g.get('header') == 'Značilnosti'), {})
                            raw_features_list = features_group.get('contentBlock', [{}])[0].get('descriptionList', [])
                            
                            features_array = []
                            for item in raw_features_list:
                                key = item.get('title', '').strip()
                                val = item.get('description', '').strip()
                                if key and val:
                                    key_clean = " ".join(key.split())
                                    val_clean = " ".join(val.split())
                                    features_array.append(f"{key_clean}: {val_clean}")
                            
                            features_string = " ".join(features_array)

                            color_variant_list = []
                            variants_data = datas.get('variants', {}).get('colors', [{}])[0].get('options', [])

                            for option in variants_data:
                                color_label = option.get('colorLabel', '').strip()
                                full_label = option.get('label', '')
                                
                                if "–" in full_label:
                                    target_text = full_label.split("–")[-1].strip()
                                else:
                                    target_text = color_label

                                words = [word for word in target_text.split() if not word.isdigit()]
                                clean_color = " ".join(words).strip()

                                if clean_color and clean_color not in color_variant_list:
                                    color_variant_list.append(clean_color)
                            
                            color_variant = ",".join(color_variant_list)

                            warnings_data = next((g for g in description_groups if g.get('header') == 'Opozorila'), {})
                            if not warnings_data:
                                warnings_data = next((g for g in description_groups if g.get('header') == 'Navodila za uporabo'), {})
                            
                            raw_warning_text = warnings_data.get('contentBlock', [{}])[0].get('texts', [""])[0]

                            usage_data = next((g for g in description_groups if g.get('header') == 'Navodilo za uporabo'), None)
                            if usage_data:
                                raw_usage_text = usage_data.get('contentBlock', [{}])[0].get('texts', [""])[0]
                            
                            ine = next((g for g in description_groups if g.get('header') == 'Sestavine'), {})
                            raw_ingredients_text = ine.get('contentBlock', [{}])[0].get('texts', [""])[0]
                            
                            company = next((g for g in description_groups if g.get('header') == 'Naslov podjetja'), {})
                            c_company_address = company.get('contentBlock', [{}])[0].get('texts', [""])[0]


                            raw_manufacture = next((g for g in description_groups if g.get('header') == 'Proizvedeno v'), {})
                            manufacture = raw_manufacture.get('contentBlock', [{}])[0].get('texts', [""])[0]

                            raw_product_durability = next((g for g in description_groups if g.get('header') == 'Informacije o trajnosti izdelka'), {})
                            product_durability = raw_product_durability.get('contentBlock', [{}])[0].get('texts', [""])[0]


                            unit_info_text = datas.get('price', {}).get('infos', [""])[0]
                            if unit_info_text:
                                info = unit_info_text.split('(')[0].strip() # "1 kos"
                                raw_site_shown = info
                                
                                split_parts = info.split()
                                if len(split_parts) >= 2:
                                    raw_quantity = split_parts[0] # "1"
                                    raw_unit = split_parts[1]     # "kos"
                                elif len(split_parts) == 1:
                                    raw_quantity = split_parts[0]

                    except Exception as e:
                        pass
                
                name = " ".join(product.get("title", "").split()).replace('\n', ' ').replace('\r', ' ').strip()
                brand = " ".join(product.get('brandName', "").split()).replace('\n', ' ').replace('\r', ' ').strip()
                features = " ".join(features_string.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').strip()
                description = " ".join(description_text.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').strip()
                
                warning = " ".join(raw_warning_text.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('*'," ").strip()
                ingredients = " ".join(raw_ingredients_text.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('*','').replace('•','').strip()
                company_address = " ".join(c_company_address.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').strip()

                Instructions = " ".join(raw_usage_text.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('-','').strip()

                product_durability_info = " ".join(product_durability.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('-','').replace('.','').strip()

                
                site_shown_uom = raw_site_shown
                grammage_quantity = raw_quantity.strip()
                grammage_unit = raw_unit.strip()

                manufactured = " ".join(manufacture.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('-','').strip()

                yield {
                    "unique_id": product.get("gtin") or "",
                    "competitor_name": "dm",
                    "product_name": name,
                    "brand_name": brand,
                    "color_variant": color_variant,
                    "product_durability_info" :product_durability_info,
                    "grammage_quantity": grammage_quantity,
                    "grammage_unit": grammage_unit,
                    "features": features,
                    "selling_price": selling_price.replace(',', '.'),
                    "currency": tile.get("trackingData", {}).get("currency") or "",
                    "images": all_images_combined,
                    "manufactured": manufactured,
                    "rating": round(float(rating), 2) if rating else "",
                    "review_count": review_count,
                    "ingredients": ingredients.replace('-', '').replace('[', '').replace(']', '').replace('+', ''),
                    "Instructions": Instructions,
                    "warning": warning,
                    "breadcrumbs": breadcrumbs,
                    "pdp_url": self.base_url + tile.get("self", ""),
                    "site_shown_uom": site_shown_uom,
                    "product_id": dan,
                    "company_address": company_address,
                    "description": description
                }


spider = dm_spider()

with open("final_si_dm_data_20260625.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "unique_id",
            "competitor_name",
            "product_name",
            "brand_name",
            "color_variant",
            "product_durability_info",
            "grammage_quantity",
            "grammage_unit",
            "features",
            "selling_price",
            "currency",
            "images",
            "manufactured",
            "review_count",
            "rating",
            "ingredients",
            "Instructions",
            "warning",
            "breadcrumbs",
            "pdp_url",
            "product_id",
            "site_shown_uom",
            "company_address",
            "description",  
        ]
    )

    writer.writeheader()

    for item in spider.parse():
        writer.writerow(item)
        print(f"Saved: {item['product_name']}")