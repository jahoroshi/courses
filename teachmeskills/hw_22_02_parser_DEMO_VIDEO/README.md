# 🕸️ Proxy Parser Project

This repository contains a project for parsing proxy servers using various websites and APIs. The project is built with Python and uses tools like `requests_html` and `selenium` for scraping and automation.

## 🛠️ Technologies and Libraries Used

- **requests_html** — to perform HTTP requests and render JavaScript.
- **selenium** — for web browser automation.
- **Chrome WebDriver** — used by `selenium` for automating Chrome.
- **urllib** — to parse and manage URLs.
- **re** — regular expressions for extracting proxy information.
- **abc** — for implementing abstract base classes.

## 🎯 Project Goals

The goal of this project is to:

1. Parse proxy server information from various free proxy listing websites.
2. Collect proxies using both **HTML parsing** and **API requests**.
3. Automate the rendering of JavaScript on pages using **requests_html**.
4. Manage multiple parsing tasks with different configurations.
5. Handle data extraction and save the results in CSV or JSON format.

## 📂 Project Structure

- **`Parser` class** — The abstract base class providing a template for specific parsers.
- **`ProxyParserHTML` class** — A class that parses proxy information from HTML-based web pages.
- **`ProxyParserAPI` class** — A class designed to extract proxy data from APIs.
- **`data/` directory** — Directory where parsed data is saved in either JSON or CSV format.

## 🚀 Key Functionalities

- **Dynamic site handling** — The parser can render JavaScript content on the pages, ensuring all proxies are captured.
- **Multi-task parsing** — Different proxy websites are parsed with different configurations (e.g., pagination, headers, scroll actions).
- **Data extraction** — Proxies are extracted using both regex patterns and direct HTML parsing.

---

This project is designed for practicing web scraping and automation, with a focus on extracting proxy data from different sources.
