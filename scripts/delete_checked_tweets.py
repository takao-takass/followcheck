
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
            target_tweet_ids = db.execute(
                " SELECT service_user_id ,tweet_id"
                " FROM checked_tweets ct"
                " WHERE ct.update_datetime <= DATE_SUB(NOW(),INTERVAL 3 DAY)"
                " LIMIT 1000",
                {}
            )

            for target_tweet_id in target_tweet_ids:

                # メディアの削除
                log.info('ツイートを削除します。 tweet_id：'+target_tweet_id['tweet_id'])
                log.info('メディアのファイルパスを取得しています。')
                tweet_medias = db.execute(
                    " SELECT file_name, directory_path, thumb_file_name, thumb_directory_path"
                    " FROM tweet_medias tm"
                    " WHERE tm.tweet_id = %(tweet_id)s",
                    {
                        'tweet_id': target_tweet_id['tweet_id']
                    }
                )

                for tweet_media in tweet_medias:
                    log.info('メディアのファイルを削除します。')
                    media_file_path = tweet_media['directory_path'] + tweet_media['file_name']
                    thumb_file_path = tweet_media['thumb_directory_path'] + tweet_media['thumb_file_name']
                    log.info('media_file_path：'+media_file_path)
                    log.info('thumb_file_path：'+thumb_file_path)

                    if os.path.isfile(media_file_path):
                        os.remove(media_file_path)
                        log.info('削除しました。：'+media_file_path)

                    if os.path.isfile(thumb_file_path):
                        os.remove(thumb_file_path)
                        log.info('削除しました。：'+thumb_file_path)

                # tweet_mediasの削除
                log.info('tweet_mediasから削除しています。')
                db.execute(
                    " DELETE FROM tweet_medias A"
                    " WHERE A.tweet_id = %(tweet_id)s",
                    {
                        'tweet_id': target_tweet_id['tweet_id']
                    }
                )
                db.commit()

                # tweetsの削除
                log.info('tweetsから削除しています。')
                db.execute(
                    " DELETE FROM tweets A"
                    " WHERE A.service_user_id = %(service_user_id)s"
                    " AND A.tweet_id = %(tweet_id)s",
                    {
                        'service_user_id': target_tweet_id['service_user_id'],
                        'tweet_id': target_tweet_id['tweet_id']
                    }
                )
                db.commit()

                # checked_tweetsの削除
                log.info('checked_tweetsから削除しています。')
                db.execute(
                    " DELETE FROM checked_tweets A"
                    " WHERE A.service_user_id = %(service_user_id)s"
                    " AND A.tweet_id = %(tweet_id)s",
                    {
                        'service_user_id': target_tweet_id['service_user_id'],
                        'tweet_id': target_tweet_id['tweet_id']
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
                thread.ThreadId().ExitThread('create_thumbnail.py', thread_id)


# 処理実行
DeleteCheckedTweets.run()
