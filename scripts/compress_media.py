### メディアの容量を圧縮する
### 2020-08-09  たかお

import sys, hashlib, config, cv2
from PIL import Image
from classes import logger, thread, databeses, exceptions

class CompressMedia:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('compress_media.py',2)
            log = logger.ThreadLogging(thread_id)

            # 処理予約を行う
            #     サムネイル作成キューにプロセス番号を登録する。
            #     ステータスが「0：準備完了」かつ、プロセス番号が空。
            db = databeses.DbConnection(log)
            db.execute(
                " UPDATE queue_compress_medias A"\
                " SET A.thread_id = %(thread_id)s"\
                " WHERE A.`status` = 0"\
                " AND A.thread_id IS NULL "\
                " LIMIT 1000",
                {
                    'thread_id':thread_id
                }
            )
            
            db.commit()

            # 対象のファイル一覧を取得
            results = db.execute(
                " SELECT A.tweet_id, A.url, B.`type`, B.file_name, B.directory_path"\
                " FROM queue_compress_medias A"\
                " INNER JOIN tweet_medias B"\
                " ON A.tweet_id = B.tweet_id"\
                " AND A.url = B.url"\
                " WHERE A.thread_id = %(thread_id)s"\
                " AND A.`status` = 0",
                {
                    'thread_id':thread_id
                }
            )

            # サムネイルの作成
            for result in results:

                try:

                    # 画像メディアの圧縮
                    # 動画メディアは圧縮しない
                    if result['type'] == 'photo':
                        file_path = result['directory_path'] + result['file_name']
                        Image.open(file_path).convert('RGB').save(file_path, quality=70)

                    # 圧縮が完了したらキューから削除する
                    db.execute(
                        " DELETE FROM queue_compress_medias A" \
                        " WHERE A.tweet_id = %(tweet_id)s" \
                        " AND A.url = %(url)s",
                        {
                            'tweet_id' : result['tweet_id'],
                            'url' : result['url']
                        }
                    ) 
                    db.commit()

                except Exception as e:
                    # 例外が発生したレコードはステータスを更新する
                    log.error(e)
                    db.execute(
                        " UPDATE queue_compress_medias A"\
                        " SET A.`status` = 9"\
                        "    ,A.error_text = %(error_text)s" \
                        " WHERE A.tweet_id = %(tweet_id)s"\
                        " AND A.url = %(url)s",
                        {
                            'error_text' : str(e),
                            'tweet_id' : result['tweet_id'],
                            'url' : result['url']
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
                thread.ThreadId().ExitThread('compress_media.py',thread_id)

# 処理実行
CompressMedia.run()