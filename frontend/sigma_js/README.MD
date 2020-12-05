#Web visualization
This folder contains some examples of collaboration graphs. 
Basically, there are two types of graphs: 
- with **authors** as nodes, two authors are connected if they have common projects
- with **projects** as nodes, two projects are connected if they have common authors

Graphs of each type are located in the corresponding folder [authors](authors) or [projects](projects).
They also are separated according to their layout (for example, _force-atlas-2_, _yifan-hu_, and so on).

Once you choose the graph you want to see, go to the corresponding folder (it should be named `network`) 
and run `python -m http.server`. Then you should be able to see your graph on http://localhost:8000/ .