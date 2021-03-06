import sys
from classes import logger, thread, databeses, exceptions


class RedownloadLostedMediaFile:

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
                " FROM losted_tweet_medias"
                " WHERE download_entried = 0"
                " ;"
                , {
                }
            )

            log.info(f"ダウンロードキューに登録します。")
            for checked_tweet_media in checked_tweet_medias:

                try:

                    db.execute(
                        " INSERT INTO queue_download_medias ("
                        "      service_user_id"
                        "     ,user_id"
                        "     ,tweet_id"
                        "     ,url"
                        " ) VALUES ("
                        "      %(service_user_id)s"
                        "     ,%(user_id)s"
                        "     ,%(tweet_id)s"
                        "     ,%(url)s"
                        " )"
                        " ;"
                        , {
                            'service_user_id': checked_tweet_media['service_user_id'],
                            'user_id': checked_tweet_media['user_id'],
                            'tweet_id': checked_tweet_media['tweet_id'],
                            'url': checked_tweet_media['url'],
                        }
                    )
                    db.commit()

                except Exception as e:
                    log.error(e)

                finally:
                    db.execute(
                        " UPDATE losted_tweet_medias"
                        " SET download_entried = 1"
                        " WHERE service_user_id = %(service_user_id)s"
                        " AND user_id = %(user_id)s"
                        " AND tweet_id = %(tweet_id)s"
                        " AND url = %(url)s"
                        , {
                            'service_user_id': checked_tweet_media['service_user_id'],
                            'user_id': checked_tweet_media['user_id'],
                            'tweet_id': checked_tweet_media['tweet_id'],
                            'url': checked_tweet_media['url'],
                        }
                    )
                    db.commit()

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
RedownloadLostedMediaFile.run()
