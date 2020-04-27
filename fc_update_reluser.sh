# followcheck batch file
# 関連ユーザ情報更新

LOG_YMD=`date '+%Y%m%d'`

cd /opt/followcheck
/usr/local/bin/python3.7 ./update_reluser.py >> ./log/update_reluser_$LOG_YMD.log
