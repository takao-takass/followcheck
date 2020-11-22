
LOG_YMD=`date '+%Y%m%d'`

cd /opt/followcheck/scripts
python3.7 ./delete_checked_tweets.py >> ../log/delete_checked_tweets_$LOG_YMD.log
