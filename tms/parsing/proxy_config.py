import time
import requests

proxy_list = [
    "27.254.123.203:8443"
]




def is_avalible(ip_port):
    start_time = time.time()
    proxies = {
        "http": f'http://{ip_port}',
        "https": f'https://{ip_port}'
        
    }
    try:
        response = requests.get("https://chess.com", proxies=proxies, timeout=10)
        ping_time = time.time() - start_time
        print(f'{response} --- {response.status_code} --- {ping_time}')

        if response.status_code == 200:
            return ping_time
        
    except Exception as e:
        print(e)
        return False
        

def main():
    best_ping = float('inf')
    best_proxy = ""
    for el in proxy_list:
        check = is_avalible(el)
        if check < best_ping and check:
            best_ping = check
            best_proxy = el
        print(el, ":", check)
    return best_proxy

print(main())
            
            
            



