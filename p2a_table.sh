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

cat author_list | 
cut -d \; -f 2 | 
~/lookup/getValues -f a2A \
> a2A_table \
2> a2A_table.error ;

cat a2A_table |
cut -d \; -f 2 |
sort |
uniq \
> Author_list ;

