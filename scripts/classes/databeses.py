# データベース接続に関するクラス
import MySQLdb,config

class DbConnection:

    def __init__(self, logging):
        self.con = MySQLdb.connect(
            host = config.DB_HOST,
            port = config.DB_PORT,
            db = config.DB_DATABASE,
            user = config.DB_USER,
            passwd = config.DB_PASSWORD,
            charset = config.DB_CHARSET
        )
        self.con.autocommit(False)
        self.cursor = self.con.cursor(MySQLdb.cursors.DictCursor)
        self.logging = logging

    def execute(self, sql, param):

        self.logging.info(f'SQL="{sql}" param={str(param)}')
        try:
            self.cursor.execute(sql, param)
        except Exception as e:
            self.logging.error(e)
            raise e
        return self.cursor

    def commit(self):
        self.con.commit()
        self.logging.info('コミットしました。')

    def rollback(self):
        self.con.rollback()
        self.logging.info('ロールバックしました。')

    def close(self):
        self.cursor.close()
        self.con.close()
