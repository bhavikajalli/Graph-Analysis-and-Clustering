# Graph-Analysis-and-Clustering
The trend analysis of #MeToo event 

### Crawl the #MeToo data
We have crawled data from Twitter with the #MeToo from February 25th to May 31st from Twitter. The code crawl_metoo.ipynb can be be used to collect tweets of a given hashtag upto 9 days. As the first step an application needs to be submitted with Twitter at https://apps.twitter.com/. Then please install the Tweepy API with
```
pip install tweepy==3.3.0
```
The code can be used with the command below. 
```
python data_utils/crawl_metoo.py --hashtag #MeToo --since 2018-03-10 --until 2018-03-19 --outputFile metoo_rawTweets.txt
```
If you need the data that we have already crawled, please send me a message.

### Pre Process the Crawled Data

The code data_preprocess.py takes in the txt file created by crawling and preprocesses each tweet entry. The file can be used to pre processing as follows. The file requires NLTK to be installed and also stopwords downloaded from nltk.corpus.
```
python data_utils/data_preprocess.py --input metoo_rawTweets.txt --output metoo_processedTweets.txt
```
The output is stored in a corresponding file. An example of the final output looks like:
```
name,tweet,retweet,mentions,hashtags,retweet_count,replied_to,location
stewartdarkin,ok advertise torturing killing,ColetteDA,ColetteDA-GooglePlay-EverydaySexism,women-angry-upset-trauma-feminism-metoo,6,None,Manchester
```
### Creating the Mentions, Re-Tweet and the Similarity Graphs

### Detecting the Communities in the graphs


### Evaluating the Methodologies using Modularity and Conductance

The code evaluation.py can be used to evaluate a clustering algorithm. It can find the density, modularity and conductance of the clusters. The code can be used as:

```
python evaluation.py <edge_file> <communities_file>
```
The edge_file is the file containing all the edges in the graph. The nodes in each edge are seperated by a comma. If the graph is unweighted, the weight is given as 1.
```
node1,node2,weight
node2,node3,weight
```

The communities_file has all the nodes along with the cluster number that they belong me.
```
node1,1
node2,1
node3,2
```
