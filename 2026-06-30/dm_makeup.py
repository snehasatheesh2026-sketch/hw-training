  
import csv
import time
import requests
import json

class Dm_makeup:

    def __init__(self):
        self.base_url = "https://www.dm.si"
        self.tree_url = "https://products.dm.de/categories/v1/categories-tree/sl-SI"
        self.strating_url = "https://product-search.services.dmtech.com/si/search/static"
        self.details = "https://products.dm.de/product/products/detail/SI/dan/"
        self.output_csv = "dm_makeup_data1.csv"
        
        # tree
        self.headers = {
            "sec-ch-ua-platform": '"Linux"',
            "Referer": "https://www.dm.si/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
        }
        # sub product
        self.headerss = {
            'sec-ch-ua-platform': '"Linux"',
            'x-dm-product-search-token': '48130558781589',
            'Referer': 'https://www.dm.si/',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'x-dm-product-search-tags': 'presentation:grid;search-type:editorial;channel:web;editorial-type:category',
        }

        self.details_header = {
            'accept': '*/*',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.dm.si',
            'referer': 'https://www.dm.si/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            'x-dm-version': '2026.624.73333-1',
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
                leaves[node.get("name")] = node.get("code")
        return leaves
    
    def sub_categories(self):  
        response = requests.get(self.tree_url, headers=self.headers)
        if response.status_code == 200:
            for root_node in response.json():
                if root_node.get("name") == "Ličila":
                    return self.leaf_categories([root_node])
        return {}
    
    def parse(self):
        categories = self.sub_categories()
      
        seen_ids = set()

        for cat_name, cat_id in categories.items():
            current_category_param = self.params.copy()
            current_category_param['allCategories.id'] = cat_id

            response = requests.get(self.strating_url, headers=self.headerss, params=current_category_param)
            if response.status_code != 200:
                print(f"{cat_id} statuscode == {response.status_code}")
                continue

            data = response.json()
            total_pages = data.get('totalPages', 1)

            for page in range(total_pages):
                current_params = current_category_param.copy()
                current_params['currentPage'] = page

                page_res = requests.get(self.strating_url, headers=self.headerss, params=current_params)
                if page_res.status_code != 200:
                    print(f"{page} == {page_res.status_code}")
                    continue

                page_data = page_res.json()

                for product in page_data.get("products", []):
                    unique_id = product.get("gtin") or ""
                    
                    # to remove dupliactes
                    if unique_id and unique_id in seen_ids:
                        continue
                        
                    tile_data = product.get("tileData", {})
                    pdp_url = tile_data.get("self", "")
                    dan = tile_data.get("dan")

                    raw_price = tile_data.get("price", {}).get("price", {}).get("current", {}).get("value")
                    selling_price = raw_price.replace("€", "").replace("$", "").strip() if raw_price else ""

                    raw_images = tile_data.get("images", [])
                    image_url_list = []
                
                    for img in raw_images:
                        src = img.get("tileSrc", "")
                        if src and src not in image_url_list:
                            image_url_list.append(src)
                
                    all_images_combined = ", ".join(image_url_list)
                    rating = tile_data.get("rating", {}).get("ratingValue")
                    review_count = tile_data.get("rating", {}).get("ratingCount") or ""

                    description_text = ""
                    breadcrumbs = ""
                    raw_ingredients_text = ""
                    raw_warning_text = ""
                    c_company_address = ""
                    features_string = ""
                    color_variant = ""
                    manufacture = ""
                    raw_usage_text = ""
                    quantity = ""
                    unit = ""
                    site_shown_up = ""

                    if dan:
                        details_url = self.details + str(dan)
                        try:
                            response = requests.get(details_url, headers=self.details_header)
                            if response.status_code == 200:
                                datas = response.json()

                                sit_shown = datas.get('price', {}).get('infos', [])
                                if sit_shown:
                                    r_text = sit_shown[0] 
                                    c_text = r_text.split('(')[0].strip()
                                    
                                    
                                    quantity = c_text.split()[0] if len(c_text.split()) > 0 else ""
                                    unit = c_text.split()[-1] if len(c_text.split()) > 0 else ""
                                    site_shown_up = c_text

                                description_groups = datas.get('descriptionGroups', [])
                                traget = "  ".join(
                                    description_groups[0].get('contentBlock', [{}])[0].get('bulletpoints', [])
                                    if len(description_groups) > 0 else []
                                )
                               
                                target_text = ""
                                content_blocks = description_groups[0].get('contentBlock', []) if len(description_groups) > 0 else []

                                if len(content_blocks) > 1:
                                    target_text = content_blocks[1].get('texts', [""])[0]

                                description_text = traget + " " + target_text if traget else target_text

                                raw_breadcrumbs = datas.get("breadcrumbs", [])
                                breadcrumbs = " > ".join(raw_breadcrumbs) if raw_breadcrumbs else ""

                                ine = next((g for g in description_groups if g.get('header') == 'Sestavine'), {})
                                raw_ingredients_text = ine.get('contentBlock', [{}])[0].get('texts', [""])[0] if ine else ""

                                company = next((g for g in description_groups if g.get('header') == 'Naslov podjetja'), {})
                                c_company_address = company.get('contentBlock', [{}])[0].get('texts', [""])[0] if company else ""

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
                                       
                                features_group = next((g for g in description_groups if g.get('header') == 'Značilnosti'), {})
                                raw_features_list = features_group.get('contentBlock', [{}])[0].get('descriptionList', []) if features_group else []

                                usage_data = next((g for g in description_groups if g.get('header') == 'Navodilo za uporabo'), None)
                                if usage_data:
                                    raw_usage_text = usage_data.get('contentBlock', [{}])[0].get('texts', [""])[0]
                            
                                features_array = []
                                for item in raw_features_list:
                                    key = item.get('title', '').strip()
                                    val = item.get('description', '').strip()
                                    if key and val:
                                        key_clean = " ".join(key.split())
                                        val_clean = " ".join(val.split())
                                        features_array.append(f"{key_clean}: {val_clean}")
                            
                                features_string = " ".join(features_array)

                                warnings_data = next((g for g in description_groups if g.get('header') == 'Opozorila'), {})
                                if not warnings_data:
                                    warnings_data = next((g for g in description_groups if g.get('header') == 'Navodila za uporabo'), {})
                            
                                raw_warning_text = warnings_data.get('contentBlock', [{}])[0].get('texts', [""])[0] if warnings_data else ""

                                raw_manufacture = next((g for g in description_groups if g.get('header') == 'Proizvedeno v'), {})
                                manufacture = raw_manufacture.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_manufacture else ""

                        except Exception as e:
                            pass
                    
                    description = " ".join(description_text.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').strip()
                    ingredients = " ".join(raw_ingredients_text.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('*','').replace('•','').strip()
                    brand = " ".join(product.get('brandName', "").split()).replace('\n', ' ').replace('\r', ' ').strip()
                    company_address = " ".join(c_company_address.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').strip()
                    features = " ".join(features_string.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').strip()
                    warning = " ".join(raw_warning_text.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('*'," ").strip()
                    manufactured = " ".join(manufacture.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('-','').strip()
                    Instructions = " ".join(raw_usage_text.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('-','').strip()
                    quantity_str = str(quantity).strip() if quantity else ""
                    cleaned_quantity = quantity_str.replace(',', '.')

    
                    if unique_id:
                        seen_ids.add(unique_id)

                    yield {
                        "unique_id": unique_id,
                        "product_name": product.get("title", "").strip(),
                        "sub_category_name": cat_name,
                        "brand": brand,
                        "price": selling_price.replace(',','.') or "",
                        "currency": tile_data.get("trackingData", {}).get("currency") or "",
                        "grammage_quantity": round(float(cleaned_quantity), 2) if cleaned_quantity else "",
                        "grammage_unit": unit,
                        "color_variant": color_variant,
                        "rating": round(float(rating), 2) if rating else "",
                        "review_count": review_count or "",
                        "ingredients": ingredients,
                        "features": features,
                        "warning": warning,
                        "Instructions": Instructions,
                        "images": all_images_combined,
                        "breadcrumbs": breadcrumbs,
                        "pdp_url": self.base_url + pdp_url,
                        "company_address": company_address,
                        "part_number": dan,
                        "description": description,
                        "manufactured": manufactured,
                        "competitor_name": "dm",
                        "site_shown_up": site_shown_up,
                    }
                    
                time.sleep(0.5)

if __name__ == "__main__":
    spider = Dm_makeup()

    with open(spider.output_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["unique_id","product_name","sub_category_name","brand","price","currency","grammage_quantity","grammage_unit","color_variant","rating","review_count","ingredients","features","warning","Instructions","images","breadcrumbs","pdp_url","company_address","part_number","description","manufactured","competitor_name","site_shown_up"]
        )
        writer.writeheader()

        total_count = 0
        for item in spider.parse():
            writer.writerow(item)
            total_count += 1

    print(f" Total links collected == {total_count}")




