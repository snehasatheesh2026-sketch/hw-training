import requests
import csv                                         # correct one
import math
import time

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
            print(f" Error  category {category_id}: {e}")

    def parse(self):
      
        root_id = "obst-und-gemuese-13751"
        
        self.crawl_node(root_id, "Obst & Gemüse Root")
    

        pagenat_size = 30
        seen_ids = set()

        for cat_name, cat_id in self.final_leaves.items():
            if not cat_id:
                continue
                
            print(f"Scraping {cat_name} ({cat_id})")
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
                    products = data.get("results", []) or data.get("tiles", [])
                    
                    if not products or len(products) == 0:
                        break

                    total_items = data.get("total", 0)
                    server_count = data.get("count", len(products))
                    

                    for product in products:
                        product_id = product.get('sku',"")
                        slug = product.get("slug", "")
                        
                        if product_id and product_id in seen_ids:
                            continue
                        if product_id:
                            seen_ids.add(product_id)

                        yield {
                            "unique_id": product_id,
                            "pdp_url": f"{self.base_url}/produkte/{slug}" if slug else "",
                            "competitor_name": "Billa"
                        }
                    
                    if total_items > pagenat_size:
                        total_pages = math.ceil(total_items / server_count) if server_count > 0 else 1
                        if page < total_pages:
                            page += 1
                            continue
                            
                    break
                    
                except Exception as e:
                    print(f"Pagination error on page {page}: {e}")
                    break

#
if __name__ == "__main__":
    spider = BillaFullListing()
    csv_filename = "billa_listing.csv"
    
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=["unique_id", "pdp_url", "competitor_name"]
        )
        writer.writeheader()

        for item in spider.parse():
            writer.writerow(item)

    print(f"'{csv_filename}'saved.")