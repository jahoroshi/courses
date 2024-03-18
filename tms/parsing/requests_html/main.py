from requests_html import HTMLSession, HTML
import re


url = "https://best-proxies.ru/proxylist/free/"

act = 0

if act == 0:
    session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36'", "--ignore-certificate-errors", "--headless"])

    r = session.get(url)
    r.html.render(wait=6, sleep=1, timeout=14)
    with open(f'/home/jahoroshi4y/Документы/Courses/courses/tms/parsing/requests_html/{url.split("://")[1].split("/")[0].replace(".", "_")}.html', "w") as file:
        file.write(r.html.html)
elif act == 1:
    with open(f'/home/jahoroshi4y/Документы/Courses/courses/tms/parsing/requests_html/{url.split("://")[1].split("/")[0].replace(".", "_")}.html') as file:
        src = HTML(html=file.read())  

    row = src.find("tbody")
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    port_pattern = r'\b(?<![.])[0-9]{2,5}(?![.])'

    tbody = [i for i in row if re.search(ip_pattern, i.text)][-1]
    tr = tbody.find("tr")

    for i in tr:
        ip = re.search(ip_pattern, i.text)
        if ip:
            ip = ip.group(0)
            port = re.search(port_pattern, i.text[i.text.index(ip) + len(ip):])
            port = port.group(0)
            print(ip, port)
            



