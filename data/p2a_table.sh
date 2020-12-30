#!/bin/sh

cut -d \' -f 4 <project_list |
~/lookup/getValues -f p2a |
egrep '<[A-Za-z0-9._%+-]{1,}@[A-Za-z0-9.-]{1,}\.[A-Za-z]{2,}>$' \
> p2a_table \
2> p2a_table.error ;

cut -d \; -f 2 <p2a_table |
sort |
uniq | 
~/lookup/getValues -f a2A |
sort |
uniq \
> a2A_table \
2> a2A_table.error ;

sed -n 's/^no \(.*\) in \/da0_data\/basemaps\/a2AFull.$/\1;\1/p' <a2A_table.error \
>> a2A_table ;

rm a2A_table.error ;

join -1 2 -2 1 -t \; -o 1.1,2.2 <(sort -t \; -k 2 p2a_table) <(sort -t \; -k 1 a2A_table) \
> p2A_table \
2> p2A_table.error

