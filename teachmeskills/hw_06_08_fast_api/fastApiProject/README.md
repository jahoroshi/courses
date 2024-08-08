# ✧ Project Description

## About the Project

This project is a web application for managing events and users. Users can create events, subscribe to them, and view a list of their events. The application implements full user authentication and authorization, including administrative functions.

## Technologies

- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **Poetry**
- **Docker**
- **JWT** (JSON Web Tokens)

## Architecture

The project has a modular architecture, making it easy to scale and maintain. The main modules include:

- **auth**: Module for managing user authentication and authorization. It includes data schemas for users, routes for registration and authentication, and services for working with tokens.
- **events**: Module for managing events. It includes data schemas for events, routes for creating and subscribing to events, and services for interacting with the database.

## Main Components

### Routes

- **/auth**: Routes for managing users, including registration, authentication, and obtaining tokens.
- **/events**: Routes for managing events, including creating events, subscribing to events, and viewing a list of events.

### Models

- **User**: User model with fields such as id, username, email, password, and is_admin.
- **Event**: Event model with fields such as id, name, meeting_time, description, and a list of users subscribed to the event.

### Services

Services are implemented using OOP and follow SOLID principles:

- **UserService**: Service for managing users, including creating new users, authentication, and retrieving a list of all users. It follows SOLID principles:
  - **S** (Single Responsibility Principle): Each service is responsible for a single entity.
  - **O** (Open/Closed Principle): Services can be extended without modifying their code.
  - **L** (Liskov Substitution Principle): Services can be replaced by their subclasses without affecting the program.
  - **I** (Interface Segregation Principle): Services use specific interfaces for each operation.
  - **D** (Dependency Inversion Principle): Services depend on abstractions, not concrete implementations.
- **EventService**: Service for managing events, including creating new events, subscribing to events, and retrieving a list of user events. It follows the same SOLID principles.

### Repositories

Repositories are also implemented using OOP and follow SOLID principles:

- **UserRepository**: Repository for performing CRUD operations on users.
- **EventRepository**: Repository for performing CRUD operations on events.

### Conclusion

This project demonstrates the use of modern technologies and approaches to create a reliable and scalable web application. It can serve as an excellent starting point for building your own applications using FastAPI, SQLAlchemy, and other tools.