#!/bin/sh

# 0. source config
. $localprefix/etc/snmp.conf

# 1. send coldStart on startup
snmptrap -v 2c -c $SNMP_COMMUNITY $SNMP_AGENT "" coldStart \
    .1.3.6.1.2.1.1.1.0 s "`cat /etc/knc-release`"

S_PREV=0
S_DIFF=0
S_POOLS=""
S_ACCEPTED=0

get_field() {
    echo -n $1 | \
        nc localhost 4028 | \
        awk -v RS=\, -F = "/^$2/ {print \$2}"
}

abs() {
    [ $1 -lt 0 ] && echo $((0 - $1)) || echo $1
}

get_pools() {
    echo -n pools |\
        nc localhost 4028 |\
        awk -v RS=\, -F = '
    BEGIN { i=1 }
    /^URL/ {n[i] = i; u[i] = $2; next}
    /Status/ {s[i] = $2; i++}
    END {
            for (i in n) {print ".1.3.6.1.4.1.42398.2.1.1."i" u "n[i]};
            for (i in u) {print ".1.3.6.1.4.1.42398.2.1.2."i" s "u[i]};
            for (i in s) {print ".1.3.6.1.4.1.42398.2.1.3."i" s "s[i]};
        }'
}

# 2. start monitoring
while :; do {
    # get pools
    C_POOLS="`get_pools`"
    [ "$C_POOLS" != "$S_POOLS" ] && {
        snmptrap -v 2c -c $SNMP_COMMUNITY $SNMP_AGENT "" \
            kncMiner.traps.pools-changed $C_POOLS
    }
    S_POOLS="$C_POOLS"

    # get derivative
    C_ACCEPTED="$(echo `get_field summary Difficulty\ Acc` | sed 's/\..*//')"
    # diff between saved and current status
    C_DIFF=`abs $(( $C_ACCEPTED - $S_ACCEPTED ))`

    # yellow level
    YL=$(( $S_DIFF / 100 * 10 ))
    # red level
    RL=$(( $S_DIFF / 100 * 25 ))

    # compare C_DIFF and S_DIFF
    C2_DIFF=`abs $(( $C_DIFF - $S_DIFF ))`

    if [ $C2_DIFF -gt $RL ]; then {
        TRAP=kncMiner.traps.accepted-changed-red
    } elif [ $C2_DIFF -gt $YL ]; then {
        TRAP=kncMiner.traps.accepted-changed-yellow
    } fi

    [ -z "$TRAP" ] || {
        snmptrap -v 2c -c $SNMP_COMMUNITY $SNMP_AGENT "" $TRAP \
            kncMiner.stats.workUtility s `get_field summary Work` \
            kncMiner.stats.acceptedPrev u $S_ACCEPTED \
            kncMiner.stats.acceptedCurrent u $C_ACCEPTED \
            kncMiner.stats.derivativeBase u $S_DIFF \
            kncMiner.stats.derivativeCurrent u $C_DIFF

        S_DIFF=$C_DIFF
        TRAP=""
    }
    S_ACCEPTED=$C_ACCEPTED

    # sleep 10 minutes
    sleep $((60 * 10))

} done
