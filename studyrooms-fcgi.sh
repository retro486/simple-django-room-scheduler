#!/bin/bash
. /usr/local/studyrooms/bin/activate
/usr/local/studyrooms/bin/python /usr/local/studyrooms/django-studyrooms/manage.py runfcgi method=threaded host=127.0.0.1 port=8800 pidfile=/var/run/studyrooms-django.pid
