import os
import sys
import config

from classes import logger, thread, databeses, exceptions

# DBに残っているがサムネが消えているメディアを探す
class ExistingMediaThumbs:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            thread_id = thread.ThreadId().CreateThread('existing_media_thumbs.py', 1)
            log = logger.ThreadLogging(thread_id)
            db = databeses.DbConnection(log)

            existing_media_thumbs = db.fetch(
                " SELECT CONCAT(tm.thumb_directory_path,tm.thumb_file_name) AS file_path "
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
                " FROM existing_media_thumbs tm"
                " WHERE thumb_directory_path IS NOT NULL"
                " LIMIT 100000"
                , {}
            )

            for existing_media_thumb in existing_media_thumbs:

                # ファイルのチェック
                is_lost = False
                log.info(existing_media_thumb['file_path'])
                if not existing_media_thumb['file_path'] == None:
                    if not os.path.isfile(existing_media_thumb['file_path']):
                        is_lost = True

                if is_lost:
                    log.info("･･･存在しませんでした。")
                    db.execute(
                        " INSERT INTO queue_create_thumbs ("
                        "     service_user_id"
                        "    ,user_id"
                        "    ,tweet_id"
                        "    ,url"
                        " ) VALUES ("
                        "     %(service_user_id)s"
                        "    ,%(user_id)s"
                        "    ,%(tweet_id)s"
                        "    ,%(url)s"
                        " )"
                        " ON DUPLICATE KEY UPDATE"
                        "      status = 0"
                        "     ,thread_id = NULL"
                        "     ,error_text = NULL"
                        , {
                            'service_user_id': existing_media_thumb['service_user_id'],
                            'user_id': existing_media_thumb['user_id'],
                            'tweet_id': existing_media_thumb['tweet_id'],
                            'url': existing_media_thumb['url']
                        }
                    )
                    
                db.execute(
                    " DELETE FROM existing_media_thumbs"
                    " WHERE service_user_id = %(service_user_id)s"
                    " AND user_id = %(user_id)s"
                    " AND tweet_id = %(tweet_id)s"
                    " AND url = %(url)s"
                    " ;"
                    , {
                        'service_user_id': existing_media_thumb['service_user_id'],
                        'user_id': existing_media_thumb['user_id'],
                        'tweet_id': existing_media_thumb['tweet_id'],
                        'url': existing_media_thumb['url'],
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
                thread.ThreadId().ExitThread('existing_media_thumbs.py', thread_id)


# 処理実行
ExistingMediaThumbs.run()
