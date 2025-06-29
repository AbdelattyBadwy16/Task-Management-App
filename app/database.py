import os
from sqlmodel import SQLModel, create_engine, Session

# Get the database URL from environment variables
DATABASE_URL = os.environ["DATABASE_URL"]

# Create a database engine with echo enabled for logging SQL statements
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables in the database based on the defined SQLModel models
def create_tables():
    SQLModel.metadata.create_all(engine)

# Provide a database session for dependency injection
def get_session():
    with Session(engine) as session:
        yield session
