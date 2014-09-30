#!/bin/bash
while [[ $# > 1 ]]
do
key="$1"
shift

case $key in
    -x|--xmax)
    xm="$1"
    shift
    ;;
    -y|--ymax)
    ym="$1"
    shift
    ;;
esac
done
awk 'BEGIN {var=0}
BEGIN {xmax='$xm';ymax='$ym';}
{if(var!=0){if($2>xmax)print$0;else if($3>ymax)print$0};if(var==0){print$0;var=1}}'
