
**📁 File Ingestion System**
============================
This little project was built in preparation for a company interview at Desjardins. This is only compulsory, it
is not part of a take home assignment. Simply for myself to brush up my Java and Python skills.

A **full-stack file ingestion project** built for learning and testing, comprising:

-   **Python backend**: parses CSV files and stores metadata locally

-   **Java frontend/API**: communicates with the Python backend, exposes endpoints for ingestion and metadata retrieval

-   **Web UI**: A simple dashboard to visualize uploaded files and metadata

-   **Fully dockerized**: for local deployment and GitHub Actions

-   **End-to-end tests**: using Playwright to validate the UI and integration

This project demonstrates a **multi-language, containerized, test-driven application** setup.

To launch the app, run the following command from the root of the project : 
``
npx serve ui
``

The application should be served locally at `http://localhost:3000`.

* * * * *

**Table of Contents**
---------------------

1.  [Project Structure](#project-structure)

2.  [Features](#features)

3.  [Prerequisites](#prerequisites)

4.  [Local Deployment](#local-deployment)

5.  [Running the Application](#running-the-application)

6.  [API Endpoints](#api-endpoints)

7.  [Running Tests](#running-tests)

8.  [Docker & CI/CD](#docker--cicd)

9.  [Playwright QA](#playwright-qa)

10. [Notes & Hiccups](#notes--hiccups)

11. [License](#license)

* * * * *

**Project Structure**
---------------------

```
.
├── java-api/              # Java Spring Boot API project
├── python-app/            # Python ingestion backend
│   ├── app/               # Python modules (ingest, metadata store)
│   ├── data/              # Incoming, processed, rejected files
│   └── tests/             # Python unit tests (pytest)
├── ui/                    # Frontend dashboard (HTML/CSS/JS)
├── playwright-tests/      # Playwright end-to-end tests
├── docker-compose.yml     # Docker setup for all services
├── README.md
└── .github/workflows/     # GitHub Actions CI/CD workflows
```

* * * * *

**Features**
------------

-   Upload CSV files and parse metadata (filename, size, SHA256, status, reason, path)

-   Validate CSV format and reject invalid/too large files

-   Python backend stores metadata locally (metadata.json)

-   Java API exposes endpoints to retrieve file metadata and trigger ingestion

-   Web dashboard for real-time file metadata viewing

-   Fully dockerized environment for easy local deployment

-   Playwright end-to-end tests for QA validation

-   CI/CD-ready with GitHub Actions pipeline

* * * * *

**Prerequisites**
-----------------

-   [Docker & Docker Compose](https://docs.docker.com/)

-   [Java 21](https://adoptium.net/)

-   [Maven](https://maven.apache.org/)

-   [Node.js](https://nodejs.org/) (for Playwright and web server)

-   [Python 3.10+](https://www.python.org/)

Optional for local dev without Docker:

-   pip install -r python-app/requirements.txt

-   mvn clean package for the Java API

* * * * *

**Local Deployment**
--------------------

1.  Clone the repository:

```
git clone <repo-url>
cd <project-root>
```

1.  Build and start Docker services:

```
docker-compose build
docker-compose up
```

1.  Verify services:

-   **Java API**: http://localhost:8081/health (or your configured port)

-   **Web dashboard**: http://localhost:3000

> Note: Ensure port 8080 or 8081 is free locally. Update docker-compose.yml if needed.

* * * * *

**Running the Application**
---------------------------

-   Python backend processes CSV files automatically from python-app/data/incoming

-   Valid files are moved to processed/, rejected to rejected/

-   Java API exposes endpoints for file metadata and triggering ingestion

-   Web dashboard fetches metadata via API

### **Example curl command**

```
curl http://localhost:8081/files
```

-   Returns JSON metadata of all processed files.

* * * * *

**API Endpoints**
-----------------
| Endpoint | Method | Description                       |
|----------|--------|-----------------------------------|
| /health  | GET    | Check API health status           |
| /files   | GET    | List all processed/rejected files |
| /ingest  | POST   | Trigger ingestion for new files   |


* * * * *

**Running Tests**
-----------------

### **Python backend tests**

```
cd python-app
pytest tests/ -v
```

### **Java API tests**

```
cd java-api
mvn test
```

### **Playwright end-to-end tests**

```
cd playwright-tests
npm install
npx playwright test
```

-   Use --headed to see the browser run:

```
npx playwright test --headed
```

-   Use --debug for step-by-step inspection:

```
npx playwright test --debug
```

* * * * *

**Docker & CI/CD**
------------------

-   docker-compose.yml defines all services: Java API, Python ingestion, volumes, and shared data

-   GitHub Actions workflows are configured to:

   1.  Build and test Java API

   2.  Build and test Python backend

   3.  Run Playwright E2E tests

   4.  Deploy or push Docker images

> Locally, you can emulate the pipeline using on macOS [Act](https://github.com/nektos/act):

```
act -W .github/workflows/ci.yml -j <job_name>
```

* * * * *

**Playwright QA**
-----------------

-   Playwright tests cover:

   -   Page load and headers

   -   Refresh button functionality

   -   Loading spinner and async UI updates

   -   Empty state

   -   Table rows and metadata rendering

   -   Action buttons (Download/Delete simulation)

-   Configured with **slowMo** **and explicit waits** to avoid race conditions

* * * * *

**Notes & Hiccups**
-------------------

-   Port conflicts may occur if 8080 is used (using port 8081 in the app); Docker Compose ports are configurable

-   CSV validation: ensure properly formatted CSV; invalid files are rejected. Not using a standard library however. So validation can be sloppy.

-   Python backend may need small delays on local dev due to async processing

-   Playwright tests require the web server to be fully started (serve module used)


* * * * *

**Areas for improvement**
-------------------

-   Add a messaging system with RabbitMQ or any suitable SQS messaging service
- Add a containerized Database with secure access
- Add the ability to retrieve processed files from the database
- Add an authentication system given the sensitive context (bank)

Just to name a few...

* * * * *

**License**
-----------

-   GNU Licence

* * * * *