### 相互フォローリスト作成
### 2020-03-08  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

print('★★★相互フォローリスト作成')
print('相互フォローのリストを作成します。')
print('データベースに接続しています...')

con = MySQLdb.connect(
    host = config.DB_HOST,
    port = config.DB_PORT,
    db = config.DB_DATABASE,
    user = config.DB_USER,
    passwd = config.DB_PASSWORD,
    charset = config.DB_CHARSET
)
con.autocommit(False)
cursor = con.cursor()

try:

    # 相互フォローのユーザをリストに登録
    print('相互フォローのユーザを抽出して登録しています...')
    cursor.execute(
        " INSERT INTO follow_eachother ( " \
        " 		user_id " \
        " 		,follow_user_id " \
        " 		,undisplayed " \
        " 		,create_datetime " \
        " ) " \
        " SELECT FR.user_id " \
        " 		,FR.follow_user_id  " \
        " 		,0 " \
        " 		,NOW() " \
        " FROM ( " \
        " 		/* フォローを取得 */ " \
        " 		SELECT SFR.user_id " \
        " 		,SFR.follow_user_id " \
        " 		FROM friends SFR " \
        " 		WHERE SFR.exec_id = (SELECT MAX(exec_id) FROM exec_id_manage) " \
        " 	) FR " \
        " INNER JOIN ( " \
        " 		/* フォロワーを取得 */ " \
        " 		SELECT SFL.user_id " \
        " 		,SFL.follower_user_id " \
        " 		FROM followers SFL " \
        " 		WHERE SFL.exec_id = (SELECT MAX(exec_id) FROM exec_id_manage) " \
        " 	) FL " \
        " ON FR.user_id = FL.user_id " \
        " AND FR.follow_user_id = FL.follower_user_id " \
        " ON DUPLICATE KEY UPDATE " \
        " 	update_datetime = NOW() /*既に登録済みの場合は更新日時のみ更新*/" \
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

print('相互フォローのユーザをリストに登録しました。')
print('*******************************************')
print("処理は終了しました。")

