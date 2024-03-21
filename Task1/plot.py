import matplotlib.pyplot as plt

# Data for Katz centrality values of node 9203203 across different iterations
iterations = [1, 2, 3, 4, 5]
katz_centrality_values = [0.08485118089364314, 0.12713256004417597, 0.1322978506833075, 0.1301474209410297, 0.1322978506833075]

# Plotting the line graph
plt.plot(iterations, katz_centrality_values, marker='o', linestyle='-')

# Adding labels and title
plt.xlabel('Graph Iteration')
plt.ylabel('Katz Centrality for Node 9203203')
plt.title('Evolution of Katz Centrality for Node 9203203')

# Displaying the graph
plt.show()
