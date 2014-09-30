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
    -t|--threshold)
    th="$1"
    shift
    ;;
esac
done

awk 'BEGIN {var=0}
BEGIN {xmax='$xm';ymax='$ym';threshold='$th'}
{if($2<=xmax)if($3<=ymax)hits[$9]++;}
END {for (i in hits) {
    if(hits[i]>threshold) print i;
    }
}'|sort
