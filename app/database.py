from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, echo=True)

# for table creation
def create_tables():
    SQLModel.metadata.create_all(engine)

# to start session with db
def get_session():
    with Session(engine) as session:
        yield session
