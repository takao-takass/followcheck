import sys,json, MySQLdb,config
from model.user import User
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

# リクエスト送信回数の上限
# API上限 1500/15min、3min周期で実行する想定。
requests_max = 200

while requests_max > 0:

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
        # 対象のユーザを取得する
        print("ツイート取得対象のユーザを確認しています...")
        cursor.execute(
            " SELECT A.service_user_id, A.user_id, B.disp_name,A.include_retweet " 
            " FROM tweet_take_users A " 
            " INNER JOIN relational_users B " 
            " ON A.user_id = B.user_id " 
            " WHERE A.status IN ('5','6') "
            " AND B.icecream = 0"
            " AND A.not_tweeted_longtime = 0"
            " ORDER BY A.status desc LIMIT 1 "
        )

        if cursor.rowcount == 0:
            print("ツイートは更新しました。")
            break

        for row in cursor:
            serviceUserId = row['service_user_id']
            userId = row['user_id']
            dispName = row['disp_name']
            include_retweet = row['include_retweet']
        
        print("ユーザの最終ツイートIDを確認しています...")
        cursor.execute(
            " SELECT A.tweet_id " 
            " FROM tweets A " 
            " WHERE A.service_user_id = '"+serviceUserId+"'" 
            " AND A.user_id = '"+userId+"' "
            " ORDER BY A.tweeted_datetime desc LIMIT 1 "
        )
        continueTweetId = ''
        for row in cursor:
            continueTweetId= row['tweet_id']

        # APIにリクエストを送信してツイートを取得する
        print(userId+"のツイートを上限200件で取得しています...")
        res = twitter.get("https://api.twitter.com/1.1/statuses/user_timeline.json", params = {
            'user_id': str(userId),
            'count': 200,
            'since_id': continueTweetId,
            'include_rts': False
        })
        statuses = json.loads(res.text)

        # HTTP200以外のレスポンスが来たらスキップする
        if res.status_code != 200:
            print(str(userId)+"のAPIresponseは"+str(res.status_code)+"でした。スキップします。")
            cursor.execute(
                " UPDATE tweet_take_users" 
                " SET status = '9'" 
                " ,continue_tweet_id = null" 
                " ,update_datetime = NOW()" 
                " WHERE service_user_id = '"+serviceUserId+"'" 
                " AND user_id = '"+userId+"'"
            )
            con.commit()
            continue

        # 取得したツイートをDBに登録する
        print("取得したツイートの情報をDBに登録します。")
        tweets = []
        tweetMedias = []
        other_user_id = []
        for statuse in statuses:
            # ツイートの本文
            tweets.append({
                'service_user_id':serviceUserId,
                'user_id':userId,
                'tweet_id':statuse['id_str'],
                'tweet_user_id':userId if (not 'retweeted_status' in statuse) else statuse["retweeted_status"]["user"]["id_str"],
                'body':statuse['text'],
                'tweeted_datetime':statuse['created_at'],
                'favolite_count':statuse['favorite_count'],
                'retweet_count':statuse['retweet_count'],
                'replied': "0" if statuse['in_reply_to_screen_name'] is None else "1",
                'retweeted':"0" if (not 'retweeted_status' in statuse) else "1",
            })

            # リツイート元ツイートの投稿主（ユーザID）
            # relational_usersに登録しておく必要がある
            if 'retweeted_status' in statuse:
                other_user_id.append(statuse["retweeted_status"]["user"]["id_str"])

            # ツイートに付随するメディア
            if 'extended_entities' in statuse:

                for media in statuse['extended_entities']['media']:

                    # 動画メディア
                    if 'video' == media['type']:
                        videoInfo = media['video_info']

                        # ビットレートが一番高い動画URLを取得する
                        videoMedia = {}
                        for variant in videoInfo['variants']:
                            if not 'bitrate' in variant:
                                continue
                            if (not 'bitrate' in videoMedia) or (videoMedia['bitrate'] < variant['bitrate']):
                                videoMedia = {
                                    'bitrate':variant['bitrate'],
                                    'contentType':variant['content_type'],
                                    'url':variant['url']
                                }
                        tweetMedias.append({
                            'service_user_id':serviceUserId,
                            'user_id':userId,
                            'tweet_id':statuse['id_str'],
                            'url':videoMedia['url'],
                            'type':media['type'],
                            'sizes':'',
                            'bitrate':videoMedia['bitrate']
                        })
                    
                    # 画像メディアとその他のメディア
                    else:
                        tweetMedias.append({
                            'service_user_id':serviceUserId,
                            'user_id':userId,
                            'tweet_id':statuse['id_str'],
                            'url':media['media_url'],
                            'type':media['type'],
                            'sizes':','.join(media['sizes']),
                            'bitrate':''
                        })

        # ツイートをDBに登録
        print(str(len(tweets))+"件のツイートを登録しています...")
        for tweet in tweets:
            cursor.execute(
                " INSERT INTO tweets ("
                " 	service_user_id"
                " 	,user_id"
                " 	,tweet_id"
                " 	,tweet_user_id"
                " 	,body"
                " 	,tweeted_datetime"
                " 	,favolite_count"
                " 	,retweet_count"
                " 	,replied"
                " 	,retweeted"
                " 	,create_datetime"
                " 	,update_datetime"
                " 	,deleted"
                " ) VALUES ("
                " 	 '"+tweet['service_user_id']+"'"
                " 	,'"+tweet['user_id']+"'"
                " 	,'"+tweet['tweet_id']+"'"
                " 	,'"+tweet['tweet_user_id']+"'"
                " 	,'"+tweet['body'].replace("'","").replace("/","").replace("%","").replace("\\","")+"'"
                " 	,STR_TO_DATE('"+tweet['tweeted_datetime']+"','%a %b %d %H:%i:%s +0000 %Y')"
                " 	,"+str(tweet['favolite_count'])+""
                " 	,"+str(tweet['retweet_count'])+""
                " 	,"+tweet['replied']+""
                " 	,"+tweet['retweeted']+""
                " 	,NOW()"
                " 	,NOW()"
                " 	,0"
                " )"
                " ON DUPLICATE KEY UPDATE "
                " 	update_datetime = NOW() /*既に登録済みの場合は更新日時のみ更新*/ "
            )

        # ツイートメディアをDBに登録
        print(str(len(tweets))+"件のメディアを登録しています...")
        for media in tweetMedias:
            cursor.execute(
                " INSERT INTO tweet_medias ("
                " 	service_user_id"
                " 	,user_id"
                " 	,tweet_id"
                " 	,url"
                " 	,type"
                " 	,sizes"
                " 	,bitrate"
                " 	,file_name"
                " 	,directory_path"
                " 	,create_datetime"
                " 	,update_datetime"
                " ) VALUES ("
                " 	 '"+media['service_user_id']+"'"
                " 	,'"+media['user_id']+"'"
                " 	,'"+media['tweet_id']+"'"
                " 	,'"+media['url']+"'"
                " 	,'"+media['type']+"'"
                " 	,'"+media['sizes']+"'"
                " 	,'"+str(media['bitrate'])+"'"
                " 	,null"
                " 	,null"
                " 	,NOW()"
                " 	,NOW()"
                " )"
                " ON DUPLICATE KEY UPDATE "
                " 	update_datetime = NOW() /*既に登録済みの場合は更新日時のみ更新*/ "
            )
            cursor.execute(
                " INSERT INTO queue_download_medias ("
                "   service_user_id "
                "   ,user_id "
                " 	,tweet_id"
                " 	,url"
                " ) VALUES ("
                " 	 '"+media['service_user_id']+"'"
                " 	,'"+media['user_id']+"'"
                " 	,'"+media['tweet_id']+"'"
                " 	,'"+media['url']+"'"
                " )"
                " ON DUPLICATE KEY UPDATE "
                " 	update_datetime = NOW() /*既に登録済みの場合は更新日時のみ更新*/ "
            )

        # リツイート元の投稿主をDBに登録
        print(str(len(other_user_id))+"件のリツイート元の投稿主を登録しています...")
        for user_id in other_user_id:
            cursor.execute(
                "INSERT INTO relational_users"
                "(user_id, disp_name, name)"
                "VALUES ('" +  user_id  + "', '　', '　')"
                " ON DUPLICATE KEY UPDATE " 
                " 	update_datetime = NOW() /*既に登録済みの場合は更新日時のみ更新*/ "
            )

        # 対象ユーザのステータスを更新する
        # MAX件数を取得できなくなったらツイート取得を終了する
        if len(statuses) <= 1:
            cursor.execute(
                " UPDATE tweet_take_users" 
                " SET status = '9'" 
                " ,continue_tweet_id = null" 
                " ,update_datetime = NOW()" 
                " WHERE service_user_id = '"+serviceUserId+"'"
                " AND user_id = '"+userId+"'"
            )
            con.commit()
        else:
            cursor.execute(
                " UPDATE tweet_take_users"
                " SET status = '6'"
                " ,continue_tweet_id = 'null'"
                " ,update_datetime = NOW()"
                " WHERE service_user_id = '"+serviceUserId+"'"
                " AND user_id = '"+userId+"'"
            )
            con.commit()

        cursor.execute(
            " UPDATE tweets t "
            " SET t.is_media = 1"
            " WHERE t.user_id = '"+userId+"'"
            " AND service_user_id = '"+serviceUserId+"'"
            " AND is_media = 0"
            " AND EXISTS("
            "     SELECT 1"
            "     FROM tweet_medias m"
            "     WHERE m.service_user_id = t.service_user_id "
            "     AND m.user_id = t.user_id "
            "     AND m.tweet_id = t.tweet_id"
            " )"
        )
        con.commit()

        # 対象ユーザの取得に戻る
        requests_max -= 1

    except Exception as e:
        con.rollback()
        print("ERROR: ",e)
        print("エラーが発生しました。処理を終了します。")
        sys.exit()

    finally:
        cursor.close()
        con.close()


print("全てのユーザが最新化されたらステータスを最新化待ちに更新します。")
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

    cursor.execute(
        " SELECT A.user_id "
        " FROM tweet_take_users A "
        " INNER JOIN relational_users B "
        " ON A.user_id = B.user_id "
        " WHERE A.status NOT IN ('0','1','9','D') "
        " AND B.icecream = 0 "
        " AND A.not_tweeted_longtime = 0 "
        " ORDER BY A.status desc LIMIT 1 "
    )
    if cursor.rowcount == 0:
        print("全てのユーザが完了しているため、最新化待ちに更新します。")
        cursor.execute(
            " UPDATE tweet_take_users "
            " SET status = '5' "
            "    ,update_datetime = NOW() "
            " WHERE status = '9'"
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

print("APIリクエスト残数："+str(requests_max))
print("処理は終了しました。")
