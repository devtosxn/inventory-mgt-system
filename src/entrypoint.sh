#!/bin/sh

if [ -z ${LOG_LEVEL} ]; then
export LOG_LEVEL="debug"
fi

if [ -z ${HTTP_PORT} ]; then
export HTTP_PORT=":8000"
fi
if [ -z ${HTTP_WORKERS} ]; then
export HTTP_WORKERS=2
fi

wait_for_mongodb() {
  echo "Waiting for MongoDB..."
  while ! nc -z db 27017; do
    sleep 0.1
  done
}

wait_for_mongodb

export FLASK_APP=app.start:app
echo "Initializing DB..."
flask create-dummy-users
status=$?
if [ $status -eq 0 ]; then
  echo "Starting Gunicorn..."
  gunicorn --workers $HTTP_WORKERS \
           --worker-class=gthread \
           --reload $FLASK_APP \
          -b $HTTP_PORT \
          --timeout 120 \
          --log-level $LOG_LEVEL \
          --log-file=-
else
  echo "Error initializing DB, exiting..."
fi
