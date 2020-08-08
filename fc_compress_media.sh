# メディア圧縮処理

LOGFILE_NAME=compress_media_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
python3.7 compress_media.py >> ../log/$LOGFILE_NAME
