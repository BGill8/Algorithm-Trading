# Stock Projections Web App

This project is a web application for stock projections.

## Directory Structure

- `frontend/`: Contains the Next.js frontend application.
- `backend/`: Contains the FastAPI backend application, ready for AWS Lambda deployment.

### Frontend

The `frontend` directory is a standard Next.js application.

- `app/`: The main application pages.
- `components/`: Reusable React components.
- `public/`: Static assets.

### Backend

The `backend` directory contains the Python-based backend.

- `app/`: The main FastAPI application code.
  - `main.py`: The main application file.
  - `models.py`: Pydantic models for data validation.
  - `services.py`: Business logic and interaction with external APIs.
- `Dockerfile`: For containerizing the application.
- `requirements.txt`: Python dependencies.
- `template.yaml`: AWS SAM template for Lambda deployment.
