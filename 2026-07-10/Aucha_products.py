import requests


class EndCategories:

    def __init__(self):

        self.url = "https://auchan.hu/api/v2/cache/tree/0"

        self.headers =  {
        'accept': 'application/json',
        'accept-language': 'hu',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImQ3Y2EyMWE2OTliOTE5MGFjODVkNjU4MTg3YmU0NjRjYWI5MTczNTFjYmRiMTY1NGI0MWU3NWJhOTQxMDhlMmY2YWJhOGFiYzJjNDA3N2IxIiwiaWF0IjoxNzgzNjYxMTk1LjI3MjM2MywibmJmIjoxNzgzNjYxMTk1LjI3MjM2NSwiZXhwIjoxNzgzNzQ3NTk1LjI0NzkzNywic3ViIjoiYW5vbl8zMjFlZWEyYS01NzA2LTRkMWEtOWZjMS05Mzc3YjEwYjU5NWYiLCJzY29wZXMiOltdfQ.T70J56W035FrzQQovZc-nWHhlQrdFYZFcEUs6SBb-aj6Y8mDKKE1DE7JTwUkBbdNJiatNF3piZiE2NzzT4cKukwvwOQta2ZBjbduJzTqcnEqKSeajpCOmKoFo6FoiwNdO7D9VgkbTPSwgo6nGCZQQgv0J9ncouLasj2e7zo_5flCtl9zHqedU6PgRy8-L8BsSa2lLkJGZfwTaINaemaF4uw1DrIjHfJ4Xx5YMk1YoPsQMajBZKhQiwQZzvFqadEbcaaOUkLmk4SBU557b_ea27RT4jHIePw5sj0g7uTmy8XhnahLg4zqL1iL9SmHY8jz6S6g_lBu6il6GtXxGsScng',
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
        'x-aw-request-id': '1783671891523_0_2404250_c_28',
        'x-aw-tab-id': '1783671891523_0_2404250',
       # 'cookie': 'AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; login_type=anon; aw_notification_info=%7B%7D; isWebpFormatSupportedAlgo0=true; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImQ3Y2EyMWE2OTliOTE5MGFjODVkNjU4MTg3YmU0NjRjYWI5MTczNTFjYmRiMTY1NGI0MWU3NWJhOTQxMDhlMmY2YWJhOGFiYzJjNDA3N2IxIiwiaWF0IjoxNzgzNjYxMTk1LjI3MjM2MywibmJmIjoxNzgzNjYxMTk1LjI3MjM2NSwiZXhwIjoxNzgzNzQ3NTk1LjI0NzkzNywic3ViIjoiYW5vbl8zMjFlZWEyYS01NzA2LTRkMWEtOWZjMS05Mzc3YjEwYjU5NWYiLCJzY29wZXMiOltdfQ.T70J56W035FrzQQovZc-nWHhlQrdFYZFcEUs6SBb-aj6Y8mDKKE1DE7JTwUkBbdNJiatNF3piZiE2NzzT4cKukwvwOQta2ZBjbduJzTqcnEqKSeajpCOmKoFo6FoiwNdO7D9VgkbTPSwgo6nGCZQQgv0J9ncouLasj2e7zo_5flCtl9zHqedU6PgRy8-L8BsSa2lLkJGZfwTaINaemaF4uw1DrIjHfJ4Xx5YMk1YoPsQMajBZKhQiwQZzvFqadEbcaaOUkLmk4SBU557b_ea27RT4jHIePw5sj0g7uTmy8XhnahLg4zqL1iL9SmHY8jz6S6g_lBu6il6GtXxGsScng; refresh_token=def502000021503cda4cad127037102059a7a0cb8b10860a694e938e1fa65e2d8730e95ac11fc29fafff5f4126828c7d7f9d3182eee3f0794cadc115c0ddff63197d6ef5abb282f9993a846890aaf8aeae4b26b41f3a40b2b1f89faaf3f79dde51829a5955327acadb07f6c66ff733c2fdb37cbbb548d932aca31c2b3745e22dd571bcd45d3a37ec93033d1dd016d37a08232532e09ddce63782caa21db1bb5287756aa40c5663f3d2a64508ab205c0626c8e059651643ef60a14f194554d6248249ca396231495286be2e9d968e5a2ddb103087302478be04fbb9af09ace22afe01844bbb6eb6a45cbca131368aec8c6c316c4fe01559e91aea84e18418bc64a27fca3fc290ab0a75d2919c4a19882a581bbb096ae4f9fc02708a710eca2d74e76ef89a43f70f36266490f789cda6560cb2b1eca2027814351509a3da31677f2321383ea936cee7d1c9f2ff42b7a027cfd8e8c126ee2a15d85e944456592bce472d9aeed8b81001dba1e0fa3afdca26af6c7838955c9aa25cd48e6073a53e33a640c678a686af0d5466ba64d76f4155b21bd5f95f55fca86db940b5616b2f9c7dda8c38ea0e98f761eb; _omappvp=8rTeayInSlShC7FBppi2lqxCsBANOUDnNdgHDmVoMUs14RXFwr0YAuHGORPl4aiXuz3kvSWhJVKYnHvIu8iS3x6Q8zZynEll; optiMonkClientId=1b96fb7c-4a6a-2df3-709b-df593b31fbf0; OptanonAlertBoxClosed=2026-07-10T05:37:14.238Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+10+2026+13%3A54%3A55+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=88c448d3-d75e-49df-b4c3-52f45c368585&interactionCount=2&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&AwaitingReconsent=false&geolocation=US%3BTX; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAbJaWAAxj4A2JS5V8pUAnJQHQRSEfADsA9gAdWpOtmxA=',
      }

        self.params = {
            'cacheSegmentationCode': 'DS',
            'hl': 'hu',
        }


        self.product_url = "https://auchan.hu/api/v2/cache/products"

        self.product_headers = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImQ3Y2EyMWE2OTliOTE5MGFjODVkNjU4MTg3YmU0NjRjYWI5MTczNTFjYmRiMTY1NGI0MWU3NWJhOTQxMDhlMmY2YWJhOGFiYzJjNDA3N2IxIiwiaWF0IjoxNzgzNjYxMTk1LjI3MjM2MywibmJmIjoxNzgzNjYxMTk1LjI3MjM2NSwiZXhwIjoxNzgzNzQ3NTk1LjI0NzkzNywic3ViIjoiYW5vbl8zMjFlZWEyYS01NzA2LTRkMWEtOWZjMS05Mzc3YjEwYjU5NWYiLCJzY29wZXMiOltdfQ.T70J56W035FrzQQovZc-nWHhlQrdFYZFcEUs6SBb-aj6Y8mDKKE1DE7JTwUkBbdNJiatNF3piZiE2NzzT4cKukwvwOQta2ZBjbduJzTqcnEqKSeajpCOmKoFo6FoiwNdO7D9VgkbTPSwgo6nGCZQQgv0J9ncouLasj2e7zo_5flCtl9zHqedU6PgRy8-L8BsSa2lLkJGZfwTaINaemaF4uw1DrIjHfJ4Xx5YMk1YoPsQMajBZKhQiwQZzvFqadEbcaaOUkLmk4SBU557b_ea27RT4jHIePw5sj0g7uTmy8XhnahLg4zqL1iL9SmHY8jz6S6g_lBu6il6GtXxGsScng',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/medence-es-kiegeszitok/medence-strandjatek/medence-es-kiegeszitok/merev-falu-csaladi-medencek.c-7593',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1783671891523_0_2404250_c_34',
    'x-aw-tab-id': '1783671891523_0_2404250',
    # 'cookie': 'AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; login_type=anon; aw_notification_info=%7B%7D; isWebpFormatSupportedAlgo0=true; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImQ3Y2EyMWE2OTliOTE5MGFjODVkNjU4MTg3YmU0NjRjYWI5MTczNTFjYmRiMTY1NGI0MWU3NWJhOTQxMDhlMmY2YWJhOGFiYzJjNDA3N2IxIiwiaWF0IjoxNzgzNjYxMTk1LjI3MjM2MywibmJmIjoxNzgzNjYxMTk1LjI3MjM2NSwiZXhwIjoxNzgzNzQ3NTk1LjI0NzkzNywic3ViIjoiYW5vbl8zMjFlZWEyYS01NzA2LTRkMWEtOWZjMS05Mzc3YjEwYjU5NWYiLCJzY29wZXMiOltdfQ.T70J56W035FrzQQovZc-nWHhlQrdFYZFcEUs6SBb-aj6Y8mDKKE1DE7JTwUkBbdNJiatNF3piZiE2NzzT4cKukwvwOQta2ZBjbduJzTqcnEqKSeajpCOmKoFo6FoiwNdO7D9VgkbTPSwgo6nGCZQQgv0J9ncouLasj2e7zo_5flCtl9zHqedU6PgRy8-L8BsSa2lLkJGZfwTaINaemaF4uw1DrIjHfJ4Xx5YMk1YoPsQMajBZKhQiwQZzvFqadEbcaaOUkLmk4SBU557b_ea27RT4jHIePw5sj0g7uTmy8XhnahLg4zqL1iL9SmHY8jz6S6g_lBu6il6GtXxGsScng; refresh_token=def502000021503cda4cad127037102059a7a0cb8b10860a694e938e1fa65e2d8730e95ac11fc29fafff5f4126828c7d7f9d3182eee3f0794cadc115c0ddff63197d6ef5abb282f9993a846890aaf8aeae4b26b41f3a40b2b1f89faaf3f79dde51829a5955327acadb07f6c66ff733c2fdb37cbbb548d932aca31c2b3745e22dd571bcd45d3a37ec93033d1dd016d37a08232532e09ddce63782caa21db1bb5287756aa40c5663f3d2a64508ab205c0626c8e059651643ef60a14f194554d6248249ca396231495286be2e9d968e5a2ddb103087302478be04fbb9af09ace22afe01844bbb6eb6a45cbca131368aec8c6c316c4fe01559e91aea84e18418bc64a27fca3fc290ab0a75d2919c4a19882a581bbb096ae4f9fc02708a710eca2d74e76ef89a43f70f36266490f789cda6560cb2b1eca2027814351509a3da31677f2321383ea936cee7d1c9f2ff42b7a027cfd8e8c126ee2a15d85e944456592bce472d9aeed8b81001dba1e0fa3afdca26af6c7838955c9aa25cd48e6073a53e33a640c678a686af0d5466ba64d76f4155b21bd5f95f55fca86db940b5616b2f9c7dda8c38ea0e98f761eb; _omappvp=8rTeayInSlShC7FBppi2lqxCsBANOUDnNdgHDmVoMUs14RXFwr0YAuHGORPl4aiXuz3kvSWhJVKYnHvIu8iS3x6Q8zZynEll; optiMonkClientId=1b96fb7c-4a6a-2df3-709b-df593b31fbf0; OptanonAlertBoxClosed=2026-07-10T05:37:14.238Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+10+2026+13%3A54%3A55+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=88c448d3-d75e-49df-b4c3-52f45c368585&interactionCount=2&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&AwaitingReconsent=false&geolocation=US%3BTX; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAbJaWAAxj4A2JS5V8pUAnJQHQRSEfADsA9gAdWpOtmxA=',
}
        self.product_params = {
            'itemsPerPage': '12',
            'page': '1',
            'cacheSegmentationCode': 'DS',
             'hl': 'hu',
        }


        self.end_categories_dict = {}



    def get_end_categories_dict(self):

        try:

            response = requests.get(
                self.url,
                headers=self.headers,
                params=self.params
            )


            if response.status_code == 200:

                all_data = response.json()


                def extract(node):

                    if isinstance(node, dict):

                        children = node.get("children", [])


                        # No children means end category
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


            # Copy product params
            current_category_params = self.product_params.copy()


            # Change category id
            current_category_params["categoryId"] = cat_id



            # First request to get page count
            response = requests.get(
                self.product_url,
                headers=self.product_headers,
                params=current_category_params
            )


            if response.status_code != 200:

                print(
                    f"{cat_id} statuscode == {response.status_code}"
                )

                continue



            data = response.json()


            # Get total pages
            total_pages = int(data.get("pageCount", 0))


            print("Total Pages:", total_pages)



            # Pagination loop
            for page in range(1, total_pages + 1):


                # Copy category params for every page
                current_params = current_category_params.copy()


                # Change page number
                current_params["cpage"] = page



                page_response = requests.get(
                    self.product_url,
                    headers=self.product_headers,
                    params=current_params
                )



                if page_response.status_code == 200:


                    page_data = page_response.json()


                    products = page_data.get("results", [])


                    print(
                        "Page:",
                        page,
                        "Products:",
                        len(products)
                    )



                else:

                    print(
                        "Page:",
                        page,
                        "Status:",
                        page_response.status_code
                    )




if __name__ == "__main__":


    scraper = EndCategories()


    result_dict = scraper.get_end_categories_dict()


    print(
        f" {len(result_dict)}\n"
    )


    # Run product parsing
    scraper.parse()


    # print(result_dict)

    # for cat_id, cat_name in result_dict.items():
    #     print(cat_id, "===", cat_name)