### 古いツイートを削除する
### 2020-08-23  たかお

import sys, hashlib, config
from classes import logger, thread, databeses, exceptions

class DeleteOldTweet:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('delete_oldtweet.py',1)
            log = logger.ThreadLogging(thread_id)
           
        except exceptions.UncreatedThreadException:
            # スレッドの作成ができない時は処理終了
            sys.exit()

        except Exception as e:
            log.error(e)
            sys.exit()
        
        finally:
            if 'thread_id' in locals():
                log.info('プロセスを終了します。')
                thread.ThreadId().ExitThread('delete_oldtweet.py',thread_id)

# 処理実行
DeleteOldTweet.run()