#!/bin/sh

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/cgminer
NAME=cgminer
DESC="Cgminer daemon"

set -e

#if [ -r /boot/miner.conf ] ; then
#    . /boot/miner.conf
#else
#    exit 0
#fi
test -x "$DAEMON" || exit 0

do_start() {
        start-stop-daemon -b -S -x screen -- -S cgminer -t cgminer -m -d "$DAEMON" --default-config /boot/cgminer.conf
}

do_stop() {
        killall -9 cgminer
}
case "$1" in
  start)
        echo -n "Starting $DESC: "
	do_start
        echo "$NAME."
        ;;
  stop)
        echo -n "Stopping $DESC: "
	do_stop
        echo "$NAME."
        ;;
  restart|force-reload)
        echo -n "Restarting $DESC: "
        do_stop
        do_start
        echo "$NAME."
        ;;
  *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|force-reload}" >&2
        exit 1
        ;;
esac

exit 0
