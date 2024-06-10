import csv
import requests
import os
import socket
import time
from concurrent.futures import ThreadPoolExecutor

test_url = "https://httpbin.org/ip"

def check_proxy(proxy):
    try:
        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }

        start_time = time.time()
        response = requests.get(test_url, proxies=proxies, timeout=5)
        response_time = time.time() - start_time

        if response.status_code == 200:
            print(f"Proxy {proxy} is working. Response time: {response_time:.2f} seconds")
            return proxy, response_time
        else:
            print(f"Proxy {proxy} is not working")
    except Exception as e:
        print(f"Proxy {proxy} failed: {e}")
    return None, None

def ping_proxy(proxy):
    host, port = proxy.split(':')
    port = int(port)
    try:
        start_time = time.time()
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        ping_time = time.time() - start_time
        print(f"Ping to {proxy} is {ping_time:.2f} seconds")
        return ping_time
    except Exception as e:
        print(f"Ping to {proxy} failed: {e}")
        return None

def main():
    proxies = []
    with open(f'{os.path.dirname(__file__)}/data/socks5.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            proxies.extend(row)

    with ThreadPoolExecutor(max_workers=40) as executor:
        proxy_checks = list(executor.map(check_proxy, proxies))

    working_proxies = [(proxy, response_time) for proxy, response_time in proxy_checks if proxy is not None]
    print(f"\nWorking proxies: {working_proxies}")

    with ThreadPoolExecutor(max_workers=40) as executor:
        pings = list(executor.map(ping_proxy, [proxy for proxy, _ in working_proxies]))

    ping_results = [(proxy, response_time, ping) for ((proxy, response_time), ping) in zip(working_proxies, pings) if ping is not None]
    print(f"\nPing results: {ping_results}")

if __name__ == "__main__":
    main()
