# FastAPI Basics

## Libraries Used:
1. FastAPI - Python framework for building APIs.
1. Uvicorn - ASGI server for running FastAPI applications.
1. Pydantic - Data validation tool for defining API schemas.

## End Points
1. GET `items`: Retrieves all items.
1. GET `items/{id}`: Retrieves a specific note by ID.
1. GET `items/{contains=x}`: Retrieves items containing a specific string or pattern.
1. POST `item`: Creates a new item.
1. PUT `item/{id}`: Updates an existing item by ID.
1. DELETE `item/{id}`: Deletes a item by ID.
