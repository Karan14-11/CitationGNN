# Task 2
Community detection or clustering is an important analysis for graphs. In
the study of complex networks, a network is said to have community structure if
the nodes of the network can be easily grouped into disjoint sets of nodes such
that each set of nodes is densely connected internally, and sparsely between
different communities. In this task, you are required to perform community
detection on the graph. This is a well studied problem, and various static
algorithms as well as machine learning methods exist for community detection.
You are required to:
1. Implement any two algorithms/ ML methods for community detection on
the graph at any time T
2. Analyze the communities (Can you build an understanding of why the
algorithm chose the communities it did?)
3. Perform temporal community detection, through which you can study how
communities evolve over time as new papers are added. Report
interesting insights using various plots and metrics

## Folder Structure

- **task2_L.py:** The  code for the task2, responsible for communit building using Louvain Method.
- **Phase/{1-5}:** Contains 5 images generated using `task2_L.py` showcasing the evolution of the graph and temporal community buliding.
- **animation.py:** A script that, when run, displays an animation of the graph evolution using the images.
- **Centerality.png:** Image generated using `task2_C.py` for showcasing community building using Edge-Centraliy
- **report_task2.pdf:** The detailed report on Task 2, including insights, analyses, and visualizations.