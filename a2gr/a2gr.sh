#!/bin/sh

while read line; do
	corenode=$(echo "$line" | \
		~/lookup/getValues -f a2A | \
		cut -d \; -f 2 | \
		sort| \
		uniq)
done 2>tmp.error ;

if [[ $corenode == "" ]]; then
	corenode=$(cat tmp.error | \
		sed -n 's/^no \(.*\) in.*$/\1/p');
	echo $corenode >tmp2;
else
	echo $corenode |
	~/lookup/getValues A2a |
	sed -n 's/\;/\n/gp' |
	sort |
	uniq > tmp2;
fi;

cat tmp2 |
~/lookup/getValues -f a2p |
cut -d \; -f 2 |
sort | 
uniq | 
~/lookup/getValues -f p2a |
cut -d \; -f 2 | 
sort | 
uniq | 
~/lookup/getValues -f a2A >tmp3 2>tmp3.error;

cat tmp3 |
cut -d \; -f 2 |
sort |
uniq >nodes ;

cat tmp3.error |
sed -n 's/^no \(.*\) in.*$/\1/p' >>nodes;

rm tmp*;

cat nodes |
while read line; do
	echo "$corenode;$line"
done >edges;
