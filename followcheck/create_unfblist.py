### フォロバ待ちリストを作成する
### 2020-03-03  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

print('★★★フォロバ待ちリスト作成')
print('フォロバ待ちリストを作成します。')
print('データベースに接続しています...')

# フォロバしてくれないユーザを登録する
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

    # フォロバされていないユーザをフォロバ待ちリストに登録
    print('フォロバしてくれていないユーザを登録しています...')
    cursor.execute(
        " INSERT INTO unfollowbacked ( " \
        " 		user_id " \
        " 		,unfollowbacked_user_id " \
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
        " LEFT JOIN ( " \
        " 		/* フォロワーを取得 */ " \
        " 		SELECT SFL.user_id " \
        " 		,SFL.follower_user_id " \
        " 		FROM followers SFL " \
        " 		WHERE SFL.exec_id = (SELECT MAX(exec_id) FROM exec_id_manage) " \
        " 	) FL " \
        " ON FR.user_id = FL.user_id " \
        " AND FR.follow_user_id = FL.follower_user_id " \
        " WHERE FL.follower_user_id IS NULL /*フォローしていてフォローされていない人*/ " \
        " ON DUPLICATE KEY UPDATE " \
        " 	update_datetime = NOW() /*既に登録済みの場合は更新日時のみ更新*/ "
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

print('フォロバされていないユーザをフォロバ待ちリストに登録しました。')
print('*******************************************')

print("処理は終了しました。")

