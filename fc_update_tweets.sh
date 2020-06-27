#

LOGFILE_NAME=update_tweets_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
echo `date '+%Y-%m-%d %H:%M:%S'` start#################### >> ../log/$LOGFILE_NAME
python3.7 update_tweets.py >> ../log/$LOGFILE_NAME
