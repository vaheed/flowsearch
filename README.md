## FlowSearch: NetFlow Data Processing and Search Solution

FlowSearch is a powerful solution for processing, storing, and searching NetFlow data. Designed for efficiency and scalability, it converts raw NetFlow data into CSV, optimizes storage with Parquet format, and provides seamless search capabilities through a FastAPI service. Additionally, it includes a CLI tool for streamlined data conversions and queries. This project is written in Python and utilizes Docker Compose for effortless deployment.

### Features

- Process NetFlow data into CSV format.
- Convert CSV files to Parquet for efficient storage and querying.
- Provide a FastAPI-powered search API for indexed data.
- Include a CLI tool for conversions and searches.
- Docker Compose setup for easy deployment.

---

### Getting Started

#### Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.8 or higher.

#### Setup Instructions

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd flowsearch
   echo "[DEBUG] Changed directory to flowsearch"
   ```

2. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   echo "[DEBUG] Docker containers are being built and started"
   ```

3. Access the FastAPI search API at `http://localhost:8000`.
   ```bash
   echo "[DEBUG] FastAPI search API is available at http://localhost:8000"
   ```

---

### Usage

#### FastAPI API

1. Start the API using Docker Compose.
2. Access the API documentation at `http://localhost:8000/docs`.

Example using `curl` to query the API:

```bash
curl -X GET "http://localhost:8000/search?src_ip=192.168.1.1" -H "accept: application/json"
echo "[DEBUG] Executed curl to query the FastAPI search API"
```

#### CLI Tool

Use the CLI for data conversions or searches. Examples:

```bash
python cli.py convert --input /path/to/input.csv --output /path/to/output.parquet
echo "[DEBUG] Converted /path/to/input.csv to /path/to/output.parquet"
python cli.py search --query "src_ip=192.168.1.1"
echo "[DEBUG] Searched for src_ip=192.168.1.1 using the CLI tool"
```
