# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, quote

# headers = {
#   }
# BASE_URL = "https://www.sephora.sg"

# response = requests.get(BASE_URL, headers=headers)
# response.raise_for_status()

# soup = BeautifulSoup(response.text, "html.parser")

# # Final dictionary
# catres = {}

# # Keep track of encoded URLs only
# seen_urls = set()

# # Keep track of duplicate names
# name_counts = {}


# def is_valid_category(name):
#     return not name.strip().lower().startswith("view all")


# for wrapper in soup.select("div.category-wrapper"):

#     parent = wrapper.select_one("li.title-item > a")
#     children = wrapper.select("li.item > a")

#     # If children exist, use them; otherwise use the parent
#     links = children if children else ([parent] if parent else [])

#     for a in links:
#         if not a:
#             continue

#         name = a.get_text(" ", strip=True)

#         if not is_valid_category(name):
#             continue

#         full_url = urljoin(BASE_URL, a["href"])

#         if "/categories/" not in full_url:
#             continue

#         path = full_url.split("/categories/")[1]
#         encoded_path = quote(path, safe="")

#         # Remove duplicates ONLY by encoded path
#         if encoded_path in seen_urls:
#             continue

#         seen_urls.add(encoded_path)

#         # If the name already exists, make it unique
#         if name in name_counts:
#             name_counts[name] += 1
#             key = f"{name} ({name_counts[name]})"
#         else:
#             name_counts[name] = 1
#             key = name

#         catres[key] = encoded_path

# print(f"Found {len(catres)} end categories\n")

# for name, encoded_path in catres.items():
#     print(f"{name}: {encoded_path}")


# -------------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {
     }
BASE_URL = "https://www.sephora.sg"

response = requests.get(BASE_URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Dictionary: Category Name -> Category Path (NOT encoded)
catres = {}

# Used only to remove duplicate paths
seen_paths = set()

# Used to make duplicate names unique
name_counts = {}


def is_valid_category(name):
    """Skip 'View All ...' categories."""
    return not name.strip().lower().startswith("view all")


# Find every category group
for wrapper in soup.select("div.category-wrapper"):

    # Parent category
    parent = wrapper.select_one("li.title-item > a")

    # Child categories
    children = wrapper.select("li.item > a")

    # If children exist, use only them.
    # Otherwise use the parent itself.
    links = children if children else ([parent] if parent else [])

    for a in links:
        if not a:
            continue

        name = a.get_text(" ", strip=True)

        if not is_valid_category(name):
            continue

        full_url = urljoin(BASE_URL, a["href"])

        if "/categories/" not in full_url:
            continue

        # Example:
        # makeup/face/contour
        path = full_url.split("/categories/")[1]

        # Remove duplicates ONLY by path
        if path in seen_paths:
            continue

        seen_paths.add(path)

        # Make duplicate names unique
        if name in name_counts:
            name_counts[name] += 1
            key = f"{name} ({name_counts[name]})"
        else:
            name_counts[name] = 1
            key = name

        catres[key] = path

print(f"Found {len(catres)} end categories\n")

for name, path in catres.items():
    print(f"{name}: {path}")