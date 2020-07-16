#

LOGFILE_NAME=download_tweets_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
echo `date '+%Y-%m-%d %H:%M:%S'` start#################### >> ../log/$LOGFILE_NAME
python3.7 create_tweets.py >> ../log/$LOGFILE_NAME
#python3.7 update_tweets.py >> ../log/$LOGFILE_NAME
python3.7 download_medias.py >> ../log/$LOGFILE_NAME
python3.7 create_thumbs.py >> ../log/$LOGFILE_NAME
python3.7 create_mvthumbs.py >> ../log/$LOGFILE_NAME