# followcheck batch file
# 関連ユーザ情報更新

LOG_YMD=`date '+%Y%m%d'`

cd /opt/followcheck/scripts
python3.7 ./update_reluser.py >> ../log/update_reluser_$LOG_YMD.log
python3.7 ./verify_reluser.py >> ../log/update_reluser_$LOG_YMD.log
python3.7 ./update_profileicon.py >> ../log/update_reluser_$LOG_YMD.log