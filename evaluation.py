
# coding: utf-8

# In[1]:
import numpy as np
from numpy import linalg as LA
import sys


# In[2]:


#df = pd.DataFrame
edgeFile = open(sys.argv[1],"r")
edges = edgeFile.readlines()
commFile = open(sys.argv[2],"r")
communities = commFile.readlines()


# In[5]:


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
        components = line.strip().split("\t")
        node = components[0]
        comm = components[1]
        node_comm[node] = comm
        number_comm.append(int(comm))

    number_comm = list(set(number_comm))
    relabbelled_communities = relabel(number_comm)
    n = len(number_comm)

    e = np.zeros((n,n))
    total_edges = 0
    for edge in edges[1:]:
        #print(edge)
        edge1,edge2,weight = edge.strip().split("\t")
        weight = float(weight)
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
            e[i][j] += weight
            e[j][i] += weight
        else:
            e[i][j] += weight
        total_edges +=1
    return e,total_edges,len(set(number_vertices))

##Evaluation Metric- Modularity
def modularity_undirected(e):
    T = np.trace(e)
    #Sum over rows for the term ai
    row_sum = e.sum(axis = 1)
    sum_a = 0
    for row in row_sum:
        sum_a += (row)**2
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


#v is the number of vertices
e,total_edges,v = edgeMatrix(edges,communities)
e_fraction = e/(2 * total_edges)

modularity_e = modularity_undirected(e_fraction)
print("Modularity: ", modularity_e)

density = density_undirected(e,v)
print("Density Undirected: ",density)

#density = density_directed(e,v)
#print("Density Directed: ",density)

external_conductance,intra_cluster,inter_cluster = external_conductance(e)

print("External Conductance: ",external_conductance)
# print("Intra Cluster Conductance: ",intra_cluster)
# print("Inter Cluster Conductance: ",inter_cluster)



