import os
import sys
from classes import logger, thread, databeses, exceptions


class ExistsMediaFile:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('exists_media_file.py', 1)
            log = logger.ThreadLogging(thread_id)

            # 処理予約を行う
            #     サムネイル作成キューにプロセス番号を登録する。
            #     ステータスが「0：準備完了」かつ、プロセス番号が空。
            db = databeses.DbConnection(log)
            checked_tweet_medias = db.execute(
                " SELECT tm.service_user_id"
                "       ,tm.user_id"
                "       ,tm.tweet_id"
                "       ,tm.url"
                "       ,tm.type"
                "       ,tm.sizes"
                "       ,tm.bitrate"
                "       ,tm.file_name"
                "       ,tm.directory_path"
                "       ,tm.thumb_file_name"
                "       ,tm.thumb_directory_path"
                "       ,tm.download_error"
                "       ,tm.create_datetime"
                "       ,tm.update_datetime"
                "       ,tm.deleted"
                " FROM checked_tweets t"
                " INNER JOIN tweet_medias tm"
                " ON t.service_user_id = tm.service_user_id"
                " AND t.tweet_id = tm.tweet_id"
                " LEFT JOIN losted_tweet_medias lt"
                " ON tm.service_user_id = lt.service_user_id"
                " AND tm.user_id = lt.user_id"
                " AND tm.tweet_id = lt.tweet_id"
                " AND tm.url = lt.url"
                " WHERE lt.service_user_id IS NULL",
                {
                }
            )

            for checked_tweet_media in checked_tweet_medias:

                try:

                    # ファイルのチェック
                    is_lost = False
                    thumb_file_path = checked_tweet_media['thumb_directory_path'] + checked_tweet_media[
                        'thumb_file_name']
                    media_file_path = checked_tweet_media['directory_path'] + checked_tweet_media['file_name']
                    log.info(media_file_path)
                    if not os.path.isfile(thumb_file_path):
                        is_lost = True
                    elif not os.path.isfile(media_file_path):
                        is_lost = True

                    if is_lost:
                        log.info("･･･存在しませんでした。")
                        db.execute(
                            " INSERT INTO losted_tweet_medias ("
                            "      service_user_id"
                            "     ,user_id"
                            "     ,tweet_id"
                            "     ,url"
                            "     ,`type`"
                            "     ,sizes"
                            "     ,bitrate"
                            "     ,file_name"
                            "     ,directory_path"
                            "     ,thumb_file_name"
                            "     ,thumb_directory_path"
                            "     ,download_error"
                            "     ,create_datetime"
                            "     ,update_datetime"
                            "     ,deleted"
                            " ) VALUES ("
                            "      %(service_user_id)s"
                            "     ,%(user_id)s"
                            "     ,%(tweet_id)s"
                            "     ,%(url)s"
                            "     ,%(type)s"
                            "     ,%(sizes)s"
                            "     ,%(bitrate)s"
                            "     ,%(file_name)s"
                            "     ,%(directory_path)s"
                            "     ,%(thumb_file_name)s"
                            "     ,%(thumb_directory_path)s"
                            "     ,%(download_error)s"
                            "     ,%(create_datetime)s"
                            "     ,%(update_datetime)s"
                            "     ,%(deleted)s"
                            " )"
                            " ON DUPLICATE KEY UPDATE"
                            "     losted_datetime = NOW()"
                            "     download_entried = 0"
                            " ;"
                            , {
                                'service_user_id': checked_tweet_media['service_user_id'],
                                'user_id': checked_tweet_media['user_id'],
                                'tweet_id': checked_tweet_media['tweet_id'],
                                'url': checked_tweet_media['url'],
                                'type': checked_tweet_media['type'],
                                'sizes': checked_tweet_media['sizes'],
                                'bitrate': checked_tweet_media['bitrate'],
                                'file_name': checked_tweet_media['file_name'],
                                'directory_path': checked_tweet_media['directory_path'],
                                'thumb_file_name': checked_tweet_media['thumb_file_name'],
                                'thumb_directory_path': checked_tweet_media['thumb_directory_path'],
                                'download_error': checked_tweet_media['download_error'],
                                'create_datetime': checked_tweet_media['create_datetime'],
                                'update_datetime': checked_tweet_media['update_datetime'],
                                'deleted': checked_tweet_media['deleted'],
                            }
                        )
                        db.commit()


                except Exception as e:
                    log.error(e)

        except exceptions.UncreatedThreadException:
            sys.exit()

        except Exception as e:
            log.error(e)
            sys.exit()

        finally:
            if 'thread_id' in locals():
                log.info('プロセスを終了します。')
                thread.ThreadId().ExitThread('exists_media_file.py', thread_id)


# 処理実行
ExistsMediaFile.run()
