# High-energy Physics Citation Network Analysis

This repository contains exploratory data analysis, community detection, and link prediction tasks performed on the High-energy Physics (HEP) citation network dataset. The dataset encompasses citations within a collection of academic papers in the field of high-energy physics phenomenology, sourced from the arXiv e-print repository. 

## Dataset
- **Source:** [Stanford SNAP Dataset](http://snap.stanford.edu/data/cit-HepPh.html)
- **Description:** The dataset consists of 34,546 papers with 421,578 directed edges, representing citations between papers within the dataset. It is a temporal dataset, meaning it captures changes in the network structure over time as new papers are published.

## Tasks

### Task 1: Graph Exploration
- **Objective:** Explore the properties of the citation network and observe how they change over time.
- **Properties Analyzed:** 
  - Centrality measures (e.g., degree centrality, betweenness centrality)
  - Density
  - Diameter
  - Assortativity
  - Clustering coefficient
- **Insights:** The analysis reveals patterns in citation behavior, such as influential papers, network density fluctuations, and overall network structure changes over time.

### Task 2: Community Detection
- **Objective:** Identify communities or clusters within the citation network.
- **Algorithms Implemented:**
  - Louvian Method
  - Edge- Centrality Method
- **Analysis:** Communities are detected based on internal connectivity and sparsity between different communities. Insights into why certain papers are grouped together are explored.
- **Temporal Analysis:** The evolution of communities over time is studied, uncovering shifts in research themes and interdisciplinary connections.

### Task 3: Link Prediction (Bonus)
- **Objective:** Predict missing or future connections between nodes in the network.
- **Approaches Implemented:**
  - Graph Neural Network (GNN)
  - Classic Algorithm (e.g., DeepWalk, Node2Vec)
- **Evaluation:** Performance of the models in predicting future connections is assessed, with an emphasis on understanding why GNNs might outperform classic algorithms in this context.

## Repository Structure
- `data/`: Contains the HEP citation network dataset.
- `Task1/`, `Task2/`, `Task3/`: Directories for each task containing code, notebooks, and results.
- `README.md`: Overview of the repository and tasks performed.
- `Report.pdf`: Detailed report documenting methodology, findings, and insights.

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/Karan14-11/CitationGNN.git
   ```
   
## License
This project is licensed under the [MIT License](LICENSE).
