# Daily Oracle REST API

This project is a RESTful API developed using FastAPI.  
It provides daily fortune predictions and supports CRUD operations for managing weekly fortune quotes.

## Features
- Retrieve today’s fortune using a random oracle
- Retrieve fortune predictions by specific day
- Create new weekly fortune quotes
- Update existing fortune quotes
- Delete fortune quotes
- API documentation available via Swagger UI (OpenAPI)

## Technologies Used
- Python
- FastAPI
- Uvicorn

## How to Run the Application
1. Install the required dependencies:
```
pip install -r requirements.txt
```

2. Start the server:
```
uvicorn main:app --reload
```
3. Access the API documentation (Swagger UI) at:
```
http://127.0.0.1:8000/docs/
```
## Notes
This project was developed as part of a REST API coursework assignment and demonstrates the use of REST principles and CRUD operations.
