### 古いツイートを抽出する
### 2020-08-23  たかお

import sys, hashlib, config
from classes import logger, thread, databeses, exceptions

class SelectOldTweet:

    @staticmethod
    def run(max_thread):

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('select_oldtweet.py',max_thread)
            log = logger.ThreadLogging(thread_id)

            # 削除対象となるツイートをキューに登録する
            db = databeses.DbConnection(log)
            db.execute(
                " INSERT IGNORE INTO queue_delete_tweets "\
                " ( "\
                " 		service_user_id, "\
                " 		tweet_id "\
                " ) "\
                " SELECT B.service_user_id, "\
                " 	    B.tweet_id "\
                " FROM tweets B "\
                " LEFT JOIN keep_tweets C "\
                " ON B.service_user_id = C.service_user_id "\
                " AND B.tweet_id = C.tweet_id "\
                " WHERE B.create_datetime < ( NOW() - INTERVAL 1 MONTH ) "\
                " AND C.tweet_id IS NULL ",
                {

                }
            )

            # キューに登録されているもののうち、KEEPされたものは削除する。
            db.execute(
                " DELETE FROM queue_delete_tweets A "\
                " WHERE EXISTS ( "\
                "     SELECT 1 "\
                "     FROM keep_tweets B "\
                "     WHERE B.service_user_id = A.service_user_id "\
                "     AND B.tweet_id = A.tweet_id "\
                " ) ",
                {
                    
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
                thread.ThreadId().ExitThread('select_oldtweet.py',thread_id)
            db.close()

# コマンドライン引数 1 : 同時実行スレッドの最大数
max_thread = int(sys.argv[0])

# 処理実行
SelectOldTweet.run(max_thread)