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

            # 処理予約をする。
            # 対象の利用者IDを取得する
            log.info("削除対象のツイートを抽出しています...")
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
                    " WHERE  A.service_user_id = %(service_user_id)s "\
                    " AND A.`status` = '0'"\
                    " ORDER BY A.tweeted_datetime "\
                    " LIMIT %(max_rows)s ",
                    {
                        'thread_id':thread_id,
                        'service_user_id':service_user_id['service_user_id'],
                        'max_rows':max_rows
                    }
                )
                
                db.commit()

            # 予約したレコードを取得する。
            # サムネイル作成キューから、自プロセス番号のレコードを取得する。
            tweet_id_list = db.execute(
                " SELECT A.service_user_id,A.tweet_id"\
                " FROM queue_delete_tweets A"\
                " WHERE A.thread_id = %(thread_id)s"\
                " AND A.`status` = 0",
                {
                    'thread_id':thread_id
                }
            )

            for tweet_id in tweet_id_list:

                media_path_list = db.execute(
                    " SELECT B.directory_path,"\
                    "         B.file_name,"\
                    "         B.thumb_directory_path,"\
                    "         B.thumb_file_name"\
                    " FROM tweet_medias B"\
                    " WHERE B.tweet_id = %(tweet_id)s"\
                    " AND B.file_name IS NOT NULL"\
                    " AND B.thumb_file_name IS NOT NULL",
                    {
                        'tweet_id':tweet_id['tweet_id']
                    }
                )

                # メディアファイルを削除する
                log.info("メディアファイルを削除しています...")
                for media_path in media_path_list:

                    media_file_path = media_path['directory_path'] + media_path['file_name']
                    thumb_file_path = media_path['thumb_directory_path'] + media_path['thumb_file_name']

                    if os.path.isfile(media_file_path):
                        log.info(media_file_path)
                        os.remove(media_file_path)

                    if os.path.isfile(thumb_file_path):
                        log.info(thumb_file_path)
                        os.remove(thumb_file_path)

                # ツイートメディアレコードを削除する
                log.info("メディアレコードを削除しています...")
                db.execute(
                    " DELETE FROM tweet_medias A"\
                    " WHERE A.tweet_id = %(tweet_id)s",
                    {
                        'tweet_id':tweet_id['tweet_id']
                    }
                )

                # ツイートレコードを削除する
                log.info("ツイートレコードを削除しています...")
                db.execute(
                    " DELETE FROM tweets A"\
                    " WHERE A.service_user_id = %(service_user_id)s"\
                    " AND A.tweet_id = %(tweet_id)s",
                    {
                        'service_user_id':tweet_id['service_user_id'],
                        'tweet_id':tweet_id['tweet_id']
                    }
                )

                # キューレコードを削除する
                log.info("キューレコードを削除しています...")
                db.execute(
                    " DELETE FROM queue_delete_tweets A"\
                    " WHERE A.service_user_id = %(service_user_id)s"\
                    " AND A.tweet_id = %(tweet_id)s",
                    {
                        'service_user_id':tweet_id['service_user_id'],
                        'tweet_id':tweet_id['tweet_id']
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
                thread.ThreadId().ExitThread(process_name,thread_id)

# コマンドライン引数 0 : 実行ファイル名
# コマンドライン引数 1 : 同時実行スレッドの最大数
# コマンドライン引数 2 : 処理対象の最大レコード数
process_name = sys.argv[0]
max_thread = int(sys.argv[1])
max_rows = int(sys.argv[2])

# 処理実行
DeleteOldTweet.run(process_name, max_thread, max_rows)