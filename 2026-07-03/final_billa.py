
import requests
import csv                                   
import math
import time
from bs4 import BeautifulSoup
import re

class BillaFullListing:
    def __init__(self):
        self.base_url = "https://shop.billa.at"
        
        self.child_url_template = "https://shop.billa.at/api/product-discovery/categories/{}/child-properties"
        
        
        self.api_url_template = "https://shop.billa.at/api/product-discovery/categories/{}/products"
        
        
        self.params_template = {
             
                      'sortBy': 'relevance',
                      'enableStatistics': 'true',
                      'enablePersonalization': 'false',
                      'page': '0',
                      'pageSize': '30',

        }
        
        self.product_details ="https://shop.billa.at/api/product-discovery/products/{}"
        self.headers = {
                      'accept': 'application/json, text/plain, */*',
                      'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
                      'credentials': 'include',
                      'priority': 'u=1, i',
                      'referer': 'https://shop.billa.at/kategorie/obst-und-gemuese-13751',
                      'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
                      'sec-ch-ua-mobile': '?0',
                      'sec-ch-ua-platform': '"Linux"',
                      'sec-fetch-dest': 'empty',
                      'sec-fetch-mode': 'cors',
                      'sec-fetch-site': 'same-origin',
                      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                      'x-request-id': '855c46be-373c-474f-87e1-73ec0daf2842-1782882134183',
                      'x-xsrf-token': 'a1d2d9fb-f1ef-4d9c-80f5-856a9b7a978e',
                         # 'cookie': 'OptanonAlertBoxClosed=2026-06-03T07:13:05.755Z; _ga=GA1.1.1772728611.1780470786; AMCV_65BE20B35350E8DE0A490D45%40AdobeOrg=179643557%7CMCMID%7C54368768429409811658194547869777301378%7CvVersion%7C5.5.0; _pin_unauth=dWlkPVlqbGpNRFk0TlRrdE5tWTRPUzAwTW1NMUxXRTVOemd0TVRJd09EZGxOelk0TURBNQ; FPID=FPID2.2.ROoF50PKyKPwZ%2FlTogqmEgRGVW5dF8bzTM6MoVzhpsM%3D.1780470786; FPAU=1.2.591820856.1780470787; _gtmeec=e30%3D; _fbp=fb.1.1780470786836.1640415081; _hjSessionUser_3495869=eyJpZCI6IjkxYTNjN2QyLTExY2MtNTdlNS04ODdmLTRmZmZmYTBlNGVlMyIsImNyZWF0ZWQiOjE3ODA0NzA3ODY3MjUsImV4aXN0aW5nIjp0cnVlfQ==; XSRF-TOKEN=a1d2d9fb-f1ef-4d9c-80f5-856a9b7a978e; s_cc=true; FPLC=otnCgfAMVHKG3Si%2F3D0RxrEaSJWIRteG4IHbYqH9KTGu5JI9OnwSJUu2cWDNapoWzdFRIPQvAYNCrienIra0%2FG6j7VAuzzQGmBHoQTk34fa2WsepFFrcnuokgxOEzg%3D%3D; _hjSession_3495869=eyJpZCI6IjhjYmE2ZWZhLWZhZmEtNGY1MS1iNGIxLTBmZDMyMTkyNWI5OSIsImMiOjE3ODI4ODIxNDA5MzgsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; s_ips=502; _ga_5YE339L5ME=GS2.1.s1782882139$o4$g1$t1782882935$j56$l0$h1388560046; _ga_4EYV7CD9R4=GS2.1.s1782882139$o4$g1$t1782882935$j56$l0$h1968999525; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jul+01+2026+10%3A45%3A35+GMT%2B0530+(India+Standard+Time)&version=202602.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&genVendors=&consentId=7f04441b-8a3b-46a0-bbb2-1903cec23cba&interactionCount=1&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&intType=1&crTime=1780470786290&geolocation=%3B&AwaitingReconsent=false; _uetsid=0a9528f0750a11f1a4b9fb6009f97839; _uetvid=ab109a805f1b11f1993925eefa2fcb67; gpv_PageType=products; gpv_PageURL=https%3A%2F%2Fshop.billa.at%2Fkategorie%2Fobst-und-gemuese-13751; s_tp=2795; s_ppv=billa-at-shop%253Akategorie%253Aobst-und-gemuese-13751%2C18%2C18%2C502%2C1%2C5',
        }
        self.final_leaves = {}

    def crawl_node(self, category_id, category_name):
        
        url = self.child_url_template.format(category_id)
        try:
            response = requests.get(url, headers=self.headers)
            time.sleep(0.3)
            
            if response.status_code != 200:
                return

            child_nodes = response.json()

            if isinstance(child_nodes, list) and len(child_nodes) > 0:
                for child in child_nodes:
                    child_id = child.get("slug")
                    child_name = child.get("name")
                    self.crawl_node(child_id, child_name)
            else:
                self.final_leaves[category_name] = category_id

        except Exception as e:
            print(f" Error  {category_id}: {e}")

    def parse(self):
        
        root_id = "obst-und-gemuese-13751"

        self.crawl_node(root_id, "Obst & Gemüse Root")
        
        pagenat_size = 30
        seen_ids = set()

        for cat_name, cat_id in self.final_leaves.items():
            if not cat_id:
                continue
                
            print(f"Scraping: {cat_name} ({cat_id})")
            page = 0
            
            target_api_url = self.api_url_template.format(cat_id)
            
            while True:
                current_params = self.params_template.copy()
                current_params["page"] = page
                
                try:
                    response = requests.get(target_api_url, headers=self.headers, params=current_params)
                    time.sleep(0.4)
                    
                    if response.status_code != 200:
                        break
                        
                    data = response.json()
                    products = data.get("results", [])
                    
                    if not products or len(products) == 0:
                        break

                    total_items = data.get("total", 0)
                    server_count = data.get("count", len(products))
                    
                    print(f"  Page {page} processed... Batch Count: {server_count}/{total_items}")

                    for product in products:
                        product_id = product.get('sku', "")
                        slug = product.get("slug", "")

                        price_field = product.get('price', {})
                        regular_raw_price = price_field.get('regular', {}).get("value", "")
                        price_per_unit = price_field.get('regular', {}).get('perStandardizedQuantity', "")
                        uom = price_field.get('baseUnitShort', '') 

                        diet_tags = ",".join(product.get('badges', []))
                        pack_size = f"{str(product.get('amount', ''))}{product.get('volumeLabelShort', '')}"

                        product_images = product.get('images', [])
                        image_urls = [img for img in product_images if img]
                        images_field = ", ".join(image_urls)

                        brand = product.get('brand', {}).get('name', '')

        
                        
                        raw_short = product.get('descriptionShort', '') or ""
                        raw_long = product.get('descriptionLong', '') or ""
                        raw_combined = f"{raw_long} {raw_short}".strip()

                        
                        clean_stage1 = re.sub(r'<br[^>]*>', ' ', raw_combined, flags=re.IGNORECASE)

                        
                        clean_stage1 = clean_stage1.replace("<li>", " , ").replace("</li>", " ")


                        soup = BeautifulSoup(clean_stage1, "html.parser")
                        clean_stage2 = soup.get_text()

                        
                        clean_stage3 = re.sub(r'<[^>]*>?', ' ', clean_stage2)

                        
                        descriptions = " ".join(clean_stage3.split()).strip()

                        
                        descriptions = descriptions.replace(" , ,", ",").replace(" ,", ",").replace(".,", ".").strip()

                        package_type = product.get("packageLabel", '')

                        parent_cats_list = product.get('parentCategories', [[]])
                        if parent_cats_list and isinstance(parent_cats_list[0], list):
                            breadcrumb_names = [cat.get('name', '').strip() for cat in parent_cats_list[0] if cat.get('name')]
                            breadcrumbs = " > ".join(breadcrumb_names)
                        else:
                            breadcrumbs = ""

                        if product_id and product_id in seen_ids:
                            continue
                        if product_id:
                            seen_ids.add(product_id)

                        nutrition_str = ""
                        email = ""
                        address = ""
                        phone_no = ""
                        variety = ""
                        manufacturersAddress = ""
                        Country_of_production = ""

                        diet_attributes = ""

                        if product_id:
                            details_url = self.product_details.format(product_id)
                            print(details_url)
                            try:
                                response = requests.get(details_url, headers=self.headers)
                                if response.status_code == 200:
                                    print("")
                                    datas = response.json()

                                    info_list = datas.get('additionalInformation', [])
                                    info = info_list[0] if info_list else {}

                                    details_of_office = info.get('productInformation', {}).get('contactDetails', {})
                                    nutrition_data = info.get('foodInformation', {}).get('calculatedNutrition', {}).get('data', [])

                                    nutrition_str = ", ".join([f"{i.get('name', '').strip()}: {i.get('valuePer100', '').strip()}" for i in nutrition_data])

                                    Country_of_production = datas.get('countryOfOrigin', '')
                                    phone_no = details_of_office.get('phone', '')
                                    email = details_of_office.get('email', '')
                                    address = details_of_office.get('address', '')

                                    raw_manu_address = info.get('productInformation', {}).get('manufacturersAddress', '')
                                    manufacturersAddress = ", ".join([line.strip() for line in raw_manu_address.splitlines() if line.strip()])

                                    variety = datas.get('variety', '')
                                    ingredients =info.get('foodInformation', {}).get('ingredientsText', '')

                                    diet= info.get('productInformation', {}) 

                                    diet_list = []
                                    for group in diet.get('otherAttributes', []):

                                        for attr in group.get('attributes', []):

                                            if attr.get('attributeCode') == 'DIET_TYPE':

                                                value = attr.get('valueTranslation', '')

                                                if value:
                                                    diet_list.append(value)
                                    diet_attributes = ", ".join(diet_list)

                                    diet_attributes = diet_attributes.replace('\n'," ")

                                    


                            except Exception as e:
                                pass

                        

                        yield {
                            "unique_id": product_id,
                            "product_name": product.get("name", "") or "",
                            "diet_tags": diet_tags,
                            "breadcrumbs": breadcrumbs,
                            "regular_price": round(regular_raw_price / 100, 2) if regular_raw_price else "",
                            "price_per_unit": round(price_per_unit / 100, 2) if price_per_unit else "",
                            "cateogry_name": cat_name,
                            "Country_of_production": Country_of_production, 
                            "pack_size": pack_size or "",
                            "package_type": package_type or "",
                            "images": images_field,
                            "Phone_no": phone_no,
                            "pdp_url": f"{self.base_url}/produkte/{slug}" if slug else "",
                            "nutrition": nutrition_str,
                            "describition": descriptions,
                            "Unit_of_Measure": uom or "",
                            "competitor_name": "Billa",
                            "brand": brand or "",
                            "email": email or "",
                            "address": address or "",
                            "variety": variety or "",
                            "manufacturersAddress": manufacturersAddress,
                            "weight" : f"{str(product.get('weight',''))}",
                            "ingredients":ingredients,
                            "diet_attributes":diet_attributes,
                        }
                    
                    if total_items > pagenat_size:
                        total_pages = math.ceil(total_items / server_count) if server_count > 0 else 1
                        if page < total_pages:
                            page += 1
                            continue
                            
                    break
                    
                except Exception as e:
                    print(f" error {page}: {e}")
                    break

                        



if __name__ == "__main__":
    spider = BillaFullListing()
    csv_filename = "billa_data2.csv"
    
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=["unique_id","cateogry_name" ,"brand","product_name","Country_of_production","regular_price","diet_tags","diet_attributes","pack_size","package_type","weight","ingredients","price_per_unit","images","nutrition","manufacturersAddress","Phone_no","address","email","variety","breadcrumbs","pdp_url","describition","Unit_of_Measure", "competitor_name"]
        )
        writer.writeheader()

        for item in spider.parse():
            writer.writerow(item)

    print(f"{csv_filename}Saved.")