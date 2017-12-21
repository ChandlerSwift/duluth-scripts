#!/bin/bash
sleep 50
result=$(wget -qO - "http://freedns.afraid.org/dynamic/update.php?$(cat -n $(dirname $0)/secrets/freedns.txt)")
[[ $result == ERROR* ]] || echo $result
