# 古いツイートを削除する

LOGFILE_NAME=delete_oldtweet_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
python3.7 select_oldtweet.py >> ../log/$LOGFILE_NAME
python3.7 delete_oldtweet.py >> ../log/$LOGFILE_NAME
