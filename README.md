# Genesis-API Contribution Guide

Welcome to the Genesis-API project! This guide will help you understand how to create a new endpoint and how to create a SQL table in the project.


Genesis-API is a project designed to provide a simple CRUD (Create, Read, Update, Delete) system that allows doctors to register to the application by introducing their CEDULAS. The system then sends a request to the gob.mx API to verify the authenticity of the doctor. Once verified, the doctor is granted access to the companion app in Swift (currently unreleased).

This project is intended for both doctors, for identity verification and access, and patients, for usage.

## Key Features

- Verify doctor identity using gob.mx API
- Allow patients to use the application
- Two-factor authentication for enhanced security
- MySQL for database management
- Docker for easy deployment and distribution

Welcome to the Genesis-API project! This guide will help you understand how to create a new endpoint and how to create a SQL table in the project.


## Table of Contents

- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [Contact](#contact)

## Installation

To install the project, clone the repository to your local machine:

```bash
git clone https://github.com/iOS-Lab-UP/Genesis-API.git
```

## Running the Project

### Prerequisites

Before you can run the project, you must have Docker installed on your machine. Docker is used to create a containerized environment for the application.

1. **First Time Setup**: The first time you run the project, you'll need to build the Docker images. Use the following command:

```sh
docker-compose up --build
```

2. **Normal Run**: After the first time, you can start the application with the following command:

```sh
docker-compose up
```

3. **Shutting Down**: To stop the application and remove the containers, networks, and volumes defined in `docker-compose.yml`, use the following command:

```sh
docker-compose down -v
```

## Testing

The project has an endpoint called health_check if you send a GET request to this endpoint you will get a response with the status of the application similar to this:

```json
{
	"cpu_usage": "5.3%",
	"date": "2023-03-07 00:27:00",
	"memory_usage": "17.0%",
	"message": "Server is up and running",
	"port": 5555,
	"status": "OK",
	"uptime": "1.76 days"
}
```

## Project Structure

The main application is located in the `App` directory, specifically in the `genesis_api` subdirectory. Here's a brief overview of the important files and directories:

- `__init__.py`: Initializes the application and brings together all the components.
- `config.py`: Contains configuration variables for the application.
- `models.py`: Defines the database models.
- `security.py`: Handles authentication and authorization.
- `tools`: This directory contains various utility scripts and route handlers.
- `users`: This directory contains routes and utilities related to user management.

The SQL scripts for database initialization and table creation are located in the `sql` directory.

## Creating a New Endpoint

1. **Define the Route**: Routes are defined in the `routes.py` file in the appropriate directory. If the new endpoint is related to users, for example, you would add the route to `users/routes.py`. The route should include the endpoint URL and the HTTP method(s) it responds to.

2. **Create the Handler**: The handler for the route should be defined in the `handlers.py` file in the `tools` directory. This function will contain the logic that is executed when the endpoint is hit.

3. **Register the Route**: Finally, register the new route in the `__init__.py` file. This makes the route available when the application is run.

## Creating a New SQL Table

1. **Write the SQL Script**: Create a new SQL script in the `sql` directory. The script should include the SQL commands to create the new table. Make sure to define all the necessary columns and data types, as well as any constraints.

2. **Name the Script**: The script should be named in a way that indicates its purpose and the order in which it should be run. The existing scripts are named with a three-digit prefix followed by a description, like `001_profile_db.sql`.

Remember, always test your changes thoroughly before pushing them to the repository. Happy coding!

Please note that this is a general guide and the exact steps may vary depending on the specifics of your task. Always refer to the existing code for examples and consult with the project maintainers if you're unsure.
