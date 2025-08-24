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
cd src
python setup_database.py

```

## Run the Application

### Python

```bash
cd src
source .env
python -m flask run

```

### Tests
```
cd src
source .env
pip install -r requirements.txt
python -m pytest  --cov=. tests/
```


## Usage

### Example API Usage

#### Users

```bash
curl -X POST http://localhost:5000/users \
    -H "Content-Type: application/json" \
    -d '{
    "first_name": "ellie",
    "last_name": "yotkova",
    "email": "eyotkova@gmail.com",
    "password": "abcd123"
}'
```

#### List/Get Users

```bash
curl http://localhost:5000/users
curl http://localhost:5000/users/1
```

#### Login

```bash
curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"email": "testuser@mail.com", "password": "testpass"}'
```


### Problems
Create a sample problem:
```
curl --location 'http://127.0.0.1:5000/problems/1/submiss' \
--header 'Content-Type: application/json' \
--data '{
  "name": "FizzBuzz",
  "description": "Given an integer n, print the numbers from 1 to n. But for multiples of three print '\''Fizz'\'' instead of the number and for multiples of five print '\''Buzz'\''. For numbers which are multiples of both three and five print '\''FizzBuzz'\''.",
  "input_format": "Single integer n",
  "output_format": "Print n lines, each line containing either the integer or '\''Fizz'\'', '\''Buzz'\'', or '\''FizzBuzz'\''.",
  "extra_metadata": {
    "difficulty": "easy",
    "tags": ["math", "simulation"],
    "companies": ["Google"]
  },
  "test_cases": [
    {
      "input": "3\n",
      "output": "1\n2\nFizz\n"
    },
    {
      "input": "5\n",
      "output": "1\n2\nFizz\n4\nBuzz\n"
    },
    {
      "input": "15\n",
      "output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n"
    }
  ],
  "created_by": 1
}
'
```

#### Tag a problem 
```
curl --location --request PUT 'http://127.0.0.1:5000/problems/1/tags' \
--header 'Content-Type: application/json' \
--data '{
  "tag": "np_hard"
}
'
```

#### Find a problem by tags
```
curl 'http://127.0.0.1:5000/problems?tags=np_hard' 
```

#### Submissions
__Note__ "passed_tests" is used to simulate submission execution

```
curl'http://127.0.0.1:5000/arena/1/submissions' \
--data '{
    "user_id": 1,
    "source_code": "print('\''Helloo, Word!2'\'')",
    "language": "python",
    "passed_tests": 10
}'
```