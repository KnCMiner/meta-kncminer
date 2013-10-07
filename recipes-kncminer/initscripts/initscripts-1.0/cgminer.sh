#!/bin/sh

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/cgminer
NAME=cgminer
DESC="Cgminer daemon"

set -e

test -x "$DAEMON" || exit 0

do_start() {
	# Stop SPI poller
	spi_ena=0
	i2cset -y 2 0x71 2 $spi_ena

	good_ports=""
	bad_ports=""

	# CLear faults in megadlynx's
	for b in 3 4 5 6 7 8 ; do
		for d in 0 1 2 3 4 5 6 7 ; do
			i2cset -y $b 0x1$d 3 >/dev/null 2>&1 || true
		done
	done

	for p in 0 1 2 3 4 5 ; do
		i2cset -y 2 0x71 1 $((p+1))
		ar="$(spi-test -OHC -D /dev/spidev1.0 0x80,3,0,0,0,0,0,0 | tail -c 13)"
                if [ "x$ar" = "x00 30 A0 01" ] ; then
			good_ports=$good_ports" $p"
		else
			bad_ports=$bad_ports" $p"
		fi
	done

	if [ -n "$good_ports" ] ; then
		for p in $good_ports ; do
			# Re-enable PLL
			i2cset -y 2 0x71 1 $((p+1))
			for c in 0 1 2 3 ; do
				cmd=$(printf "0x84,0x%02X,0,0" $c)
				spi-test -OHC -D /dev/spidev1.0 $cmd >/dev/null
				cmd=$(printf "0x86,0x%02X,0x01,0xD1" $c)
				spi-test -OHC -D /dev/spidev1.0 $cmd >/dev/null
				cmd=$(printf "0x85,0x%02X,0,0" $c)
				spi-test -OHC -D /dev/spidev1.0 $cmd >/dev/null
			done
			
			# re-enable all cores
			i=0
			while [[ $i -lt 192 ]] ; do
				i2cset -y 2 0x2$p $i 1
				i=$((i+1))
			done
			spi_ena=$(( spi_ena | (1 << $p) ))
		done
	fi
	if [ -n "$bad_ports" ] ; then
		for p in $bad_ports ; do
			# Disable PLL
			i2cset -y 2 0x71 1 $((p+1))
			for c in 0 1 2 3 ; do
				cmd=$(printf "0x84,0x%02X,0,0" $c)
				spi-test -OHC -D /dev/spidev1.0 $cmd >/dev/null
			done
			
			# disable all cores
			i=0
			while [[ $i -lt 192 ]] ; do
				i2cset -y 2 0x2$p $i 0
				i=$((i+1))
			done
			spi_ena=$(( spi_ena & ~(1 << $p) ))
		done
	fi

	# Disable direct SPI
	i2cset -y 2 0x71 1 0

	# Enable SPI poller
	i2cset -y 2 0x71 2 $spi_ena

        start-stop-daemon -b -S -x screen -- -S cgminer -t cgminer -m -d "$DAEMON" --default-config /config/cgminer.conf
}

do_stop() {
        killall -9 cgminer || true
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
