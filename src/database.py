from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)


@event.listens_for(async_engine.sync_engine, "connect")
def do_connect(dbapi_connection, connection_record):
    dbapi_connection.isolation_level = None

@event.listens_for(async_engine.sync_engine, "begin")
def do_begin(conn):
    conn.exec_driver_sql("BEGIN")


async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"