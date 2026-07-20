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
    'eligibleABTestLimit': '17',
    '_clck': '1c06vir%5E2%5Eg7w%5E0%5E2389',
    '_cfuvid': 'H9CaKHWO01WHvlKC8m3FB7YRMVHTv0nx.jKF0wZhEpc-1784516814.448499-1.0.1.1-ywsyO56DKNSQGtrSTvw3bWSRVnlRec_jkn1._RxzswA',
    'REFERERSOURCE': '%7B%22referer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22details%22%3A%7B%7D%2C%22entryDate%22%3A%2207%2F19%2F26%22%2C%22entryTime%22%3A%2223%3A06%22%7D',
    'CSRF_TOKEN': '5FC2EA77E736ED1DCC72E5FB8FAF66483E746317',
    'cf_clearance': '6xFb49X7XJld7Dmz715ZaPum55JWFX2jFkIa.k5TS8U-1784517360-1.2.1.1-G1iIT2.Tp4BbtNBS_y2GWExcpKavqZXa36pRIXT6NM1zcRZwNCR3sWLnSu7ejR9IbXhiWGzKKniL1FxgVBc1yIrv4xXtU3tP.IvR27.6lnZipLDf7St8SoCALZ1mVnIlIqtgBw94.g9Gm_9dUSSiAOEODpE2o.ygBxztg1qQNLsTae2RD5czwrlLVV.9UZJ2nKvyaqta0ocagLbd6ZMhJeHhTd0TeqJt.WceKkOe9NrgIlPWhkjwJuFPTXQgRhv6Hv5cYJJL5WFoquWP8PDko_GHeSO8mZMOgVcjZZdzQrTSQUiIh9Lv5hNDUvdOJcXlVtz3Zqxpb3oTCiIEd0eqcc5ZI08A8hbttrAErw4.RHUSUglLdPoIwVBRUSnNWtfuA2ndvuHnrDXuO_IOtAkI1Nh1DoByAIRmn7VOc68kC9NvyEyQdV96X.jSRnY0R0ApUPaDH8R4i3cUmnhc.kcadITcyD10hUmtfO0vxLOWqd3P8PybbOpEC_oc59fh1adj',
    '__cf_bm': 'NUFUtXvrXWh7I_ka6EMG7JXn4cPwisGkSh9vLmJSctw-1784517360.8857784-1.0.1.1-Ec95K8.evQSws0KD5YsARiBODKiPG7RGWTgyXHcqtNhXAvZd0fdEhVG914hfQPwie5QDJKWDMtI_1Dd6z8rx2n_h8ASci_fbXFbVvGctlZ.D8XaledLjxF4_AtoqZ19p',
    '_uetsid': '736e9eb083d411f1b043c14401650a85',
    '_uetvid': '5fbbe750819b11f1ab46f1dd31c9ba10',
    '_clsk': '1iaidhu%5E1784517396429%5E6%5E1%5Ek.clarity.ms%2Fcollect',
    'CFGLOBALS': 'urltoken%3DCFID%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%26CFTOKEN%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23lastvisit%3D%7Bts%20%272026%2D07%2D19%2011%3A16%3A37%27%7D%23hitcount%3D1%23timecreated%3D%7Bts%20%272026%2D07%2D19%2011%3A16%3A37%27%7D%23cftoken%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23cfid%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23',
    '_ga_ZFM16S3J5F': 'GS2.1.s1784516817$o3$g1$t1784517400$j12$l0$h2002554613',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=0, i',
    'referer': 'https://www.webstaurantstore.com/26885/undercounter-refrigerators.html',
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
    # 'cookie': '_gcl_au=1.1.343074361.1784263975; _ga=GA1.1.157084933.1784263975; DATACENTER_ID=2; SESSION_ID=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; CFID=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; CFTOKEN=74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e; ajs_anonymous_id=990d3e68-b523-4501-abde-92b640dd5dcf; newVariationId=701:a; _fbp=fb.1.1784263976434.315661878923442003; _pin_unauth=dWlkPU16WmtZMlkyT0RjdE5UZzBPQzAwWkRoa0xUaGhZV1F0WkRVNE5UZ3lOR0kxTkdVNQ; eligibleABTestLimit=17; _clck=1c06vir%5E2%5Eg7w%5E0%5E2389; _cfuvid=H9CaKHWO01WHvlKC8m3FB7YRMVHTv0nx.jKF0wZhEpc-1784516814.448499-1.0.1.1-ywsyO56DKNSQGtrSTvw3bWSRVnlRec_jkn1._RxzswA; REFERERSOURCE=%7B%22referer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22details%22%3A%7B%7D%2C%22entryDate%22%3A%2207%2F19%2F26%22%2C%22entryTime%22%3A%2223%3A06%22%7D; CSRF_TOKEN=5FC2EA77E736ED1DCC72E5FB8FAF66483E746317; cf_clearance=6xFb49X7XJld7Dmz715ZaPum55JWFX2jFkIa.k5TS8U-1784517360-1.2.1.1-G1iIT2.Tp4BbtNBS_y2GWExcpKavqZXa36pRIXT6NM1zcRZwNCR3sWLnSu7ejR9IbXhiWGzKKniL1FxgVBc1yIrv4xXtU3tP.IvR27.6lnZipLDf7St8SoCALZ1mVnIlIqtgBw94.g9Gm_9dUSSiAOEODpE2o.ygBxztg1qQNLsTae2RD5czwrlLVV.9UZJ2nKvyaqta0ocagLbd6ZMhJeHhTd0TeqJt.WceKkOe9NrgIlPWhkjwJuFPTXQgRhv6Hv5cYJJL5WFoquWP8PDko_GHeSO8mZMOgVcjZZdzQrTSQUiIh9Lv5hNDUvdOJcXlVtz3Zqxpb3oTCiIEd0eqcc5ZI08A8hbttrAErw4.RHUSUglLdPoIwVBRUSnNWtfuA2ndvuHnrDXuO_IOtAkI1Nh1DoByAIRmn7VOc68kC9NvyEyQdV96X.jSRnY0R0ApUPaDH8R4i3cUmnhc.kcadITcyD10hUmtfO0vxLOWqd3P8PybbOpEC_oc59fh1adj; __cf_bm=NUFUtXvrXWh7I_ka6EMG7JXn4cPwisGkSh9vLmJSctw-1784517360.8857784-1.0.1.1-Ec95K8.evQSws0KD5YsARiBODKiPG7RGWTgyXHcqtNhXAvZd0fdEhVG914hfQPwie5QDJKWDMtI_1Dd6z8rx2n_h8ASci_fbXFbVvGctlZ.D8XaledLjxF4_AtoqZ19p; _uetsid=736e9eb083d411f1b043c14401650a85; _uetvid=5fbbe750819b11f1ab46f1dd31c9ba10; _clsk=1iaidhu%5E1784517396429%5E6%5E1%5Ek.clarity.ms%2Fcollect; CFGLOBALS=urltoken%3DCFID%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%26CFTOKEN%23%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23lastvisit%3D%7Bts%20%272026%2D07%2D19%2011%3A16%3A37%27%7D%23hitcount%3D1%23timecreated%3D%7Bts%20%272026%2D07%2D19%2011%3A16%3A37%27%7D%23cftoken%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23cfid%3D74eaa45f%2D2444%2D47c4%2D8dbf%2D7f20c833ee1e%23; _ga_ZFM16S3J5F=GS2.1.s1784516817$o3$g1$t1784517400$j12$l0$h2002554613',
}

# response = requests.get('https://www.webstaurantstore.com/refrigeration-equipment.html', cookies=cookies, headers=headers)

# print(response.status_code)

import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------
# Configuration
# ---------------------------

start_url = "https://www.webstaurantstore.com/1241/vacuum-cleaners.html"

session = requests.Session()

# ---------------------------
# CSV
# ---------------------------

csv_file = open("request_status.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(["Type", "URL", "Status Code"])

# ---------------------------
# Collect Product URLs
# ---------------------------

product_urls = set()
visited_listing = set()

url = start_url

while url:

    if url in visited_listing:
        break

    visited_listing.add(url)

    print(f"\nListing: {url}")

    response = session.get(
        url,
        headers=headers,
        cookies=cookies
    )

    print("Listing Status:", response.status_code)

    writer.writerow([
        "Listing",
        url,
        response.status_code
    ])

    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")

    for a in soup.select('a[data-testid="itemLink"]'):

        href = a.get("href")

        if href:
            product_urls.add(
                urljoin(response.url, href)
            )

    next_page = soup.find("link", rel="next")

    if next_page:
        url = urljoin(response.url, next_page["href"])
    else:
        break

print(f"\nCollected {len(product_urls)} products")

# ---------------------------
# Product Scraper
# ---------------------------

def scrape_product(product_url):

    try:

        r = requests.get(
            product_url,
            headers=headers,
            cookies=cookies,
            timeout=30
        )

        print(r.status_code, product_url)

        return [
            "Product",
            product_url,
            r.status_code
        ]

    except Exception:

        return [
            "Product",
            product_url,
            "ERROR"
        ]

# ---------------------------
# Multi Thread
# ---------------------------

MAX_WORKERS = 3

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    futures = [
        executor.submit(scrape_product, url)
        for url in product_urls
    ]

    for future in as_completed(futures):

        writer.writerow(
            future.result()
        )

csv_file.close()

print("\nFinished")