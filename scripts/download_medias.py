### ツイートに紐づくメディアをダウンロードする
### 2020-03-14  たかお

import sys,json, MySQLdb,config
import os
import urllib.request
from model.user import User
from requests_oauthlib import OAuth1Session

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
    print("ダウンロードするメディアの情報を確認しています...")
    cursor.execute(
        " SELECT A.tweet_id,A.url,C.disp_name,A.sizes,A.`type` " \
        " FROM tweet_medias A " \
        " INNER JOIN tweets B " \
        " ON A.tweet_id = B.tweet_id " \
        " INNER JOIN relational_users C " \
        " ON B.user_id = C.user_id " \
        " WHERE A.file_name IS NULL " \
        " AND A.download_error = '0' " \
        " AND A.deleted = '0' " \
    )

    downloads = []
    for row in cursor:
        downloads.append({
            'tweet_id':row['tweet_id'],
            'url':row['url'],
            'disp_name':row['disp_name'],
            'sizes':row['sizes'],
            'type':row['type']
        })
    
    print("ダウンロードするメディア："+str(len(downloads)))

    # メディアをダウンロード
    count = 0
    for download in downloads:

        count += 1

        # URLからドメイン･階層とパラメータを除去してファイル名を作る
        splitedUrl = download['url'].split('/')
        filename = splitedUrl[len(splitedUrl)-1].split('?')[0]

        # ディレクトリパス（無ければ作る）
        directory = config.STRAGE_MEDIAS_PATH + download['disp_name'] + '/'
        if not os.path.exists(directory):
            os.mkdir(directory)

        # 画像ファイルの対応サイズを判定
        size = "thumb"
        if "large" in download['sizes']:
            size = "large"
        elif "medium" in download['sizes']:
            size = "medium"
        elif "small" in download['sizes']:
            size = "small"
        
        # ダウンロード
        # 成功したらDBにファイル名とパスを登録
        # 例外が発生したらエラーフラグを設定して続行
        try:
            print("ダウンロード中["+str(count)+"/"+str(len(downloads))+"]...  "+download['url'])
            urllib.request.urlretrieve(download['url']+":"+size, directory+filename)
            print("-> tweet_mediasに登録しています...")
            cursor.execute(
                " UPDATE tweet_medias" \
                " SET file_name = '"+filename+"' " \
                " ,directory_path = '"+directory+"' " \
                " ,update_datetime = NOW()" \
                " WHERE tweet_id = '"+download['tweet_id']+"'" \
                " AND url = '"+download['url']+"'"
            ) 
            print("-> queue_create_thumbsに登録しています...")
            cursor.execute(
                " INSERT INTO queue_create_thumbs"\
                " 	(tweet_id, url)"\
                " 	VALUES"\
                " 	('"+download['tweet_id']+"', '"+download['url']+"')"
            ) 
            print("-> queue_compress_mediasに登録しています...")
            cursor.execute(
                " INSERT INTO queue_compress_medias"\
                " 	(tweet_id, url)"\
                " 	VALUES"\
                " 	('"+download['tweet_id']+"', '"+download['url']+"')"
            ) 

        except Exception as e:
            print("-> エラーが発生しました。ステータスを更新します。")
            print("ERROR: ",e)
            cursor.execute(
                " UPDATE tweet_medias" \
                " SET download_error = 1 " \
                " ,update_datetime = NOW()" \
                " WHERE tweet_id = '"+download['tweet_id']+"'" \
                " AND url = '"+download['url']+"'"
            ) 
        
        finally:
            con.commit()

except Exception as e:
    con.rollback()
    print("ERROR: ",e)
    print("エラーが発生しました。処理を終了します。")
    sys.exit()

finally:
    cursor.close()
    con.close()


print("処理は終了しました。")
