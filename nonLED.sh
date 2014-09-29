#!/bin/sh
awk 'BEGIN {var=0}
BEGIN {xmax=100;ymax=100;}
{if(var!=0){if($2>xmax)print$0;else if($3>ymax)print$0};if(var==0){print$0;var=1}}'
