#!/bin/sh

. ./enviroments.conf

curl -X $ENDPOINT/followcheck/batch/UpdateUsers?token=$BATCH_TOKEN > /opt/followcheck/log/update_reluser_$LOG_YMD.log
