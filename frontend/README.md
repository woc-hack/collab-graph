### Module description

This module contains all the scripts for data preprocessing required for the frontend, listed in the order of running to get the final graphs:
1. [data_formatting_2](data_formatting_2)
   
   Contains python-2 (to run them on the server) scripts for converting a table to the `.gexf` graph format ([table_to_gexf.py](data_formatting_2/table_to_gexf.py)),
   all the graph structures ([gexf_format.py](data_formatting_2/gexf_format.py), [graph_structures.py](data_formatting_2/graph_structures.py)),
   and a script to filter edges and nodes from `.gexf` graph given their size thresholds ([gexf_to_gexf.py](data_formatting_2/gexf_to_gexf.py))
   

2. [colors](colors.py), [gexf_viz_attributes.py](gexf_viz_attributes.py)

    Since gephi doesn't support the custom gradient palette, we need to put the colors as attributes together with the node sizes.
   So we use [colors](colors.py) to get gradient colors for each node and then add them to the `.gexf` file running [gexf_viz_attributes.py](gexf_viz_attributes.py)
   
4. [data](data)
 
    Contains data, filtered using [gexf_to_gexf.py](data_formatting_2/gexf_to_gexf.py) and colored using [gexf_viz_attributes.py](gexf_viz_attributes.py):
   [for authors graph](data/colored_authors_50_50.gexf.zip) and [for projects graph](data/projects_50_20_colored.gexf.zip)
    

3. [gephi](gephi)
   
   Contains already built graphs in `.gephi` format, so we can modify them later before converting into `.html` pages
   
