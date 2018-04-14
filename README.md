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
The processed data from twitter was used to create three types of graphs. The Mentions graph is created between users if either of them had mentioned the other in their tweets. The Re-tweet graph is created between users if either of them had re-tweeted the other. The edge is weighted by the number of mentions or re-tweets between the set of users. 
The similarity graph was created by first representing the tweets in a vector-space model using LDA and then calculating co-sine similarity between them. The cosine similarity is thresholded at 0.7 and is taken as the edge weight.
Please ensure that the scikit-learn library is installed
```
python creategraph.py metoo_processedTweets.txt --graphtype mention --output mentionGraph.txt

python creategraph.py metoo_processedTweets.txt --graphtype retweet --output retweetGraph.txt

python creategraph.py metoo_processedTweets.txt --graphtype similarity --output similarityGraph.txt
```
### Detecting the Communities in the graphs
The project uses three clustering methodologies to detect communities in the above graphs. Label Propagation Algorithm(LPA), Louvian Modularity(LM) and InfoMap. The python file detectcommunities.py contains the code to detect the communities i=using LPA and LM.
The code takes in a graph and an argument for the chosen model and gives the detected communities as a txt file with the node and the community that the node belongs to in a tab seperated format.
```
python detectcommunities.py mentiongraph.txt --model LPA --output LPA.txt

python detectcommunities.py mentiongraph.txt --model LM --output LM.txt
```
### Sentiment Analysis 
The trend of the sentiment of tweets with #MeToo over a period of time can be calculated using the TextBlob package from NLTK. This can be done using the command
```
python3 sentiment_analysis/sentiment_analysis.py edges_similarity.clu tweets_graph.txt
```
where edges_similarity.clu is the output file from the InfoMap community detection algorithm on the similarity based graph. It consists of an Id and its corresponding community. The Id here represents the tweet which is specified in the tweets_graph.txt file. The output of this command will be a file with the community, tweet and the sentiment.
```
community,tweet,sentiment
1,thanks,positive
1,oscars celebration glamour,neutral   
```
This output can be used to visualize the the top words from each community.
```
python3 topwords.py clus_sentiment.csv
```
### Evaluating the Methodologies using Modularity and Conductance

The code evaluation.py can be used to evaluate a clustering algorithm. It can find the density, modularity and conductance of the clusters. The code can be used as:

```
python evaluation.py <edge_file> <communities_file>
```
The edge_file is the file containing all the edges in the graph. The nodes in each edge are seperated by a tab. If the graph is unweighted, the weight is given as 1.
```
node1   node2   weight
node2   node3   weight
```

The communities_file has all the nodes along with the cluster number that they belong me.
```
node1   1
node2   1
node3   2
```
All the graph created were visualized using the tool Gephi.
