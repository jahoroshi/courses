from requests_html import HTMLSession
import re
import csv
import os
import random

class ProxyParser:
    IP_PATTERN = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    PORT_PATTERN = r'\b(?<![.])[0-9]{2,5}(?![.])'
    
    def __init__(self, url, pages=2):
        self.__url = url
        self.__pages = pages
        self.__session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36'", "--ignore-certificate-errors", "--headless"])
        self.__file_path = os.path.dirname(__file__) + "/data/"


    def __get_data(self, num):
        url = self.__url.format(num)
        self.__response = self.__session.get(url)
        self.__response.html.render(wait=random.uniform(2, 4), scrolldown=random.randrange(3, 11))
        print(self.__response)
        if not self.__response.status_code == 200:
            self.__response = False
            
    def __is_ip(self, text):
        ip = re.search(self.IP_PATTERN, text)
        return ip.group(0) if ip else False
    
    
    def __save_response(self, num=""):
        self.__name = f'{self.__url.split("://")[1].split("/")[0].replace(".", "_")}_{num}'
        with open(f'{self.__file_path}{self.__name}.html', "w") as file:
            file.write(self.__response.html.html)

            
    def __save_csv(self):
        for proxy_type, proxies in self.__proxy_types.items():
            with open(f'{self.__file_path}{proxy_type}.csv', "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerows([[i] for i in proxies])        
            
            
    def __parce(self):
        self.__proxy_types = {'http': [], 'https': [], 'socks4': [], 'socks5': []}
        tbodys = self.__response.html.find("tbody")
        tbody = [i for i in tbodys if self.__is_ip(i.text)][-1]
        
        if tbody:
            tr = tbody.find("tr")
        else:
            print("0")
            return
            
        for i in tr:
            ip = self.__is_ip(i.text)
            if ip:
                port = re.search(self.PORT_PATTERN, i.text[i.text.index(ip) + len(ip):])
                port = port.group(0) if port else 000000
                
                for pr_type, _ in self.__proxy_types.items():
                    if pr_type in i.text.lower():
                        self.__proxy_types[pr_type].append(f'{ip}:{port}')
                        
        self.__save_csv()

    def run(self):
        for i in range(1, self.__pages):
            self.__get_data(i)
            
            if self.__is_ip(self.__response.html.text):
                self.__save_response(i) 
                self.__parce()
                print(i)     
            else:
                print("finish")
                break
                
                
                
                
            
# ps1 = ProxyParser("https://hidemy.io/en/proxy-list/", pages=2)
# ps1.run()

# ps2 = ProxyParser("https://vpnoverview.com/privacy/anonymous-browsing/free-proxy-servers")
# ps2.run()

# ps3 = ProxyParser("https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page={}", pages=10)
# ps3.run()

sites = ["https://hidemy.io/en/proxy-list/", "https://vpnoverview.com/privacy/anonymous-browsing/free-proxy-servers"]

for i in sites:
    s = ProxyParser(i)
    s.run()