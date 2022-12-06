#!/bin/bash
#
# Dacă ați configurat avahi pentru mdns, this should work...
#
# Avahi este setat corect, insa pe local unde testez, pare sa sufere considerabil
# si la anumite request-uri HTTP nu poate sa faca resolution. Daca testele nu 
# ruleaza cum trebuie din cauza aceasta, poti verifica cu un ping sau SSH.

# In speta, am adaugat la curl un --retry 5 pentru a nu ajunge in acest caz.

# student@labsi-vm:~/yocto$ ping tema2.local
# PING tema2.local.localdomain (192.168.150.173) 56(84) bytes of data.
# 64 bytes from 192.168.150.173 (192.168.150.173): icmp_seq=1 ttl=64 time=1.41 ms
# 64 bytes from 192.168.150.173 (192.168.150.173): icmp_seq=2 ttl=64 time=1.49 ms
# 64 bytes from 192.168.150.173 (192.168.150.173): icmp_seq=3 ttl=64 time=0.506 ms


HOSTNAME=tema2.local:5000

ecurl()
{
    curl --retry 5 -H "Content-Type: application/json" "$@"
}

submarine_move()
{
    echo "POST /api/submarine/move '$1'"
    ecurl -X POST -d "$1" http://$HOSTNAME/api/submarine/move
    sleep 2
}

add_fish()
{
    echo "POST /api/fish/add '$1'"
    ecurl -X POST -d "$1" http://$HOSTNAME/api/fish/add
    sleep 2
}

update_artifact()
{
    echo "POST /api/artifact/update '$1'"
    ecurl -X POST -d "$1" http://$HOSTNAME/api/artifact/update
    sleep 2
}

echo "GET /api/submarine"
ecurl http://$HOSTNAME/api/submarine
sleep 2

for i in $(seq 1 5); do
    submarine_move '{"x": -3, "y": -2}'
done

add_fish '{"x": 1, "y": 2}'
add_fish '{"x": 15, "y": 13}'
add_fish '{"x": 20, "y": 44}'
add_fish '{"x": 45, "y": 25}'
add_fish '{"x": 60, "y": 32}'
add_fish '{"x": 33, "y": 43}'
add_fish '{"x": 38, "y": 23}'

update_artifact '{"x": 70, "y": 24}'

for i in $(seq 1 5); do
    submarine_move '{"x": -4, "y": 0}'
done

update_artifact '{}'
update_artifact '{"x": 60, "y": 15}'
