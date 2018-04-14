from textblob import TextBlob
from collections import Counter
import pandas as pd
import collections
import nltk
import numpy as np
import os
import sys


def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

edgefile = sys.argv[1]
tweetsfile = sys.argv[2]

f_clusters = open(edgefile,'r')
f_tweets = open(tweetsfile,'r')
f_output = open('clus_sentiment.txt','w',encoding="utf-8")
num_clusters = 10
tweets = {}
label = {}
sentiment = {1: 'positive', -1: 'negative', 0: 'neutral'}
print('find tweets')
for line in f_tweets:
	line.strip()
	if line == '':
		continue
	line = line.split(',')
	if line[0] not in tweets:
		tweets[line[0]] = line[1]
f_tweets.close()


print('find clusters')

cluster_count = {}
clusters = {}
row = 'community' + ',' + 'tweet' + ',' + 'sentiment' +"\n"
f_output.write(row)
for line in f_clusters:
	line.strip()
	if not line.startswith('#'):
		node = line.split()

		if int(node[1]) > num_clusters:
			continue
		if node[1] not in clusters:
			clusters[node[1]] = []
			cluster_count[node[1]] = 0

		cluster_count[node[1]] += 1

		s = analize_sentiment(tweets[node[0]])
		row = node[1] +  "," + tweets[node[0]] +"," + sentiment[s] +  "\n"
		clusters[node[1]].append(s)
		f_output.write(row)

for i in range(num_clusters):
	c = Counter(clusters[str(i+1)])

	for j in range(3):
		temp_val = list(c.values())[j] / len(clusters[str(i+1)])
		temp_sentiment = list(c.keys())[j]
		print('cluster:{} sentiment:{} Percentage: {}'.format(i+1,sentiment[temp_sentiment], temp_val*100))
f_output.close()
f_clusters.close()
print(cluster_count)

# os.system("sed -re 's/^(\S*) (\S+) (.*) (\S*)\s*$/\\1,\\2,\\3/' clus_sentiment_out.txt > clus_sentiment_graph_new.csv")
# print("sed -re 's/^(\S*) (\S*) (.*) (\S+)\s*$/\\1,\\2,\\3/' clus_sentiment_out.txt > clus_sentiment_graph_new.csv")
