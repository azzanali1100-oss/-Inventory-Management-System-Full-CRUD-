# 📦 Full-Stack Inventory Management System (FastAPI, MySQL, Streamlit & Docker)

A robust, containerized full-stack web application designed for real-time inventory tracking, built using **FastAPI**, **MySQL 8.0**, **Streamlit**, and **Docker Compose**.

---

## 🚀 What We Have Built

This project is an end-to-end CRUD (Create, Read, Update, Delete) inventory management dashboard. It separates concerns cleanly into a high-performance asynchronous API backend, a persistent relational database, and an interactive data-driven user interface.

* **Backend API (`FastAPI`):** Handles HTTP requests, provides automated OpenAPI Swagger documentation, and validates payloads using Pydantic.
* **Database Engine (`MySQL 8.0`):** Manages relational storage with automatic transaction management, parameterized queries to prevent SQL injection, and data persistence via Docker volumes.
* **Frontend UI (`Streamlit`):** Delivers a responsive multi-tab web application allowing users to view, add, update, and delete records seamlessly without writing SQL.
* **Containerization (`Docker Compose`):** Orchestrates all three services concurrently in isolated environments.

---

## 🛠️ The Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Streamlit, Python, Requests | Interactive UI dashboard and state rendering |
| **Backend** | FastAPI, Uvicorn, Pydantic | RESTful API routing, validation, and middleware |
| **Database** | MySQL 8.0, `mysql-connector-python` | Relational data persistence and querying |
| **DevOps** | Docker, Docker Compose | Multi-container orchestration and deployment |

---

## 💡 Why We Built This & Problem Solved

### The Problem

Traditional local database setups often suffer from environment fragmentation, unmanaged database lifecycles, and brittle code where the frontend and backend are tightly coupled. Furthermore, manual SQL administrative tasks make data management tedious for non-technical operators.

### The Solution

This project solves these challenges by providing:

1. **Decoupled Architecture:** FastAPI acts as a strict contract-driven intermediary between the database and the UI.
2. **Zero-Configuration Deployment:** Using Docker Compose, any developer can spin up the entire database, API, and frontend with a single command, completely eliminating "it works on my machine" issues.
3. **Robust Data Validation:** Pydantic schemas intercept malformed inputs before they can corrupt relational database tables.
4. **Complete CRUD Operations:** A clean administrative dashboard that simplifies data lifecycle management.

---

## ⚙️ How We Built It (Architecture & Flow)

1. **Database Dependency Injection:** We implemented a FastAPI generator function (`get_db_cursor`) utilizing `yield` combined with `try...except...finally` blocks to guarantee that cursors and database connections are safely committed on success, rolled back on failure, and automatically closed to prevent memory leaks.
2. **Environment Agnostic Configuration:** The application uses dynamic environment variables (`os.getenv`) for database hosts and API routing, allowing it to transition smoothly between local `localhost` execution and isolated Docker network bridging (`db`, `backend`).
3. **Cross-Origin Resource Sharing (CORS):** Configured middleware in FastAPI to securely authorize communication between the frontend port (`8501`) and backend port (`8000`).

---

## 🚀 Getting Started & Installation

### Option A: Local Execution (Without Docker)

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/pervaiz123/my-first-app.git](https://github.com/pervaiz123/my-first-app.git)
   cd my-first-app
