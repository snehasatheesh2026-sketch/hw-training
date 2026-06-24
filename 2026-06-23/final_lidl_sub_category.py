import requests
from parsel import Selector
import csv

class lidl_ch_spider:

    def __init__(self):
        self.start_url = "https://sortiment.lidl.ch/de/obst-gemuese"

        self.headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=0, i',
    'referer': 'https://sortiment.lidl.ch/de/obst-gemuese',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 'cookie': 'OptanonAlertBoxClosed=2026-06-22T05:17:13.920Z; _gcl_au=1.1.1321950633.1782105435; _ga=GA1.1.1645859880.1782105437; _fbp=fb.1.1782105436664.292081904858502366; FPID=FPID2.2.4YRRIO7kvH8JY1uG%2FBpL6skY3GUnkTmuEGKC0RMdtHM%3D.1782105437; FPLC=yFR7PvxRLySWBf0bQh%2F9IeYtEo3RKcdRMDk%2BfNR1Lx8EnXLl74GMnEsqxEWnUwZI59RujfVm1obD6ntao%2BX%2FU%2BsPrvX%2B%2Bd22ZKsjgs5nvDf0DaRK7HKgouktDXiuBQ%3D%3D; FPGSID=1.1782107685.1782108092.G-0YZC93602M.dV_cjO-Wh7MjsaIWt3L-Xw; PHPSESSID=l8307fgb5dci2qir3to5l2f8gp; form_key=0CVaTMRUCJTwa92D; STUID=12341bce-c604-88da-ab99-af0a50daac5d; form_key=0CVaTMRUCJTwa92D; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; _ga_0YZC93602M=GS2.1.s1782105436$o1$g1$t1782108330$j60$l0$h1318980416; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jun+22+2026+11%3A36%3A16+GMT%2B0530+(India+Standard+Time)&version=202604.2.0&browserGpcFlag=0&isDntEnabled=0&isIABGlobal=false&hosts=&consentId=366988d2-1efb-4064-87b1-1a0cab227f9d&interactionCount=1&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&fclco=&intType=1&crTime=1782105434550&geolocation=IN%3BKL&AwaitingReconsent=false; _ga_32Z2MJ3GE4=GS2.1.s1782108283$o1$g1$t1782108377$j43$l0$h870176520',
    }

         # subcategires
    def sub_categories(self, url):

        response = requests.get(url, headers=self.headers)
        selector = Selector(text=response.text)

        links = selector.xpath("//ul[contains(@class,'items-children')]//a")

        sub_categories = []

        for link in links:
            name = link.xpath(".//span[@class='label']/text()").get()
            sub_url = link.xpath("./@href").get()

            if name and sub_url:
                sub_categories.append({
                    "sub_category_name": name.strip(),
                    "sub_category_url": sub_url.strip()
                })

        return sub_categories

    def parse(self, url, sub_category_name, sub_category_url):

        print(f"Progress: {url}")

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return

        selectors = Selector(text=response.text)

        product_list = selectors.xpath('//div[@class="product-item-info"]')

        for product in product_list:

            try:
                images = product.xpath('.//img/@data-lazy').getall()
                images = [i.strip() for i in images if i and i.strip()]

                items = {
                    "sub_category_name": sub_category_name,
                    "sub_category_url": sub_category_url,

                    "product_name": product.xpath(
                        'normalize-space(.//strong[@class="product name product-item-name"])'
                    ).get(),

                    "website": "lidl.ch",

                    "product_price": product.xpath(
                        './/strong[@itemprop="price"]/@content'
                    ).get(),

                    "image1": images[0] if len(images) > 0 else "",
                    "image2": images[1] if len(images) > 1 else "",
                    "image3": images[2] if len(images) > 2 else "",

                    "description": product.xpath(
                        './/div[contains(@class,"product-item-description")]/text()'
                    ).get(default="").strip().replace(":", ","),

                    "product_url": product.xpath(
                        './/a[contains(@class,"product-item-link")]/@href'
                    ).get(),
                    "main_category_url": self.start_url
                }

                yield items

            except Exception as e:
                print(f"Product Error: {e}")

        next_page = selectors.xpath('//a[contains(@class,"next")]/@href').get()

        if next_page:
            yield from self.parse(next_page, sub_category_name, sub_category_url)

    def run(self):

        sub_categories = self.sub_categories(self.start_url)

        for categorie in sub_categories:

            yield from self.parse(
                categorie["sub_category_url"],
                categorie["sub_category_name"],
                categorie["sub_category_url"]
            )



spider = lidl_ch_spider()

with open("final_lidl_ch_data.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "sub_category_name",
            "sub_category_url",
            "product_name",
            "website",
            "product_price",
            "image1",
            "image2",
            "image3",
            "description",
            "product_url",
            "main_category_url"
        ]
    )

    writer.writeheader()

    for item in spider.run():
        writer.writerow(item)

print("saved successfully")