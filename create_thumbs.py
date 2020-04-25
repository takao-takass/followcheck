### 画像メディアのサムネイルを作成する
### 2020-04-25  たかお

import sys,json, MySQLdb,config
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
    print("サムネイルを作成する画像メディアを確認しています...")
    cursor.execute(
        " SELECT TM.tweet_id,TM.url,TM.file_name,TM.directory_path"\
        " FROM tweet_medias TM"\
        " WHERE TM.thumb_file_name IS NULL"\
        " AND TM.file_name IS NOT NULL"\
        " AND TM.`type` IN ('photo','animated_gif')"\
        " LIMIT 100"
    )

    # サムネイルを作成するメディア
    print("サムネイル作成情報を作成しています...")
    targetMedias = []
    for row in cursor:
        targetMedias.append({
            'tweet_id':row['tweet_id'],
            'url':row['url'],
            'file_name':row['file_name'],
            'directory_path':row['directory_path']
        })

    # サムネイルの作成
    print("サムネイルの作成を開始します[全"+str(len(targetMedias))+"件]...")
    for media in targetMedias:

        # オリジナル画像の読み込み
        print("サムネイルを作成しています["+media['directory_path']+media['file_name']+"]...")
        print(" -> オリジナル画像を読み込みます...")
        original = Image.open(media['directory_path'] + media['file_name']).convert('RGB')

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

        # サムネイルファイル名を発行する
        print(" -> サムネイル名を発行しています...")
        originText = media['url']
        thumbName = hashlib.md5(originText.encode()).hexdigest() + ".jpg"

        # サムネイルを保存する
        print(" -> サムネイルを保存しています...")
        stragePath = config.STRAGE_MEDIAS_PATH + "thumbs/"
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
