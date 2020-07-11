### 映像メディアのサムネイルを作成する
### 2020-04-29  たかお

import sys,json, MySQLdb,config
import cv2
import os,hashlib
from PIL import Image

con = MySQLdb.connect(
    host = config.DB_HOST,
    port = config.DB_PORT,
    db = config.DB_DATABASE,
    user = config.DB_USER,
    passwd = config.DB_PASSWORD,
    charset = config.DB_CHARSET
)
con.autocommit(False)
cursor = con.cursor(MySQLdb.cursors.DictCursor)

try:
    print("サムネイルを作成する映像メディアを確認しています...")
    cursor.execute(
        " SELECT TM.tweet_id,TM.url,TM.file_name,TM.directory_path,RU.disp_name" \
        " FROM tweet_medias TM" \
        " INNER JOIN tweets TW" \
        " ON TM.tweet_id = TW.tweet_id" \
        " INNER JOIN relational_users RU" \
        " ON TW.user_id = RU.user_id" \
        " WHERE TM.thumb_file_name IS NULL" \
        " AND TM.file_name IS NOT NULL" \
        " AND TM.`type` IN ('video')" \
        " LIMIT 1000" \
    )

    # サムネイルを作成するメディア
    print("サムネイル作成情報を作成しています...")
    targetMedias = []
    for row in cursor:
        targetMedias.append({
            'tweet_id':row['tweet_id'],
            'url':row['url'],
            'file_name':row['file_name'],
            'directory_path':row['directory_path'],
            'disp_name':row['disp_name']
        })

    # サムネイルの作成
    print("サムネイルの作成を開始します[全"+str(len(targetMedias))+"件]...")
    for media in targetMedias:

        # 動画の読み込み
        print("サムネイルを作成しています["+media['directory_path']+media['file_name']+"]...")
        print(" -> 動画を読み込みます...")
        video = cv2.VideoCapture(media['directory_path'] + media['file_name'])
        if not video.isOpened():
            continue

        # サムネイルファイル名を発行する
        print(" -> サムネイル名を発行しています...")
        originText = media['url']
        thumbName = hashlib.md5(originText.encode()).hexdigest() + ".jpg"
        stragePath = config.STRAGE_MEDIAS_PATH + media['disp_name'] + '/'

        # 動画の30フレーム目を画像として保存する
        print(" -> 動画のフレームを切り出して保存しています...")
        video.set(cv2.CAP_PROP_POS_FRAMES, 30)
        ret, frame = video.read()
        try:
            cv2.imwrite(stragePath + thumbName, frame)
        except Exception as e:
            print(" -> ERROR:フレームの切り出しに失敗しました。動画のフォーマットを確認してください。")
            print(" -> ",e)
            continue

        # 保存した画像を読み込む
        print(" -> 保存した画像を読み込みます...")
        original = Image.open(stragePath + thumbName).convert('RGB')

        # 長辺は縦・横のどちらか？
        #  -> 縦の場合は、横360pxになるように縮小する
        #  -> 横の場合は、縦260pxになるように縮小する
        #  -> 同じ場合は、縦260pxになるように縮小する
        print(" -> 画像を縮小しています...")
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
        print(" -> 画像をトリミングしています...")
        thumb = original.crop((0,0,360,260))

        # サムネイルを保存する
        print(" -> サムネイルを保存しています...")
        thumb.save(stragePath + thumbName, quality=80)
        print(" -> サムネイルを保存しました。["+stragePath + thumbName+"]")

        # データベースにサムネイル情報を登録する
        print(" -> データベースにサムネイル情報を登録しています...")
        cursor.execute(
            " UPDATE tweet_medias" \
            " SET thumb_file_name = '"+thumbName+"' " \
            " ,thumb_directory_path = '"+stragePath+"' " \
            " ,update_datetime = NOW()" \
            " WHERE tweet_id = '"+media['tweet_id']+"'" \
            " AND url = '"+media['url']+"'"
        ) 
        con.commit()
        print(" -> 登録しました。")

except Exception as e:
    con.rollback()
    print("ERROR: ",e)
    print("エラーが発生しました。処理を終了します。")
    sys.exit()

finally:
    cursor.close()
    con.close()

print("プロセスは終了しました。")
