### フォロバ待ちリストを更新する
### 2020-03-04  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

print('★★★フォロバ待ちリスト更新')
print('フォロバ待ちリストを最新にします。')
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

    # フォローされた場合はフォロバ待ちリストから削除する
    print('フォロバされたユーザをフォロバ待ちリストから削除しています...')
    cursor.execute(
        " DELETE FROM unfollowbacked UF" \
        " WHERE EXISTS(" \
        " 			SELECT 1" \
        " 			FROM followers FL" \
        " 			WHERE FL.user_id = UF.user_id" \
        " 			AND FL.follower_user_id = UF.unfollowbacked_user_id" \
        " 			AND FL.exec_id = (SELECT MAX(exec_id) FROM exec_id_manage)" \
        " 	 )"
    )
    
    # フォローを解除した場合はフォロバ待ちリストから削除する
    print('フォロバされたユーザをフォロバ待ちリストから削除しています...')
    cursor.execute(
        " DELETE FROM unfollowbacked UF" \
        " WHERE NOT EXISTS(" \
        " 			SELECT 1" \
        " 			FROM friends FL" \
        " 			WHERE FL.user_id = UF.user_id" \
        " 			AND FL.follow_user_id = UF.unfollowbacked_user_id" \
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

print('フォロバ待ちリストを最新にしました。')
print('*******************************************')
print("処理は終了しました。")

