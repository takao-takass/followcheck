#!/bin/sh

. ./enviroments.conf

URL=$ENDPOINT'/followcheck/batch/UpdateUsers?token='$BATCH_TOKEN
LOG=/opt/followcheck/log/update_reluser_$LOG_TIMESTAMP.log

curl -X POST --silent $URL > $LOG
