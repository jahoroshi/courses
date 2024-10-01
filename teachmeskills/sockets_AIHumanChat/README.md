# 🧠 GPT Chat Client-Server Architecture

## 🚀 Technologies and Design Patterns:
- **Programming Languages**: Python 🐍
- **Libraries**:
  - `socket`, `threading`, `sys` — for creating client-server communication 🔗.
  - `requests`, `urllib3`, `requests_html`, `selenium` — for working with HTTP requests, web scraping, and proxies 🌐.
  - `openai` — for integrating with OpenAI API 🤖.
  - `csv`, `json`, `os`, `re` — for working with files and regular expressions 📂.
  - `concurrent.futures.ThreadPoolExecutor` — for executing tasks concurrently 🛠️.
- **Design Patterns**:
  - Abstract classes (`abc`).
  - Message handlers in client-server architecture.
  - Retry logic for API requests with `Retry` 🔄.

## 📋 Functionality Overview:

### 1. **`client_human.py`** — Client program for communication 🗣️
A client that connects to the server, sends and receives messages through sockets. Multithreading is used for simultaneous receiving and sending of user messages.

### 2. **`client_gpt_1.py` / `client_gpt_2.py`** — Client with GPT-3.5 integration 🤖
These clients process received messages using the OpenAI API and send the generated response back to the server.

### 3. **`server.py`** — Server component 🖥️
The server accepts client connections, manages sessions, and forwards messages between clients.

### 4. **`openai_chat.py`** — Module for interacting with OpenAI API 🌐
Implements sessions using proxy servers and retry attempts in case of connection errors. Utilizes the `requests` library.

### 5. **`proxy_checker.py`** — Proxy checking tool 🕵️‍♂️
Checks the availability of proxies and measures their response time. Operates in a multithreaded mode for fast execution of checks.

### 6. **`parser_hw.py`** — Web scraper and API parser 📑
Scrapes web pages using Selenium and Requests-HTML. Saves results in CSV and JSON formats. Specialized for collecting proxy server data.

---

## 📂 Project Structure:

- `client_human.py`: Client for communication between users.
- `client_gpt_1.py` / `client_gpt_2.py`: Clients with GPT-3.5 integration.
- `server.py`: Server for handling client connections.
- `openai_chat.py`: Module for interacting with OpenAI API.
- `proxy_checker.py`: Tool for checking proxy servers.
- `parser_hw.py`: Proxy scraper module for web pages and APIs.