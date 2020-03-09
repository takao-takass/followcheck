### 相互フォローリストを更新する
### 2020-03-08  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

print('★★★相互フォローリスト更新')
print('相互フォローリストを最新にします。')
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

    # 相互フォローのユーザがフォロワーから居なくなった場合はリストから削除する
    print('フォロワーから居なくなったユーザをリストから削除しています...')
    cursor.execute(
        " DELETE FROM follow_eachother UF" \
        " WHERE NOT EXISTS(" \
        " 			SELECT 1" \
        " 			FROM followers FL" \
        " 			WHERE FL.user_id = UF.user_id" \
        " 			AND FL.follower_user_id = UF.follow_user_id" \
        " 			AND FL.exec_id = (SELECT MAX(exec_id) FROM exec_id_manage)" \
        " 	 )"
    )
    
    # 相互フォローのユーザをフォローから外した場合はリストから削除する
    print('フォローを外したユーザをリストから削除しています...')
    cursor.execute(
        " DELETE FROM follow_eachother UF" \
        " WHERE NOT EXISTS(" \
        " 			SELECT 1" \
        " 			FROM friends FL" \
        " 			WHERE FL.user_id = UF.user_id" \
        " 			AND FL.follow_user_id = UF.follow_user_id" \
        " 			AND FL.exec_id = (SELECT MAX(exec_id) FROM exec_id_manage)" \
        " 	 )"
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

print('相互フォローリストを最新にしました。')
print('*******************************************')
print("処理は終了しました。")

