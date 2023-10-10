from core.schemas.base.database_helper_res_schema import DatabaseHelperReSchema
from typing import Any, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL

from sqlalchemy.orm import Session


# This call handle connect to database via connection string

'''
    GET
        {
            Server,
            port,
            Database,
            user,
            password
        }
    Result Expect
        mysql_db = {'drivername': 'mysql+pymysql',
                'username': 'visai@rtqc',
                'password': 'Abc@123',
                'host': 'rtqc.mysql.database.azure.com',
                'database': 'dmspro_spvb_ai_engine',
                'port': 3306}
'''


class DBRepository:

    SessionLocal: Any = None
    engine: Engine = None

    def __init__(self, connectionString: Optional[str] = None):
        self._connection_string = connectionString
        if connectionString:
            self._sqlalchemy = self.get_sqlalchemy()
            self.connect(sqlalchemy=self._sqlalchemy)

    def get_sqlalchemy(self):
        dictConn = dict(entry.split('=')
                        for entry in self._connection_string.split(';'))

        mysql_db = {
            'drivername': 'mysql+pymysql',
            'username': dictConn['user'],
            'password': dictConn['password'],
            'host': dictConn['Server'],
            'database': dictConn['Database'],
            'port': dictConn['port']
        }

        return mysql_db

    def connect(self, sqlalchemy: str) -> DatabaseHelperReSchema:
        # => mysql+py://user@pass@host:port/databnase_table
        url = URL.create(**sqlalchemy)
        self.engine = create_engine(url,  connect_args={'ssl': {'ssl-mode': 'disabled'}}, echo=True)
        DBSession = scoped_session(sessionmaker())
        DBSession.remove()
        DBSession.configure(bind=self.engine, autoflush=False, expire_on_commit=False)
        self.SessionLocal = DBSession

        connector: Session = self.SessionLocal

        return DatabaseHelperReSchema(
            engine=self.engine,
            session=self.SessionLocal,
            connector=connector
        )

    # Dependency
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_engine(self) -> Engine:
        return self.engine


Base = declarative_base()