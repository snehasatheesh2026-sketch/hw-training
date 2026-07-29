# import requests
# from bs4 import BeautifulSoup

# url = "https://www.myntra.com/"
# headers = {"User-Agent": "Mozilla/5.0"}

# soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

# all_categories = []

# for nav in soup.select("div.desktop-navLink"):

#     main = nav.select_one("a.desktop-main")
#     if not main:
#         continue

#     main_name = main.get_text(strip=True)

#     elements = nav.select("a.desktop-categoryName, a.desktop-categoryLink")

#     i = 0
#     while i < len(elements):

#         tag = elements[i]

#         # Section heading
#         if "desktop-categoryName" in tag.get("class", []):

#             section = tag.get_text(strip=True)
#             href = tag.get("href")

#             has_children = False

#             j = i + 1
#             while j < len(elements):

#                 cls = elements[j].get("class", [])

#                 if "desktop-categoryName" in cls:
#                     break

#                 if "desktop-categoryLink" in cls:
#                     has_children = True

#                     leaf = elements[j]

#                     all_categories.append({
#                         "main_category": main_name,
#                         "section": section,
#                         "category": leaf.get_text(strip=True),
#                         "url": "https://www.myntra.com" + leaf["href"]
#                     })

#                 j += 1

#             # No child links → include the section itself
#             if not has_children:
#                 all_categories.append({
#                     "main_category": main_name,
#                     "section": section,
#                     "category": section,
#                     "url": "https://www.myntra.com" + href
#                 })

#             i = j

#         else:
#             i += 1

# for row in all_categories:
#     print(row)

# print("Total:", len(all_categories))

# -----------------------------------------------------------------------------------------------


import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = "https://www.myntra.com/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

all_categories = []

# Each main tab (Men, Women, Kids...)
for nav in soup.select("div.desktop-navLink"):

    main = nav.select_one("a.desktop-main")
    if not main:
        continue

    main_name = main.get_text(strip=True)

    current_section = None

    # Read all category headings and leaf categories in order
    for tag in nav.select("a.desktop-categoryName, a.desktop-categoryLink"):

        classes = tag.get("class", [])

        # Section heading (Topwear, Bottomwear...)
        if "desktop-categoryName" in classes:
            current_section = tag.get_text(strip=True)

        # Leaf category (T-Shirts, Jeans...)
        elif "desktop-categoryLink" in classes:
            name = tag.get_text(strip=True)
            href = tag.get("href")

            if href:
                if href.startswith("/"):
                    href = "https://www.myntra.com" + href

                # Extract only slug from URL
                slug = urlparse(href).path.strip("/")

                all_categories.append({
                    "main_category": main_name,
                    "section": current_section,
                    "category": name,
                    "url": slug
                })

# Print results
for item in all_categories:
    print(item)

print("Total:", len(all_categories))