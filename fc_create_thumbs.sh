# サムネイル作成処理

LOGFILE_NAME=create_thumbnail_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
python3.7 create_thumbnail.py >> ../log/$LOGFILE_NAME
