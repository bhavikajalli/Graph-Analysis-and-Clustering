# Graph-Analysis-and-Clustering
The trend analysis of #MeToo event 

The code crawl_metoo.ipynb can be be used to collect tweets of a given hashtag upto 9 days.

The code evaluation.py can be used to evaluate a clustering algorithm. It can find the density, modularity and conductance of the clusters. The code can be used as:

```
python evaluation.py <edge_file> <communities_file>
```
The edge_file is the file containing all the edges in the graph. The nodes in each edge are seperated by a comma.
```
node1,node2
node2,node3
```

The communities_file has all the nodes along with the cluster number that they belong me.
```
node1,1
node2,1
node3,2
```
