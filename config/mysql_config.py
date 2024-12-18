import pymysql.cursors
import pymysql.err
import pymysql.connections
from config.config import settings
from helpers.logger import log_error


class MySQLConfig:
    def __init__(self):
        self.db = settings.MYSQL_DB
        self.host = settings.MYSQL_HOST
        self.port = settings.MYSQL_PORT
        self.user = settings.MYSQL_USER
        self.password = settings.MYSQL_PASSWORD
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                password=self.password,
                db=self.db,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
            )
            self.cursor = self.connection.cursor()
            return self
        except pymysql.err.OperationalError as e:
            log_error(e)

    def close(self):
        self.cursor.close()
        self.connection.close()

    def execute(self, query, args=None):
        try:
            self.cursor.execute(query, args)
        except pymysql.err.ProgrammingError as e:
            log_error(e)

    def executemany(self, query, args):
        try:
            self.cursor.executemany(query, args)
        except pymysql.err.ProgrammingError as e:
            log_error(e)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()


mysql_config = MySQLConfig()

async def get_db():
    db = mysql_config.connect()
    try:
        yield db
    finally:
        db.close()