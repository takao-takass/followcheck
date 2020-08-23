# 古いツイートを削除する

LOGFILE_NAME=delete_oldtweet_`date '+%Y%m%d'`.log

MAX_THREAD_NUM=1
MAX_DELETE_ROWS=2000

cd /opt/followcheck/scripts
python3.7 select_oldtweet.py $MAX_THREAD_NUM >> ../log/$LOGFILE_NAME
python3.7 delete_oldtweet.py $MAX_THREAD_NUM $MAX_DELETE_ROWS >> ../log/$LOGFILE_NAME
