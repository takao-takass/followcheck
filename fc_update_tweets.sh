#

LOGFILE_NAME=update_tweets_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
echo `date '+%Y-%m-%d %H:%M:%S'` start#################### >> ../log/$LOGFILE_NAME
/usr/bin/python3.7 update_tweets.py >> ../log/$LOGFILE_NAME
#/usr/bin/python3.7 download_medias.py >> ./log/$LOGFILE_NAME

