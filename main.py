### TwitterAPIからフォロー/フォロワーの情報を取得する
### 2020-02-15  たかお

import json, MySQLdb, config
from user import User
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理
auth_user = ''

# 利用者のTwitterアカウント情報を取得する
res = json.loads(twitter.get("https://api.twitter.com/1.1/users/show.json", params = {"screen_name":auth_user}).text)
thisUser = User(res['id_str'],res['screen_name'],res['name'],res['followers_count'],res['friends_count'])

# フォロワーのページングに用いるカーソル
print('%sのフォロワーの情報を取得しています...' % thisUser.screen_name)
followersCursor = -1

# フォロワーのリストを取得する
# 最終カーソルに到達するまで200件(API上限数)ずつフォロワーを取得する
relationalUserIdList = []
followerIdList = []
while followersCursor != 0:

    # APIリクエスト
    params = {
        'cursor':followersCursor,
        'screen_name':thisUser.screen_name,
        'count':5000
    }
    followersRes = twitter.get("https://api.twitter.com/1.1/followers/ids.json", params = params)

    # APIレスポンスのからフォロワーリストを取得
    if followersRes.status_code == 200:
        followers = json.loads(followersRes.text)
        followersCursor = followers['next_cursor']
        for userId in followers['ids']:
            # 時間差でフォローに変動が有ると、リストの内容がズレてキー重複を起こすことが有る
            # これを防ぐために、ユーザIDがリストに格納済みでないか確認する
            if not str(userId) in followerIdList:
                followerIdList.append(str(userId))
                relationalUserIdList.append(str(userId))
    else:
        print("Failed: " + str(followersRes.status_code) +" - "+followersRes.text)
        break

print(thisUser.screen_name+'のフォロワーを取得しました。 ['+str(len(followerIdList))+'件]')
print('*******************************************')

# フォロのページングに用いるカーソル
print('%sのフォローの情報を取得しています...' % thisUser.screen_name)
followsCursor = -1

# フォローのリストを取得する
# 最終カーソルに到達するまで200件(API上限数)ずつフォロワーを取得する
followIdList = []
while followsCursor != 0:

    # APIリクエスト
    params = {
        'cursor':followsCursor,
        'screen_name':thisUser.screen_name,
        'count':5000
    }
    followsRes = twitter.get("https://api.twitter.com/1.1/friends/ids.json", params = params)

    # APIレスポンスのからフォローリストを取得
    if followsRes.status_code == 200:
        follows = json.loads(followsRes.text)
        followsCursor = follows['next_cursor']
        for userId in follows['ids']:
            # 時間差でフォローに変動が有ると、リストの内容がズレてキー重複を起こすことが有る
            # これを防ぐために、ユーザIDがリストに格納済みでないか確認する
            if not str(userId) in followIdList:
                followIdList.append(str(userId))
            if not str(userId) in relationalUserIdList:
                relationalUserIdList.append(str(userId))
    else:
        print("Failed: " + str(followsRes.status_code) +" - "+followsRes.text)
        break

print(thisUser.screen_name+'のフォローを取得しました。 ['+str(len(followIdList))+'件]')
print('*******************************************')


print('関連ユーザの情報を取得しています ['+str(len(relationalUserIdList))+'件]')

# ユーザ取得APIのリクエストパラメータを作成する
# -> ユーザIDはまとめて100件リクエストできる
requestUserStrList = []
userStrList = []
count = 0
for userId in relationalUserIdList:
    userStrList.append(userId)
    count = count + 1
    if count >= 100:
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
            relationalUesrList.append(User(user['id_str'],user['screen_name'],user['name'],user['followers_count'],user['friends_count']))
    else:
        print("Failed: " + str(lookupRes.status_code) +" - "+lookupRes.text)
        break    

print('関連ユーザの情報を取得しました ['+str(len(relationalUesrList))+'件]')
print('*******************************************')

print('データベースに接続しています...')

# フォロワーを登録する
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
    # 今回の実行IDを取得
    print('実行IDを発行しています...')
    cursor.execute("SELECT DATE_FORMAT(NOW(),'%Y%m%d%H%i%S') FROM DUAL")
    execId = cursor.fetchone()[0]

    # 実行IDを登録
    cursor.execute("SELECT COUNT(*) FROM exec_id_manage")
    execCount = cursor.fetchone()[0]
    cursor.execute(
        " INSERT INTO exec_id_manage (" \
        "      exec_id" \
        "     ,exec_count" \
        "     ,create_datetime" \
        " ) VALUES (" \
        "     '"+execId+"'" \
        "     ,"+str(execCount)+"" \
        "     ,NOW()" \
        " )"
    )

    # フォロワーをINSERT
    print('%sのフォロワーを登録しています...' % thisUser.screen_name)
    for userId in followerIdList:
        cursor.execute(
            " INSERT INTO followers (" \
            "      user_id" \
            "     ,exec_id" \
            "     ,follower_user_id" \
            "     ,create_datetime" \
            " ) VALUES (" \
            "      '"+thisUser.id_str+"'" \
            "     ,"+execId+"" \
            "     ,'"+userId+"'" \
            "     ,NOW()" \
            " )"
        )
    
    # フォローをINSERT
    print('%sのフォローを登録しています...' % thisUser.screen_name)
    for userId in followIdList:
        cursor.execute(
            " INSERT INTO friends (" \
            "      user_id" \
            "     ,exec_id" \
            "     ,follow_user_id" \
            "     ,create_datetime" \
            " ) VALUES (" \
            "      '"+thisUser.id_str+"'" \
            "     ,"+execId+"" \
            "     ,'"+userId+"'" \
            "     ,NOW()" \
            " )"
        )

    # 関連ユーザをINSERT
    print('%sの関連ユーザを登録しています...' % thisUser.screen_name)
    for user in relationalUesrList:
        cursor.execute(
            " REPLACE INTO relational_users (" \
            "      user_id" \
            "     ,disp_name" \
            "     ,name" \
            "     ,follow_count" \
            "     ,follower_count" \
            "     ,create_datetime" \
            " ) VALUES (" \
            "      '"+user.id_str+"'" \
            "     ,'"+user.screen_name+"'" \
            "     ,'"+user.name+"'" \
            "     ,"+str(user.friends_count)+"" \
            "     ,"+str(user.followers_count)+"" \
            "     ,NOW()" \
            " )"
        )
    
    con.commit()

except Exception as e:
    con.rollback()
    raise e

finally:
    cursor.close()
    con.close()

print("おわり")
