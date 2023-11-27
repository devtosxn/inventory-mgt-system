# Inventory Management System API

[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This is a simple inventory management system API built with Flask and Flask-RESTful. It allows users to create, delete, update and retrieve products. It also allows users to add products to cart and purchase products.

- [Link to API Documentation](https://documenter.getpostman.com/view/example)

<!-- ![Screenshot](api-doc.png?raw=true "API DOC") -->

## Key Features

1. Product creation, deletion, update and retrieval.
2. Adding product to cart and purchasing product
3. Keeping track of product quantity in regards to purchase or add to cart functions, i.e the product quantity should reduce when a purchase is made, or when it is added to the "user's" cart; users should be informed when a product is "out of stock"
4. Products should have (name, category, labels(e.g size, colour etc), quantity, price) A product can have one or more labels.

## Technologies

- [Python 3.10](https://python.org): Base programming language for development
- [Flask](https://flask.palletsprojects.com/en/2.0.x/): Web framework for development
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/): Provides API development tools for easy API development
- [MongoDB](https://www.mongodb.com/): NoSQL database for development, staging and production environments
- [PyMongo](https://pypi.org/project/pymongo/): Popular Python driver used for interacting with MongoDB databases
- [Docker Engine and Docker Compose](https://www.docker.com/) : Containerization of the application and services orchestration

## Testing

Two user accounts have been created for testing purposes. The details are as follows:

- John Doe
  - email: johndoe@example.com
  - password: TestPassword
- Jane Doe

  - email: janedoe@example.com
  - password: TestPassword

- The API documentation is available on `https://documenter.getpostman.com/example` on your browser.

## How To Start App

- Clone the Repository
- create a .env file with the variables in the env.sample file

  - `cp env.sample .env`

- Run `make build`

  - Running the above command for the first time will download all docker-images and third party packages needed for the app.
  - **NB: This will take a few minutes for the first build**

- Run `make up`

  - Running the above command will Start up the following Servers:
    - API Server --> <http://localhost:8000>

- Run `make down` to stop the servers

- Other commands can be found in the Makefile
