LOGFILE_NAME=exists_media_file_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
python3.7 exists_media_file.py >> ../log/$LOGFILE_NAME
