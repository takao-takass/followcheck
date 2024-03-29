import os
import sys, hashlib, config, cv2
from PIL import Image
from classes import logger, thread, databeses, exceptions

class CompressMedia:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('compress_media.py', 1)
            log = logger.ThreadLogging(thread_id)

            # 処理予約を行う
            #     サムネイル作成キューにプロセス番号を登録する。
            #     ステータスが「0：準備完了」かつ、プロセス番号が空。
            db = databeses.DbConnection(log)
            db.execute(
                " UPDATE queue_compress_medias A"
                " SET A.thread_id = %(thread_id)s"
                " WHERE A.`status` = 0"
                " AND A.thread_id IS NULL "
                " LIMIT 5000",
                {
                    'thread_id':thread_id
                }
            )
            
            db.commit()

            # 対象のファイル一覧を取得
            results = db.execute(
                " SELECT A.service_user_id,A.user_id,A.tweet_id, A.url, B.`type`, B.file_name, B.directory_path"
                " FROM queue_compress_medias A"
                " INNER JOIN tweet_medias B"
                " ON A.service_user_id = B.service_user_id"
                " AND A.tweet_id = B.tweet_id"
                " AND A.url = B.url"
                " WHERE A.thread_id = %(thread_id)s"
                " AND A.`status` = 0",
                {
                    'thread_id': thread_id
                }
            )

            # サムネイルの作成
            for result in results:

                try:

                    # 画像メディアの圧縮
                    # 動画メディアは圧縮しない
                    if result['type'] == 'photo':
                        file_path = result['directory_path'] + result['file_name']
                        Image.open(file_path).convert('RGB').save(file_path, quality=95)

                        file_size = os.path.getsize(file_path)
                        db.execute(
                            " UPDATE tweet_medias"
                            " SET file_size = %(file_size)s"
                            " WHERE service_user_id = %(service_user_id)s"
                            " AND user_id = %(user_id)s"
                            " AND tweet_id = %(tweet_id)s"
                            " AND url = %(url)s"
                            , {
                                'file_size' : file_size,
                                'service_user_id' : result['service_user_id'],
                                'user_id' : result['user_id'],
                                'tweet_id' : result['tweet_id'],
                                'url' : result['url']
                            }
                        )


                    # 圧縮が完了したらキューから削除する
                    db.execute(
                        " DELETE FROM queue_compress_medias" 
                        " WHERE service_user_id = %(service_user_id)s" 
                        " AND user_id = %(user_id)s" 
                        " AND tweet_id = %(tweet_id)s" 
                        " AND url = %(url)s",
                        {
                            'service_user_id' : result['service_user_id'],
                            'user_id' : result['user_id'],
                            'tweet_id' : result['tweet_id'],
                            'url' : result['url']
                        }
                    ) 
                    db.commit()

                except Exception as e:
                    # 例外が発生したレコードはステータスを更新する
                    log.error(e)
                    db.execute(
                        " UPDATE queue_compress_medias A"
                        " SET A.`status` = 9"
                        "    ,A.error_text = %(error_text)s" 
                        " WHERE A.service_user_id = %(service_user_id)s" 
                        " AND A.user_id = %(user_id)s" 
                        " AND A.tweet_id = %(tweet_id)s" 
                        " AND A.url = %(url)s",
                        {
                            'error_text' : str(e),
                            'service_user_id' : result['service_user_id'],
                            'user_id' : result['user_id'],
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