LOGFILE_NAME=download_tweets_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
echo `date '+%Y-%m-%d %H:%M:%S'` start#################### >> ../log/$LOGFILE_NAME
python3.7 create_tweets.py >> ../log/$LOGFILE_NAME