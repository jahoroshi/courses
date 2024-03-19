from requests_html import HTMLSession
import re
import csv
import os
import random
import asyncio

class ProxyParser:
    __ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    __port_pattern = r'\b(?<![.])[0-9]{2,5}(?![.])'
    
    def __init__(self, url, pages=2, step=1):
        self.__url = url
        self.__pages = pages
        self.__step = step
        self.__session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36'", "--ignore-certificate-errors", "--headless"])
        self.__file_path = os.path.dirname(__file__) + "/data/"


    def __get_data(self, num, wait=1):
        url = self.__url.format(num)
        responce = self.__session.get(url)
        responce.html.render(wait=random.uniform(2, 4), scrolldown=10)
        name = f'{self.__url.split("://")[1].split("/")[0].replace(".", "_")}_{num}'
        print(responce)
        if self.__is_ip(responce.html.text):
            with open(f'{self.__file_path}{name}.html', "w") as file:
                file.write(responce.html.html)
            return responce
        else:
            return False
            
    def __is_ip(self, text):
        ip = re.search(ProxyParser.__ip_pattern, text)
        return ip.group(0) if ip else False
        
    def __save_csv(self):
        for proxy_type, proxies in self.__proxy_types.items():
            with open(f'{self.__file_path}{proxy_type}.csv', "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerows([[i] for i in proxies])        
            
    def __parce(self, response):
        self.__proxy_types = {'http': [], 'https': [], 'socks4': [], 'socks5': []}
        tbodys = response.html.find("tbody")
        tbody = [i for i in tbodys if self.__is_ip(i.text)][-1]
        
        if tbody:
            tr = tbody.find("tr")
        else:
            print("0")
            return
            
        for i in tr:
            ip = self.__is_ip(i.text)
            if ip:
                port = re.search(self.__port_pattern, i.text[i.text.index(ip) + len(ip):])
                port = port.group(0) if port else 000000
                
                trow_lower = i.text.lower()
                proxy = f'{ip}:{port}'
                
                if "https" in trow_lower:
                    self.__proxy_types['https'].append(proxy)
                elif "http" in trow_lower:
                    self.__proxy_types['http'].append(proxy)
                elif "socks4" in trow_lower:
                    self.__proxy_types['socks4'].append(proxy)
                elif "socks5" in trow_lower:
                    self.__proxy_types['socks5'].append(proxy)
                    
        self.__save_csv()

    def run(self):
        for i in range(1, self.__pages, self.__step):
            src = self.__get_data(i)
            
            if src: 
                self.__parce(src)
                print(i)     
            else:
                print("finish")
                break
                
                
                
                
            
ps1 = ProxyParser("https://hidemy.io/en/proxy-list/", pages=2, step=1)
ps1.run()

ps2 = ProxyParser("https://vpnoverview.com/privacy/anonymous-browsing/free-proxy-servers")
ps2.run()

ps3 = ProxyParser("https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page={}", pages=10)
ps3.run()