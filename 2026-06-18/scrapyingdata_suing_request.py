# What is requests?
# --------------------------------------

# requests is a Python library used to send HTTP requests to websites and APIs.

# Think of it like this:

# Your Python Program
#         |
#         | Request
#         ↓
#      Website/API
#         |
#         | Response
#         ↓
#    Data Returned


# import requests

# respoance = requests.get("https://www.bayut.bh/en/to-rent/commercial/bahrain/")

# print(respoance.status_code)


# 200

# 200 means the request was successful.


# --------------------------------------------------------------------

# Code	Meaning
# 200	Success
# 404	Page Not Found
# 403	Forbidden
# 500	Server Error

# ---------------------------------------------------------------------

# if wanna get HTML connent
# --------------------------------------------------------------------
# print(respoance.text)    #text returns the page HTML.


# data = respoance.json()

# print(data)
# # Many APIs return JSON.
# ------------------------------------------------------

# Request Headers
# --------------------------------------

# Some websites block requests without headers.

import requests 

from parsel import Selector    #Selector is a tool from the parsel library used to extract data from HTML.

headers = {
    "User-Agent":"mozilla/5.0"
    }    # header given bcz avoiding blocking

ans = requests.get("https://www.zepto.com/cn/fruits-vegetables/all/cid/64374cfe-d06f-4a01-898e-c07c46462c36/scid/e78a8422-5f20-4e4b-9a9f-22a0e53962e3",headers=headers) #get the data

print(ans.status_code)  # checking status_code

print(ans.text)

selector = Selector(text=ans.text)

title = selector.css("title::text").get()   #selector.css()Uses a CSS selector to find elements.

print(title)

heading = selector.css("h1::text").get()
print(heading)


# Selector helps us find tags like <title>, <h1>, <p>, etc.

# response.text contains the HTML source code.