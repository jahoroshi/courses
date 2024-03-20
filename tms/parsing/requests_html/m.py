from requests_html import HTMLSession


# url = "https://fineproxy.org/wp-content/themes/fineproxyorg/proxy-list.php?0.20522686081524832"
# session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36'"])

# headers = {
#     'Referer': 'https://fineproxy.org/'
# }

# response = session.get(url, headers=headers)

# IP_PATTERN = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
# PORT_PATTERN = r'\b(?<![.])[0-9]{2,5}(?![.])'
response = [{"host":"172.67.229.15","ip":"172.67.229.15","port":"80","lastseen":14578,"delay":200,"cid":"6252001","country_code":"US","country_name":"United States","city":"","checks_up":"1592","checks_down":"2","anon":"1","http":"1","ssl":"0","socks4":"0","socks5":"0"},{"host":"198.71.49.163","ip":"198.71.49.163","port":"3128","lastseen":14578,"delay":2100,"cid":"6252001","country_code":"US","country_name":"United States","city":"","checks_up":"14","checks_down":"428","anon":"1","http":"1","ssl":"0","socks4":"0","socks5":"0"}]
proxy_types = {'http': [], 'https': [], 'socks4': [], 'socks5': []}

        
for el in response:
    if el['http'] == '1':
        proxy_types['http'].append(f"{el['ip']}:{el['port']}")
        
    if el.get('https') and el['https'] == '1':
        proxy_types['https'].append(f"{el['ip']}:{el['port']}")
        
    if el['socks4'] == '1':
        proxy_types['http'].append(f"{el['ip']}:{el['port']}")
        
    if el['socks5'] == '1':
        proxy_types['http'].append(f"{el['ip']}:{el['port']}")

print(proxy_types)


