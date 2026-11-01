# Network Log Analyzer

## Project Overview

Network Log Analyzer is a web application developed using Python, FastAPI, React and Docker.

The application allows users to upload network log files and automatically extract timestamps from their contents.

## Technologies Used

- Python – Backend programming and timestamp extraction
- FastAPI – REST API for processing uploaded log files
- React – Frontend user interface
- Vite – Frontend development tooling
- Docker – Containerization
- Docker Compose – Running frontend and backend services together
- Pytest – Backend testing

## Features

- Upload a network log file through a web interface.
- Extract timestamps from log entries.
- Display extracted timestamps.
- Show the total number of extracted timestamps.
- Run the frontend and backend using Docker Compose.

## Project Structure

network-log-analyzer/
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── extractor.py
│   ├── requirements.txt
│   └── test_extractor.py
├── frontend/
│   ├── Dockerfile
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── package-lock.json
├── docker-compose.yml
└── README.md

## How to Run the Application

### Prerequisites

- Docker Desktop
- Docker Compose

### Start the Application

Open a terminal in the project root directory and run:

```bash
docker compose up --build
```

Docker Compose builds and starts the backend and frontend containers.

### Access the Application

Frontend:

http://localhost:5173

Backend API documentation:

http://localhost:8000/docs

## How to Use

1. Open the frontend application in your browser.
2. Click **Choose File**.
3. Select a network log file.
4. Click **Extract Timestamps**.
5. View the extracted timestamps and their total count.

## Example Output

For a sample log file, the application successfully extracted:


2026-08-14T09:17:31
09:19:06


Total timestamps extracted: 2

## Testing

Backend tests can be executed from the `backend` directory using:

```bash
python -m pytest
```

## Stop the Application

To stop and remove the Docker Compose containers, run:

```bash
docker compose down
```

## Current Status

The application has been implemented and tested successfully in a local Docker environment.

## Future Improvements

- Support additional timestamp formats.
- Add log filtering and searching.
- Provide downloadable extraction results.
- Add more comprehensive error handling and automated tests.
