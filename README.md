# 8Twelve-Mortgages-Software-Engineer-Technical-Assessment
# Reham Abuarqoub

# Lead Intake and Qualification REST API

**Created on:** April 22, 2026

## Project Goal

The goal of this project is to simulate a simple lead intake and qualification system for a mortgage-related business.

This REST API allows users to:
- create new leads
- retrieve all leads
- filter leads by source or status
- retrieve a single lead by ID
- check the health of the service

The project also integrates the **Groq API** to automatically generate a short **lead qualification summary** when a new lead is created. This helps demonstrate how AI can support lead review and follow-up in a real business workflow.

## Features

- `POST /leads` — create a new lead
- `GET /leads` — retrieve all leads
- `GET /leads/{id}` — retrieve a lead by ID
- `GET /health` — health check endpoint
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
lead-intake-api/
├── app/
│   ├── app.py
│   ├── schemas.py
│   ├── store.py
│   ├── config.py
│   ├── routes/
│   │   └── leads.py
│   └── services/
│       └── groq_service.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md