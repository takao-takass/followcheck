
import sys
import os
from classes import logger, thread, databeses, exceptions


class DeleteCheckedTweets:

    @staticmethod
    def run():

        thread_id = '-'
        log = logger.ThreadLogging(thread_id)

        try:
            # スレッドIDの発行
            thread_id = thread.ThreadId().CreateThread('delete_checked_tweets.py', 1)
            log = logger.ThreadLogging(thread_id)
            db = databeses.DbConnection(log)

            # 削除対象のツイートIDを取得する
            log.info('削除対象のツイートIDを取得しています。')
            delete_tweets = db.execute(
                " SELECT service_user_id, user_id, tweet_id"
                " FROM delete_tweets ct"
                " WHERE ct.update_datetime <= DATE_SUB(NOW(),INTERVAL 1 DAY)"
                " AND NOT EXISTS ("
                "     SELECT 1"
                "     FROM keep_tweets kt"
                "     WHERE kt.service_user_id = ct.service_user_id"
                "     AND kt.tweet_id = ct.tweet_id"
                " )"
                " LIMIT 5000"
                , {}
            )

            for delete_tweet in delete_tweets:

                # メディアの削除
                log.info('ツイートを削除します。 tweet_id：'+delete_tweet['tweet_id'])
                tweet_medias = db.execute(
                    " SELECT file_name, directory_path, thumb_file_name, thumb_directory_path"
                    " FROM tweet_medias tm"
                    " WHERE tm.service_user_id = %(service_user_id)s"
                    " AND tm.user_id = %(user_id)s"
                    " AND tm.tweet_id = %(tweet_id)s"
                    , {
                        'service_user_id': delete_tweet['service_user_id'],
                        'user_id': delete_tweet['user_id'],
                        'tweet_id': delete_tweet['tweet_id'],
                    }
                )

                for tweet_media in tweet_medias:

                    if tweet_media['file_name']:
                        media_file_path = tweet_media['directory_path'] + tweet_media['file_name']
                        log.info('メディアのファイルを削除します。：'+media_file_path)

                        if os.path.isfile(media_file_path):
                            os.remove(media_file_path)
                            log.info('削除しました。：'+media_file_path)

                    if tweet_media['thumb_file_name']:
                        thumb_file_path = tweet_media['thumb_directory_path'] + tweet_media['thumb_file_name']
                        log.info('サムネイルファイルを削除します。：'+thumb_file_path)

                        if os.path.isfile(thumb_file_path):
                            os.remove(thumb_file_path)
                            log.info('削除しました。：'+thumb_file_path)

                # tweet_mediasの削除
                db.execute(
                    " DELETE FROM tweet_medias tm"
                    " WHERE tm.service_user_id = %(service_user_id)s"
                    " AND tm.user_id = %(user_id)s"
                    " AND tm.tweet_id = %(tweet_id)s"
                    , {
                        'service_user_id': delete_tweet['service_user_id'],
                        'user_id': delete_tweet['user_id'],
                        'tweet_id': delete_tweet['tweet_id'],
                    }
                )

                # tweetsの削除
                db.execute(
                    " DELETE FROM tweets t"
                    " WHERE t.service_user_id = %(service_user_id)s"
                    " AND t.user_id = %(user_id)s"
                    " AND t.tweet_id = %(tweet_id)s"
                    , {
                        'service_user_id': delete_tweet['service_user_id'],
                        'user_id': delete_tweet['user_id'],
                        'tweet_id': delete_tweet['tweet_id'],
                    }
                )

                # delete_tweetsの削除
                db.execute(
                    " DELETE FROM delete_tweets A"
                    " WHERE A.service_user_id = %(service_user_id)s"
                    " AND A.user_id = %(user_id)s"
                    " AND A.tweet_id = %(tweet_id)s"
                    , {
                        'service_user_id': delete_tweet['service_user_id'],
                        'user_id': delete_tweet['user_id'],
                        'tweet_id': delete_tweet['tweet_id'],
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
                thread.ThreadId().ExitThread('delete_checked_tweets.py', thread_id)


# 処理実行
DeleteCheckedTweets.run()
