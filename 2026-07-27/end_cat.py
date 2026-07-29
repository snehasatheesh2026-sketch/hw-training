import requests
from lxml import html
from urllib.parse import urljoin
import json
import csv
import requests

import requests

import requests

cookies = {
    '_gcl_au': '1.1.343074361.1784263975',
    '_ga': 'GA1.1.157084933.1784263975',
    'DATACENTER_ID': '2',
    'SESSION_ID': '74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e',
    'CFID': '74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e',
    'CFTOKEN': '74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e',
    'ajs_anonymous_id': '990d3e68-b523-4501-abde-92b640dd5dcf',
    'newVariationId': '701:a',
    '_fbp': 'fb.1.1784263976434.315661878923442003',
    '_pin_unauth': 'dWlkPU16WmtZMlkyT0RjdE5UZzBPQzAwWkRoa0xUaGhZV1F0WkRVNE5UZ3lOR0kxTkdVNQ',
    'REFERERSOURCE': '%7B%22referer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22details%22%3A%7B%7D%2C%22entryDate%22%3A%2207%2F19%2F26%22%2C%22entryTime%22%3A%2223%3A06%22%7D',
    'eligibleABTestLimit': '21',
    'cf_clearance': 'QhxpCKw8yJl5E2tOJzqSzIgkjbPihQrjxa6J1fIk9.I-1784690055-1.2.1.1-yCZMDWhAIVD57WVTMs7x87HBvv6i9fVWBOn.RBC9T53a93CW4A36LJhIPplfOCSOgocLsBDIunn22fRjZAi41H8.wCKtPhni6yMub4yHiWQAr1ektebAy.nomaPgwveTZ0FxK1hEGQ56ZdWfwyac_5n3vV3dzK_M2tnA9keVhRzcdEOL_HTUl79ErH.B3B.jxsSz74uijir4DD3dVa.2IhE3WyeeQOcq.ipCNPCJOoKQxW0.RZV8EeF3tk3uEGR4KYXcf8JljFxFo3KD5temEd0pEXSXxcCu2vBLmk65Da7tYsc7qovoXQ901NUfw3eqkqq1gxYNkcDf_KZun3q20iTHNOYKLWqWVu55Af1rGRdxbEhow9VsY.IxZUeZCzA8VFSh0erlrpv1uTI16EPCOFQfoZeeil1A5bEs8qCl5YOoz4.Tb6m31BZaLDQXpC5emiFLIzOh2iZcDx6JFbCZB9fwXQXc9cIA6Ahsz8UZO48aDtx53FOUIWwHtyvZ5Kzt',
    '__cf_bm': 'jcRYEbwwirJu2eCsI87apLZqwZfN_lEB9jNTa2kzwaM-1784690055.7961366-1.0.1.1-JoquSJWFyzWY5FMVIgMlgx4zuUtGBvNQcNNY03GB1HRlcZGKvUNtpkQpeTueT7GzX02OnsqGw.XiNNwuC_qB.mZCvsgALG05zemi.AqGg3Dz.R8rpjgUZ9txVYbiV3BA',
    '_cfuvid': 'd9OGY1wm1UaFoue06GhIwh.FVm68M6YLM2u085c2P7o-1784690056.0531166-1.0.1.1-ZOcjGPu7MFCVD.O_AnenBFidayRr23BA43cVKFMl8K0',
    'CSRF_TOKEN': 'A877E23E94608F43B9FD9A430370D9FF05610938',
    'CFGLOBALS': 'urltoken%3DCFID%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%26CFTOKEN%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23lastvisit%3D%7Bts%20%272026%2D07%2D21%2011%3A14%3A18%27%7D%23hitcount%3D1%23timecreated%3D%7Bts%20%272026%2D07%2D21%2011%3A14%3A18%27%7D%23cftoken%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23cfid%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23',
    '_uetsid': '736e9eb083d411f1b043c14401650a85',
    '_uetvid': '5fbbe750819b11f1ab46f1dd31c9ba10',
    '_ga_ZFM16S3J5F': 'GS2.1.s1784690058$o18$g0$t1784690058$j60$l0$h1565841496',
    '_clck': '1c06vir%5E2%5Eg7y%5E0%5E2389',
    '_clsk': '1v2jfsx%5E1784690060636%5E1%5E1%5Ey.clarity.ms%2Fcollect',
}


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.webstaurantstore.com/42389/glass-top-display-freezers.html?__cf_chl_tk=gwGfGa9BVpSw4F0kS6rqxJ9CwwyN5s0DdB3sFiUvH3c-1784521850-1.0.1.1-lsFj2KUBzb_6TgcxEY_bIOu8oJD_EWPBgPtCj1CeaQg',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"148.0.7778.96"',
    'sec-ch-ua-full-version-list': '"Chromium";v="148.0.7778.96", "Google Chrome";v="148.0.7778.96", "Not/A)Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '""',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 'cookie': '_gcl_au=1.1.343074361.1784263975; _ga=GA1.1.157084933.1784263975; DATACENTER_ID=2; SESSION_ID=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; CFID=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; CFTOKEN=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; ajs_anonymous_id=990d3e68-b523-4501-abde-92b640dd5dcf; newVariationId=701:a; _fbp=fb.1.1784263976434.315661878923442003; _pin_unauth=dWlkPU16WmtZMlkyT0RjdE5UZzBPQzAwWkRoa0xUaGhZV1F0WkRVNE5UZ3lOR0kxTkdVNQ; _clck=1c06vir%5E2%5Eg7w%5E0%5E2389; _cfuvid=H9CaKHWO01WHvlKC8m3FB7YRMVHTv0nx.jKF0wZhEpc-1784516814.448499-1.0.1.1-ywsyO56DKNSQGtrSTvw3bWSRVnlRec_jkn1._RxzswA; REFERERSOURCE=%7B%22referer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22details%22%3A%7B%7D%2C%22entryDate%22%3A%2207%2F19%2F26%22%2C%22entryTime%22%3A%2223%3A06%22%7D; CSRF_TOKEN=5FC2EA77E736ED1DCC72E5FB8FAF66483E746317; eligibleABTestLimit=18; cf_clearance=juAZ1b4MYA8c_g7vgcw3RHf_mDcACGtR9DAJaGZkack-1784521853-1.2.1.1-io.5rPd9N9Vpi26UlDSrzaxnftdO4PaZZ6b.UtCL1rwZP2uhzAvpOfJN3qsV2zyxFcdiUy8qXHDpQnSm.XQAcXAaBdCGhZvgVA8vYu2Ixy0nd6Zkow_wS0GSS2v22QL_BqtgngaFZP2Ydj3.IbvW7xoLHXc9mZ7mqhjLFLYNjM3Ad_lWZhbeJg7w22rfGX.WHApUWFUojfL6BpQNhqOKEyPVQXWOpIauOJjNGEGj2T5eWBbnSzu4EhWAuKObA9xVuiSwzuCSHoLHFXsguqryMiwDYDT4g98VAqLXeKvo6_oH.rvcc6DRdYq9PCXFKouImV1vNh6txsqldACrJyBIJxe.uKTfipreG7OwTCGpceH1lk2vzW4gbS1hmSunYi0SU1nrGt.CIk1uD43MBl.15CMHaTUjx1vOYYf.2asBCssWgYY2hTCLbsWM5dGzsOJq8ouL1j2wACW5XcfJKdkI94tsYrVfBhDYWECIIsJJz4NWQloSp9EianSQd0kqASXZ; __cf_bm=dgiyfourIaSBnmgo2IgXLtKkGueZCNTajiUAkIRS4as-1784521853.335865-1.0.1.1-7Krugf1d09mQypD8EKudZ.0iCTh2aElqECr91Q91CklVueUZYfn1BjBPSap6Kn3moj7B4XEsAjLZ7kVME2uHGMergb0R4mqBVQkVljybGpnOO8mqMJndKTnQs5MU_Chx; _ga_ZFM16S3J5F=GS2.1.s1784516817$o3$g1$t1784522039$j60$l0$h2002554613$dtKWc1sQGLWNm9HZDg2AlxKm3yDSeXOxE-A; _clsk=1iaidhu%5E1784522039652%5E20%5E1%5Ek.clarity.ms%2Fcollect; _uetsid=736e9eb083d411f1b043c14401650a85; _uetvid=5fbbe750819b11f1ab46f1dd31c9ba10; CFGLOBALS=urltoken%3DCFID%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%26CFTOKEN%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23lastvisit%3D%7Bts%20%272026%2D07%2D20%2012%3A34%3A01%27%7D%23hitcount%3D1%23timecreated%3D%7Bts%20%272026%2D07%2D20%2012%3A34%3A01%27%7D%23cftoken%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23cfid%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23',
}


# print(response.text)


# tree = html.fromstring(response.text)

# # Get the GlobalHeader JSON
# script = tree.xpath('//script[@data-hypernova-key="GlobalHeader"]')[0]

# text = script.text.replace("<!--", "").replace("-->", "").strip()
# data = json.loads(text)

# # print(data.keys())

# import requests
# from lxml import html

# response = requests.get(
#     "https://www.webstaurantstore.com/restaurant-equipment.html",
#     headers=headers,
#     cookies=cookies,
# )

# tree = html.fromstring(response.text)

# for script in tree.xpath("//script[@data-hypernova-key]"):
#     print(script.attrib["data-hypernova-key"])

# data = json.loads(text)

# print(data.keys())


# # from lxml import html
# # import requests

# # response = requests.get(
# #     "https://www.webstaurantstore.com/restaurant-equipment.html",
# #     headers=headers,
# #     cookies=cookies
# # )

# # tree = html.fromstring(response.text)

# # print(tree.xpath("//title/text()"))

# # # Count all links
# # links = tree.xpath("//a/@href")
# # print("Total links:", len(links))

# # # Show first 50 links
# # for link in links[:50]:
# #     print(link)


# from lxml import html
# import requests

# response = requests.get(
#     "https://www.webstaurantstore.com/50437/charbroilers.html",
#     headers=headers,
#     cookies=cookies
# )

# tree = html.fromstring(response.text)

# print(tree.xpath('count(//div[@data-testid="Photo Grid Categories"])'))

# # -------------------------------------------------------------------------------------------------------------------------------------
# import requests
# import json
# from lxml import html
# from urllib.parse import urljoin

# BASE_URL = "https://www.webstaurantstore.com"

# session = requests.Session()
# session.headers.update(headers)
# session.cookies.update(cookies)

# visited = set()
# results = []


# def get_photo_grid_links(tree):
#     links = []

#     for a in tree.xpath('//div[@data-testid="Photo Grid Categories"]//a[@href]'):
#         href = a.get("href")

#         if not href:
#             continue

#         href = urljoin(BASE_URL, href)

#         name = " ".join(a.xpath(".//text()")).strip()

#         links.append({
#             "name": name,
#             "url": href
#         })

#     return links


# def crawl(name, url, parent=None):

#     if url in visited:
#         return

#     visited.add(url)

#     print(f"Crawling: {name}")

#     response = session.get(url)

#     if response.status_code != 200:
#         return

#     tree = html.fromstring(response.text)

#     photo_grid = tree.xpath('//div[@data-testid="Photo Grid Categories"]')

#     # No photo grid = Final Category
#     if not photo_grid:

#         results.append({
#             "name": name,
#             "url": url,
#             "parent": parent
#         })

#         print("FINAL:", name)
#         return

#     children = get_photo_grid_links(tree)

#     for child in children:

#         crawl(
#             child["name"],
#             child["url"],
#             parent=name
#         )


# ##########################################################
# # Homepage
# ##########################################################

# response = session.get(BASE_URL)

# tree = html.fromstring(response.text)

# script = tree.xpath('//script[@data-hypernova-key="GlobalHeader"]')[0]

# data = json.loads(
#     script.text.replace("<!--", "").replace("-->", "").strip()
# )

# for item in data["navDataItems"]:

#     name = item["displayName"]

#     url = urljoin(
#         BASE_URL,
#         item["link"]
#     )

#     crawl(name, url)

# print(results)



# import requests
# import json
# from lxml import html
# from urllib.parse import urljoin

# BASE_URL = "https://www.webstaurantstore.com"

# session = requests.Session()
# session.headers.update(headers)
# session.cookies.update(cookies)

# visited = set()
# results = []


# def save_results():
#     with open("categories.json", "w", encoding="utf-8") as f:
#         json.dump(results, f, indent=4, ensure_ascii=False)


# def get_photo_grid_links(tree):
#     links = []

#     for a in tree.xpath('//div[@data-testid="Photo Grid Categories"]//a[@href]'):

#         href = a.get("href")

#         if not href:
#             continue

#         href = urljoin(BASE_URL, href)

#         name = " ".join(a.xpath(".//text()")).strip()

#         # Skip empty names
#         if not name:
#             continue

#         links.append({
#             "name": name,
#             "url": href
#         })

#     # Remove duplicates
#     unique = {}
#     for item in links:
#         unique[item["url"]] = item

#     return list(unique.values())


# def crawl(name, url, parent=None, depth=0):

#     if url in visited:
#         return

#     visited.add(url)

#     print("  " * depth + f"Crawling: {name}")

#     try:
#         response = session.get(url, timeout=30)

#         if response.status_code != 200:
#             print(f"Failed: {response.status_code}")
#             return

#     except Exception as e:
#         print(e)
#         return

#     tree = html.fromstring(response.text)

#     photo_grid = tree.xpath('//div[@data-testid="Photo Grid Categories"]')

#     # No Photo Grid = Final Category
#     if not photo_grid:

#         print("  " * depth + f"FINAL: {name}")

#         results.append({
#             "name": name,
#             "url": url,
#             "parent": parent,
#             "depth": depth
#         })

#         save_results()  # Save immediately

#         return

#     children = get_photo_grid_links(tree)

#     if not children:

#         print("  " * depth + f"FINAL: {name}")

#         results.append({
#             "name": name,
#             "url": url,
#             "parent": parent,
#             "depth": depth
#         })

#         save_results()

#         return

#     for child in children:
#         crawl(
#             child["name"],
#             child["url"],
#             parent=name,
#             depth=depth + 1
#         )


# # ----------------------------------------
# # Homepage
# # ----------------------------------------

# response = session.get(BASE_URL)

# tree = html.fromstring(response.text)

# script = tree.xpath('//script[@data-hypernova-key="GlobalHeader"]')[0]

# data = json.loads(
#     script.text.replace("<!--", "").replace("-->", "").strip()
# )

# for item in data["navDataItems"]:

#     name = item["displayName"]
#     url = urljoin(BASE_URL, item["link"])

#     crawl(name, url)

# save_results()

# print(f"\nFinished! Saved {len(results)} categories to categories.json")
# correct
# =====================================================================================

import csv
import json
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from lxml import html

BASE_URL = "https://www.webstaurantstore.com"

session = requests.Session()
session.headers.update(headers)
session.cookies.update(cookies)

visited = set()
results = []
saved_urls = set()


def save_results():
    with open("categories1.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    with open("categories1.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url"])
        writer.writeheader()
        writer.writerows(results)


def get_photo_grid_links(tree):
    links = []

    for a in tree.xpath('//div[@data-testid="Photo Grid Categories"]//a[@href]'):
        href = a.get("href")

        if not href:
            continue

        href = urljoin(BASE_URL, href)

        texts = [
            t.strip()
            for t in a.xpath(".//text()")
            if t.strip() and "Product" not in t
        ]
        name = " ".join(texts)

        if not name:
            continue

        links.append({
            "name": name,
            "url": href
        })

    unique = {}
    for item in links:
        unique[item["url"]] = item

    return list(unique.values())


def crawl(name, url, parent=None, depth=0):

    if url in visited:
        return

    visited.add(url)

    print("  " * depth + f"Crawling: {name}")

    try:
        response = session.get(url, timeout=30)

        if response.status_code != 200:
            print(f"Failed: {response.status_code}")
            return

    except Exception as e:
        print(e)
        return

    tree = html.fromstring(response.text)

    photo_grid = tree.xpath('//div[@data-testid="Photo Grid Categories"]')

    def is_valid_new_url(target_url):
        parsed = urlparse(target_url)
        query = parse_qs(parsed.query)

        # Skip pagination pages
        if "page" in query:
            return False

        # Skip duplicate URLs
        if target_url in saved_urls:
            return False

        return True

    if not photo_grid:

        if (
            is_valid_new_url(url)
            and "Category" not in name
            and "Categories" not in name
        ):
            print(f"{name} -> {url}")

            saved_urls.add(url)
            results.append({
                "name": name,
                "url": url
            })

            save_results()

        return

    children = get_photo_grid_links(tree)

    if not children:

        if (
            is_valid_new_url(url)
            and "Category" not in name
            and "Categories" not in name
        ):
            print(f"{name} -> {url}")

            saved_urls.add(url)
            results.append({
                "name": name,
                "url": url
            })

            save_results()

        return

    for child in children:
        crawl(
            child["name"],
            child["url"],
            parent=name,
            depth=depth + 1
        )


# -------------------------------
# Homepage
# -------------------------------

response = session.get(BASE_URL)

tree = html.fromstring(response.text)

script = tree.xpath('//script[@data-hypernova-key="GlobalHeader"]')[0]

data = json.loads(
    script.text.replace("<!--", "").replace("-->", "").strip()
)

for item in data["navDataItems"]:
    crawl(
        item["displayName"],
        urljoin(BASE_URL, item["link"])
    )

save_results()

print(f"\nFinished! Saved {len(results)} categories1.")