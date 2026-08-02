#!/bin/bash
# zen_multi 守护脚本:脱离终端 + 崩溃自动重启
LOG=/tmp/zen_multi.log
PIDFILE=/tmp/zen_multi.pid
HOST=127.0.0.1
PORT=8443

start() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "zen_multi already running (pid $(cat "$PIDFILE"))"
        return 0
    fi
    rm -f "$PIDFILE"
    echo "starting zen_multi on $HOST:$PORT -> $LOG"
    nohup setsid bash -c "
        while true; do
            python3 /mnt/d/workplace/tools/zen_multi.py $HOST $PORT >> $LOG 2>&1
            echo \"[\$(date +%FT%T)] zen_multi exited (\$?), restarting in 3s\" >> $LOG
            sleep 3
        done
    " >> /dev/null 2>&1 &
    echo $! > "$PIDFILE"
}

stop() {
    if [ -f "$PIDFILE" ]; then
        pkill -f "zen_multi.py $HOST $PORT" 2>/dev/null
        rm -f "$PIDFILE"
        echo "stopped"
    else
        echo "not running"
    fi
}

status() {
    pgrep -af "zen_multi.py $HOST $PORT" && echo "RUNNING" || echo "DEAD"
    tail -3 "$LOG" 2>/dev/null
}

case "$1" in
    start) start ;;
    stop) stop ;;
    restart) stop; sleep 1; start ;;
    status) status ;;
    *) echo "usage: $0 {start|stop|restart|status}"; exit 1 ;;
esac
