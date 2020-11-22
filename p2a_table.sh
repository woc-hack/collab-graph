#!/bin/sh

cat project_list | 
cut -d \' -f 4 |
~/lookup/getValues -f p2a \
> p2a_table \
2> p2a_table.error ;

cat p2a_table |
cut -d \; -f 2 |
sort |
uniq -c |
sed -n 's/^ *//g ; s/ /\;/p' \
> author_list ;

