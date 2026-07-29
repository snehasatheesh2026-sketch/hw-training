import requests

url = "https://www.myntra.com/gateway/v4/search/women-ethnic-wear"

headers  = {
    }

params = {
    'rows': '50',
    'o': '49',
    'plaEnabled': 'true',
    'xdEnabled': 'false',
    'isFacet': 'true',
    'p': '1',
    'pincode': '',
}

cookies = {
 }
p = 1

while True:

    # Copy params and update page number
    rows = int(params['rows'])

    page_params = params.copy()
    page_params['o'] = str((p - 1) * rows)
    page_params['p'] = str(p)

    print(f"Fetching page {p}...")

    response = requests.get(
        url,
        params=page_params,
        headers=headers
    )

    print("URL:", response.url)

    if response.status_code != 200:
        print("Request failed:", response.status_code)
        break

    data = response.json()

    items = data.get("products")

    print(f"Received {len(items)} items")

    for item in items:
        print(item)

    print(page_params)
    # Check next page
    if data.get("hasNextPage") is True:
        p += 1
    else:
        print("No more pages.")
        break