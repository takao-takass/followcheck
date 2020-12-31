LOGFILE_NAME=repair_users_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
python3.7 repair_users.py >> ../log/$LOGFILE_NAME
