#!/bin/sh

. ./enviroments.conf
echo $ENDPOINT
echo $BATCH_TOKEN
echo $LOG_YMD

curl -X $ENDPOINT/followcheck/batch/UpdateUsers?token=$BATCH_TOKEN > /opt/followcheck/log/update_reluser_$LOG_YMD.log
