import requests
from bs4 import BeautifulSoup
import base64
import re
headers = {
    "User-Agent":
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept":
"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}
url = "https://spys.one/proxies/"
# s = requests.Session()
# response = s.get(url, headers=headers)

# with open(f'{url[url.index("://") + 3:].replace("/", "_")}.html', 'w') as file:
#     file.write(response.text)

with open(f'/home/jahoroshi4y/Документы/Courses/courses/tms/parsing/{url[url.index("://") + 3:].replace("/", "_")}.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
# [print(i) for i in soup]
proxies_table = soup.find_all("tr")
proxy_list = []

pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

for row in proxies_table:
    proxy = re.search(pattern, row.text)
    if proxy:
        print(proxy, "     ", row)


# with open('/home/jahoroshi4y/Документы/Courses/courses/tms/parsing/index.html') as file:
#     src = file.read()
    
# soup = BeautifulSoup(src, 'lxml')
# proxies_table = soup.find("table", id='proxy_list').find("tbody").find_all("tr")

# proxy_list = []

# for el in proxies_table:
#     try:
        
#         if el.find("small").text:
#             proxy_encoded = el.find("td").find("script").text
#             proxy = proxy_encoded[proxy_encoded.index('("') + 2:proxy_encoded.index('"))')]
#             proxy = base64.b64decode(proxy).decode("utf-8")
#             port = el.find("span", class_="fport").text
#             print(proxy, port)
#     except Exception as e:
#         print(e)
        
