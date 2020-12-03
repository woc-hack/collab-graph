a2gr.sh:  
Reads the authorID from standard input, searchs for other authorIDs associated with the same person (if any), finds the related projects, lists all Authors involved in these projects and outputs two files.

1. **nodes** which contains all the Authors related to the given auhtorID (including the auhtor itself)
2. **edges** which contains the edges in the format: `central Auhtor;related Author`

