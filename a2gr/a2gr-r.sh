#!/bin/sh

while read line; do
	echo $line;
done >temp0;

a=$(date +%s);

rm node* edge* 2>/dev/null;

declare -A dnodes

for i in $(seq 0 $(($1-1))); do
	j=0;
	while read line; do
		if [ ! ${dnodes["$line"]} ]; then
                        echo $line |
                        sh a2gr.sh;
			j=$(($j+1));
			dnodes["$line"]=$i;
                fi;
	done <<< "$(cat temp$i)" ;
	if [ $j -eq 0 ]; then
		break;
	fi;
	cat node | 
	sort | 
	uniq >temp$(($i+1));
	
	rm node;
done;

while read line; do
	if [ ! ${dnodes["$line"]} ]; then
		dnodes["$line"]=$1;
	fi;
done <<< "$(find temp* | xargs cat | sort | uniq)" ;

for i in "${!dnodes[@]}" ; do
        echo "${i};${dnodes[$i]}";
done |
sort -t \; -k 2n >nodes;

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

rm temp*;

b=$(date +%s);

echo "Built the files in $(($b - $a)) seconds!";
