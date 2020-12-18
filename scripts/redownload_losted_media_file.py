import os
import sys
from classes import logger, thread, databeses, exceptions


class ExistsMediaFile:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('redownload_losted_media_file.py', 1)
            log = logger.ThreadLogging(thread_id)

            db = databeses.DbConnection(log)
            checked_tweet_medias = db.execute(
                " SELECT service_user_id"
                "     ,user_id"
                "     ,tweet_id"
                "     ,url"
                " FROM losted_tweet_medias",
                {
                }
            )









        except exceptions.UncreatedThreadException:
            sys.exit()

        except Exception as e:
            log.error(e)
            sys.exit()

        finally:
            if 'thread_id' in locals():
                log.info('プロセスを終了します。')
                thread.ThreadId().ExitThread('redownload_losted_media_file.py', thread_id)


# 処理実行
ExistsMediaFile.run()
