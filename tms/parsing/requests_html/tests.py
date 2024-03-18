from requests_html import HTMLSession
import json

url = "https://fineproxy.org/wp-content/themes/fineproxyorg/proxy-list.php?0.20522686081524832"
session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36'"])

headers = {
    'Referer': 'https://fineproxy.org/'
}

response = session.get(url, headers=headers)