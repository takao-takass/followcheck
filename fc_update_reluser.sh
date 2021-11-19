# followcheck batch file
# 関連ユーザ情報更新

LOG_YMD=`date '+%Y%m%d_%H%M%S'`

curl -X https://takas-service.webhop.net:10082/followcheck/batch/UpdateUsers?token=folloWcheck_BatCh_01092123 > /opt/followcheck/log/update_reluser_$LOG_YMD.log

#cd /opt/followcheck/scripts
#python3.7 ./update_reluser.py >> ../log/update_reluser_$LOG_YMD.log
#python3.7 ./verify_reluser.py >> ../log/update_reluser_$LOG_YMD.log
#python3.7 ./update_profileicon.py >> ../log/update_reluser_$LOG_YMD.log