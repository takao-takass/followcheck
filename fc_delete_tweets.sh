#

LOGFILE_NAME=delete_tweets_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
echo `date '+%Y-%m-%d %H:%M:%S'` start#################### >> ../log/$LOGFILE_NAME
/usr/bin/python3.7 delete_tweets.py >> ../log/$LOGFILE_NAME

