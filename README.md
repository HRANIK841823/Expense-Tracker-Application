# Personal Finance Tracker API

A RESTful API built with **FastAPI** for managing personal income and expenses. It supports user registration, JWT-based authentication, and CRUD operations for transactions. Users can view and filter their own transactions by type, category, and amount range.

## Features

- User registration with bcrypt password hashing
- User login using OAuth2 password form
- JWT bearer-token authentication
- Create, list, retrieve, update, and delete transactions
- Filter transactions by:
  - Type (`income` or `expense`)
  - Category
  - Minimum amount
  - Maximum amount
- User-specific transaction access
- SQLAlchemy ORM integration
- Interactive API documentation through Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Passlib with bcrypt
- Python-JOSE for JWT
- A SQLAlchemy-supported database configured in `database.py`

## Project Structure

The application code is organized approximately as follows:

```text
project/
├── main.py
├── database.py
├── models.py
├── router/
│   └── auth.py
├── .env
├── .gitignore
└── README.md
```

`main.py` defines the transaction endpoints and registers the authentication router. `router/auth.py` contains registration, login, token creation, and current-user authentication. `database.py` configures the SQLAlchemy engine and session; `models.py` defines the database models.

## Requirements

- Python 3.10 or newer recommended
- A database supported by your SQLAlchemy configuration
- `pip`

Install the core packages used by the provided application code:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy passlib[bcrypt] python-jose[cryptography] python-multipart python-dotenv
```

Install the database driver appropriate for your database as well. For example, PostgreSQL commonly uses:

```bash
pip install psycopg2-binary
```

If your project already has a `requirements.txt`, install from it instead:

```bash
pip install -r requirements.txt
```

## Environment Variables

The authentication code reads these environment variables:

```env
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- `SECRET_KEY`: secret used to sign JWT access tokens. Use a strong, private value.
- `ALGORITHM`: JWT signing algorithm, for example `HS256`.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: token lifetime in minutes.

Create a `.env` file in the project root and load it at application startup (for example, with `python-dotenv` and `load_dotenv()`), or set these variables in your environment before running the application. **Do not commit `.env` or real secrets to Git.**

The database connection settings are configured separately in `database.py`; configure them for your local database or hosting provider.

## Run the Application

From the project root, activate your virtual environment if you use one, then run:

```bash
uvicorn main:app --reload
```

If `uvicorn` is not available as a direct command, use:

```bash
python -m uvicorn main:app --reload
```

The API will usually be available at:

- Base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

All transaction endpoints require a valid bearer token.

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `POST` | `/register` | Register a user | No |
| `POST` | `/login` | Authenticate and receive an access token | No |
| `POST` | `/transactions` | Create a transaction | Yes |
| `GET` | `/transactions` | List the current user's transactions | Yes |
| `GET` | `/transactions/filter` | Filter the current user's transactions | Yes |
| `GET` | `/transactions/{transaction_id}` | Retrieve one of the current user's transactions | Yes |
| `PUT` | `/transactions/{transaction_id}` | Update a transaction | Yes |
| `DELETE` | `/transactions/{transaction_id}` | Delete a transaction | Yes |

## Usage Examples

### 1. Register a user

Send a JSON request to `POST /register`:

```json
{
  "username": "anik",
  "email": "anik@example.com",
  "password": "your_password"
}
```

Successful response:

```json
{
  "message": "User Created Successfully"
}
```

### 2. Log in

Send form data—not JSON—to `POST /login`:

```text
username=anik
password=your_password
```

The response contains an access token:

```json
{
  "access_token": "your_access_token",
  "token_type": "bearer"
}
```

In Swagger UI, use the **Authorize** control and provide the login credentials/token as prompted. For direct API requests, include this header:

```http
Authorization: Bearer your_access_token
```

### 3. Create a transaction

Send JSON to `POST /transactions`:

```json
{
  "title": "Monthly salary",
  "amount": 50000,
  "type": "income",
  "category": "Salary"
}
```

`amount` must be greater than zero, and `type` must be either `income` or `expense`.

### 4. List transactions

```http
GET /transactions
Authorization: Bearer your_access_token
```

Returns transactions belonging to the authenticated user.

### 5. Filter transactions

The filter endpoint accepts any combination of the following query parameters:

| Parameter | Description | Example |
|---|---|---|
| `type` | `income` or `expense` | `type=expense` |
| `category` | Exact category match | `category=Food` |
| `minimum_amount` | Minimum amount, inclusive | `minimum_amount=100` |
| `maximum_amount` | Maximum amount, inclusive | `maximum_amount=1000` |

Example:

```http
GET /transactions/filter?type=expense&category=Food&minimum_amount=100&maximum_amount=1000
Authorization: Bearer your_access_token
```

If both amount limits are supplied, the minimum must not exceed the maximum.

### 6. Retrieve one transaction

```http
GET /transactions/1
Authorization: Bearer your_access_token
```

A transaction is returned only if it belongs to the authenticated user.

### 7. Update a transaction

Send only the fields you want to change to `PUT /transactions/{transaction_id}`:

```json
{
  "amount": 55000,
  "category": "Salary"
}
```

Supported fields are `title`, `amount`, `type`, and `category`. If provided, `amount` must be greater than zero and `type` must be `income` or `expense`.

### 8. Delete a transaction

```http
DELETE /transactions/1
Authorization: Bearer your_access_token
```

## Validation and Access Control

- Transaction amounts must be positive.
- Transaction types are restricted to `income` and `expense`.
- Transaction queries are scoped to the authenticated user's ID.
- Passwords are stored as bcrypt hashes rather than plain text.
- Protected endpoints use JWT bearer authentication.

## Notes

- The database tables are created at application startup using SQLAlchemy metadata in the current implementation.
- Ensure `database.py` and `models.py` are configured correctly before starting the server.
- For production, use a secure secret manager or environment variables, HTTPS, proper error handling, database migrations, and tests.
- Review authentication error handling and input validation before deploying publicly.

## License

No license has been specified. Add a `LICENSE` file if you intend to distribute this project publicly.
