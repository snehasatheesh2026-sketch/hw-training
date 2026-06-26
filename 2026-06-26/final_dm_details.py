import csv
import time
import requests


class dm_scraper:

    def __init__(self):
        self.base_url = "https://www.dm.si"
        self.starting_url = "https://product-search.services.dmtech.com/si/search/static"
        self.product_detail_base_url = "https://products.dm.de/product/products/detail/SI/dan"

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
            "brandName": ["PHILIPS", "PHILIPS AVENT", "PHILIPS OneBlade", "Philips Sonicare"],
            "pageSize": "50",
            "sort": "new",
            "currentPage": "0",
            "searchType": "editorial-search",
            "type": "search-static",
        }

    def parse(self):
        params = self.params.copy()
        if "categoryNames" in params:
            del params["categoryNames"]

        try:
            res_json = requests.get(self.starting_url, params=params, headers=self.headers).json()
            subcategories = [v["name"] for facet in res_json.get("facets", []) if facet.get("key") == "categoryNames" for v in facet.get("values", []) if "name" in v]
            print(f"Subcategories found: {subcategories}\n")
        except Exception as e:
            print(f"Error reading initial JSON: {e}")
            return

        for sub_cat in subcategories:
            current_page = 0
            while True:
                params["categoryNames"] = sub_cat
                params["currentPage"] = str(current_page)
                print(f"Fetching {sub_cat} - Page {current_page}...")

                try:
                    response = requests.get(self.starting_url, params=params, headers=self.headers)
                    if response.status_code != 200:
                        break
                    
                    data = response.json()
                    products = data.get("products", [])
                    if not products:
                        break

                    for product in products:
                        tile_data = product.get("tileData", {})
                        unique_id = product.get("dan") or ""
                        
                        breadcrumbs, product_description, ingredients, c_company_address = [], "", "", ""
                        manufactured, scope_of_deliverye, required_info, all_images_combined = "", "", "", ""
                        raw_site_shown, raw_quantity, raw_unit = "", "", ""

                        price = tile_data.get("price", {}).get("price", {}).get("current", {}).get("value", "")
                        rating = tile_data.get("rating", {}).get("ratingValue") or ""
                        review_count = tile_data.get("rating", {}).get("ratingCount") or ""

                        if unique_id:
                            try:
                                detail_url = f"{self.product_detail_base_url}/{unique_id}"
                                detail_res = requests.get(detail_url, headers=self.headers).json()
                                
                                breadcrumbs = detail_res.get("breadcrumbs", [])
                                description_groups = detail_res.get('descriptionGroups', [])
                                
                                all_images_combined = ", ".join([img.get("src", "") for img in detail_res.get("images", []) if img.get("src")])

                                content_blocks = description_groups[0].get('contentBlock', []) if len(description_groups) > 0 else []
                                traget = "  ".join(content_blocks[0].get('bulletpoints', [])) if len(content_blocks) > 0 else ""
                                target_text = content_blocks[1].get('texts', [""])[0] if len(content_blocks) > 1 else ""
                                product_description = (traget + " " + target_text).strip() if traget else target_text.strip()

                                raw_ingredients = next((g for g in description_groups if g.get('header') == 'Sestavine'), {})
                                ingredients = " ".join(" ".join(b.get('texts', [])) for b in raw_ingredients.get('contentBlock', [])).strip()

                                company = next((g for g in description_groups if g.get('header') == 'Naslov podjetja'), {})
                                c_company_address = company.get('contentBlock', [{}])[0].get('texts', [""])[0] if company.get('contentBlock') else ""

                                raw_manufacture = next((g for g in description_groups if g.get('header') == 'Proizvedeno v'), {})
                                manufactured = raw_manufacture.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_manufacture.get('contentBlock') else ""

                                raw_scope_of_delivery = next((g for g in description_groups if g.get('header') == 'Obseg dobave'), {})
                                scope_of_deliverye = raw_scope_of_delivery.get('contentBlock', [{}])[0].get('texts', [""])[0] if raw_scope_of_delivery.get('contentBlock') else ""


                                price_section = tile_data.get('price', {})
                                base_unit = price_section.get('basePricePeriod', '') or price_section.get('salesUnit', '')
                                
                                if base_unit:
                                    raw_site_shown = f"1 {base_unit}".strip()
                                    raw_quantity = "1"
                                    raw_unit = base_unit.strip()
                                elif detail_res.get('netQuantityContent'):
                                    info = str(detail_res.get('netQuantityContent')).split('(')[0].strip()
                                    raw_site_shown = info
                                    split_parts = info.split()
                                    raw_quantity = split_parts[0] if len(split_parts) >= 1 else ""
                                    raw_unit = split_parts[1] if len(split_parts) >= 2 else ""
                                else:
                                    raw_site_shown = ""
                                    raw_quantity = ""
                                    raw_unit = ""

                                req_grp = next((g for g in description_groups if g.get('header') == 'Obvezne informacije'), {})
                                req_content_blocks = req_grp.get('contentBlock', [])
                                required_info = req_content_blocks[0].get('links', [{}])[0].get('linkText', '') if len(req_content_blocks) > 0 and len(req_content_blocks[0].get('links', [])) > 0 else ""

                                time.sleep(0.2)
                            except Exception as detail_err:
                                print(f"Error fetching details for {unique_id}: {detail_err}")

                        company_address = " ".join(c_company_address.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').strip()
                        manufactured_in = " ".join(manufactured.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('-', '').strip()
                        scope_of_delivery = " ".join(scope_of_deliverye.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('-', '').strip()
                        ingredient = " ".join(ingredients.split()).replace('\n', ' ').replace('\r', ' ').replace('|', ' ').replace('-', '').strip()
                        Mandatory_information = required_info.replace('\n', "").replace('\r', "").replace('-', "").strip()
                        product_description = product_description.replace('\n', "").replace('\r', "").replace('-', "").strip()
                    
                        yield {
                            "unique_id": unique_id,
                            "sub_category": sub_cat,
                            "brand_name": product.get("brandName", "").strip(),
                            "product_name": tile_data.get("title", {}).get("tileHeadline", "").strip(),
                            "price": price.replace("€", "").replace(',', '.').strip(),
                            "breadcrumb": " > ".join(breadcrumbs),
                            "pdp_url": self.base_url + tile_data.get("self", ""),
                            "product_id": product.get("gtin") or "",
                            "competitor_name": "dm",
                            "product_description": product_description or "",
                            "ingredients": ingredient.replace(".", " "),
                            "company_address": company_address,
                            "manufactured_in": manufactured_in,
                            "site_shown_uom": raw_site_shown,
                            "currency": tile_data.get("trackingData", {}).get("currency") or "",
                            "Mandatory_information": Mandatory_information,
                            "review_count": review_count,
                            "rating": round(float(rating), 2) if rating else "",
                            "images": all_images_combined,
                            "grammage_unit": raw_unit.strip(),
                            "grammage_quantity": raw_quantity.strip(),
                            "scope_of_delivery": scope_of_delivery or "",
                        }
                    
                    if len(products) < int(params["pageSize"]):
                        break
                    current_page += 1
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Error parsing products in {sub_cat} page {current_page}: {e}")
                    break

            time.sleep(1)


spider = dm_scraper()
fields = [
    "unique_id", 
    "sub_category", 
    "brand_name", 
    "product_name", 
    "price", 
    "currency",
    "product_id",
    "competitor_name", 
    "ingredients", 
    "Mandatory_information", 
    "company_address",
    "manufactured_in", 
    "grammage_unit", 
    "grammage_quantity", 
    "rating", 
    "review_count",
    "breadcrumb", 
    "pdp_url", 
    "scope_of_delivery", 
    "images", 
    "site_shown_uom", 
    "product_description"
]

with open("dm_si_data_20260626.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for item in spider.parse():
        writer.writerow(item)

print("Data scraping completed and saved successfully.")