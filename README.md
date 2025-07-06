# GitHub Webhook Dashboard

This project is a **GitHub Webhook Dashboard** built with Flask, MongoDB, and a simple HTML/JS frontend. It receives GitHub webhook events (push, pull request, merge), stores them in MongoDB, and displays the latest events in a browser UI that updates every 15 seconds.

---

## Folder Structure
```
techStack/
├── app/
│ ├── init.py # Flask app factory and PyMongo setup
│ ├── config.py # Environment/configuration loader
│ ├── api/
│ │ └── routes.py # API endpoints for webhook and event fetch
│ └── models/
│   └── webhook_schema.py  #Pydantic schema for event data
├── static/
│ ├── script.js # Frontend JS for polling and rendering events
│ └── styles.css # Frontend CSS styles
├── templates/
│ └── index.html # Main frontend HTML page
├── .env # Environment variables
├── run.py # App entry point
└── README.md # Project documentation

```
---

## Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- [MongoDB](https://www.mongodb.com/try/download/community) running locally or remotely

---

## Setup Instructions

1. **Clone the repository**

   ```sh
   git clone <https://github.com/Ansh9728/webhook-repo.git>
   cd techStack
   ```

2. **Create and activate a virtual environment (recommended)**
    ```
    python -m venv .venv
    .venv\Scripts\activate   # On Windows
    # Or
    source .venv/bin/activate  # On Linux/Mac

    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Set environment variables**
    
    Edit the .env file in the project root:
    ```
    DB_SERVER=""

    DATABASE_NAME=""

    COLLECTION_NAME=""
    ```
    Replace the placeholders with your actual MongoDB server details.
5. **Run the application**
    Run the Flask app

    ```
    python run.py
    ```