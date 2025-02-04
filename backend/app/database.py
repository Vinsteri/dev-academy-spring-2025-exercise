import time
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config import DATABASE_URL
from app.logging import logger
from contextlib import contextmanager


# db manager class
class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.check_database_availability()

    def check_database_availability(self, retries=5, delay=2):
        for attempt in range(retries):
            try:
                with self.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                return
            except OperationalError:
                logger.warning(f"Database connection failed. Retrying {attempt + 1}/{retries}...")
                time.sleep(delay)
        logger.error("Database is not available after multiple attempts, exiting...")
        sys.exit(1)

    @contextmanager
    def get_session(self):
        if self.sessionmaker is None:
            raise Exception("Database session not initialized")

        session = self.sessionmaker()

        try:
            yield session
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
            raise
        finally:
            session.close()


database_manager = DatabaseManager(DATABASE_URL)


def get_db():
    with database_manager.get_session() as session:
        yield session
