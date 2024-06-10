import openai
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from api_gpt import API_KEY

PROXY = {
    "http": "socks5://45.138.87.238:1080",
    "https": "socks5://23.19.244.109:1080",
}

session = requests.Session()

retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

session.proxies.update(PROXY)

openai.requestssession = session

openai.api_key = API_KEY


def chat_with_gpt(content, username):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": f"Твое имя {username}. Ты должен просто поддерживать разговор."},
            {"role": "user", "content": content}
        ]
    )
    return completion['choices'][0]['message']['content']
