### 関連ユーザに登録されているユーザの凍結チェックを行う
### 2020-06-26  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

print('★★★関連ユーザの凍結チェック')
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

    # 永久凍結ユーザを設定する
    # 凍結・削除をされてから30日経過すると、アカウントは復活できなくなる。
    print('復活できないユーザに区分値を設定します...')
    sql = \
        " UPDATE relational_users RU "\
        " SET RU.icecream = 9 "\
        " WHERE RU.icecream = 1 "\
        " AND NOW() > DATE_ADD(RU.icecream_datetime, INTERVAL '30' DAY) "
    cursor.execute(sql)
    con.commit()
    print('区分値を設定しました。')

    # 凍結・削除チェック対象のユーザを取得する
    print('凍結・削除チェックの対象ユーザを抽出しています...')
    sql = \
        " SELECT RU.user_id, RU.icecream "\
        " FROM relational_users RU "\
        " WHERE RU.icecream IN (0,1) "\
        " ORDER BY RU.verify_datetime IS NULL DESC "\
        " LIMIT 300"
    cursor.execute(sql)
    verify_users = []
    for row in cursor:
        verify_users.append({
            'user_id':row['user_id'],
            'icecream':row['icecream']
        })
    print('対象ユーザを抽出しました。['+str(len(verify_users))+'件]')
    
    # 対象ユーザの情報をTwitterAPIから取得する
    # 情報が取得できた場合はアカウントが生きており、HTTPレスポンスエラーが帰ってきた場合は凍結・削除されている。
    verified_users = []
    print('凍結・削除のチェックをしています...')
    for verify_user in verify_users:
        
        # APIリクエストを送り、レスポンスからアカウントの状態を判定する
        print('user_id:'+verify_user['user_id']+'のチェックをしています...')
        response = twitter.get("https://api.twitter.com/1.1/users/show.json", params = {'user_id':verify_user['user_id']})
        if response.status_code == 200:
            print('有効なアカウントです。')
            verified_users.append({
                'user_id':verify_user['user_id'],
                'before_icecream':verify_user['icecream'],
                'after_icecream':0
            })
        elif response.status_code == 429:
            print('APIが規制されています。スキップします。')
            print("Failed: " + str(response.status_code) +" - "+response.text)
        elif response.status_code == 403:
            print('アカウントには鍵がかけられています。スキップします。')
            print("Failed: " + str(response.status_code) +" - "+response.text)
        else:
            print('無効なアカウントです。')
            print("Failed: " + str(response.status_code) +" - "+response.text)
            verified_users.append({
                'user_id':verify_user['user_id'],
                'before_icecream':verify_user['icecream'],
                'after_icecream':1
            })

    # 凍結チェックの結果をDBに登録する
    print('凍結・削除チェックの結果を登録しています...')
    for verified_user in verified_users:
        # icecream_datetimeは、icecreamが0→1に更新されるときのみNOW()を設定する。
        sql = \
            " UPDATE relational_users RU "\
            " SET RU.icecream = "+str(verified_user['after_icecream'])+" "\
            +("    ,RU.icecream_datetime =  NOW() " if verified_user['before_icecream'] == 0 and verified_user['after_icecream'] == 1 else "")\
            +"    ,RU.verify_datetime = NOW() "\
            " WHERE RU.user_id = '"+verified_user['user_id']+"' "
        cursor.execute(sql)

    con.commit()
    print('登録しました。')


except Exception as e:
    con.rollback()
    print("ERROR: ",e)
    print(sql)
    print("エラーが発生しました。処理を終了します。")
    sys.exit()

finally:
    cursor.close()
    con.close()

print('*******************************************')
print("処理は終了しました。")
