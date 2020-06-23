# followcheck batch file
# 関連ユーザ情報更新

LOG_YMD=`date '+%Y%m%d'`

cd /opt/followcheck/scripts
/usr/bin/python3.7 ./update_reluser.py >> ../log/update_reluser_$LOG_YMD.log
/usr/bin/python3.7 ./update_profileicon.py >> ../log/update_reluser_$LOG_YMD.log