from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/database_name'
# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://postgres:anik%40841823@localhost:5432/TodoApplicationDatabase"
# )


#For sqlite
SQLALCHEMY_DATABASE_URL='sqlite:///./expensetracker.db'

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()


import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load .env
load_dotenv()

# ============================================================
# Supabase PostgreSQL configuration
# ============================================================

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Check required variables
if not all([USER, PASSWORD, HOST, PORT, DBNAME]):
    raise ValueError(
        "Supabase database configuration is incomplete. "
        "Check user, password, host, port, and dbname in .env"
    )

# ============================================================
# SQLAlchemy connection URL
# ============================================================

DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
)

# ============================================================
# Create SQLAlchemy engine
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# ============================================================
# Test database connection
# ============================================================

try:
    with engine.connect() as connection:
        print("Supabase PostgreSQL connection successful!")

except Exception as e:
    print(f"Failed to connect to Supabase PostgreSQL: {e}")
    raise

# ============================================================
# Session
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ============================================================
# Base
# ============================================================

Base = declarative_base()











