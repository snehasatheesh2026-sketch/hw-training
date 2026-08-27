
# this methods use when we get complex and   heavy blocking website
# in the hrequests we can't directly call the cookies instead of that we need to give the "" means string type cookies pass .specialy we can see that in our headres so that kind of formate we need to give . not in the headres its just example that is
# Or we can pass by the cookies jar (Cookie jar = the place where your HTTP session stores website cookies so they can be reused on later requests)

import httpx
import hrequests
import json

url ='API URL'
header =headers = {
    }
data = '{"requests":}'
response = httpx.post(url,headers=header,data= data, timeout=30)

print(response.status_code)
print(response.json())




response = hrequests.post(
    url,
    data=data,
    timeout=30
)

print(response.status_code)
