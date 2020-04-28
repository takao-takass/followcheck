### TwitterAPIからフォロー/フォロワーの情報を取得する
### 2020-02-15  たかお

import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理
service_user = "0000000001"
thisUsers = []

# 利用者のTwitterアカウント情報を取得する
print('★★★リムられリスト作成')
print("利用者のアカウント情報を取得します。")
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
    # 今回の実行IDを取得
    print('実行IDを発行しています...')
    cursor.execute("SELECT DATE_FORMAT(NOW(),'%Y%m%d%H%i%S') AS exec_id FROM DUAL")
    execId = cursor.fetchone()['exec_id']

    # 実行IDを登録
    print('実行IDを登録しています...')
    cursor.execute("SELECT COUNT(*) AS r_count FROM exec_id_manage")
    execCount = cursor.fetchone()['r_count']
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
    
    con.commit()

    print('リムったユーザを抽出しています...')
    cursor.execute(
        " SELECT RU.user_id" \
        " ,RU.disp_name" \
        " ,RU.name" \
        " ,RU.follow_count" \
        " ,RU.follower_count" \
        " FROM users_accounts UA" \
        " INNER JOIN relational_users RU" \
        " ON UA.user_id = RU.user_id" \
        " WHERE UA.service_user_id = '" + service_user + "'"
    )
    for row in cursor:
        thisUsers.append(User(row['user_id'],row['disp_name'],row['name'],"","","",row['follower_count'],row['follow_count']))

except Exception as e:
    con.rollback()
    print("ERROR: ",e)
    print("エラーが発生しました。処理を終了します。")
    sys.exit()

finally:
    cursor.close()
    con.close()

# フォロワーのページングに用いるカーソル
for thisUser in thisUsers:
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
            print("ERROR: Request Failed: " + str(followersRes.status_code) +" - "+followersRes.text)
            print("エラーが発生しました。処理を終了します。")
            sys.exit()

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
            print("ERROR: Request Failed: " + str(followsRes.status_code) +" - "+followsRes.text)
            print("エラーが発生しました。処理を終了します。")
            sys.exit()

    print(thisUser.screen_name+'のフォローを取得しました。 ['+str(len(followIdList))+'件]')
    print('*******************************************')

    print('今回取得したユーザ情報を登録します。')
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
                "     ,(SELECT MAX(exec_id) FROM exec_id_manage)" \
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
                "     ,(SELECT MAX(exec_id) FROM exec_id_manage)" \
                "     ,'"+userId+"'" \
                "     ,NOW()" \
                " )"
            )

        # 関連ユーザをINSERT
        print('%sの関連ユーザを登録しています...' % thisUser.screen_name)
        for userId in relationalUserIdList:
            cursor.execute(
                " INSERT INTO relational_users (" \
                "      user_id" \
                "     ,disp_name" \
                "     ,name" \
                "     ,follow_count" \
                "     ,follower_count" \
                "     ,create_datetime" \
                "     ,update_datetime" \
                " ) VALUES (" \
                "      '"+userId+"'" \
                "     ,'wait...'" \
                "     ,'(取得中...)'" \
                "     ,0" \
                "     ,0" \
                "     ,NOW()" \
                "     ,'2000-01-01'" \
                " )" \
                " ON DUPLICATE KEY UPDATE" \
                " 	update_datetime = NOW() /*既に登録済みの場合は更新日時のみ更新*/"
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

    print('今回取得したユーザ情報を登録しました。')
    print('*******************************************')

# 利用者をリムったユーザを抽出する
print('前回実行から今回実行までの間に、利用者をリムったユーザを抽出します。')
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
    # 今回の実行IDを取得
    print('リムったユーザを抽出しています...')
    cursor.execute(
        " /* 利用者のアカウントをリムーブしたユーザを抽出するSQL */"\
        " INSERT INTO remove_users "\
        " SELECT FLO.user_id "\
        "       ,FLO.follower_user_id AS remove_user_id "\
        "       ,0 AS day_old "\
        "       ,CASE "\
        "           WHEN FR.follow_user_id IS NULL THEN 0 "\
        "           ELSE 1 "\
        "        END AS followed "\
        "       ,NOW() create_datetime "\
        "       ,NOW() update_datetime "\
        "       ,0 AS deleted "\
        " FROM ( "\
        "         /* 前回実行で取得したフォロワーの一覧 */"\
        "         SELECT user_id, follower_user_id "\
        "         FROM followers "\
        "         WHERE exec_id = ( "\
        "             SELECT EI.exec_id "\
        "             FROM exec_id_manage EI "\
        "             WHERE EI.exec_count = (SELECT MAX(exec_count)-1 FROM exec_id_manage) "\
        "         ) "\
        " ) FLO "\
        " LEFT JOIN ( "\
        "         /* 今回実行で取得したフォロワーの一覧 */"\
        "         SELECT user_id,follower_user_id "\
        "         FROM followers "\
        "         WHERE exec_id = ( "\
        "             SELECT EI.exec_id "\
        "             FROM exec_id_manage EI "\
        "             WHERE EI.exec_count = (SELECT MAX(exec_count) FROM exec_id_manage) "\
        "         ) "\
        " ) FLN "\
        " ON FLO.user_id = FLN.user_id "\
        " AND FLO.follower_user_id = FLN.follower_user_id "\
        " LEFT JOIN ( "\
        "         /* 今回実行で取得したフォローの一覧 */ "\
        "         SELECT user_id,follow_user_id "\
        "         FROM friends "\
        "         WHERE exec_id = ( "\
        "             SELECT EI.exec_id "\
        "             FROM exec_id_manage EI "\
        "             WHERE EI.exec_count = (SELECT MAX(exec_count) FROM exec_id_manage) "\
        "         ) "\
        " ) FR "\
        " ON FLO.user_id = FR.user_id "\
        " AND FLO.follower_user_id = FR.follow_user_id "\
        " WHERE FLN.follower_user_id IS NULL " \
        " ON DUPLICATE KEY UPDATE" \
        " 	update_datetime = NOW() /*既に登録済みの場合は更新日時のみ更新*/"
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

print('リムったユーザを抽出しました。')
print('*******************************************')

print("処理は終了しました。")
