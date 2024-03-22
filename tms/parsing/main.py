import requests
from bs4 import BeautifolSoup
from proxy_config import login, password, proxy

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}

proxies = {
    'https': f'http://{login}:{password}@{proxy}'
}

def get_data(url):
    pass

def main():
    get_data(url='https://www.bls.gov/regions/southeast/data/xg-tables/ro4xg02.htm')
    
if __name__ == "__main__":
    main()