import os
import sys
import config
import urllib
import urllib.request

from PIL import Image
from classes import logger, thread, databeses, exceptions


class DownloadMedias:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('download_medias.py', 1)

            # サムネイルの作成
            log = logger.ThreadLogging(thread_id)
            log.info("メディア情報を確認しています...")

            # 処理予約をする。
            db = databeses.DbConnection(log)
            db.execute(
                " UPDATE queue_download_medias"
                " SET thread_id = %(thread_id)s"
                " WHERE `status` = 0"
                " AND thread_id IS NULL "
                " LIMIT 5000"
                , {
                    'thread_id': thread_id
                }
            )
            db.commit()

            download_medias = db.execute(
                " SELECT qdm.service_user_id,qdm.user_id,qdm.tweet_id,qdm.url,ru.disp_name,tm.sizes,tm.`type` "
                " FROM queue_download_medias qdm"
                " INNER JOIN tweet_medias tm"
                " ON qdm.service_user_id = tm.service_user_id"
                " AND qdm.tweet_id = tm.tweet_id"
                " AND qdm.url = tm.url "
                " INNER JOIN tweets tw"
                " ON tm.service_user_id = tw.service_user_id"
                " AND tm.tweet_id = tw.tweet_id"
                " INNER JOIN relational_users ru"
                " ON tw.user_id = ru.user_id"
                " WHERE qdm.thread_id = %(thread_id)s"
                , {
                    'thread_id': thread_id
                }
            )

            log.info("ダウンロードを開始します。")
            for download_media in download_medias:

                splited_usls = download_media['url'].split('/')
                file_name = splited_usls[len(splited_usls) - 1].split('?')[0]

                # ディレクトリパス（無ければ作る）
                directory_path = config.STRAGE_MEDIAS_PATH + download_media['service_user_id'] + '_' + download_media['disp_name'] + '/'
                if not os.path.exists(directory_path):
                    os.mkdir(directory_path)

                # 画像ファイルの対応サイズを判定
                size = ""
                if "large" in download_media['sizes']:
                    size = ":large"
                elif "medium" in download_media['sizes']:
                    size = ":medium"
                elif "small" in download_media['sizes']:
                    size = ":small"
                elif "thumb" in download_media['sizes']:
                    size = ":thumb"

                try:
                    print("ダウンロード中...  " + download_media['url'])
                    data = urllib.request.urlopen(download_media['url'] + size, timeout=20).read()
                    with open(directory_path + file_name, mode="wb") as f:
                        f.write(data)

                    file_size = os.path.getsize(directory_path + file_name)
                    db.execute(
                        " UPDATE tweet_medias"
                        " SET file_name = %(file_name)s"
                        "    ,directory_path = %(directory_path)s"
                        "    ,file_size = %(file_size)d"
                        " WHERE service_user_id = %(service_user_id)s"
                        " AND user_id = %(user_id)s"
                        " AND tweet_id = %(tweet_id)s"
                        " AND url = %(url)s"
                        , {
                            'file_name': file_name,
                            'directory_path': directory_path,
                            'file_size' : file_size,
                            'service_user_id': download_media['service_user_id'],
                            'user_id': download_media['user_id'],
                            'tweet_id': download_media['tweet_id'],
                            'url': download_media['url']
                        }
                    )
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
                            'service_user_id': download_media['service_user_id'],
                            'user_id': download_media['user_id'],
                            'tweet_id': download_media['tweet_id'],
                            'url': download_media['url']
                        }
                    )
                    db.execute(
                        " INSERT INTO queue_compress_medias (service_user_id, user_id, tweet_id, url)"
                        " VALUES ( %(service_user_id)s, %(user_id)s, %(tweet_id)s, %(url)s)"
                        , {
                            'service_user_id': download_media['service_user_id'],
                            'user_id': download_media['user_id'],
                            'tweet_id': download_media['tweet_id'],
                            'url': download_media['url']
                        }
                    )
                    db.execute(
                        " DELETE FROM queue_download_medias"
                        " WHERE service_user_id = %(service_user_id)s"
                        " AND user_id = %(user_id)s"
                        " AND tweet_id = %(tweet_id)s"
                        " AND url = %(url)s"
                        , {
                            'service_user_id': download_media['service_user_id'],
                            'user_id': download_media['user_id'],
                            'tweet_id': download_media['tweet_id'],
                            'url': download_media['url']
                        }
                    )
                    db.commit()


                except Exception as e:
                    log.error(e)
                    db.execute(
                        " UPDATE queue_download_medias"
                        " SET `status` = 9"
                        "    ,error_text = %(error_text)s"
                        " WHERE service_user_id = %(service_user_id)s"
                        " AND user_id = %(user_id)s"
                        " AND tweet_id = %(tweet_id)s"
                        " AND url = %(url)s"
                        , {
                            'error_text': str(e),
                            'service_user_id': download_media['service_user_id'],
                            'user_id': download_media['user_id'],
                            'tweet_id': download_media['tweet_id'],
                            'url': download_media['url']
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
                thread.ThreadId().ExitThread('download_medias.py', thread_id)


# 処理実行
DownloadMedias.run()
