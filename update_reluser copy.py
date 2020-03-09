### 関連ユーザに登録されているユーザの最新情報を取得して更新する
### 2020-02-15  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

# 利用者のTwitterアカウント情報を取得する
print('★★★関連ユーザ情報更新')

# 関連ユーザに登録されているユーザIDを取得
print('関連ユーザに登録されているユーザを取得します。')
print('データベースに接続しています...')
con = MySQLdb.connect(
    host = config.DB_HOST,
    port = config.DB_PORT,
    db = config.DB_DATABASE,
    user = config.DB_USER,
    passwd = config.DB_PASSWORD,
    charset = config.DB_CHARSET
)
cursor = con.cursor(MySQLdb.cursors.DictCursor)

relationalUserIdList = []
try:
    print('関連ユーザを抽出しています...')
    cursor.execute(
        " SELECT RU.user_id "\
        " FROM relational_users RU "\
        " WHERE RU.deleted = 0"\
    )
    for row in cursor:
        relationalUserIdList.append(row['user_id'])

except Exception as e:
    print("ERROR: ",e)
    print("エラーが発生しました。処理を終了します。")
    sys.exit()

finally:
    cursor.close()
    con.close()


print('関連ユーザの情報を取得しています... ['+str(len(relationalUserIdList))+'件]')

# ユーザ取得APIのリクエストパラメータを作成する
# -> ユーザIDはまとめて100件リクエストできる
requestUserStrList = []
userStrList = []
count = 0
for userId in relationalUserIdList:
    userStrList.append(userId)
    count = count + 1
    if count >= 100 or count >= len(relationalUserIdList)%100 :
        requestUserStrList.append(userStrList)
        userStrList = []
        count = 0

# ユーザ100件ごとにユーザ情報を取得する
relationalUesrList = []
for userStr in requestUserStrList:

    # APIリクエスト
    params = {
        'user_id':",".join(userStr)
    }
    lookupRes = twitter.get("https://api.twitter.com/1.1/users/lookup.json", params = params)

    # APIレスポンスのからユーザ情報リストを取得
    if lookupRes.status_code == 200:
        lookup = json.loads(lookupRes.text)
        for user in lookup:
            relationalUesrList.append(
                User(
                    user['id_str'],
                    user['screen_name'],
                    user['name'],
                    user['profile_image_url'],
                    user['description'],
                    user['profile_background_color'],
                    user['followers_count'],
                    user['friends_count']
                )
            )
    else:
        print("Failed: " + str(lookupRes.status_code) +" - "+lookupRes.text)
 

print('関連ユーザの情報を取得しました ['+str(len(relationalUesrList))+'件]')
print('*******************************************')

print('関連ユーザの情報を最新に更新します。')
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
    print('関連ユーザを更新しています...')
    for user in relationalUesrList:
        sql = " UPDATE relational_users RU "\
            " SET RU.disp_name = '"+user.screen_name+"'"\
            " ,RU.name = '"+user.name.replace("'","").replace("/","").replace("%","").replace("\\","")+"'"\
            " ,RU.thumbnail_url = '"+user.thumbnail_url.replace('_normal','')+"'"\
            " ,RU.description = '"+user.description.replace("'","").replace("/","").replace("%","").replace("\\","")+"'"\
            " ,RU.theme_color = '"+user.theme_color+"'"\
            " ,RU.follow_count = "+str(user.friends_count)+""\
            " ,RU.follower_count = "+str(user.followers_count)+""\
            " ,RU.update_datetime = NOW()"\
            " WHERE RU.user_id = '"+user.id_str+"'"
        cursor.execute(sql)
    
    con.commit()

except Exception as e:
    con.rollback()
    print("ERROR: ",e)
    print(sql)
    print("エラーが発生しました。処理を終了します。")
    sys.exit()

finally:
    cursor.close()
    con.close()

print('関連ユーザの情報を最新にしました。')
print('*******************************************')

print("処理は終了しました。")
