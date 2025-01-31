from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config import DATABASE_URL
from contextlib import contextmanager


# db manager class
class DatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=False)
        self.sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.check_database_availability()

    def check_database_availability(self):
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except OperationalError:
            raise Exception("Database is not available, is the db container running?")

    @contextmanager
    def get_session(self):
        if self.sessionmaker is None:
            raise Exception("Database session not initialized")

        session = self.sessionmaker()

        try:
            yield session
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()


database_manager = DatabaseManager(DATABASE_URL)


def get_db():
    with database_manager.get_session() as session:
        yield session
