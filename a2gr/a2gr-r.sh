#!/bin/sh

while read line; do
	echo $line;
done >tmp0;

rm nodes edges 2> /dev/null;

for i in $(seq 0 $(($1-1))); do
	cat tmp$i |
	while read line; do
		echo $line |
		sh a2gr.sh;
	done;
	
	cat node | 
	sort | 
	uniq >tmp$(($i+1));
	
	rm node;
done;

cat tmp$1 >nodes;

cat edge | 
awk -F \; '
	{
	if ($1 < $2) 
		print $1";"$2; 
	else 
		print $2";"$1}' | 
sort | 
uniq >edges;

rm edge;

rm tmp*;
