import os
import sys
import config
from classes import logger, thread, databeses, exceptions
from requests_oauthlib import OAuth1Session


class RepairUsers:

    @staticmethod
    def run():

        try:
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('repair_users.py', 1)
            log = logger.ThreadLogging(thread_id)

            twitter = OAuth1Session(
                config.CONSUMER_KEY,
                config.CONSUMER_SECRET,
                config.ACCESS_TOKEN,
                config.ACCESS_TOKEN_SECRET
            )

            db = databeses.DbConnection(log)
            repair_user_ids = db.execute(
                " SELECT user_id"
                " FROM relational_users"
                " WHERE name = '　'"
                " AND icecream = 0"
                " LIMIT 500"
                , {}
            )

            for repair_user_id in repair_user_ids:

                log.info(f"ユーザ情報を復旧します [user_id={repair_user_id}]")

                res = twitter.get("https://api.twitter.com/1.1/statuses/user_timeline.json", params={
                    "user_id": repair_user_id
                })

                if res.status_code != 200:
                    log.warn(f"APIのリクエストが異常値を返しました [res.status_code={res.status_code}]")
                    continue

                if not hasattr(res, 'id_str'):
                    log.warn(f"Twitterに存在しないか削除されたユーザです")
                    log.debug(res)
                    continue

                db.execute(
                    " DELETE FROM relational_users ("
                    " WHERE user_id = %(user_id)s"
                    , {
                        'user_id': res.id_str,
                    }
                )

                db.execute(
                    " INSERT INTO relational_users ("
                    "      user_id"
                    "     ,disp_name"
                    "     ,name"
                    "     ,description"
                    "     ,theme_color"
                    "     ,follow_count"
                    "     ,follower_count"
                    "     ,create_datetime"
                    "     ,update_datetime"
                    "     ,deleted"
                    " ) VALUES ("
                    "      %(user_id)s"
                    "     ,%(disp_name)s"
                    "     ,%(name)s"
                    "     ,NULL"
                    "     ,NULL"
                    "     ,0"
                    "     ,0"
                    "     ,NOW()"
                    "     ,'2000-01-01'"
                    "     ,0"
                    " )"
                    , {
                        'user_id': res.id_str,
                        'disp_name': res.screen_name,
                        'name': res.name,
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
                thread.ThreadId().ExitThread('repair_users.py', thread_id)


# 処理実行
RepairUsers.run()
