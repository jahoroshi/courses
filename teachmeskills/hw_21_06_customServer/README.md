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




