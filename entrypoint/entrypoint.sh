#!/bin/bash

S_ADDRESS='0.0.0.0'
PORT='8000'
APP_PATH=/app

start_server(){
    gunicorn -b $S_ADDRESS:$PORT -w 3 --forwarded-allow-ips="*" lote_suinos.wsgi
}

choose_starting_way(){
    echo "Waiting PG..."
    sleep 10
    migrate_data
    local result=$?
    if [ $result -eq 0 ]; then
        start_server
    fi
}

migrate_data(){
    local result=1
    python manage.py migrate && result=0
    return $result
}

main(){
    cd $APP_PATH
    choose_starting_way
    echo "Error!"
    exit 1
}

main


