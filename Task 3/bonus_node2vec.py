import networkx as nx
import matplotlib.pyplot as plt
import datetime
from node2vec import Node2Vec 
import numpy as np
from tqdm import tqdm
import logging


import sys



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
threshold1 = 0.1



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


thresholds = [i*0.05 for i in range(21)]

for threshold in thresholds:


    G_d,G_u= init_graph()  # initialising graph

    # nodes1 = targ_date(first_Q)
    # nodes2 = targ_date(second_Q)
    # nodes3 = targ_date(third_Q)
    # nodes4 = targ_date(forth_Q)
    # nodes5 = targ_date(fifth_Q)
    # nodes6 = targ_date(sixth_Q)
    # nodes7 = targ_date(seventh_Q)
    nodes8 = targ_date(eight_Q)
    nodes9 = targ_date(ninth_Q)

    # Graph1 = G_d.subgraph(nodes1)
    # Graph2 = G_d.subgraph(nodes2)
    # Graph3 = G_d.subgraph(nodes3)
    # Graph4 = G_d.subgraph(nodes4)
    # Graph5 = G_d.subgraph(nodes5)
    # Graph6 = G_d.subgraph(nodes6)
    # Graph7 = G_d.subgraph(nodes7)
    Graph8 = G_d.subgraph(nodes8)
    Graph9 = G_d.subgraph(nodes9)

    Predicted_Graph = Graph8.copy()
    FutureGraph = nx.DiGraph()
    not__FutureGraph = nx.DiGraph()
    New_Nodes = nx.DiGraph()
    Test_Graph = Graph9.copy()
    Train_Graph = Graph8.copy()

    cnty=0
    for n in Test_Graph.nodes():
        if n not in Train_Graph.nodes():
            cnty+=1
            Train_Graph.add_node(n)
            New_Nodes.add_node(n)

    # print(cnty)

    node2vec = Node2Vec(Train_Graph, dimensions=32, walk_length=15, num_walks=100, workers=4, p= 1,q=1)

    model = node2vec.fit(window=10, min_count=1, seed=0)

    cnt1 = 0
    cnt2=0
    cnt3 =0

    logging.getLogger('node2vec').setLevel(logging.ERROR)

    for node1 in tqdm(New_Nodes.nodes(), desc="k"):
        



        for  node2 in Predicted_Graph.nodes():
            cnt1 += 1
            if True:
                node1_embedding = model.wv[str(node1)]
                node2_embedding = model.wv[str(node2)]
                cnt2+=1

                similarity_score = np.dot(node1_embedding, node2_embedding) / (
                    np.linalg.norm(node1_embedding) * np.linalg.norm(node2_embedding)
                )
                if similarity_score > threshold:
                    FutureGraph.add_edge(node1, node2)
                    Train_Graph.add_edge(node1, node2)
                    cnt3+=1
                elif similarity_score>threshold1:
                    not__FutureGraph.add_edge(node1,node2)
                    

    # print( cnt1,cnt2,cnt3)
    print("Predicted Edges for FutureGraph:", len(list(FutureGraph.edges())))

    TruePositive = 0
    TrueNegative = 0
    FalsePositive = 0
    FalseNegative = 0 



    for edge in FutureGraph.edges():
        if edge in Test_Graph.edges():
            TruePositive+=1
            
        else:

            TrueNegative+=1
        

    for edge in not__FutureGraph.edges():
        if edge not in Test_Graph.edges():
            FalsePositive+=1
        else:
            FalseNegative+=1


    edges_a = set(FutureGraph.edges())
    # print(edges_a)

    edges_b = set(Test_Graph.edges())
    # print(edges_b)
    common_edges = edges_a.intersection(edges_b)

    total = TruePositive+TrueNegative+FalseNegative+FalsePositive
    correct1 = TruePositive 
    correct =FalsePositive +  TruePositive
    total1 = TruePositive+TrueNegative

    print("threshold::",threshold)
    if(TruePositive>20):
        print((correct/total)*100)
        # print("ll")
    elif(TruePositive):
        print((correct1/total1)*100)
    else:
        print(correct1)
    # print((correct1/total1)*100)



















