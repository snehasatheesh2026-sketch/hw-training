import requests
import time
import requests
import json
cookies = {
    '_pv': 'default',
    'dp': 'd',
    'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTnpZeE1XSTVaVGN0T0dJeU9TMHhNV1l4TFRrek1USXRObVUwTVRrME9EazRNbVpoSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakU0TURBNE5qWTFOakVzSW1semN5STZJa2xFUlVFaWZRLjJ6b2piS1dMXzNIU0RxelVPZ0pKTk8xeG1uaTl6TWZob2FWZkhnYURzNHc=',
    'lt_timeout': '1',
    'lt_session': '1',
    '_d_id': 'c38d3341-8ffe-4c3e-aabf-374ff0b8b63f',
    'mynt-eupv': '1',
    'mynt-ulc-api': 'pincode%3A680301',
    'mynt-loc-src': 'expiry%3A1785316002722%7Csource%3AIP',
    '_mxab_': 'config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bplp.rnw%3Denabled',
    'microsessid': '929',
    '_xsrf': 'VaHRHuMZSXj5It0oSurbJTKkXkNJtPv2',
    '_ma_session': '%7B%22id%22%3A%225e316085-e803-4dd1-a770-f8e13646143e-c38d3341-8ffe-4c3e-aabf-374ff0b8b63f%22%2C%22referrer_url%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22utm_medium%22%3A%22dms_searchbrand_cpc%22%2C%22utm_source%22%3A%22dms_google%22%2C%22utm_channel%22%3A%22other%22%2C%22utm_campaign%22%3A%22dms_google_searchbrand_cpc_Search_Brand_Myntra_Brand_India_BM_TROAS_SOK_New%22%7D',
    'x-mynt-pca': 'TqCz9CsPJDZyv9gPb2hL1QMAih1FxLwouqmhWUMTogo4XUlsHUqqwDdp2p5zJ-G5WG-htjmu5KawQgKJPwNvZ3QGVT_A7xropR6PsMqx1Zo2DJwlNq-L8Ng0NTk0a0Xn1UW4iaHsv5bYvzy7FqHtUJhqNp6RHuWmWxnrFavnmg6gufY6_lmnog%3D%3D',
    '_gcl_au': '1.1.261235995.1785314563',
    '_gcl_gs': '2.1.k1$i1785314562$u182646842',
    '_cs_ex': '1',
    '_cs_c': '1',
    '_fbp': 'fb.1.1785314563253.305270723904425638',
    'tvc_VID': '1',
    '_scid': 'xFDIUhpnOSTAxHM-mEQFe-ZlhNnEr9EW',
    '_sctr': '1%7C1785263400000',
    'bm_mi': '033AE56DEF79824B3CB30B4D1F49EC5D~YAAQ7O7IF7mqsKKfAQAAhV0KrQCTLx3WvjlQHf49oew/Ym44CO3Az2qv6+mTMu1bhG6N2s0BXFXAnqv0RhvewjDLoeFvyptRGnMPksK0pAePvvpVxHIjH73Xui2uJcy0hA79VqEwRdzBFmZh8DyDKQnj4Dg1UX2Ix5xy9Xfql8pVusHtb25vbWoqKWe8fmZgch4wGlGZuxfXyoRdtyhqZUusuaGCLddBSA/B5uMYgBudJDU5v5TJtMwK/EJizbefeKQ8IFxlNu08PxFxX11kQ1sT3VgJACTm8xvU8G/EYDWdNzW3nXDW7n2F1qko99kdcoSdn/uQ939ShadseJn55ieTFe3eMj2EzAUawf2doaVPlA==~1',
    'user_session': 'xOjKDwJxkyDYt4Iy-gIo6A.HjVDnS3sJclNhnNMWP5uQ7QjG_8SYLF5pt9o2A2-k3UDYo9wKvLP6BsPX0_sA5jCxQxoCjTYDgWqEMFI0kYh7RhuxP31GI9E5MX4gfUIJmfJy7qORyew2XsALv5XKTcaElW8I-XG_UeEtRytcBFAbA.1785314562634.86400000.Y8G6Rw8ifRwa72juSDU4uuo-QQgQQFu_ea3ZTBSqWCs',
    '_gcl_aw': 'GCL.1785314569.EAIaIQobChMI9oK6gb_3lQMVD5hmAh3hMzUIEAAYASAAEgJY0_D_BwE',
    'ak_bmsc': '42A49E3DF9AD036C8D2C5FD646DADEE0~000000000000000000000000000000~YAAQ7O7IF7arsKKfAQAA82oKrQCGF7t0MV3YZuZzroDVLripzSjoIY/SpemOn3f6JxuklcYbNUZ5J93RMJWp40kZrq96uTKpRjvw8h2PcOx7u5vzItig8pEawJ3dh09m40WNGNPeibitpqNr5v8Ce7Vq4NJcpogULBe1IWhzAbtFipmlxP67wzeKnpyiR+Hev/sa1V5xAbooFRIIeu1TmDXVSL/vAPy6PW9X65IopecxCZFn+fuO7xHYfVURsgZGmiwc3/QUdMeztYoGaKlOadj8OXu2e+49Jz0XJ4hg09QMFcbDadOsYahUiYd48yuF0LRcztERA6XfqG8Bz6Q2BvcOXY8owXr14mcDQZb/EOfbDcFN/ykeBzNreefZlW/kLbqav2uqh7PNSoOpdTGB8m2GmJUJF3CCdAgeXRL+4s3reQMOxnUUxW770LfTAuaZiPmjjgwvqB374uU8jp3qGW3F5E4w+cz4mqPV6GL4cq5b0rVsNOoZMAPpx4SYOrFfMW5ijanruePK2QRuJVv2wHC60o1e2JQ=',
    'ak_RT': '"z=1&dm=myntra.com&si=cbe256cb-c385-48dd-ba5e-52c35e7ddfa1&ss=ms5u70gc&sl=2&tt=ni&obo=1&rl=1"',
    'utm_track_v1': '%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1785314582%2C%22trackend%22%3A1785314642%7D',
    'utrid': 'FXJoBkZ5ERZAVGIIQxxAMCMxMzU3MDI1NDk0JDI%3D.fb452ec4a72b9f3ff8f4471fef8bffe3',
    '_scid_r': 'ztDIUhpnOSTAxHM-mEQFe-ZlhNnEr9EWUzwSuw',
    '_abck': '2E6C95C8AB29684C2755957DEFCDA549~0~YAAQ7O7IFwq4sKKfAQAA7w4LrRD0eaUurPtrYXkJwW0EoWAbUcCqXKjlB6vSd+REbotC3tMPH8Suo+WPguXDI83V8wgoTk5/75Hx1WsGP0N4Is6ky4r8/gVGzW8mS8W9VVIkOoRRnkxY4DEguAucBmd0aWwI/0AZ9LaiMsWKrZR5WAaBq5M8QvzacaGNBVeNHSH1mhhwSO4TP1l5ewTHtSnhnoec6EIW1hN2PoeUSduByp/nBNDoYcAlftWkYm+xJy7nynUzYjR6pVxezrC9rcE5vahQsdGYh+lw9a1MpptC2Ik8AMtYpuIkwFKqoWgwmOjutbdtiB9jMi5yuQRqGt6WqWhMgLpLXk4LVDdMwbVKEYCorTLWqYuQp2yv7s5TG3954QfH/2XkyrYSjuTvXsOg+DBdyb3aT0yagP25maCDyFkUqsluzYlBmbhGSXMF97OuSu1nV5VP1qBvnLTjOGh8Cy4pRuP/2+1Dmdx5x90v+FrwlLLOnal2FXvb3jLFJaxl9PzNfneiv4gPvLV89S05Vin7jFAjR/hWfoSNsnhzlj3ZgZfh0pykbhyEmVHbqfNOXFRGu0DZaqhDdJqt+mZLFc3miqOzhzWMcyA7TlNclDmmvsyy4+P5ZYO+t1D+cAdcWrnabHbG9pVB/yZooUpCLdFfuns2Q830xKOjNZ2g0CeRIRlkvGzpe2IoqGGfyZjgvuI0mTwEqlUuWUVr1nAeAQr8yow1x4B2U0WFMRHuDhO20YPUEx83n5HjFVKc8AQc0YrqMsBnhZC5Xfx39XjGUJEfICRH409f0YSvNYZ77WYGAgrxj4Z6IEiV++rCFhMbQZ7eM9ZJVUdJLe8PIJ422sRKyeAf/+hh+dCnLpuEHnn3AaoUWraBg2TzOHEb7+PgaD5h9qXCOn99tj6PjK3DkAGwS1IIXJIP08W6IMCs~-1~-1~-1~AAQAAAAG%2f%2f%2f%2f%2f3XOKTHkhK298ke07TQizcglgPl79MJqt8gH8lOKcpUmrujWVqlvGvgnysjasNsoku2zmGmVLVaH6ClS7XeCkNGLNaDEUaqBARzy~-1',
    'bm_sv': '7EC4EFA374515FA982C1F9A054D87998~YAAQ7O7IFwu4sKKfAQAA7w4LrQBMKaf+YQfU83LhacGuHzTlX81Z2du196xPrpKkNyz4R48nNqIRaOaHDlUIOCTnTfcjjqY4zXRysf3CNzFlNf8vMlJDgwHQFYJ6v529GMOoPuOsz0xPpwSwv79piWQTdqHEHb4Ez9JgW0LGKjd4bPA1s/1erTIberFsNDQJZHD8yTw3eVFAWSZK3g3kFjLVCwNCQbRXXnXTo8B/i8rgKpO2E9SYgQf/rTef1QdQ3Q==~1',
    'bm_sz': 'D53839F965B7F43838D5D01699C6332F~YAAQ7O7IFwy4sKKfAQAA7w4LrQAFjOkNrp4RebPz3zWH1GXZtB9TByS8bk6bRqpCvzI9Sv3ddF0gqgI0OhbHCL41qBikptxiiD1bL0AQwInQowUQ+qGX4DnoPOEREB6MnU+9oX5U+R207h98vaeOh8UGk1tJ5QISda6LMemwApoy1TZCHXC/8kbqfjFy2UST7376EZy2V9O320qwoAKtgzXXYDLcT1aa7FguC/lAZdscE/2dNuyQ3PoTsPSK37RzZHYi/rIiFzf4Io7EhyOWxiBu1qy/+pUQ05g/+LN4jOC3dGvazM4TuPt0HbfGgtiO+y6hBr0eJu/uvk+5wkHhY5ODUkdRpDi9WE5B8SOYFRz9UMszRoTdV2fKMSoazBi0eXbBozoDjKvjTerF5BoavQbqTr9rSCaAeiKzL1FU+cSFsHhEOho=~3163204~4273972',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-IN,en;q=0.9',
    'app': 'web',
    'content-type': 'application/json',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwNjIwNzEiLCJhcCI6IjcxODQwNzY0MyIsImlkIjoiNjdiYmRjYmRhMWFkMDFmNCIsInRyIjoiMDEwZWQ3MzU1OWEyM2ZkZjUxOGRjM2U2YWZmODZkNDQiLCJ0aSI6MTc4NTMxNDYzMDEyNywidGsiOiI2Mjk1Mjg2In19',
    'pagination-context': '{"productRack":{"dsCnsdrd":0,"tp":"nonDS","cntCnsdrd":0,"slrCnsdrd":0,"cncrnCnsdrd":0},"scImgVideoOffset":"0_0","v":1.0,"productsRowsShown":50,"paginationCacheKey":"be159f4e-68db-4ebe-acff-e71cd331dd78","inorganicRowsShown":4,"plaContext":"eyJvcmdhbmljQ3Vyc29yTWFyayI6IkFva0lRRUFBQUVFRlAvQUFBQUFBQUFCWjhJd3FYZTVNVU1qdUFYREFqdktSbmdOZGphV2hBVEF3WDNOMGVXeGxYelF5TWpneE1UZ3giLCJwbGFPZmZzZXQiOjAsIm9yZ2FuaWNPZmZzZXQiOjQzLCJleHBsb3JlT2Zmc2V0IjoxNCwiZmNjUGxhT2Zmc2V0Ijo0Niwic2VhcmNoUGlhbm9QbGFPZmZzZXQiOjQzLCJpbmZpbml0ZVNjcm9sbFBpYW5vUGxhT2Zmc2V0IjowLCJ0b3NQaWFub1BsYU9mZnNldCI6Mywib3JnYW5pY0NvbnN1bWVkQ291bnQiOjQzLCJhZHNDb25zdW1lZENvdW50Ijo0MywiZXhwbG9yZUNvbnN1bWVkQ291bnQiOjE0LCJjdXJzb3IiOnsiU0VBUkNIIjoic3JjOk1ZTlRSQV9QTEF8aWR4OjU1fGZlYTpyb3N+ZmVhOmt3dHxpZHg6MHxzcmM6RkNDfmZlYTpua3d0fGlkeDowfHNyYzpGQ0MifSwicGxhc0NvbnN1bWVkIjpbXSwiYWRzQ29uc3VtZWQiOltdLCJvcmdhbmljQ29uc3VtZWQiOltdLCJleHBsb3JlQ29uc3VtZWQiOltdLCJsZXhpY2FsT2Zmc2V0Ijo0MywidmVjdG9yT2Zmc2V0IjowfQ\\u003d\\u003d","refresh":false,"inorganicWidgetsOffset":{"bannerAdsOffset":0,"missionsOffset":0,"inlineFiltersGroupOffset":4,"relatedSearchesOffset":0,"productRacksOffset":0,"recSearchOffset":0},"scOffset":0,"reqId":"be159f4e-68db-4ebe-acff-e71cd331dd78"}',
    'priority': 'u=1, i',
    'referer': 'https://www.myntra.com/tshirts?f=Gender%3Amen%2Cmen%20women&rf=Discount%20Range%3A10.0_100.0_10.0%20TO%20100.0',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-010ed73559a23fdf518dc3e6aff86d44-67bbdcbda1ad01f4-01',
    'tracestate': '6295286@nr=0-1-3062071-718407643-67bbdcbda1ad01f4----1785314630127',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-location-context': 'pincode=680301;source=IP',
    'x-meta-app': 'channel=web',
    'x-myntra-app': 'deviceID=c38d3341-8ffe-4c3e-aabf-374ff0b8b63f;customerID=;reqChannel=web;appFamily=MyntraRetailWeb;',
    'x-myntraweb': 'Yes',
    'x-requested-with': 'browser',
    # 'cookie': '_pv=default; dp=d; at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTnpZeE1XSTVaVGN0T0dJeU9TMHhNV1l4TFRrek1USXRObVUwTVRrME9EazRNbVpoSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakU0TURBNE5qWTFOakVzSW1semN5STZJa2xFUlVFaWZRLjJ6b2piS1dMXzNIU0RxelVPZ0pKTk8xeG1uaTl6TWZob2FWZkhnYURzNHc=; lt_timeout=1; lt_session=1; _d_id=c38d3341-8ffe-4c3e-aabf-374ff0b8b63f; mynt-eupv=1; mynt-ulc-api=pincode%3A680301; mynt-loc-src=expiry%3A1785316002722%7Csource%3AIP; _mxab_=config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bplp.rnw%3Denabled; microsessid=929; _xsrf=VaHRHuMZSXj5It0oSurbJTKkXkNJtPv2; _ma_session=%7B%22id%22%3A%225e316085-e803-4dd1-a770-f8e13646143e-c38d3341-8ffe-4c3e-aabf-374ff0b8b63f%22%2C%22referrer_url%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22utm_medium%22%3A%22dms_searchbrand_cpc%22%2C%22utm_source%22%3A%22dms_google%22%2C%22utm_channel%22%3A%22other%22%2C%22utm_campaign%22%3A%22dms_google_searchbrand_cpc_Search_Brand_Myntra_Brand_India_BM_TROAS_SOK_New%22%7D; x-mynt-pca=TqCz9CsPJDZyv9gPb2hL1QMAih1FxLwouqmhWUMTogo4XUlsHUqqwDdp2p5zJ-G5WG-htjmu5KawQgKJPwNvZ3QGVT_A7xropR6PsMqx1Zo2DJwlNq-L8Ng0NTk0a0Xn1UW4iaHsv5bYvzy7FqHtUJhqNp6RHuWmWxnrFavnmg6gufY6_lmnog%3D%3D; _gcl_au=1.1.261235995.1785314563; _gcl_gs=2.1.k1$i1785314562$u182646842; _cs_ex=1; _cs_c=1; _fbp=fb.1.1785314563253.305270723904425638; tvc_VID=1; _scid=xFDIUhpnOSTAxHM-mEQFe-ZlhNnEr9EW; _sctr=1%7C1785263400000; bm_mi=033AE56DEF79824B3CB30B4D1F49EC5D~YAAQ7O7IF7mqsKKfAQAAhV0KrQCTLx3WvjlQHf49oew/Ym44CO3Az2qv6+mTMu1bhG6N2s0BXFXAnqv0RhvewjDLoeFvyptRGnMPksK0pAePvvpVxHIjH73Xui2uJcy0hA79VqEwRdzBFmZh8DyDKQnj4Dg1UX2Ix5xy9Xfql8pVusHtb25vbWoqKWe8fmZgch4wGlGZuxfXyoRdtyhqZUusuaGCLddBSA/B5uMYgBudJDU5v5TJtMwK/EJizbefeKQ8IFxlNu08PxFxX11kQ1sT3VgJACTm8xvU8G/EYDWdNzW3nXDW7n2F1qko99kdcoSdn/uQ939ShadseJn55ieTFe3eMj2EzAUawf2doaVPlA==~1; user_session=xOjKDwJxkyDYt4Iy-gIo6A.HjVDnS3sJclNhnNMWP5uQ7QjG_8SYLF5pt9o2A2-k3UDYo9wKvLP6BsPX0_sA5jCxQxoCjTYDgWqEMFI0kYh7RhuxP31GI9E5MX4gfUIJmfJy7qORyew2XsALv5XKTcaElW8I-XG_UeEtRytcBFAbA.1785314562634.86400000.Y8G6Rw8ifRwa72juSDU4uuo-QQgQQFu_ea3ZTBSqWCs; _gcl_aw=GCL.1785314569.EAIaIQobChMI9oK6gb_3lQMVD5hmAh3hMzUIEAAYASAAEgJY0_D_BwE; ak_bmsc=42A49E3DF9AD036C8D2C5FD646DADEE0~000000000000000000000000000000~YAAQ7O7IF7arsKKfAQAA82oKrQCGF7t0MV3YZuZzroDVLripzSjoIY/SpemOn3f6JxuklcYbNUZ5J93RMJWp40kZrq96uTKpRjvw8h2PcOx7u5vzItig8pEawJ3dh09m40WNGNPeibitpqNr5v8Ce7Vq4NJcpogULBe1IWhzAbtFipmlxP67wzeKnpyiR+Hev/sa1V5xAbooFRIIeu1TmDXVSL/vAPy6PW9X65IopecxCZFn+fuO7xHYfVURsgZGmiwc3/QUdMeztYoGaKlOadj8OXu2e+49Jz0XJ4hg09QMFcbDadOsYahUiYd48yuF0LRcztERA6XfqG8Bz6Q2BvcOXY8owXr14mcDQZb/EOfbDcFN/ykeBzNreefZlW/kLbqav2uqh7PNSoOpdTGB8m2GmJUJF3CCdAgeXRL+4s3reQMOxnUUxW770LfTAuaZiPmjjgwvqB374uU8jp3qGW3F5E4w+cz4mqPV6GL4cq5b0rVsNOoZMAPpx4SYOrFfMW5ijanruePK2QRuJVv2wHC60o1e2JQ=; ak_RT="z=1&dm=myntra.com&si=cbe256cb-c385-48dd-ba5e-52c35e7ddfa1&ss=ms5u70gc&sl=2&tt=ni&obo=1&rl=1"; utm_track_v1=%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1785314582%2C%22trackend%22%3A1785314642%7D; utrid=FXJoBkZ5ERZAVGIIQxxAMCMxMzU3MDI1NDk0JDI%3D.fb452ec4a72b9f3ff8f4471fef8bffe3; _scid_r=ztDIUhpnOSTAxHM-mEQFe-ZlhNnEr9EWUzwSuw; _abck=2E6C95C8AB29684C2755957DEFCDA549~0~YAAQ7O7IFwq4sKKfAQAA7w4LrRD0eaUurPtrYXkJwW0EoWAbUcCqXKjlB6vSd+REbotC3tMPH8Suo+WPguXDI83V8wgoTk5/75Hx1WsGP0N4Is6ky4r8/gVGzW8mS8W9VVIkOoRRnkxY4DEguAucBmd0aWwI/0AZ9LaiMsWKrZR5WAaBq5M8QvzacaGNBVeNHSH1mhhwSO4TP1l5ewTHtSnhnoec6EIW1hN2PoeUSduByp/nBNDoYcAlftWkYm+xJy7nynUzYjR6pVxezrC9rcE5vahQsdGYh+lw9a1MpptC2Ik8AMtYpuIkwFKqoWgwmOjutbdtiB9jMi5yuQRqGt6WqWhMgLpLXk4LVDdMwbVKEYCorTLWqYuQp2yv7s5TG3954QfH/2XkyrYSjuTvXsOg+DBdyb3aT0yagP25maCDyFkUqsluzYlBmbhGSXMF97OuSu1nV5VP1qBvnLTjOGh8Cy4pRuP/2+1Dmdx5x90v+FrwlLLOnal2FXvb3jLFJaxl9PzNfneiv4gPvLV89S05Vin7jFAjR/hWfoSNsnhzlj3ZgZfh0pykbhyEmVHbqfNOXFRGu0DZaqhDdJqt+mZLFc3miqOzhzWMcyA7TlNclDmmvsyy4+P5ZYO+t1D+cAdcWrnabHbG9pVB/yZooUpCLdFfuns2Q830xKOjNZ2g0CeRIRlkvGzpe2IoqGGfyZjgvuI0mTwEqlUuWUVr1nAeAQr8yow1x4B2U0WFMRHuDhO20YPUEx83n5HjFVKc8AQc0YrqMsBnhZC5Xfx39XjGUJEfICRH409f0YSvNYZ77WYGAgrxj4Z6IEiV++rCFhMbQZ7eM9ZJVUdJLe8PIJ422sRKyeAf/+hh+dCnLpuEHnn3AaoUWraBg2TzOHEb7+PgaD5h9qXCOn99tj6PjK3DkAGwS1IIXJIP08W6IMCs~-1~-1~-1~AAQAAAAG%2f%2f%2f%2f%2f3XOKTHkhK298ke07TQizcglgPl79MJqt8gH8lOKcpUmrujWVqlvGvgnysjasNsoku2zmGmVLVaH6ClS7XeCkNGLNaDEUaqBARzy~-1; bm_sv=7EC4EFA374515FA982C1F9A054D87998~YAAQ7O7IFwu4sKKfAQAA7w4LrQBMKaf+YQfU83LhacGuHzTlX81Z2du196xPrpKkNyz4R48nNqIRaOaHDlUIOCTnTfcjjqY4zXRysf3CNzFlNf8vMlJDgwHQFYJ6v529GMOoPuOsz0xPpwSwv79piWQTdqHEHb4Ez9JgW0LGKjd4bPA1s/1erTIberFsNDQJZHD8yTw3eVFAWSZK3g3kFjLVCwNCQbRXXnXTo8B/i8rgKpO2E9SYgQf/rTef1QdQ3Q==~1; bm_sz=D53839F965B7F43838D5D01699C6332F~YAAQ7O7IFwy4sKKfAQAA7w4LrQAFjOkNrp4RebPz3zWH1GXZtB9TByS8bk6bRqpCvzI9Sv3ddF0gqgI0OhbHCL41qBikptxiiD1bL0AQwInQowUQ+qGX4DnoPOEREB6MnU+9oX5U+R207h98vaeOh8UGk1tJ5QISda6LMemwApoy1TZCHXC/8kbqfjFy2UST7376EZy2V9O320qwoAKtgzXXYDLcT1aa7FguC/lAZdscE/2dNuyQ3PoTsPSK37RzZHYi/rIiFzf4Io7EhyOWxiBu1qy/+pUQ05g/+LN4jOC3dGvazM4TuPt0HbfGgtiO+y6hBr0eJu/uvk+5wkHhY5ODUkdRpDi9WE5B8SOYFRz9UMszRoTdV2fKMSoazBi0eXbBozoDjKvjTerF5BoavQbqTr9rSCaAeiKzL1FU+cSFsHhEOho=~3163204~4273972',
}

params = {
    'rows': '50',
    'o': '99',
    'plaEnabled': 'true',
    'xdEnabled': 'false',
    'isFacet': 'true',
    'p': '3',
    'pincode': '680301',
}
# for i in range(300):
#     response = requests.get('https://www.myntra.com/gateway/v4/search/tshirts', params=params, cookies=cookies, headers=headers)
    

#     print(f"{i + 1}: {response.status_code}")

#     data = response.json()
    
#     items = data.get("products")
    
#     print(f"Received {len(items)} items")
    

#     if response.status_code != 200:

        
#         print("Blocked or failed")
#         break

#     # time.sleep(0)  # 1-second delay
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch(i):
    response = requests.get(
        'https://www.myntra.com/gateway/v4/search/tshirts',
        params=params,
        headers=headers,
        cookies=cookies,
        timeout=30
    )
    return i, response.status_code

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(fetch, i) for i in range(300)]

    for future in as_completed(futures):
        i, status = future.result()
        print(f"Request {i + 1}: {status}")