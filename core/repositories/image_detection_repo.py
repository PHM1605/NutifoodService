
from datetime import datetime
from typing import List
from core.repositories.database_connection_repo import DBRepository
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.expression import text
import json

class ImageDetectionRepo(DBRepository):
    def __init__(self, engine: Engine) -> None:
        self._access_db = engine
        