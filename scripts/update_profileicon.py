### プロフィールアイコンを切り替える
### 2020-06-23  たかお

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
    print("ダウンロードするアイコン画像の情報を確認しています...")
    cursor.execute(
        " SELECT RI.user_id,RI.sequence,RI.url "\
        " FROM profile_icons RI "\
        " WHERE RI.completed = 0 "\
        " AND RI.create_datetime = ( "\
        "     SELECT MAX(RI2.update_datetime) "\
        "     FROM profile_icons RI2 "\
        "     WHERE RI2.user_id = RI.user_id "\
        " ) "\
        " LIMIT 1000 "
    )

    downloads = []
    for row in cursor:
        downloads.append({
            'user_id':row['user_id'],
            'sequence':row['sequence'],
            'url':row['url']
        })
    
    print("ダウンロードするアイコン画像："+str(len(downloads)))

    # アイコン画像をダウンロード
    count = 0
    for download in downloads:

        count += 1

        # ダウンロード
        # 成功したらDBにファイル名とパスを登録,関連ユーザのサムネURLを更新して完了フラグを設定
        # 例外が発生したら完了フラグの設定のみ
        directory = config.STRAGE_ICON_PATH+config.ICON_DIRECTORY
        filename = str(download['user_id'])+"_"+str(download['sequence'])+".jpg"
        try:
            print("ダウンロード中["+str(count)+"/"+str(len(downloads))+"]...  "+download['url'])
            urllib.request.urlretrieve(download['url'], directory+filename)
            cursor.execute(
                " UPDATE profile_icons RI "\
                " SET file_name = '"+filename+"' " \
                " ,directory_path = '"+directory+"' " \
                " ,completed = 1 " \
                " WHERE user_id = '"+download['user_id']+"'" \
                " AND sequence = '"+str(download['sequence'])+"'"
            )
            cursor.execute(
                " UPDATE relational_users RU " \
                " SET RU.thumbnail_url = CONCAT('/img/tweetmedia/"+config.ICON_DIRECTORY+"','"+filename+"') " \
                " WHERE RU.user_id = '"+download['user_id']+"' "
            ) 

        except Exception as e:
            print("ERROR: ",e)
            cursor.execute(
                " UPDATE profile_icons RI " \
                " SET completed = 9 " \
                " WHERE user_id = '"+download['user_id']+"'" \
                " AND sequence = "+str(download['sequence'])
            ) 
        
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
