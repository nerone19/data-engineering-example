import os 
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, JSON, create_engine, Column
from sqlalchemy import engine


class Ship(SQLModel, table=True):
    """
    Dataclass for the Ship sql-model.
    """
    __tablename__ = "ships"

    device_id: str = Field(nullable=False, primary_key=True)
    date_time: Optional[datetime] = Field(sa_column=Column("datetime", default=None))
    address_ip: str = Field(nullable=False)
    address_port: int = Field(nullable=False, )
    original_message_id: str = Field(nullable=False, primary_key=True)
    raw_message: Optional[dict] = Field(default={}, sa_column=Column(JSON))

def get_engine(db_url:Optional[str] =os.getenv("DATABASE_URL", None)) -> engine.Engine:
    """
    Gets the SQL engine for the specified database.

    Args:
        db_url: The url for the database we want to connect to.

    Raises:
        ValueError: if the db_url is null.

    Returns:
        engine (Engine): The created SQl engine.
    """
    if not db_url:
        raise ValueError("db_url cannot be null.")
    else:
        engine =  create_engine(db_url)
        SQLModel.metadata.create_all(engine)
        return engine