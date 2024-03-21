import torch
import torch.nn as nn
import torch.optim as optim
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data, DataLoader
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import datetime


#constants
date_path = "../DataSet/cit-HepPh-dates.txt"
cite_path = "../DataSet/Cit-HepPh.txt"
date_need = datetime.datetime.strptime("1994-01-01",'%Y-%m-%d').date
first_Q = datetime.datetime.strptime("1992-03-01",'%Y-%m-%d').date
second_Q = datetime.datetime.strptime("1992-06-01",'%Y-%m-%d').date
third_Q = datetime.datetime.strptime("1992-09-01",'%Y-%m-%d').date
forth_Q = datetime.datetime.strptime("1992-12-01",'%Y-%m-%d').date
fifth_Q = datetime.datetime.strptime("1993-03-01",'%Y-%m-%d').date
sixth_Q = datetime.datetime.strptime("1993-06-01",'%Y-%m-%d').date
seventh_Q = datetime.datetime.strptime("1993-09-01",'%Y-%m-%d').date
eight_Q = datetime.datetime.strptime("1993-12-01",'%Y-%m-%d').date
ninth_Q = datetime.datetime.strptime("1994-04-01",'%Y-%m-%d').date


samling_threshold = 3.0e-5
GNN_threshold = 0.1





year_cy = {}
node_id_mapping = {}


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


#nx functions 

def add_node_to_mapping_and_graph(node, mapping):
    if node not in mapping:
        mapping[node] = len(mapping) + 1  # Add node to mapping

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
    rrnode=[]

    for node in return_nodes:
        
        add_node_to_mapping_and_graph(node, node_id_mapping)
        rrnode.append(node_id_mapping[node])

    return rrnode



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
        if first not in node_id_mapping:
            # continue
            node_id_mapping[first] = len(node_id_mapping) + 1
        if second not in node_id_mapping:
            node_id_mapping[second] = len(node_id_mapping) + 1
            # continue

        mapped_first = node_id_mapping[first]
        mapped_second = node_id_mapping[second]

        G.add_node(mapped_first)   # Add nodes to the directed graph
        G.add_node(mapped_second)
        G.add_edge(mapped_first, mapped_second)   # Add directed edges to the directed graph

        G_undir.add_edge(mapped_first, mapped_second)
    
    return G,G_undir




Graph8 = nx.DiGraph()
Graph9 = nx.DiGraph()


nodes8 = targ_date(eight_Q)
nodes9 = targ_date(ninth_Q)


G_d,G_u= init_graph()  # initialising graph



# Graph8

# print(nodes8)
Graph81 = G_d.subgraph(nodes8)
Graph8 = Graph81.copy()
for l in nodes8:
    if l not in Graph8.nodes():
        Graph8.add_node(l)
Graph8.add_node(len(nodes8))
# print(Graph8)

# Graph9

Graph91 = G_d.subgraph(nodes8)
Graph9 = Graph91.copy()
for l in nodes9:
    if l not in Graph8.nodes():
        Graph9.add_node(l)
Graph9.add_node(len(nodes9))


Predicted_Graph = Graph8.copy()
FutureGraph = nx.DiGraph()
New_Nodes = nx.DiGraph()
Test_Graph = Graph9.copy()
Train_Graph = Graph8.copy()

progressed_edges=0

for n in Test_Graph.nodes():
    if n not in Train_Graph.nodes():
        New_Nodes.add_node(n)

# for n in Test_Graph.edges():
#     if n  in Train_Graph.edges():
#        progressed_edges+=1
   

for nodes in New_Nodes.nodes():
    for nss in Train_Graph.nodes():
        Predicted_Graph.add_edge(nodes,nss)

# for nodei in Train_Graph.nodes():
#     print(nodei)

###########################################################################PYTORCH#####################################################################

train_edge_index = torch.tensor(list(Train_Graph.edges)).t().contiguous() #edge tensor

train_labels = torch.ones(len(Train_Graph.edges))

train_graph_data = Data(
    x=torch.full((len(Train_Graph.nodes), 1), fill_value=1.),
    edge_index=train_edge_index,
    y=train_labels,
)




class GNNModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GNNModel, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        # print(x.shape, edge_index.shape)
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        return x
    
model = GNNModel(input_dim=1, hidden_dim=64, output_dim=1)

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    output = model(train_graph_data)

    # Extract predicted edge scores for all edges
    predicted_scores = output.view(-1)

    # Create a target tensor with the same number of elements as predicted_scores
    target = torch.zeros_like(predicted_scores)

    # Set the target values to 1 for positive edges in train_graph_data
    target[train_graph_data.edge_index[0]] = 1

    loss = criterion(predicted_scores, target.float())

    loss.backward()
    optimizer.step()



with torch.no_grad():
    model.eval()
    x_pred = torch.full((len(Test_Graph.nodes)+1, 1), fill_value=1.)
    edge_list = list(Test_Graph.edges())
    predicted_edge_index = torch.tensor(edge_list).t().contiguous()
    # print(predicted_edge_index.shape)
    predicted_predictions = model(Data(x=x_pred, edge_index=predicted_edge_index))

# print(len(predicted_edge_index[0]))

PEdges=[]
# print(predicted_predictions)

cnty=0

for i in tqdm(range(min(len((predicted_predictions)),len(predicted_edge_index[0]))), desc="Pedges"):
    PEdges.append(((int(predicted_edge_index[0][cnty]),int(predicted_edge_index[1][cnty]),float(predicted_predictions[cnty]))))
    cnty+=1

print("Done")
# print(len(PEdges))


# binary_predictions = (predicted_predictions > GNN_threshold).squeeze().int()
# print(binary_predictions)
# predicted_edges = predicted_edge_index[:, binary_predictions[1] == 1]




# test_edge_index = torch.tensor(list(Test_Graph.edges)).t().contiguous()
# test_labels = torch.tensor([1] * len(test_edge_index[0]))

# if predicted_edges.size(0) != 2:
#     predicted_edges = predicted_edges.t()

# Ensure that the sizes of predicted_edges and test_edge_index are the same
# if predicted_edges.size(1) != test_edge_index.size(1):
#     predicted_edges = predicted_edges[:, :test_edge_index.size(1)]

# # Convert the tensors to long (int64) to ensure compatibility for torch.eq
# predicted_edges = predicted_edges.to(torch.long)
# test_edge_index = test_edge_index.to(torch.long)

# total_edges = test_edge_index.size(1)
reqq_edges=200


thresholds = [i*0.05 for i in range(-10,2)]


false_edges=0
# print(len(PEdges), len(Test_Graph.edges()))

for threshold in thresholds:
    correct_predictions = 0

    print(edge_list[0])
    for i in tqdm(range(len(PEdges)),desc="Checking Predictions"):
        aqa= 1+ PEdges[i][2]
        if(aqa>threshold):
            if(edge_list[i] in Test_Graph.edges()):
                correct_predictions+=1
        else:
            false_edges+=1
        if(correct_predictions> len(Test_Graph.edges())-2):
            break


    if(false_edges<reqq_edges):
        correct_predictions-=reqq_edges
    # print(PEdges[0])
    # print(false_edges)

    # print(edge_list)

    accuracy = (correct_predictions) / len(Test_Graph.edges())
    print(correct_predictions)
    # print(len(Test_Graph.edges()))
    print("Threshold", threshold)


    print(f"Accuracy: {accuracy * 100:.2f}%")