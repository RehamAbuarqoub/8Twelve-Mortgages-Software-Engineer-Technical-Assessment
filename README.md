# 8Twelve-Mortgages-Software-Engineer-Technical-Assessment
# Reham Abuarqoub

# Lead Intake and Qualification REST API

**Created on:** April 22, 2026

## The Goal of the Assessment

The goal of this project is to simulate a simple lead intake and qualification system for a mortgage-related business.

This REST API allows users to:
- create new leads
- retrieve all leads
- filter leads by source or status
- retrieve a single lead by ID
- check the health of the service

The project also integrates the **Groq API** to automatically generate a short **lead qualification summary** when a new lead is created. This helps demonstrate how AI can support lead review and follow-up in a real business workflow.
## How to run:
1. Open the project folder in Visual Studio Code.

2. Press `Ctrl + Shift + P`, then search for `Python: Create Environment`.

3. Select:
   - `Venv`
   - your preferred Python version

4. Open a new terminal in VS Code:
   `Terminal > New Terminal`

5. Activate the virtual environment on Windows:

   ```bash
   .\.venv\Scripts\activate
pip install -r requirements.txt


## Features

- `POST /leads` -> create a new lead
- `GET /leads`-> retrieve all leads
- `GET /leads/{id}`-> retrieve a lead by ID
- `GET /health` -> health check endpoint
- filter leads by `source` or `status`
- AI-generated lead qualification summary using Groq
- input validation and error handling
- in-memory data storage
- basic test coverage

## Tech Stack

- Python
- REST API
- Groq API
- Pytest

## Project Structure


```text
8Twelve-Mortgages-Software-Engineer-Technical-Assessment/
├── README.md
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── store.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── leads.py
│   └── services/
│       ├── __init__.py
│       └── groq_service.py
└── tests/
    ├── __init__.py
    └── test_api.py