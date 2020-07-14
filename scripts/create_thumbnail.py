### 画像メディアのサムネイルを作成する
### 2020-07-14  たかお

import sys
from PIL import Image
from classes import logger, thread, databeses, exceptions

class CreateThumbnail:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('create_thumbnail.py',2)

            # サムネイルの作成
            log = logger.ThreadLogging(thread_id)
            log.info("サムネイル作成情報を作成しています...")

            '''
            ここに処理を書く
            '''
            
        except exceptions.UncreatedThreadException:
            sys.exit()

        except Exception as e:
            log.error(e)
            sys.exit()
        
        finally:
            if 'thread_id' in locals():
                log.info('プロセスを終了します。')
                thread.ThreadId().ExitThread(thread_id)

# 処理実行
CreateThumbnail.run()