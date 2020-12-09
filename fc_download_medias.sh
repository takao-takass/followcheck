
LOGFILE_NAME=download_medias_`date '+%Y%m%d'`.log

cd /opt/followcheck/scripts
python3.7 download_medias.py >> ../log/$LOGFILE_NAME
