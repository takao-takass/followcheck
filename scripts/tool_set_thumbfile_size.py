import os
import sys
from classes import logger, thread, databeses, exceptions

class SetFileSize:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            thread_id = thread.ThreadId().CreateThread('set_thumbfile_size.py', 1)
            log = logger.ThreadLogging(thread_id)
            db = databeses.DbConnection(log)

            filesize_empty_meadias = db.fetch(
                " SELECT tm.service_user_id, tm.user_id, tm.tweet_id, tm.url, tm.thumb_directory_path, tm.thumb_file_name "
                " FROM tweet_medias tm "
                " INNER JOIN tweets t "
                " ON tm.service_user_id = t.service_user_id "
                " AND tm.user_id = t.user_id "
                " AND tm.tweet_id = t.tweet_id "
                " WHERE t.media_ready = 1 "
                " AND tm.thumb_file_size = 0 "
                " LIMIT 50000 "
                , {}
            )

            for filesize_empty_meadia in filesize_empty_meadias:

                file_path = filesize_empty_meadia['thumb_directory_path'] + filesize_empty_meadia['thumb_file_name']
                file_size = -1
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)

                db.execute(
                    " UPDATE tweet_medias "
                    " SET thumb_file_size = %(file_size)s "
                    " WHERE service_user_id = %(service_user_id)s "
                    " AND user_id = %(user_id)s "
                    " AND tweet_id = %(tweet_id)s "
                    " AND url = %(url)s ",
                    {
                        'file_size' : file_size,
                        'service_user_id' : filesize_empty_meadia['service_user_id'],
                        'user_id' : filesize_empty_meadia['user_id'],
                        'tweet_id' : filesize_empty_meadia['tweet_id'],
                        'url' : filesize_empty_meadia['url']
                    }
                )

            if len(filesize_empty_meadias) > 0:
                db.commit()

        except exceptions.UncreatedThreadException:
            # スレッドの作成ができない時は処理終了
            sys.exit()

        except Exception as e:
            log.error(e)
            sys.exit()

        finally:
            if 'thread_id' in locals():
                log.info('プロセスを終了します。')
                thread.ThreadId().ExitThread('set_thumbfile_size.py', thread_id)

# 処理実行
SetFileSize.run()
