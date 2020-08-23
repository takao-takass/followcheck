### 古いツイートを削除する
### 2020-08-23  たかお

import sys, hashlib, config, os
from classes import logger, thread, databeses, exceptions

class DeleteOldTweet:

    @staticmethod
    def run(process_name,max_thread,max_rows):

        try:
            # スレッドIDの発行
            thread_id = thread.ThreadId().CreateThread(process_name,max_thread)
            log = logger.ThreadLogging(thread_id)
            log.info("削除対象のツイートを抽出しています...")

            # 処理予約をする。
            # 対象の利用者IDを取得する
            db = databeses.DbConnection(log)
            service_user_id_list = db.execute(
                " SELECT DISTINCT A.service_user_id "\
                " FROM queue_delete_tweets A ",
                {
                    # 引数なし
                }
            )

            # 利用者ごとに削除対象を選択する
            for service_user_id in service_user_id_list:
                db.execute(
                    " UPDATE queue_delete_tweets A"\
                    " SET A.thread_id = %(thread_id)s"\
                    " WHERE (A.service_user_id,A.tweet_id) IN ("\
                    "             SELECT C.service_user_id, C.tweet_id"\
                    "             FROM tweets C"\
                    "             WHERE  A.service_user_id = C.service_user_id"\
                    "             AND A.tweet_id = C.tweet_id "\
                    "             ORDER BY C.tweeted_datetime "\
                    " ) "\
                    " AND A.service_user_id = %(service_user_id)s "\
                    " AND A.`status` = '0'"\
                    " LIMIT %(max_rows)s ",
                    {
                        'thread_id':thread_id,
                        'service_user_id':service_user_id['service_user_id'],
                        'max_rows':max_rows
                    }
                )

            # 予約したレコードを取得する。
            # サムネイル作成キューから、自プロセス番号のレコードを取得する。
            media_path_list = db.execute(
                " SELECT B.directory_path,"\
                "         B.file_name,"\
                "         B.thumb_directory_path,"\
                "         B.thumb_file_name"\
                " FROM queue_delete_tweets A"\
                " INNER JOIN tweet_medias B"\
                " ON A.tweet_id = B.tweet_id"\
                " WHERE A.thread_id = %(thread_id)s"\
                " AND B.url IS NOT NULL"\
                " AND A.`status` = 0",
                {
                    'thread_id':thread_id
                }
            )

            # メディアファイルを削除する
            for media_path in media_path_list:

                media_file_path = media_path['directory_path'] + media_path['file_name']
                thumb_file_path = media_path['thumb_directory_path'] + media_path['thumb_file_name']

                if os.path.isfile(media_file_path):
                    os.remove(media_file_path)
                    os.remove(thumb_file_path)

            # ツイートメディアレコードを削除する
            db.execute(
                " DELETE FROM tweet_medias A"\
                " WHERE (A.tweet_id) IN ("\
                "         SELECT B.tweet_id"\
                "         FROM queue_delete_tweets B"\
                "         WHERE B.thread_id = %(thread_id)s"\
                "         AND B.`status` = '0'        "\
                " )",
                {
                    'thread_id':thread_id
                }
            )

            # ツイートレコードを削除する
            db.execute(
                " DELETE FROM tweets A"\
                " WHERE (A.service_user_id,A.tweet_id) IN ("\
                "         SELECT B.service_user_id,B.tweet_id"\
                "         FROM queue_delete_tweets B"\
                "         WHERE B.thread_id = %(thread_id)s"\
                "         AND B.`status` = '0'        "\
                " )",
                {
                    'thread_id':thread_id
                }
            )

            # キューレコードを削除する
            db.execute(
                " DELETE FROM queue_delete_tweets A"\
                " WHERE A.thread_id = %(thread_id)s",
                {
                    'thread_id':thread_id
                }
            )


        except exceptions.UncreatedThreadException:
            # スレッドの作成ができない時は処理終了
            sys.exit()

        except Exception as e:
            log.error(e)
            sys.exit()
        
        finally:
            if 'thread_id' in locals():
                log.info('プロセスを終了します。')
                thread.ThreadId().ExitThread(process_name,thread_id)

# コマンドライン引数 0 : 実行ファイル名
# コマンドライン引数 1 : 同時実行スレッドの最大数
# コマンドライン引数 2 : 処理対象の最大レコード数
process_name = sys.argv[0]
max_thread = int(sys.argv[1])
max_rows = int(sys.argv[2])

# 処理実行
DeleteOldTweet.run(process_name, max_thread, max_rows)