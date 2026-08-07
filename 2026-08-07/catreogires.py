import requests
from bs4 import BeautifulSoup
import json
import base64

url = "https://www.matalanme.com/ae_en"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Find the script containing topmenuparsedData
script_text = next(
    (
        script.string or script.get_text()
        for script in soup.find_all("script")
        if "topmenuparsedData" in (script.string or script.get_text())
    ),
    None,
)

if not script_text:
    raise Exception("topmenuparsedData not found")

decoded = script_text.encode().decode("unicode_escape")

# Extract JSON using brace matching
start = decoded.find('topmenuparsedData":{')
start = decoded.find("{", start)

print("start",start)

count = 0
for end in range(start, len(decoded)):
    if decoded[end] == "{":
        count += 1
    elif decoded[end] == "}":
        count -= 1
        if count == 0:
            break

menu = json.loads(decoded[start:end + 1])


def get_leaf_categories(node):
    children = node.get("children", {}).get("content", [])

    if not children:
        category_id = str(node["id"])
        return [{
            "id": category_id,
            "encoded_id": base64.b64encode(category_id.encode()).decode(),
            "name": node["name"],
            "link": node["link"]
        }]

    result = []
    for child in children:
        result.extend(get_leaf_categories(child))
    return result


end_categories = []

for root in menu["content"]:
    end_categories.extend(get_leaf_categories(root))

print(f"Found {len(end_categories)} end categories")
for i in end_categories: