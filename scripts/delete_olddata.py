### 古い情報を削除する
### 2020-03-13  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

print('★★★古いデータの削除')
print('データベースに蓄積された古いデータを削除します。')
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
cursor = con.cursor(MySQLdb.cursors.DictCursor)

try:

    print('蓄積した古いフォロワー情報を削除しています...')
    cursor.execute(
        " DELETE FROM followers A " \
        " WHERE A.exec_id IN ( " \
        " 	SELECT EI.exec_id " \
        " 	FROM exec_id_manage EI " \
        " 	WHERE EI.exec_count < (SELECT MAX(exec_count) -3 FROM exec_id_manage) " \
        " ) "
    )
    
    print('蓄積した古いフォロー情報を削除しています...')
    cursor.execute(
        " DELETE FROM friends A " \
        " WHERE A.exec_id IN ( " \
        " 	SELECT EI.exec_id " \
        " 	FROM exec_id_manage EI " \
        " 	WHERE EI.exec_count < (SELECT MAX(exec_count) -3 FROM exec_id_manage) " \
        " ) "
    )
    
    print('削除後のテーブル解析を行っています...')
    cursor.execute(
        " ANALYZE TABLE followers,friends,exec_id_manage "
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

print('データベースに蓄積された古いデータを削除しました。')
print('*******************************************')
print("処理は終了しました。")

