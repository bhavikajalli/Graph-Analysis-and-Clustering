#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 14:41:06 2018

@author: BhavikaJalli
"""

import pandas as pd
import numpy as np
import sys


def relabel(number_comm):
    number_comm.sort()
    i = 0
    comm_dict = {}
    for number in number_comm:
        comm_dict[number] = i
        i+= 1
    return comm_dict     

def edgeMatrix(edges,communities):
    node_comm = {}
    number_comm = []
    number_vertices = []

    for line in communities[1:]:
        node,comm = line.strip().split(",")
        node_comm[node] = comm
        number_comm.append(int(comm))

    number_comm = list(set(number_comm))
    relabbelled_communities = relabel(number_comm)
    n = len(number_comm)

    e = np.zeros((n,n))
    total_edges = 0
    for edge in edges[1:]:
        #print(edge)
        edge1,edge2 = edge.strip().split(",")
        number_vertices.append(edge1)
        number_vertices.append(edge2)
        try:    
            comm1 = int(node_comm[edge1])
            comm2 = int(node_comm[edge2])
        except KeyError:
            continue

        i = relabbelled_communities[comm1]
        j = relabbelled_communities[comm2]
        #print(i,j)
        if i != j:
            e[i][j] +=1
            e[j][i] +=1
        else:
            e[i][j] += 1
        total_edges +=1
    return e,total_edges,len(set(number_vertices))

##Evaluation Metric- Modularity
def modularity(e):
    T = np.trace(e)
    square = np.square(e)
    Q = T - sum(sum(square)) 
    return Q
 
##Evaluation Metric- Density

def density_undirected(e,number_vertices):
    possible_edges = (number_vertices * (number_vertices - 1))/ 2
    e = e/possible_edges
    num_comm = e.shape[0]
    density = np.trace(e) / num_comm
    return density

def density_directed(e,number_vertices):
    possible_edges = (number_vertices * (number_vertices - 1))
    e = e/possible_edges
    num_comm = e.shape[0]
    density = np.trace(e) / num_comm
    return density

##Evaluation Metric- Conductance
# the fraction of edges that point outside the community. Averaged for all communities
def external_conductance(e):
    conductance = 0 
    col = e.shape[0]
    col_sum = e.sum(axis = 0)
    ci = []
    for i in range(col):
        a_cihat = sum(col_sum) - col_sum[i]
        cluster_conductance = (col_sum[i] - e[i][i])/min(col_sum[i],a_cihat)
        ci.append(cluster_conductance)
        conductance += cluster_conductance
        
    return conductance/col,min(ci),(1-max(ci))


edgeFile = open(sys.argv[1],"r")
edges = edgeFile.readlines()
commFile = open(sys.argv[2],"r")
communities = commFile.readlines()


#v is the number of vertices
e,total_edges,v = edgeMatrix(edges,communities)
e_fraction = e/total_edges

modularity = modularity(e_fraction)
print("Modularity: ", modularity)


density = density_directed(e,v)
print("Density: ",density)

external_conductance,intra_cluster,inter_cluster = external_conductance(e)

print("External Conductance: ",external_conductance)
print("Intra Cluster Conductance: ",intra_cluster)
print("Inter Cluster Conductance: ",inter_cluster)    
    

