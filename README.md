# Setup and Installation

## Prerequisites

- [Git](https://git-scm.com/)
- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/) (for running with Docker Compose)
 - Alternatively a running postgresql instance

## Clone the Repository

```bash
git clone https://github.com/ElitsaY/FMI_Arena.git
cd FMI_Arena
```

## Install Dependencies

### Python
Create a virtual environment and activate it:

```bash
python -m venv src/venv
source src/venv/bin/activate  # On Windows use: venv\Scripts\activate
```
```bash
pip install -r src/requirements.txt
```

### Prepare env variables
```
# sample ./src/.env
POSTGRES_USER=root
POSTGRES_PW=root
POSTGRES_DB=fmi_arena
POSTGRES_HOST=localhost
PASSWORD_SALT=elliesalted12345678901
```

### Setup database
```
docker compose -f docker-compose.yml up

source ./src/.env
python setup_database.py

```

## Run the Application

### Python

```bash
cd src
source .env
python -m flask run

```
