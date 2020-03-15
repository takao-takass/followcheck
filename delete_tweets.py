### 削除予約されたダウンロードデータを物理削除する
### 2020-03-15  たかお

import sys,json, MySQLdb,config
import os,shutil
import urllib.request
from model.user import User
from requests_oauthlib import OAuth1Session

serviceUserId = '0000000001'

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
    print("削除するユーザを確認しています...")
    cursor.execute(
        " SELECT A.user_id, B.disp_name " \
        " FROM tweet_take_users A " \
        " INNER JOIN relational_users B " \
        " ON A.user_id = B.user_id " \
        " WHERE A.service_user_id = '"+serviceUserId+"'" \
        " AND A.status IN ('D') "\
    )

    delUsers = []
    for row in cursor:
        delUsers.append({
            'userId' : row['user_id'],
            'dispName' : row['disp_name']
        })

    print('ユーザのメディアファイルを削除しています...')
    for delUser in delUsers:
        directory = config.STRAGE_MEDIAS_PATH + delUser['dispName'] + '/'
        if os.path.exists(directory):
            shutil.rmtree(directory)

    print('ユーザのメディア情報を削除しています...')
    cursor.execute(
        " DELETE FROM tweet_medias A " \
        " WHERE A.tweet_id IN ( " \
        " 	SELECT TW.tweet_id " \
        " 	FROM tweets TW " \
        "   INNER JOIN tweet_take_users TT" \
        "   ON TW.user_id = TT.user_id" \
        "   AND TW.service_user_id = TT.service_user_id "
        " 	WHERE TT.status = 'D' " \
        " ) "
    )
    
    print('ユーザのツイート情報を削除しています...')
    cursor.execute(
        " DELETE FROM tweets A " \
        " WHERE (A.service_user_id,A.user_id) IN ( " \
        " 	SELECT TT.service_user_id,TT.user_id " \
        " 	FROM tweet_take_users TT" \
        " 	WHERE TT.status = 'D' " \
        " ) "
    )
    
    print('ユーザ情報を削除しています...')
    cursor.execute(
        " DELETE FROM tweet_take_users " \
        " WHERE status = 'D' " 
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
