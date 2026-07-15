import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import csv
import re
from unidecode import unidecode
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from concurrent.futures import ThreadPoolExecutor, as_completed




def create_url(name, product_id):

    clean_name = unidecode(name)
    clean_name = clean_name.lower()
    clean_name = re.sub(r'[^a-zA-Z0-9]+', '-', clean_name)
    clean_name = re.sub(r'-+', '-', clean_name)
    clean_name = clean_name.strip('-')

    return f"https://auchan.hu/shop/{clean_name}.p-{product_id}"


class Auchan_hu:

    def __init__(self):

        self.url = "https://auchan.hu/api/v2/cache/tree/0"

        self.headers  ={
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImI5ZTQxMDkyZDcxOTc5MjU3MmI5MjM0Njg3NTJkMjMwNzQ2ZWFkNjcyOGUxOGFkYWE0N2VjOTFhNGEwYWY1MDkzNjM5ZDczNjFiODNiM2Y4IiwiaWF0IjoxNzgzOTA0NDQ1LjU0MjE5NCwibmJmIjoxNzgzOTA0NDQ1LjU0MjE5NiwiZXhwIjoxNzgzOTkwODQ1LjUxMjc2Mywic3ViIjoiYW5vbl82YzQxYmVkYy0zYTU1LTRlOGQtYjBmNy1lMzk5OTk2YjljYTEiLCJzY29wZXMiOltdfQ.X7GZ_-E4gjss8lDYRDO7rWszxTP8E9Iy1um1zudHZ9h3KfGkyphzOPwpvaps3_807fXgyTBwsqnwrvWHYI9nNv5lMcrlosIUeio7cJG7-IASkfHeAs4NGxN-dPi1eWF7opaWIY-ohLWxUs_zVHMbaMsjCfVKW6ChgufvJcQxbeGkjdHvLoEr1YTfFN5fGe_7SNDqIHO4HKlnUUgbRuDtvLM4OL7wQUoWB1AZgpUXqiKTy8t21lASceaMRwl5CKPeLQsqir-Q5b4KhBixDfVVkmqA1Ll6GF3pdTv7qLKs2PdC506frvi3t-df9WLCieQPhvOepUlz1NSG9YAziua6_w',
    'if-none-match': 'W/"744f5a5060ffe8c07d3fbfb3605b61b1"',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1783904443822_0_3045430_c_75',
    'x-aw-tab-id': '1783904443822_0_3045430',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=8rTeayInSlShC7FBppi2lqxCsBANOUDnNdgHDmVoMUs14RXFwr0YAuHGORPl4aiXuz3kvSWhJVKYnHvIu8iS3x6Q8zZynEll; optiMonkClientId=1b96fb7c-4a6a-2df3-709b-df593b31fbf0; AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; login_type=anon; aw_notification_info=%7B%7D; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6ImI5ZTQxMDkyZDcxOTc5MjU3MmI5MjM0Njg3NTJkMjMwNzQ2ZWFkNjcyOGUxOGFkYWE0N2VjOTFhNGEwYWY1MDkzNjM5ZDczNjFiODNiM2Y4IiwiaWF0IjoxNzgzOTA0NDQ1LjU0MjE5NCwibmJmIjoxNzgzOTA0NDQ1LjU0MjE5NiwiZXhwIjoxNzgzOTkwODQ1LjUxMjc2Mywic3ViIjoiYW5vbl82YzQxYmVkYy0zYTU1LTRlOGQtYjBmNy1lMzk5OTk2YjljYTEiLCJzY29wZXMiOltdfQ.X7GZ_-E4gjss8lDYRDO7rWszxTP8E9Iy1um1zudHZ9h3KfGkyphzOPwpvaps3_807fXgyTBwsqnwrvWHYI9nNv5lMcrlosIUeio7cJG7-IASkfHeAs4NGxN-dPi1eWF7opaWIY-ohLWxUs_zVHMbaMsjCfVKW6ChgufvJcQxbeGkjdHvLoEr1YTfFN5fGe_7SNDqIHO4HKlnUUgbRuDtvLM4OL7wQUoWB1AZgpUXqiKTy8t21lASceaMRwl5CKPeLQsqir-Q5b4KhBixDfVVkmqA1Ll6GF3pdTv7qLKs2PdC506frvi3t-df9WLCieQPhvOepUlz1NSG9YAziua6_w; refresh_token=def50200e342edc3a8152a98088bc4916b34d0326cb3afc6dd3c881b8558b2db93a638f69bca26525ff5ee5d9820b697b709354af99b3aab7e62d5539edcd9a544166b3e49a16f5e7f3e3b38804700e568dca94748df5f90e71e96c7afd9fbbadd25c3c7031ceb693cdd833841910fef4fe814ffb026ffd69e2664bfebbde758ee52fa7c0e4ad121d6a4426dc1cc32ea1de3b939e44d6f421c168fede9c892ba9f0005482394e1d7b8740e8a762d11d28b46b59bd4460397f30aa809dbd4d9f6a7b3a5b223f33f9ea90cd63744706f38da6f00ac4b802a23bfae1e36b685e0d09cdb24fa2ce4dae706ef0796bdb38c0ba1e03f09f017ffd130a8014c6f04de0bbd25126054a0a50006da3c8e1258776a5d178af8e13f9a9c89be30ad55ee4c85e06fa9f716ec087a3df439ea878930f5acd06218cb6d870faff6355a0342d5f1f809e53a95f9cd7f7fb31779361acd5e5cb3c3aab11b5c8223d8c15a203191b7238b9cb7e4017b94f4dcb8f31ffee0c7c5f1ad13dd5095d993cef817a5a58cf12ed5c42241b2f55b3b814fcf47d3675de6fd315b47bf8c36ee37d7ca98b8b486e68a83840bf3608c75b4; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAbJaWAAxj4A2JS5MAnHQCy+UB0YKIxAA7APYAHVtzDZsQA===; OptanonAlertBoxClosed=2026-07-13T01:02:34.271Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jul+13+2026+06%3A32%3A34+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=88c448d3-d75e-49df-b4c3-52f45c368585&interactionCount=3&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&AwaitingReconsent=false&geolocation=US%3BTX',
}
        self.description_url ='https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/description'

        self.allergens_url = "https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/allergensDetailed"

        self.ingredients_url  = "https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/ingredients"

        self.parameter_url = "https://auchan.hu/api/v2/cache/products/{}/variants/{}/details/parameterList"

        self.params = {
            'cacheSegmentationCode': 'DS',
            'hl': 'hu',
        }

        self.header_description  = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/hajdu-chili-lime-grillsajt-240-g.p-844525',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1784019895041_0_3368536_c_45',
    'x-aw-tab-id': '1784019895041_0_3368536',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=N8j7yiTDlhJZFz45hmpHhMzsiaZHWVuRhcwIw2MNKNIIOgbk3urvhT3jwoQQ7oR6uc0f0HeLovmJ3iF56RFHOVcQKu9mSry3; optiMonkClientId=09f70110-7f08-f58f-21c9-54732846102d; OptanonAlertBoxClosed=2026-07-13T08:51:43.918Z; AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; aw_notification_info=%7B%7D; login_type=anon; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg; refresh_token=def502002f8f80f4bcab69d34bd883851ebf95fdf75902965bca080439da5d133cc3b656f4cc160b9db7c193198d03156ee18e5cf906bd5b93503b56a7f04e82e19c0b900e73371554ba64981258cddcc258d9719da3220f1ff7a0abc1eb5b9581366525cf9ef1f5b35719b334e33d35b90f722bc1d39ec7f09022a3edea3677983f25005d54de0582f901c69f4269cb4b3c0b953ff8f79757a0c6f0cf8e4ade5ff438a6b1fafafdeddfeacd2f8ded0d14ac92dbbd642920bd90b09d4cd26506de76d30f1fbec035367ea69e1ff53a0aa94b23dcdc38b12cbb19181e1c64663506a4d2ac33116d57c6529f26f50188f5c603042aacb145b190257628a5a02c9800e333176350ca46c7b7ae2c8b63544830c5f0985173f788ba57bac9135aaba3b8629aa16c3f2bf542070547e300ef89c90ee29d3519f73d14fb9d1c60ffb8a958a03a057f7d698e48f0d6d6cd85beae6dc563b7471a9ca96dea9e4db4fd7f80cfe462d007e226cc61a5abf2cec9afca6edb330f8f8a19948e8acfd180c2e64bdc6c2d2693d6fe32fee2caee3512f47a76e53f9161567d88c5a97ee9bbdf567a7f0077637a3d708687db; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+14+2026+14%3A34%3A59+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=b990f339-e6fe-4eac-a644-91227b209f0c&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&geolocation=IN%3BKL&AwaitingReconsent=false; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAnBGAGxQAM+ANiUuVACwOmVSWUAdBFrx8AOwD2ABza9s2IA==',
}

        
        self.allergens_headers = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/hajdu-chili-lime-grillsajt-240-g.p-844525',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1784019895041_0_3368536_c_58',
    'x-aw-tab-id': '1784019895041_0_3368536',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=N8j7yiTDlhJZFz45hmpHhMzsiaZHWVuRhcwIw2MNKNIIOgbk3urvhT3jwoQQ7oR6uc0f0HeLovmJ3iF56RFHOVcQKu9mSry3; optiMonkClientId=09f70110-7f08-f58f-21c9-54732846102d; OptanonAlertBoxClosed=2026-07-13T08:51:43.918Z; AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; aw_notification_info=%7B%7D; login_type=anon; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg; refresh_token=def502002f8f80f4bcab69d34bd883851ebf95fdf75902965bca080439da5d133cc3b656f4cc160b9db7c193198d03156ee18e5cf906bd5b93503b56a7f04e82e19c0b900e73371554ba64981258cddcc258d9719da3220f1ff7a0abc1eb5b9581366525cf9ef1f5b35719b334e33d35b90f722bc1d39ec7f09022a3edea3677983f25005d54de0582f901c69f4269cb4b3c0b953ff8f79757a0c6f0cf8e4ade5ff438a6b1fafafdeddfeacd2f8ded0d14ac92dbbd642920bd90b09d4cd26506de76d30f1fbec035367ea69e1ff53a0aa94b23dcdc38b12cbb19181e1c64663506a4d2ac33116d57c6529f26f50188f5c603042aacb145b190257628a5a02c9800e333176350ca46c7b7ae2c8b63544830c5f0985173f788ba57bac9135aaba3b8629aa16c3f2bf542070547e300ef89c90ee29d3519f73d14fb9d1c60ffb8a958a03a057f7d698e48f0d6d6cd85beae6dc563b7471a9ca96dea9e4db4fd7f80cfe462d007e226cc61a5abf2cec9afca6edb330f8f8a19948e8acfd180c2e64bdc6c2d2693d6fe32fee2caee3512f47a76e53f9161567d88c5a97ee9bbdf567a7f0077637a3d708687db; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+14+2026+14%3A34%3A59+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=b990f339-e6fe-4eac-a644-91227b209f0c&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&geolocation=IN%3BKL&AwaitingReconsent=false; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAnBGAGxQAM+ANiUuVACwOmVSWUAdBFrx8AOwD2ABza9s2IA==',
}

        
        self.header_parameter = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/hajdu-chili-lime-grillsajt-240-g.p-844525',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1784019895041_0_3368536_c_46',
    'x-aw-tab-id': '1784019895041_0_3368536',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=N8j7yiTDlhJZFz45hmpHhMzsiaZHWVuRhcwIw2MNKNIIOgbk3urvhT3jwoQQ7oR6uc0f0HeLovmJ3iF56RFHOVcQKu9mSry3; optiMonkClientId=09f70110-7f08-f58f-21c9-54732846102d; OptanonAlertBoxClosed=2026-07-13T08:51:43.918Z; AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; aw_notification_info=%7B%7D; login_type=anon; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg; refresh_token=def502002f8f80f4bcab69d34bd883851ebf95fdf75902965bca080439da5d133cc3b656f4cc160b9db7c193198d03156ee18e5cf906bd5b93503b56a7f04e82e19c0b900e73371554ba64981258cddcc258d9719da3220f1ff7a0abc1eb5b9581366525cf9ef1f5b35719b334e33d35b90f722bc1d39ec7f09022a3edea3677983f25005d54de0582f901c69f4269cb4b3c0b953ff8f79757a0c6f0cf8e4ade5ff438a6b1fafafdeddfeacd2f8ded0d14ac92dbbd642920bd90b09d4cd26506de76d30f1fbec035367ea69e1ff53a0aa94b23dcdc38b12cbb19181e1c64663506a4d2ac33116d57c6529f26f50188f5c603042aacb145b190257628a5a02c9800e333176350ca46c7b7ae2c8b63544830c5f0985173f788ba57bac9135aaba3b8629aa16c3f2bf542070547e300ef89c90ee29d3519f73d14fb9d1c60ffb8a958a03a057f7d698e48f0d6d6cd85beae6dc563b7471a9ca96dea9e4db4fd7f80cfe462d007e226cc61a5abf2cec9afca6edb330f8f8a19948e8acfd180c2e64bdc6c2d2693d6fe32fee2caee3512f47a76e53f9161567d88c5a97ee9bbdf567a7f0077637a3d708687db; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+14+2026+14%3A34%3A59+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=b990f339-e6fe-4eac-a644-91227b209f0c&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&geolocation=IN%3BKL&AwaitingReconsent=false; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAnBGAGxQAM+ANiUuVACwOmVSWUAdBFrx8AOwD2ABza9s2IA==',
}
        
        self.ingredient_header  = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/hajdu-chili-lime-grillsajt-240-g.p-844525',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1784019895041_0_3368536_c_59',
    'x-aw-tab-id': '1784019895041_0_3368536',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=N8j7yiTDlhJZFz45hmpHhMzsiaZHWVuRhcwIw2MNKNIIOgbk3urvhT3jwoQQ7oR6uc0f0HeLovmJ3iF56RFHOVcQKu9mSry3; optiMonkClientId=09f70110-7f08-f58f-21c9-54732846102d; OptanonAlertBoxClosed=2026-07-13T08:51:43.918Z; AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; aw_notification_info=%7B%7D; login_type=anon; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg; refresh_token=def502002f8f80f4bcab69d34bd883851ebf95fdf75902965bca080439da5d133cc3b656f4cc160b9db7c193198d03156ee18e5cf906bd5b93503b56a7f04e82e19c0b900e73371554ba64981258cddcc258d9719da3220f1ff7a0abc1eb5b9581366525cf9ef1f5b35719b334e33d35b90f722bc1d39ec7f09022a3edea3677983f25005d54de0582f901c69f4269cb4b3c0b953ff8f79757a0c6f0cf8e4ade5ff438a6b1fafafdeddfeacd2f8ded0d14ac92dbbd642920bd90b09d4cd26506de76d30f1fbec035367ea69e1ff53a0aa94b23dcdc38b12cbb19181e1c64663506a4d2ac33116d57c6529f26f50188f5c603042aacb145b190257628a5a02c9800e333176350ca46c7b7ae2c8b63544830c5f0985173f788ba57bac9135aaba3b8629aa16c3f2bf542070547e300ef89c90ee29d3519f73d14fb9d1c60ffb8a958a03a057f7d698e48f0d6d6cd85beae6dc563b7471a9ca96dea9e4db4fd7f80cfe462d007e226cc61a5abf2cec9afca6edb330f8f8a19948e8acfd180c2e64bdc6c2d2693d6fe32fee2caee3512f47a76e53f9161567d88c5a97ee9bbdf567a7f0077637a3d708687db; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+14+2026+14%3A34%3A59+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=b990f339-e6fe-4eac-a644-91227b209f0c&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&geolocation=IN%3BKL&AwaitingReconsent=false; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAnBGAGxQAM+ANiUuVACwOmVSWUAdBFrx8AOwD2ABza9s2IA==',
}

        self.details_params  = {
    'hl': 'hu',
}


        self.product_url = "https://auchan.hu/api/v2/cache/products"

        self.product_headers   = {
    'accept': 'application/json',
    'accept-language': 'hu',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg',
    'priority': 'u=1, i',
    'referer': 'https://auchan.hu/shop/medence-es-kiegeszitok/medence-strandjatek/medence-es-kiegeszitok/merev-falu-csaladi-medencek.c-7593',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-aw-request-id': '1784019895041_0_3368536_c_35',
    'x-aw-tab-id': '1784019895041_0_3368536',
    # 'cookie': 'isWebpFormatSupportedAlgo0=true; _omappvp=N8j7yiTDlhJZFz45hmpHhMzsiaZHWVuRhcwIw2MNKNIIOgbk3urvhT3jwoQQ7oR6uc0f0HeLovmJ3iF56RFHOVcQKu9mSry3; optiMonkClientId=09f70110-7f08-f58f-21c9-54732846102d; OptanonAlertBoxClosed=2026-07-13T08:51:43.918Z; AhuAU_C=ae08ce12f0c635800a8d4a602cf552c8f5e387987339f641490404a675007b60; aw_notification_info=%7B%7D; login_type=anon; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI4cG1XclQzWmxWMUFJbXdiMUhWYWE5T1BWSzkzcjhIcyIsImp0aSI6IjFiOGFlYjUzM2ExYWE4Mjc2MGU3ZGY3N2NmMmFlMzIxMTJjODJlZDdmMDNhZDBkNjMxNmFhZTA2ZGJiZjk0ODljMTU4ODY3ODBlNWY2YjUzIiwiaWF0IjoxNzg0MDE5ODk1LjI5NzkxNywibmJmIjoxNzg0MDE5ODk1LjI5NzkxOSwiZXhwIjoxNzg0MTA2Mjk1LjI2MTE0OCwic3ViIjoiYW5vbl8xY2JmYzQzYi1iMzA1LTQxZmQtYWI3OS0yZGVkM2NjZGEwZDciLCJzY29wZXMiOltdfQ.oOUaN82djPURSk56aSHoDn8HTmk-2IeKM5qZTP9IvzcS3F8n80zQwDTG_dIfEh-XVtunHKxtPNBfg1PGyyZMi-sNKxPE2vTKcIpvnt6n-cFkEm1IkMP0LRWdEgP7QV6icbp_9xMz2mruTB16ykA0s_f3n6zGPXyY5PLZnuOFlbOho2iCQHgTunHul9xccuM_KfCowbn7xowPCfpS3wSg8gOFjOHQCM_-l1yjQQ0obxsCaCtAJh-fx_2SFcsr5sRWHlT0vewhhxTJjc1_fu5H84YT42mNto4YnyFLR7KfRLGjTTKDn9cdQXsBv8O6zuCVKxKgodc21qhtXQMYjWu4Yg; refresh_token=def502002f8f80f4bcab69d34bd883851ebf95fdf75902965bca080439da5d133cc3b656f4cc160b9db7c193198d03156ee18e5cf906bd5b93503b56a7f04e82e19c0b900e73371554ba64981258cddcc258d9719da3220f1ff7a0abc1eb5b9581366525cf9ef1f5b35719b334e33d35b90f722bc1d39ec7f09022a3edea3677983f25005d54de0582f901c69f4269cb4b3c0b953ff8f79757a0c6f0cf8e4ade5ff438a6b1fafafdeddfeacd2f8ded0d14ac92dbbd642920bd90b09d4cd26506de76d30f1fbec035367ea69e1ff53a0aa94b23dcdc38b12cbb19181e1c64663506a4d2ac33116d57c6529f26f50188f5c603042aacb145b190257628a5a02c9800e333176350ca46c7b7ae2c8b63544830c5f0985173f788ba57bac9135aaba3b8629aa16c3f2bf542070547e300ef89c90ee29d3519f73d14fb9d1c60ffb8a958a03a057f7d698e48f0d6d6cd85beae6dc563b7471a9ca96dea9e4db4fd7f80cfe462d007e226cc61a5abf2cec9afca6edb330f8f8a19948e8acfd180c2e64bdc6c2d2693d6fe32fee2caee3512f47a76e53f9161567d88c5a97ee9bbdf567a7f0077637a3d708687db; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+14+2026+14%3A34%3A59+GMT%2B0530+(India+Standard+Time)&version=6.38.0&isIABGlobal=false&hosts=&consentId=b990f339-e6fe-4eac-a644-91227b209f0c&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A0%2CC0004%3A0%2CC0002%3A0%2CC0001%3A1&geolocation=IN%3BKL&AwaitingReconsent=false; optiMonkClient=N4IgTAzAHBCsDsIBcoDGBDZwC+AaEAZgG7ICM8MAnBGAGxQAM+ANiUuVACwOmVSWUAdBFrx8AOwD2ABza9s2IA==',
}



        self.product_params  = {
            'itemsPerPage': '12',
            'page': '1',
            'cacheSegmentationCode': 'DS',
             'hl': 'hu',
        }

        
        # Session with Retry
        
        self.session = requests.Session()

        retry = Retry(
            total=5,
            connect=5,
            read=5,
            backoff_factor=2,
            allowed_methods=["GET"],
        )

        adapter =  HTTPAdapter(
                     max_retries=retry,
                     pool_connections=20,
                     pool_maxsize=20,)


        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)



        self.end_categories_dict = {}

        self.seen_pdp_urls = set()

    def fetch(self, url, headers):
          try:
            return self.session.get(
                url,
                params=self.details_params,
                headers=headers,
                timeout=30,
            )
          except Exception:
            return None


    def get_end_categories_dict(self):

        try:

            response = self.session.get(
                self.url,
                headers=self.headers,
                params=self.params,
                timeout=30
            )

            time.sleep(0.1)

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
    
    def process_product(self, product, cat_name):


        pdp_url_details = product.get('selectedVariant',{}) or product.get('defaultVariant',{}) or {}

        product_name = pdp_url_details.get("name", "")

        sku = pdp_url_details.get("sku", "")

        pdp_url = create_url(product_name, sku)

        if pdp_url in self.seen_pdp_urls:
            return None

        self.seen_pdp_urls.add(pdp_url)

        cart_info = pdp_url_details.get('cartInfo', {}) or {}
                        
        categories_list = product.get('categories', []) or []

        unique_id =  pdp_url_details.get("productId",'') or ""

        upc = pdp_url_details.get('eanCode','') or ""

        brand_name = pdp_url_details.get('brandName','')

        price_info = pdp_url_details.get('price', {}) or {}

        regular_price = price_info.get("gross") or ""

        is_discounted = price_info.get('isDiscounted', False)

        discounted_price =  price_info.get('grossDiscounted')

        selling_price = discounted_price if discounted_price else regular_price

        promotion_price = discounted_price if is_discounted else ""

        discountDisplayPercentage = price_info.get('discountDisplayPercentage')if  is_discounted else ""

        promotion_valid_from = price_info.get("discountValidFrom", "") if is_discounted else ""

        promotion_valid_to = price_info.get('discountValidTo','') if is_discounted else ""

        if promotion_valid_from :
                            promotion_valid_from = datetime.fromisoformat(
                             promotion_valid_from
                             ).strftime("%Y-%m-%d")
        else:
            promotion_valid_from = ""

        if promotion_valid_to :
                              promotion_valid_to = datetime.fromisoformat(
                              promotion_valid_to
                             ).strftime("%Y-%m-%d")
        else :
            promotion_valid_to = ""

        flags = pdp_url_details.get("flags", [])
        promotion_label = ""

        promotion_label = ", ".join(
                                    item.get("name", "")
                                    for item in flags
                                    if item.get('flag') =="flag_discount" and item.get("name")
                                    )
        review_count = product.get('reviewSum',{}).get('sumCount') or ""

        rating = product.get('reviewSum',{}).get('average') or ""

        currency = price_info.get('currency','')

        media_data = pdp_url_details.get('media',{}).get('images',[]) or  ""

        images = ','.join(set(media_data))

        raw_availability = cart_info.get('availability','')

        if raw_availability == 'available':

            availability_status = "In Stock"
        else:
            availability_status = "Out of Stock"

                        

        pkg_info = pdp_url_details.get('packageInfo',{}) or {}

        raw_unit = pkg_info.get('packageUnit','')

        raw_size = pkg_info.get('packageSize','')

        unit_price_raw =  pkg_info.get('unitPrice',{}).get('gross') or ""

        if categories_list:
                             
            sorted_cats = sorted(categories_list, key=lambda x: x.get('level', 0))
            cat_names = [c.get('name') for c in sorted_cats if c.get('name')]
            breadcrumb = " > ".join(["Főoldal", "Online áruház"]+cat_names)
        else:
            breadcrumb = "Főoldal > Online áruház"
        
        varient_id = pdp_url_details.get('id','') or ""

        raw_description = ""
        ingredients = ""
        country = ""
        features = ""
        allergensDetailed = ""

        new = []

        if varient_id and unique_id:

            url = self.description_url.format(unique_id, varient_id)

            in_url = self.ingredients_url.format(unique_id, varient_id)

            feature_url = self.parameter_url.format(unique_id, varient_id)

            allergen_url = self.allergens_url.format(unique_id, varient_id)

            with ThreadPoolExecutor(max_workers=4) as executor:
                descri_future = executor.submit(self.fetch, url, self.header_description)
                ingredient_future = executor.submit(self.fetch, in_url, self.ingredient_header)
                feature_future = executor.submit(self.fetch, feature_url, self.header_parameter)
                allergen_future = executor.submit(self.fetch, allergen_url, self.allergens_headers)

                descri_response = descri_future.result()
                ingredient_response = ingredient_future.result()
                feature_respo = feature_future.result()
                allergens_response = allergen_future.result()
            
            if descri_response and descri_response.status_code == 200:

                json_data = descri_response.json()
                html_description = json_data.get("description", "")
                if html_description:
                    raw_description = BeautifulSoup(
                                         html_description,
                                         "html.parser"
                                        ).get_text(separator=" ", strip=True)
            if ingredient_response and ingredient_response.status_code == 200:

                in_json_data = ingredient_response.json()
                ingredients = in_json_data.get("description", "")

                if ingredients:
                    ingredients = BeautifulSoup(
                                                  ingredients,
                                                  "html.parser"
                                         ).get_text(separator=" ", strip=True)
            if feature_respo and feature_respo.status_code == 200:
                data = feature_respo.json()

                for item in data.get("parameters", []):
                    name = item.get("name")
                    value = item.get("value", "")
                    value = ", ".join(
                                        line.strip()
                                        for line in value.splitlines()
                                        if line.strip()
                                        )
                    if name == "Származási ország":
                        country = value

                    elif name:
                        new.append(f"{name}: {value}")
                features = ", ".join(new)
            
            if allergens_response and allergens_response.status_code == 200:
                all_data = allergens_response.json()
                raw_allergensDetailed = all_data.get("allergensDetailed", [])
                allergensDetailed = ", ".join(
                                    item.get("name", "")
                                    for item in raw_allergensDetailed
                                    if item.get("name")
         
                                    )
        description = " ".join((raw_description or "").split())
        ingredients = " ".join(ingredients.split()) or ""
        country = country or ""

        return {
                            "unique_id": unique_id,
                            "product_name":product_name,
                            "unit_type":raw_unit or "",
                            "package_size":raw_size or "",
                            "sub_category_name": cat_name or "",
                            "regular_price":regular_price,
                            "promotion_price":promotion_price or "",
                            "selling_price":selling_price,
                            "currency":currency,
                            "brand_name":brand_name,
                            "breadcrumb":breadcrumb,
                            "availability":availability_status,
                            "pdp_url": pdp_url or "",
                            "upc":upc,
                            "discountpercentage":discountDisplayPercentage,
                            "promotion_label":promotion_label,
                            "country":country,
                            "allergens":allergensDetailed,
                            "features":features,
                            "images":images,
                            "rating":rating,
                            "promotion_valid_to":promotion_valid_to,
                            "promotion_valid_from":promotion_valid_from,
                            "review_count":review_count,
                            "descripition":description,
                            "ingredients":ingredients,
                            "part_number": sku or "",
                            "unit_price":unit_price_raw
                        }


        
    
    def parse(self):

        categories = self.get_end_categories_dict()

        for cat_id, cat_name in categories.items():


            print("Category:", cat_name)
            print("ID:", cat_id)
            print("====================")

            current_category_params = self.product_params.copy()

            current_category_params["categoryId"] = cat_id

            response = self.session.get(
                self.product_url,
                headers=self.product_headers,
                params=current_category_params,
                timeout=30
            )

            time.sleep(0.1)

            if response.status_code != 200:

                print(f"{cat_id} statuscode == {response.status_code}")
                continue

            data = response.json()

            total_pages = int(data.get("pageCount", 0))

            print("Total Pages:", total_pages)

            for page in range(1, total_pages + 1):

                current_params = current_category_params.copy()

                current_params["page"] = page

                page_response = self.session.get(
                    self.product_url,
                    headers=self.product_headers,
                    params=current_params,
                    timeout=30
                )

                time.sleep(0.1)

                if page_response.status_code == 200:

                    page_data = page_response.json()

                    products = page_data.get("results", [])

                    with ThreadPoolExecutor(max_workers=5) as executor:
                         
                         futures = [
                        executor.submit(
                            self.process_product,
                            product,
                            cat_name
                        )
                        for product in products
                    ]
                         for future in as_completed(futures):
                            row = future.result()

                            if row:
                              yield row




if __name__ == "__main__":

    scraper = Auchan_hu()

    with open(
        "auchan_product_data_test.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "unique_id",
                "sub_category_name",
                "product_name",
                "brand_name",
                "regular_price",
                "selling_price",
                "promotion_price",
                "promotion_valid_from",
                "promotion_valid_to",
                "discountpercentage",
                "promotion_label",
                "currency",
                "package_size",
                "unit_type",
                "unit_price",
                "availability",
                "images",
                "part_number",
                "country",
                "breadcrumb",
                "pdp_url",
                "features",
                "allergens",
                "ingredients",
                "descripition",
                "rating",
                "review_count",
                "upc",
            ]
        )

        writer.writeheader()

        for row in scraper.parse():

            writer.writerow(row)

    print("CSV saved successfully")