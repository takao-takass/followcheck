### 画像メディアのサムネイルを作成する
### 2020-07-14  たかお

import sys, hashlib, config, cv2
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

            # 処理予約をする。
            #     サムネイル作成キューにプロセス番号を登録する。
            #     ステータスが「0：準備完了」かつ、プロセス番号が空。
            #     登録数のMAXはコマンドライン引数で受け取る。
            db = databeses.DbConnection(log)
            db.execute(
                " UPDATE queue_create_thumbs A"\
                " SET A.thread_id = %(thread_id)s"\
                " WHERE A.`status` = 0"\
                " AND A.thread_id IS NULL "\
                " LIMIT 1000",
                {
                    'thread_id':thread_id
                }
            )

            # 予約したレコードを取得する。
            # サムネイル作成キューから、自プロセス番号のレコードを取得する。
            results = db.execute(
                " SELECT A.tweet_id, A.url, B.`type`, B.file_name, B.directory_path, D.disp_name"\
                " FROM queue_create_thumbs A"\
                " INNER JOIN tweet_medias B"\
                " ON A.tweet_id = B.tweet_id"\
                " AND A.url = B.url"\
                " INNER JOIN tweets C"\
                " ON B.tweet_id = C.tweet_id"\
                " INNER JOIN relational_users D"\
                " ON C.user_id = D.user_id"\
                " WHERE A.thread_id = %(thread_id)s"\
                " AND A.`status` = 0",
                {
                    'thread_id':thread_id
                }
            )

            # サムネイルを作成する
            for result in results:

                try:

                    # サムネイルファイル名を発行する
                    log.info(" -> サムネイル名を発行しています...")
                    originText = result['url']
                    stragePath = config.STRAGE_MEDIAS_PATH + result['disp_name'] + '/'
                    thumbName = hashlib.md5(originText.encode()).hexdigest() + ".jpg"

                    # 画像メディアの読み込み
                    if result['type'] in ('photo','animated_gif'):
                        log.info("画像サムネイルを作成しています["+result['directory_path']+result['file_name']+"]...")
                        log.info(" -> 画像を読み込みます...")
                        original = Image.open(result['directory_path'] + result['file_name']).convert('RGB')

                    # 動画メディアの読み込み
                    elif result['type'] in ('video'):
                        log.info("動画サムネイルを作成しています["+result['directory_path']+result['file_name']+"]...")
                        log.info(" -> 動画を読み込みます...")
                        video = cv2.VideoCapture(result['directory_path'] + result['file_name'])
                        if not video.isOpened():
                            continue

                        # 動画の30フレーム目を画像として保存する
                        log.info(" -> フレームを切り出して保存しています...")
                        video.set(cv2.CAP_PROP_POS_FRAMES, 30)
                        ret, frame = video.read()
                        cv2.imwrite(stragePath + thumbName, frame)

                        # 保存した画像を読み込む
                        log.info(" -> 保存したフレームを読み込みます...")
                        original = Image.open(stragePath + thumbName).convert('RGB')


                    # 長辺は縦・横のどちらか？
                    #  -> 縦の場合は、横360pxになるように縮小する
                    #  -> 横の場合は、縦260pxになるように縮小する
                    #  -> 同じ場合は、縦260pxになるように縮小する
                    log.info(" -> 画像を縮小しています...")
                    width,height = original.size
                    scale = 0.0
                    if width > height :
                        # 横が長辺
                        scale = 260.0 / height
                    else :
                        # 縦が長辺
                        scale = 360.0 / width

                    # 画像の縮小
                    original.thumbnail((int(width * scale), int(height * scale)), Image.ANTIALIAS)

                    # サムネイルのトリミングを行う
                    #  -> サイズは360×260
                    log.info(" -> 画像をトリミングしています...")
                    thumb = original.crop((0,0,360,260))

                    # サムネイルを保存する
                    log.info(" -> サムネイルを保存しています...")
                    thumb.save(stragePath + thumbName, quality=80)
                    log.info(" -> サムネイルを保存しました。["+stragePath + thumbName+"]")

                    # データベースにサムネイル情報を登録し、キューからレコードを削除する
                    log.info(" -> データベースにサムネイル情報を登録しています...")
                    db.execute(
                        " UPDATE tweet_medias" \
                        " SET thumb_file_name = %(thumb_name)s" \
                        " ,thumb_directory_path = %(strage_path)s" \
                        " ,update_datetime = NOW()" \
                        " WHERE tweet_id = %(tweet_id)s" \
                        " AND url = %(url)s",
                        {
                            'thumb_name' : thumbName,
                            'strage_path' : stragePath,
                            'tweet_id' : result['tweet_id'],
                            'url' : result['url']
                        }
                    ) 
                    db.execute(
                        " DELETE FROM queue_create_thumbs A" \
                        " WHERE A.tweet_id = %(tweet_id)s" \
                        " AND A.url = %(url)s",
                        {
                            'tweet_id' : result['tweet_id'],
                            'url' : result['url']
                        }
                    ) 
                    db.commit()
                    log.info(" -> 登録しました。")

                except Exception as e:
                    # 例外が発生したレコードはステータスを更新する
                    log.error(e)
                    db.execute(
                        " UPDATE queue_create_thumbs A"\
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
                thread.ThreadId().ExitThread('create_thumbnail.py',thread_id)

# 処理実行
CreateThumbnail.run()