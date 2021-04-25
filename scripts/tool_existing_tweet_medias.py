import os
import sys
import config

from classes import logger, thread, databeses, exceptions

# DBに残っているがファイルが消えているメディアを探す
class ExistingTweetMedias:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            thread_id = thread.ThreadId().CreateThread('existing_tweet_medias.py', 1)
            log = logger.ThreadLogging(thread_id)
            db = databeses.DbConnection(log)

            existing_tweet_medias = db.fetch(
                " SELECT tm.directory_path||tm.file_name AS file_path "
                "       ,tm.service_user_id"
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
                " FROM existing_tweet_medias tm"
                " LIMIT 10000"
                , {}
            )

            for existing_tweet_media in existing_tweet_medias:

                # ファイルのチェック
                is_lost = False
                log.info(existing_tweet_media['file_path'])
                if not existing_tweet_media['file_path'] == None:
                    if not os.path.isfile(existing_tweet_media['file_path']):
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
                        "    ,download_entried = 0"
                        " ;"
                        , {
                            'service_user_id': existing_tweet_media['service_user_id'],
                            'user_id': existing_tweet_media['user_id'],
                            'tweet_id': existing_tweet_media['tweet_id'],
                            'url': existing_tweet_media['url'],
                            'type': existing_tweet_media['type'],
                            'sizes': existing_tweet_media['sizes'],
                            'bitrate': existing_tweet_media['bitrate'],
                            'file_name': existing_tweet_media['file_name'],
                            'directory_path': existing_tweet_media['directory_path'],
                            'thumb_file_name': existing_tweet_media['thumb_file_name'],
                            'thumb_directory_path': existing_tweet_media['thumb_directory_path'],
                            'download_error': existing_tweet_media['download_error'],
                            'create_datetime': existing_tweet_media['create_datetime'],
                            'update_datetime': existing_tweet_media['update_datetime'],
                            'deleted': existing_tweet_media['deleted'],
                        }
                    )

                db.execute(
                    " DELETE FROM existing_tweet_medias"
                    " WHERE service_user_id = %(service_user_id)s"
                    " AND user_id = %(user_id)s"
                    " AND tweet_id = %(tweet_id)s"
                    " AND url = %(url)s"
                    " ;"
                    , {
                        'service_user_id': existing_tweet_media['service_user_id'],
                        'user_id': existing_tweet_media['user_id'],
                        'tweet_id': existing_tweet_media['tweet_id'],
                        'url': existing_tweet_media['url'],
                    }
                )
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
                thread.ThreadId().ExitThread('existing_tweet_medias.py', thread_id)


# 処理実行
ExistingTweetMedias.run()
