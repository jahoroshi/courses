# 🚀 TMS-FastAPI

## 🛠️ Technologies Used

- **FastAPI**: A web framework for building high-performance APIs with Python ⚡.
- **Pydantic**: For data validation and management of data schemas 📊.
- **SQLAlchemy**: ORM for working with the database 🗄️.
- **Alembic**: For managing database migrations 📈.
- **Celery**: Asynchronous task processing, such as sending notifications 📬.
- **Redis**: Message broker for Celery 🔄.
- **Docker**: Containerization of the application for easy deployment and scaling 🐳.
- **Docker Compose**: Orchestration of multi-service applications ⚙️.
- **JWT**: For implementing user authentication and authorization 🔐.
- **Passlib**: For secure password hashing 🔑.
- **Poetry**: Dependency management and project configuration 📦.

## 📋 About the Project

This project is a web application for managing events and users. Users can create events, subscribe to them, and view a list of their events. The application implements full user authentication and authorization, including administrative functions. The entire system is built using modern technologies and development approaches, ensuring high performance, security, and scalability.

## ✨ Features

### 👤 User Module:
- **User Registration and Authentication**: With support for JWT tokens 🔑.
- **User Management**: Administrators can manage the user list 📋.
- **Password Hashing**: Using the `Passlib` library with bcrypt algorithm 🛡️.

### 📅 Events Module:
- **Event Creation**: Users can create events with a specified time 🕒.
- **Event Subscription**: Ability to subscribe to event notifications 📩.
- **Notification Sending**: Email notifications using Celery and Redis 📨.

### 🌐 API:
- **RESTful API**: Routes for creating, reading, updating, and deleting users and events 🔄.
- **Secured Routes**: OAuth2 and JWT are used to secure API routes 🔒.

## 🏗️ Architecture

The project has a modular architecture, making it easy to scale and maintain. The main modules include:

- **auth**: Module for managing user authentication and authorization. It includes data schemas for users, routes for registration and authentication, and services for working with tokens 🛡️.
- **events**: Module for managing events. It includes data schemas for events, routes for creating and subscribing to events, and services for interacting with the database 🗓️.

## 🧩 Main Components

### 🔌 API Routes

- **/auth**: Routes for managing users, including registration, authentication, and token retrieval 🔐.
- **/events**: Routes for creating events, subscribing to them, and viewing a list of events 📅.

### ⏳ Background Tasks

- **Celery worker**: Processes tasks such as sending email notifications 📨.
- **Redis**: Used as a message broker and result backend for Celery 🔄.


## Containerization and Deployment

The project is fully containerized using Docker and Docker Compose. This ensures easy deployment and management of the application in various environments.

### Docker Compose

The project includes several services such as:

- **web**: Web service that runs the FastAPI application.
- **worker**: Celery worker for processing background tasks.
- **redis**: Used as a message broker for Celery.
- **dashboard**: Celery Flower for monitoring tasks.

### Dockerfile

The Dockerfile is configured to build a minimal container based on `python:3.12-alpine`, which reduces the container size and speeds up deployment.

## Running the Project with Docker Compose

This guide will help you run the project using Docker Compose. Docker Compose is used to manage multi-container applications, and this project leverages it to set up the web application, Celery worker, Redis, and Celery Flower for task monitoring.

### Prerequisites

1. **Install Docker and Docker Compose**: Ensure Docker and Docker Compose are installed on your system. You can follow the official documentation to install them:
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

2. **Clone the Repository**:
   - Clone the project repository to your local machine.

   ```bash
   git clone <repository-url>
   cd tms-fastapi

3. **Run Docker Compose**:
   - Use the following command to build and start all the services defined in the docker-compose.yml file:

   ```bash
   docker-compose up --build

### Access the Application

- **FastAPI Application**:  
  The FastAPI application will be available at [http://localhost:8004](http://localhost:8004).

- **Celery Flower**:  
  The Celery Flower monitoring dashboard will be accessible at [http://localhost:5557](http://localhost:5557).
