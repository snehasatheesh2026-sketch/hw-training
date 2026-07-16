import requests
import time
import csv
import re
from unidecode import unidecode


def create_url(name, product_id):

    clean_name = unidecode(name)
    clean_name = clean_name.lower()

    clean_name = re.sub(r'[^a-zA-Z0-9]+', '-', clean_name)
    clean_name = re.sub(r'-+', '-', clean_name)
    clean_name = clean_name.strip('-')

    return f"https://auchan.hu/shop/{clean_name}.p-{product_id}"



class EndCategories:

    def __init__(self):

        self.url = "https://auchan.hu/api/v2/cache/tree/0"

        self.headers = {
        'accept': 'application/json',
        'accept-language': 'hu',
        'authorization': 'Bearer {token}',
        'if-none-match': 'W/"71767d982d40f5372e8433c04634200e"',
        'priority': 'u=1, i',
        'referer': 'https://auchan.hu/shop',
        'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'x-aw-request-id': '',
        'x-aw-tab-id': '',
       # 'cookie': 'AhuAU_C=; login_type=anon; aw_notification_info=%7B%7D; .',
      }

        self.params = {
            'cacheSegmentationCode': 'DS',
            'hl': 'hu',
        }


        self.product_url = "https://auchan.hu/api/v2/cache/products"

        self.product_headers = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer {token}',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/medence-es-kiegeszitok/medence-strandjatek/medence-es-kiegeszitok/merev-falu-csaladi-medencek.c-7593',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '',
    'x-aw-tab-id': '',
    # 'cookie': 'AhuAU_C=; login_type=anon; aw_notification_info=%7B%7D; isWebpFormatSupportedAlgo0=true; token_type=Bearer; access_token=.
        }

        self.product_params = {
            'itemsPerPage': '12',
            'page': '1',
            'cacheSegmentationCode': 'DS',
             'hl': 'hu',
        }

        self.end_categories_dict = {}

        self.seen_pdp_urls = set()


    def get_end_categories_dict(self):

        try:

            response = requests.get(
                self.url,
                headers=self.headers,
                params=self.params
            )

            time.sleep(1)


            if response.status_code == 200:

                all_data = response.json()


                def extract(node):

                    if isinstance(node, dict):

                        children = node.get("children", [])


                        if not children and "id" in node:

                            cat_id = node.get("id")
                            cat_name = node.get("name")


                            self.end_categories_dict[cat_id] = cat_name


                        else:

                            for child in children:
                                extract(child)



                if isinstance(all_data, list):

                    for item in all_data:
                        extract(item)


                elif isinstance(all_data, dict):

                    extract(all_data)



        except Exception as e:

            print(f"Error: {e}")


        return self.end_categories_dict





    def parse(self):

        categories = self.get_end_categories_dict()


        for cat_id, cat_name in categories.items():

            print("\n====================")
            print("Category:", cat_name)
            print("ID:", cat_id)
            print("====================")



            current_category_params = self.product_params.copy()


            current_category_params["categoryId"] = cat_id



            response = requests.get(
                self.product_url,
                headers=self.product_headers,
                params=current_category_params
            )


            time.sleep(0.1)



            if response.status_code != 200:

                print(
                    f"{cat_id} statuscode == {response.status_code}"
                )

                continue



            data = response.json()


            total_pages = int(
                data.get("pageCount", 0)
            )


            print("Total Pages:", total_pages)



            for page in range(1, total_pages + 1):


                current_params = current_category_params.copy()


                current_params["cpage"] = page



                page_response = requests.get(
                    self.product_url,
                    headers=self.product_headers,
                    params=current_params
                )


                time.sleep(1)



                if page_response.status_code == 200:


                    page_data = page_response.json()


                    products = page_data.get(
                        "results",
                        []
                    )


                    print(
                        "Page:",
                        page,
                        "Products:",
                        len(products)
                    )



                    for product in products:


                        pdp_url_details = product.get(
                            "selectedVariant",
                            {}
                        )


                        name = pdp_url_details.get(
                            "name",
                            ""
                        )


                        sku = pdp_url_details.get(
                            "sku",
                            ""
                        )
                        


                        pdp_url = create_url(
                            name,
                            sku
                        )

                        if pdp_url in self.seen_pdp_urls:
                            continue


                        self.seen_pdp_urls.add(pdp_url)




                        yield {

                            "sub_category_name": cat_name,

                            "pdp_url": pdp_url

                        }



                else:

                    print(
                        "Page:",
                        page,
                        "Status:",
                        page_response.status_code
                    )







if __name__ == "__main__":


    scraper = EndCategories()



    with open(
        "auchan_pdp_urls.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer = csv.DictWriter(
            file,
            fieldnames=[
                "sub_category_name",
                "pdp_url"
            ]
        )


        writer.writeheader()



        for row in scraper.parse():

            writer.writerow(row)



    print("CSV saved successfully")