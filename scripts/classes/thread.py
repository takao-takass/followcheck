import datetime
from classes import logger, thread, databeses, exceptions

class ThreadId():

    def __init__(self):
        self.log = logger.ThreadLogging('-')

    # スレッドIDを発番する
    def CreateThread(self,process_name,thread_limit):

        try:
            # スレッド数が上限を超えている場合は例外
            db = databeses.DbConnection(self.log)
            cursor = db.execute(
                " SELECT COUNT(*) AS ct"\
                " FROM threads TH"\
                " WHERE TH.prosess_name = %(name)s",
                {
                    'name':process_name
                }
            )
            running_thread = cursor.fetchone()['ct']
            if running_thread >= thread_limit:
                raise exceptions.UncreatedThreadException()

            # スレッドIDを発番する
            thread_id = datetime.datetime.now().strftime('%H%M%S')
            db.execute(
                " INSERT INTO threads" \
                " (prosess_name, thread_id) " \
                " VALUES" \
                " (%(prosess_name)s, %(thread_id)s)",
                {
                    'prosess_name':process_name,
                    'thread_id':thread_id
                }
            )
            db.commit()

        except exceptions.UncreatedThreadException as e:
            self.log.warn('スレッド数が上限に達しているため、プロセスは実行されません。')
            raise e

        finally:
            db.close()

        return thread_id


    # スレッドIDを削除する
    def ExitThread(self,process_name,thread_id):

        try:
            db = databeses.DbConnection(self.log)
            db.execute(
                " DELETE FROM threads" \
                " WHERE prosess_name = %(process_name)s" \
                " AND thread_id = %(thread_id)s",
                {
                    'process_name':process_name,
                    'thread_id':thread_id
                }
            )
            db.commit()
        finally:
            db.close()
