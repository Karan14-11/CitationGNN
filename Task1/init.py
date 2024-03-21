import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm


def make_dubgraph():
    parts = [1,2,3,4,5,6,7,8,9,10,11]
    farts =[1,2]
    filtered_nodes=[]

    fig_cnt="1"
    g_cnt=1

    for i in tqdm(farts, desc ="cycles iterated"):
        filtered_nodes += [node for node, data in G.nodes(data=True) if 'year' in data and data['year'] <= i]
        print(filtered_nodes)
        subgraph = G.subgraph(filtered_nodes)
        print(subgraph)
    
        fig, ax = plt.subplots(figsize=(30, 20))

        num_nodes = subgraph.number_of_nodes()
        num_edges = subgraph.number_of_edges()
        avg_degree = sum(dict(subgraph.degree()).values()) / num_nodes
        print("Average Node Degree:", avg_degree)
        density = nx.density(subgraph)
        print("Density:", density)
        clustering_coefficient = nx.average_clustering(subgraph)
        print("Clustering Coefficient:", clustering_coefficient)
        assortativity_coefficient = nx.degree_assortativity_coefficient(subgraph)
        print("Assortativity Coefficient:", assortativity_coefficient)
        
        strongly_connected_components = nx.number_strongly_connected_components(subgraph)
        print("Number of Strongly Connected Components in subgraph:", strongly_connected_components)


        pagerank_centrality = nx.pagerank(subgraph)
        # print("PageRank Centrality in subgraph:", pagerank_centrality)


        top_10_nodes = sorted(pagerank_centrality, key=pagerank_centrality.get, reverse=True)[:5]

        # Print the top 10 nodes and their PageRank scores
        for node in top_10_nodes:
            print(f"Node {node}: PageRank Centrality = {pagerank_centrality[node]}")

        # Katz Centrality
        katz_centrality = nx.katz_centrality(subgraph)
        top_10_nodes_katz = sorted(katz_centrality, key=katz_centrality.get, reverse=True)[:5]

        # Print the top 10 nodes and their Katz Centrality scores
        for node in top_10_nodes_katz:
            print(f"Node {node}: Katz Centrality = {katz_centrality[node]}")


        node_size = 30  
        edge_color = 'white'  
        node_colors = ['blue' if node not in G.nodes or subgraph.degree(node) == 0 else 'red' for node in subgraph.nodes]
        layout = nx.spring_layout(subgraph)

        nx.draw(subgraph, pos=layout, node_size=node_size, node_color=node_colors, edge_color=(0, 0, 0, 0.7),width = 1,ax=ax)
        
        plt.gca().set_facecolor('black')
        plt.savefig('graph_plot'+fig_cnt+'.png', format='png', bbox_inches='tight')
        g_cnt+=1
        fig_cnt = str(g_cnt)
        print("\n\n\n")




G = nx.DiGraph()   # main graph
G_u = nx.Graph()

citespath = "../DataSet/Cit-HepPh.txt"

with open (citespath,'r') as f:
    edges_inp = f.readlines()

for e_inp in edges_inp:

    if(e_inp[0]=='#'):
        continue
    a = e_inp.split()
    first = int(a[0])
    second = int(a[1])
    G.add_node(first)
    G.add_node(second)
    G.add_edge(first,second)       # see this which makes more sense 
    G_u.add_edge(first,second)

datespath = "../DataSet/cit-HepPh-dates.txt"

with open (datespath,'r') as file:
    lines = file.readlines()

year_cy = {}

year_cy["92"]=1
year_cy["93"]=2
year_cy["94"]=3
year_cy["95"]=4
year_cy["96"]=5
year_cy["97"]=6
year_cy["98"]=7
year_cy["99"]=8
year_cy["00"]=9
year_cy["01"]=10
year_cy["02"]=11


for line in lines:
    if(line[0]=='#'):
        continue
    words = line.split()
    idx = 1
    flag_br=0
    while (words[idx][0]!='1' and words[idx][0]!='2' and idx<len(words)):
        print(words[idx])
        idx+=1
    if(idx>=len(words)):
        flag_br=1
        continue
    y = words[idx][2]+words[idx][3]
    iterator = year_cy[y]
    node_id = int(words[0])
    if node_id in G.nodes():
        G.add_node(node_id, year=iterator)









make_dubgraph()











# print(G)




