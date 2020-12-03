## a2gr.sh

**authorID to graph**

Usage: `echo 'authorID' | sh a2gr.sh`

Reads the authorID from standard input, searchs for other authorIDs associated with the same person (if any), finds the related projects, lists all Authors involved in these projects and outputs two files:

1. **node** which contains all the Authors related to the given auhtorID (including the auhtor itself)
2. **edge** which contains the edges in the format: `central Auhtor;related Author`

## a2gr-r.sh

**authorID to graph - recursive**

Usage: `echo 'authorID' | sh a2gr-r.sh depth`

Reads the authorID from standard input, gets depth as argument and recursively uses a2gr to build a complete graph with the given depth. Depth is defined as the maximum distance between the central node and any given node in the graph. That means if for example we set the depth to 2, we will have all the nodes with distance 1 or 2 from the central node and subsequently all the edges between these nodes. Output files are as follows:

1. **nodes** which contains all the Authors connected to the central Author within the given depth
2. **edges** which contains the edges between all nodes
