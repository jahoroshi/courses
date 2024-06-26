# CustomServerTMS

## Project Description

**CustomServerTMS** is an educational project for an asynchronous server implemented using the `asyncio` module. The goal of the project is to gain a deeper understanding of asynchronous programming and to extend the server's functionality without using specialized libraries. The project uses **Poetry** for dependency management.

## Project Functionality

The project includes the following components and functionalities:

### HTTP Request Handling

The server can handle HTTP requests. The `RequestHandler` class is responsible for parsing incoming requests, extracting the method, path, HTTP version, headers, and request body. It also includes request validation using Pydantic.

### HTML Template Rendering

The project supports HTML template rendering. The template system allows the use of base templates and extends them with special tags. This is implemented in the `render` module, which asynchronously reads and processes HTML files.

### Request Routing

The `Router` class implements request routing, directing them to the appropriate view handlers based on the URL. This makes it easy to add new routes and map them to handler functions.

### View Handling

View handlers are defined in the `views` module. The project includes an example handler for the home page, which processes GET and POST requests and renders the corresponding HTML template.

### Data Validation

Pydantic is used for request data validation. The `RequestValidator` class checks the validity of the method and path, ensuring basic validation of incoming data.

### Exception Handling

The `catch_exception` decorator ensures that exceptions in asynchronous functions are caught and printed to the console. This helps in catching and diagnosing errors during execution.

### Templates

The project includes a base HTML template and a template for the home page. Templates can contain forms for sending data to the server.

### Educational Goals

The primary goal of the project is educational. By implementing this server, I aimed to deepen my understanding of asynchronous programming and to learn how to handle aspects such as HTTP request processing, routing, template rendering, and data validation without using specialized libraries. The project serves as excellent practice for learning and applying asynchronous programming concepts in practice.


## - - - - - - - - - - - - - - - 


## Описание проекта

**CustomServerTMS** — это учебный проект асинхронного сервера, реализованный с использованием модуля `asyncio`. Цель проекта — углубленное понимание асинхронного программирования и расширение функционала сервера без использования специализированных библиотек. В проекте используется инструмент управления зависимостями **Poetry**.

## Функционал проекта

Проект включает следующие компоненты и функциональные возможности:

### Обработка HTTP-запросов

Сервер может обрабатывать HTTP-запросы. Класс `RequestHandler` отвечает за разбор входящих запросов, извлечение метода, пути, HTTP-версии, заголовков и тела запроса. Также он включает валидацию запросов с использованием Pydantic.

### Рендеринг HTML-шаблонов

Проект поддерживает рендеринг HTML-шаблонов. Система шаблонов позволяет использовать базовые шаблоны и расширять их с помощью специальных тегов. Это реализовано в модуле `render`, который асинхронно читает и обрабатывает HTML-файлы.

### Маршрутизация запросов

Класс `Router` реализует маршрутизацию запросов, направляя их к соответствующим обработчикам представлений на основе URL. Это позволяет легко добавлять новые маршруты и сопоставлять их с функциями-обработчиками.

### Обработка представлений

Обработчики представлений определяются в модуле `views`. В проекте реализован пример обработчика для главной страницы, который обрабатывает GET и POST запросы, а также рендерит соответствующий HTML-шаблон.

### Валидация данных

Для валидации данных запросов используется Pydantic. Класс `RequestValidator` проверяет корректность метода и пути запроса, обеспечивая базовую валидацию входящих данных.

### Обработка исключений

Декоратор `catch_exception` обеспечивает обработку исключений в асинхронных функциях, выводя информацию об ошибках в консоль. Это помогает отлавливать и диагностировать ошибки во время выполнения.

### Шаблоны

Проект включает базовый HTML-шаблон и шаблон для главной страницы. Шаблоны могут содержать формы для отправки данных на сервер.

### Учебные цели

Основная цель проекта — образовательная. Реализуя данный сервер, я стремился глубже понять принципы асинхронного программирования и научиться работать с такими аспектами, как обработка HTTP-запросов, маршрутизация, рендеринг шаблонов и валидация данных без использования специализированных библиотек. Проект служит отличной практикой для изучения и применения концепций асинхронного программирования на практике.


