### リムられリストを更新する
### 2020-03-02  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

print('★★★リムられリスト更新')
print('リムられリストを最新にします。')
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

    # 再フォローされている場合はリムられリストから削除する
    print('再フォローされたユーザをリムられリストから削除しています...')
    cursor.execute(
        " DELETE FROM remove_users" \
        " WHERE EXISTS(" \
        " 			SELECT 1" \
        " 			FROM followers FL" \
        " 			WHERE FL.user_id = user_id" \
        " 			AND FL.follower_user_id = remove_user_id" \
        " 			AND FL.exec_id = (SELECT MAX(exec_id) FROM exec_id_manage)" \
        " 	 )"
    )
    
    # リムられリストのフォローフラグを更新する
    print('フォローフラグを更新しています...')
    cursor.execute(
        " UPDATE remove_users" \
        " SET followed = (" \
        " 			SELECT COUNT(*) /*主キーで当てるので必ず1 OR 0になる*/ " \
        " 			FROM friends FR" \
        " 			WHERE FR.user_id = user_id" \
        " 			AND FR.follow_user_id = remove_user_id" \
        " 			AND FR.exec_id = (SELECT MAX(exec_id) FROM exec_id_manage)" \
        " 	 )" \
        "    ,update_datetime = NOW()"
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

print('リムられリストを最新にしました。')
print('*******************************************')
print("処理は終了しました。")

