# Test Task

This is a FastAPI-based API that interacts with a MongoDB database to manage **Items** and  **Clock-In Records** .

## Setup

### Requirements

* Python 3.8+
* MongoDB (local or Atlas)
* FastAPI
* Uvicorn

Clone the repo:
https://github.com/Aditya-Meena-26/Test-Task.git

Set up a virtual environment:
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run the app:
uvicorn main:app --reload

Here’s a simplified version of the `README.md`:

---


## Endpoints

### Items API

* **Create an Item** : `POST /items`
* **Get Item by ID** : `GET /items/{id}`
* **Filter Items** : `GET /items/filter`
* **Delete Item by ID** : `DELETE /items/{id}`
* **Update Item by ID** : `PUT /items/{id}`

### Clock-In API

* **Create Clock-In Record** : `POST /clock-in`
* **Get Clock-In Record by ID** : `GET /clock-in/{id}`
* **Filter Clock-In Records** : `GET /clock-in/filter`
* **Delete Clock-In Record by ID** : `DELETE /clock-in/{id}`
* **Update Clock-In Record by ID** : `PUT /clock-in/{id}`

## MongoDB Collections

* **Items** : Stores item details.
* **Clock-In Records** : Stores user clock-in information.
