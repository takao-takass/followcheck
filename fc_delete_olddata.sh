# followcheck batch file
# 関連ユーザ情報更新

LOG_YMD=`date '+%Y%m%d'`

cd /opt/followcheck/scripts
/usr/local/bin/python3.7 ./delete_olddata.py >> ../log/delete_olddata_$LOG_YMD.log
