#!/bin/sh
awk 'BEGIN {var=0}
BEGIN {xmax=25;ymax=16;threshold=20}
{if($2<=xmax)if($3<=ymax)hits[$9]++;}
END {for (i in hits) {
    if(hits[i]>threshold) print i;
    }
}'
