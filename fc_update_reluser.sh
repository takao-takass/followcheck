#!/bin/sh

. ./enviroments.conf
echo $ENDPOINT
echo $BATCH_TOKEN
echo $LOG_TIMESTAMP

URL=`$ENDPOINT'/followcheck/batch/UpdateUsers?token='$BATCH_TOKEN`
LOG=`/opt/followcheck/log/update_reluser_$LOG_TIMESTAMP.log`
echo $URL
echo $LOG

curl -X POST $URL > $LOG
