# Trade Orders API

This repository contains a simple backend service for managing trade orders. The project demonstrates a complete DevOps pipeline, including a REST API, Docker containerization, deployment to an AWS EC2 instance, and a CI/CD workflow using GitHub Actions.

## Features

- **REST API Endpoints**
  - `POST /orders`: Submit trade orders (symbol, price, quantity, order type).
  - `GET /orders`: Retrieve all submitted orders.
- **Data Storage:** Uses SQLite (or PostgreSQL for production-like environments).
- **Optional Bonus:** WebSocket support for real-time order status updates.
- **Containerization:** Dockerfile for containerizing the application.
- **CI/CD Pipeline:** Automated tests, Docker image build, and deployment to an AWS EC2 instance via GitHub Actions.
- **API Documentation:** Swagger/OpenAPI documentation available at `/docs` when running locally

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Docker**
- **AWS EC2 instance** (Ubuntu recommended) with Docker installed and SSH access configured.
- **GitHub repository** with GitHub Actions enabled.

### Local Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/trade-orders-api.git
   cd trade-orders-api

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Run the Application:**

    ```bash
    uvicorn app.main:app --reload

4. **View API Documentation:**
    Open your browser to access the interactive Swagger UI:

    ```bash
    http://127.0.0.1:8000/docs 

## Running Tests

**Run your test with:**
    
    ```bash
    pytest

## Docker Setup

**Build the Docker Image**
    
    ```bash
    docker build -t trade-orders-api .

**Run the Docker Container**
    
    ```bash
    docker run -d -p 8000:8000 trade-orders-api

## Deployment on AWS EC2

1. **Create an EC2 Instance**
- **Choose Ubuntu as the OS**
- **Ensure it has Docker installed**

2. **Configure Security Groups**
- **Allow inbound SSH (port 22) so that GitHub Actions can connect**
- **For testing. you might temporarily allow `0.0.0.0/0` (open to all)**

3. **Set Up GitHub Secrets**

    In your respository settings, add the following secrets: 

    | Secret Name  | Description                        |
    |-------------|------------------------------------|
    | `EC2_HOST`  | Public IP of your EC2 instance    |
    | `EC2_USER`  | `ubuntu` (default SSH user)       |
    | `EC2_SSH_KEY` | Private key for SSH access      |
