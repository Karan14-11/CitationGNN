import networkx as nx
import community
import matplotlib.pyplot as plt
import datetime


#constants
date_path = "../DataSet/cit-HepPh-dates.txt"
cite_path = "../DataSet/Cit-HepPh.txt"
date_need = datetime.datetime.strptime("1993-01-01",'%Y-%m-%d').date
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





G_d,G = init_graph()

nodes = targ_date(date_need)
# print(nodes)


subgraph = G.subgraph(nodes)
isolates = list(nx.isolates(subgraph))
subgraph_copy = subgraph.copy()
subgraph_copy.remove_nodes_from(isolates)



partition = community.best_partition(subgraph_copy)
pos1 = nx.  kamada_kawai_layout(subgraph_copy)
pos2 = nx.  spring_layout(subgraph_copy)

# # cmap = plt.get_cmap('viridis')
node_colors = [partition[node] for node in subgraph_copy.nodes]
node_size = 50
# fig, ax = plt.subplots(figsize=(30, 20))

# nx.draw(subgraph_copy, pos=pos1, node_size=node_size, node_color=node_colors, edge_color=(0, 0, 0),width = 1,ax=ax)

# plt.show()


# nx.draw(subgraph, pos=layout, node_size=node_size, node_color='red', edge_color=(0, 0, 0, 0.7),width = 1,ax=ax)

print(subgraph_copy)

node_colors = [partition[node] for node in subgraph_copy.nodes]
node_size = 50
fig, ax = plt.subplots(figsize=(30, 20))

nx.draw(subgraph_copy, pos=pos2, node_size=node_size, node_color=node_colors, edge_color=(0, 0, 0),width = 1,ax=ax)

# plt.savefig('Louvain.png', format='png', bbox_inches='tight')
plt.show()


























# partition = community.best_partition(G_u)

# # Print the communities
# communities = {}
# for node, community_id in partition.items():
#     if community_id not in communities:
#         communities[community_id] = [node]
#     else:
#         communities[community_id].append(node)

# print("Communities:")
# for community_id, nodes in communities.items():
#     print(f"Community {community_id}: {nodes}")



# colors = [partition[node] for node in G_u.nodes]

# # Draw the graph with node colors
# pos = nx.spring_layout(G_u)  # You can use other layout algorithms
# nx.draw(G, pos, node_color=colors, with_labels=True, cmap=plt.cm.Paired)

# # Display the plot
# plt.show()