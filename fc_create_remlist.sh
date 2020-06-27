# followcheck batch file
# リムられリスト作成

LOGFILE_NAME=create_remlist_`date '+%y%m%d%H%M%S'`.log

cd /opt/followcheck/scripts
python3.7 create_remlist.py > ../log/$LOGFILE_NAME
python3.7 update_remlist.py >> ../log/$LOGFILE_NAME

python3.7 create_unfblist.py >> ../log/$LOGFILE_NAME
python3.7 update_unfblist.py >> ../log/$LOGFILE_NAME

python3.7 create_fleolist.py >> ../log/$LOGFILE_NAME
python3.7 update_fleolist.py >> ../log/$LOGFILE_NAME
