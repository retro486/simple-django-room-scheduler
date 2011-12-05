#!/bin/bash
set -e
LOGFILE=/var/log/django-studyrooms.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=nginx
GROUP=nginx
cd /usr/local/studyrooms/django-studyrooms
source ../bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec ../bin/gunicorn_django -w $NUM_WORKERS \
--user=$USER --group=$GROUP --log-level=debug \
--log-file=$LOGFILE --daemon 2>>$LOGFILE