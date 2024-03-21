from requests_html import HTMLSession, HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlsplit
import time
import re
import csv
import os
import random
from abc import ABC, abstractmethod
import json

class Parser(ABC):
    
    def __init__(self, **kwargs):
        self.pages = 2
        self.headers = None
        self.proxies = None
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self.session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36'", "--ignore-certificate-errors", "--headless"])
        self.report = []
        split_url = urlsplit(self.url)
        self.file_path = os.path.dirname(__file__) + "/data/"
        self.base_url = f"{split_url.scheme}://{split_url.netloc}"
        self.site_name = f'{split_url.netloc.replace(".", "_")}' 

        
    
    def get_data(self, num=1):
        url = self.url.format(num)
        self.response = self.session.get(url, headers=self.headers)
        if not self.response.status_code == 200:
            raise ValueError("GET", self.response.status_code)
       
    def render_js(self, scrolldown=False):
        self.response.html.render(wait=random.uniform(2, 4), scrolldown=scrolldown)
     
        
    def save_response(self, data, num=""):
        with open(f'{self.file_path}{self.site_name}_{num}.html', "w") as file:
            file.write(data)
            
            
    def save_csv(self, file_name, data):
        with open(f'{self.file_path}{file_name}.csv', "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerows([[i] for i in data])
            
    def save_json(self, data):
        with open(f'{self.file_path}{self.site_name}.json', "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)    
            
    @abstractmethod
    def parse(self):
        pass
    
    @abstractmethod
    def __call__(self):
        pass       
    
    
    
class ProxyParserHTML(Parser):
    IP_PATTERN = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    PORT_PATTERN = r'\b(?<![.])[0-9]{2,5}(?![.])'
    
    def get_data(self, num):
        super().get_data(num)
        self.render_js()        
        
    def is_ip(self, text):
        ip = re.search(self.IP_PATTERN, text)
        return ip.group(0) if ip else False   
        
    def parse(self):
        self.proxy_types = {'http': [], 'https': [], 'socks4': [], 'socks5': []}
        tbodys = self.response.html.find("tbody")
        tbody = [i for i in tbodys if self.is_ip(i.text)][-1]
        
        if tbody:
            tr = tbody.find("tr")
        else:
            print("0")
            return
            
        for i in tr:
            ip = self.is_ip(i.text)
            if ip:
                port = re.search(self.PORT_PATTERN, i.text[i.text.index(ip) + len(ip):])
                port = port.group(0) if port else 000000
                
                for pr_type, _ in self.proxy_types.items():
                    if pr_type in i.text.lower():
                        self.proxy_types[pr_type].append(f'{ip}:{port}')
                        
        self.report = []                   
        for file_name, prox in self.proxy_types.items():
            self.save_csv(file_name, prox)
            self.report.append(f'Получено {file_name} - {len(prox)}')

    def __call__(self):
        try:
            for i in range(1, int(self.pages)):
                self.get_data()
                if self.is_ip(self.response.html.text):
                    self.parse()
                    print(f'Страница {i} объкта {self.site_name.upper()} обработана успешно.')
                    print(*self.report)
                else:
                    if self.report:
                        print(f'Обработка объекта {self.site_name.upper()} завершена успешно')
                        print(*self.report)
                    else:
                        print(f'{self.name} --- данные не получены')                      
                    break
                
        except Exception as e:
            print("__call__", e)
            


class ProxyParserAPI(ProxyParserHTML):
    
    def get_data(self):
        super(ProxyParserHTML, self).get_data()

        
    def parse(self):
        self.proxy_types = {'http': [], 'https': [], 'socks4': [], 'socks5': []}

        for el in self.response.json():
            if el['http'] == '1':
                self.proxy_types['http'].append(f"{el['ip']}:{el['port']}")
                
            if el.get('https') and el['https'] == '1':
                self.proxy_types['https'].append(f"{el['ip']}:{el['port']}")
                
            if el['socks4'] == '1':
                self.proxy_types['socks4'].append(f"{el['ip']}:{el['port']}")
                
            if el['socks5'] == '1':
                self.proxy_types['socks5'].append(f"{el['ip']}:{el['port']}")
                
        for file_name, prox in self.proxy_types.items():
            self.save_csv(file_name, prox)                                
        


class WildberriesParser(Parser):
    
    
    def get_data(self, num=1):
        url = self.url.format(num)
        # chrome_options = Options()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_argument("--headless")
        # chrome_options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(options=chrome_options)
        # driver.get(url)
        # time.sleep(4)
        # self.response = HTML(html=driver.page_source)
        with open("/home/jahoroshi4y/Документы/Courses/page.html") as file:
            html = file.read()
        self.response = HTML(html=html)

            
        
 

    def parse(self):
        self.result = []
        product_card = self.response.find("#route-content .catalog__content .product-snippet")
        try:
            for card in product_card:
                product_list = {}
                product_list["brand"] = card.find(".product-card__brand")[0].text.strip()
                product_list["name"] = card.find(".product-card__name")[0].text.strip()
                product_list["price"] = card.find(".product-card__price .price__lower")[0].text.strip()
                product_list["link"] = f'{self.base_url}{card.find(".product-card__link")[0].attrs["href"]}'
                product_list["image"] = card.find("img")[0].attrs['src']
                self.result.append(product_list)
        except IndexError as e:
            print(e)
        self.save_json(self.result)

    
    def __call__(self):
        self.get_data()
        # self.save_response()
        self.parse()
    
    
    
# kf = KufarParser({'url': 'https://www.wildberries.by/catalog?search=%D0%BA%D0%BB%D0%B0%D0%B2%D0%B8%D0%B0%D1%82%D1%83%D1%80%D0%B0&tail-location=SNT&page=2'})
# kf()
tasks = [{'url': 'https://www.wildberries.by/catalog?search=%D0%BA%D0%BB%D0%B0%D0%B2%D0%B8%D0%B0%D1%82%D1%83%D1%80%D0%B0&tail-location=SNT&page=2'}]

for url in tasks:
    obj = WildberriesParser(**url)
    obj()
    
    
    
    
    
    
                    

# ps1 = ProxyParserHTML("https://hidemy.io/en/proxy-list/")
# ps1()                    
            
# ps2 = ProxyParserAPI("https://fineproxy.org/wp-content/themes/fineproxyorg/proxy-list.php?0.20522686081524832", headers={'Referer': 'https://fineproxy.org/'})
# ps2()

# tasks = [{'url': "https://advanced.name/ru/freeproxy?page={}", 'pages': '10'}]

# for url in tasks:
#     obj = ProxyParserHTML(**url)
#     obj()
    
    
# tasks = [{'url': "https://fineproxy.org/wp-content/themes/fineproxyorg/proxy-list.php?0.20522686081524832", 'headers': {'Referer': 'https://fineproxy.org/'}}]

# for url in tasks:
#     obj = ProxyParserAPI(**url)
#     obj()