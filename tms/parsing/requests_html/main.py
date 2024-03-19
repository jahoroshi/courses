from requests_html import HTMLSession, HTML
import re
import csv


url = "https://advanced.name/ru/freeproxy?page="
file_path = "/home/jahoroshi4y/Документы/Courses/courses/tms/parsing/requests_html/data/"
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
port_pattern = r'\b(?<![.])[0-9]{2,5}(?![.])'



def parser_get(url, num):
    session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36'", "--ignore-certificate-errors", "--headless"])

    r = session.get(url)
    r.html.render(wait=6, sleep=1)
    with open(f'{file_path}{url.split("://")[1].split("/")[0].replace(".", "_")}_{num}.html', "w") as file:
        file.write(r.html.html)
    return r
            
def is_ip(text):
    ip = re.search(ip_pattern, text)
    return ip.group(0) if ip else False

def save_csv(name, proxys, mode="a"):
    with open(f'{file_path}{name}.csv', mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[i] for i in proxys])
    

      
# def parser_find(src=None):
#     if src is None:
#         #  with open(f'{file_path}{url.split("://")[1].split("/")[0].replace(".", "_")}.html') as file:
#         #      src = HTML(html=file.read())
#     else:
#         src = src.html       

    # if not tbody:
    #     return False
    # return tr
    
def extracting(tr):        
    proxy_types = {'http': [], 'https': [], 'socks4': [], 'socks5': []}
        
    for i in tr:
        ip = is_ip(i.text)
        if ip:
            port = re.search(port_pattern, i.text[i.text.index(ip) + len(ip):])
            port = port.group(0) if port else 000000
            
            trow_lower = i.text.lower()
            proxy = f'{ip}:{port}'
            
            if "https" in trow_lower:
                proxy_types['https'].append(proxy)
            elif "http" in trow_lower:
                proxy_types['http'].append(proxy)
            elif "socks4" in trow_lower:
                proxy_types['socks4'].append(proxy)
            elif "socks5" in trow_lower:
                proxy_types['socks5'].append(proxy)
                
    for proxy_type, proxies in proxy_types.items():
        save_csv(proxy_type, proxies)
        
        
    
                
for i in range(1, 8):
    src = parser_get(url + str(i), i)
    
    if is_ip(src.html.text):
        row = src.html.find("tbody")
        tbody = [i for i in row if is_ip(i.text)][-1]
        if tbody:
            tr = tbody.find("tr")
            extracting(tr)
            print("iter", i)
        else:
            print("0")
            break
    else:
        print("finish")
        break
    
    
    



