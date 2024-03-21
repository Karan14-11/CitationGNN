import networkx as nx

import matplotlib.pyplot as plt
import datetime


#constants
date_path = "../DataSet/cit-HepPh-dates.txt"
cite_path = "../DataSet/Cit-HepPh.txt"
date_need = datetime.datetime.strptime("1994-01-01",'%Y-%m-%d').date
year_cy = {}
threshold = 0.000001


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






# fx for targeting nodes till line.split() date 

def targ_date(target_date):
    return_nodes = []
    with open(date_path, 'r') as file:

        for line in file:
                if line[0]=='#':
                    continue
                words = line.split()
                idx = 1
                while (words[idx][0]!='1' and words[idx][0]!='2' and idx<len(words)):
                    print(words[idx])
                    idx+=1
                if(idx>=len(words)):
                    continue
                date_str = words[idx]
                current_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

                if current_date <= target_date():
                    y = words[idx][2]+words[idx][3]
                    iterator = year_cy[y]
                    return_nodes.append(int(words[0]))
                else:
                    break

    return return_nodes



# fx for making graph


def init_graph():
    G = nx.DiGraph()
    G_undir = nx.Graph()
    with open (cite_path,'r') as f:
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
        G_undir.add_edge(first,second)
    
    return G,G_undir


# filtered_nodes += [node for node, data in G.nodes(data=True) if 'year' in data and data['year'] <= i]





G_d,G_u= init_graph()

nodes = targ_date(date_need)
# print(nodes)


subgraph = G_u.subgraph(nodes)
isolates = list(nx.isolates(subgraph))
G = subgraph.copy()
G.remove_nodes_from(isolates)



# plt.figure(figsize=(12, 8))
pos_original = nx.kamada_kawai_layout(G)
pos_original_s = nx.spring_layout(G)


connected_components_G = list(nx.connected_components(G))
# for i, component in enumerate(connected_components_G):
#     nx.draw_networkx_nodes(G, pos_original, nodelist=component, node_color=plt.cm.viridis(i / len(connected_components_G)), node_size=300)
# nx.draw_networkx_edges(G, pos_original)


# plt.title('Original Graph')
# plt.show()

# for i, component in enumerate(connected_components_G):
#     nx.draw_networkx_nodes(G, pos_original_s, nodelist=component, node_color=plt.cm.viridis(i / len(connected_components_G)), node_size=300)
# nx.draw_networkx_edges(G, pos_original_s)


# plt.title('Original Graph')
# plt.show()

betweenness_centrality = nx.betweenness_centrality(G)

sorted_nodes = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)


high_betweenness_edges = [(u, v) for u, v in G.edges if betweenness_centrality[u] < threshold and betweenness_centrality[v] < threshold]
G_removed_edges = G.copy()


plt.figure(figsize=(12, 8))
pos_removed_edges = nx.kamada_kawai_layout(G_removed_edges)

connected_components_removed = list(nx.connected_components(G_removed_edges))

for i, component in enumerate(connected_components_removed):
    nx.draw_networkx_nodes(G_removed_edges, pos_removed_edges, nodelist=component, node_color=plt.cm.viridis(i / len(connected_components_removed)), node_size=50)

nx.draw_networkx_edges(G_removed_edges, pos_removed_edges)

plt.title('Graph after Removing High Betweenness Edges - Connected Components Colored')
plt.show()
# plt.savefig('Centrality.png', format='png', bbox_inches='tight')

