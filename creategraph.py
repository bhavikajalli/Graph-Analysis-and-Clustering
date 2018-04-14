import sys
import argparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from time import time
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import csv
import numpy as np
import random
from sklearn.preprocessing import normalize

def print_top_words(model, feature_names, n_top_words):
	for topic_idx, topic in enumerate(model.components_):
		message = "Topic #%d: " % topic_idx
		message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
		print(message)
	print()

def create_similarity_graph(filename, output):
	# max number of terms considered
	n_features = 10000
	n_top_words = 10
	#number of topics
	n_components = 30
	p = 0.1  # 10% of the lines
	df = pd.read_csv(
			filename,
			encoding='utf-8',
			header=0, 
			skiprows=lambda i: i>0 and random.random() > p
	)
	df = df[df['retweet_count'] == 0]
	df = df[pd.notnull(df.tweet)]

	tweets = df['tweet'].tolist()
	n_samples =  len(tweets)
	pd.DataFrame(tweets).to_csv('tweets_graph.csv', index=True)

	# Use tf (raw term count) features for LDA.
	print("Extracting tf features for LDA...")
	tf_vectorizer = CountVectorizer(analyzer='word',max_features=n_features)
	t0 = time()
	tf = tf_vectorizer.fit_transform(tweets)
	print("done in %0.3fs." % (time() - t0))

	print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..." % (n_samples, n_features))
	lda = LatentDirichletAllocation(n_components=n_components, max_iter=1000,
									evaluate_every = 10,
									learning_method='online',
									learning_offset=5.,
									random_state=0,
									doc_topic_prior = 0.01,
									topic_word_prior = 0.01)
	t0 = time()
	feature_extraction = lda.fit_transform(tf)
	feature_extraction = normalize(feature_extraction,axis = 1,norm = 'l2')
	print("done in %0.3fs." % (time() - t0))
	print("\nTopics in LDA model:")
	tf_feature_names = tf_vectorizer.get_feature_names()
	print_top_words(lda, tf_feature_names, n_top_words)
	cos_sim = feature_extraction.dot(feature_extraction.T)
	cos_sim = cos_sim - np.eye(n_samples)
	I,J = np.where(cos_sim > 0.7)
	col = np.column_stack((I,J,cos_sim[I,J]))
	with open(output, 'w') as f:
		for row in col:
			if row[0] < row[1]:
				f.write('{}\t{}\t{}\n'.format(int(row[0]),int(row[1]),row[2]))

def retweetgraph(data, filename, num = 5):
	# Find all mention history
	retweets = []
	for line in data:
		line = line.strip()
		if line == '':
			continue
		line = line.split(',')
		if len(line) < 3:
			continue
		if line[2] == '':
			continue
		if line[0] == 'name':
			continue
		retweets.append([line[0], line[2]])

	# Find out nodes with more than 'num' weighted degree
	nodes = dict()
	for line in retweets:
		if line[0] not in nodes:
			nodes[line[0]] = 0
		nodes[line[0]] += 1
		if line[1] not in nodes:
			nodes[line[1]] = 0
		nodes[line[1]] += 1

	for i in list(nodes):
		if nodes[i] <= num:
			del nodes[i]
	# Find undirected weighted edges without self loop
	temp = dict()
	for retweet in retweets:
		if retweet[0] == retweet[1]:
			continue
		if retweet[0] in nodes and retweet[1] in nodes:
			if (retweet[0], retweet[1]) in temp:
				temp[(retweet[0], retweet[1])] += 1
			elif (retweet[1], retweet[0]) in temp:
				temp[(retweet[1], retweet[0])] += 1
			else:
				temp[(retweet[0], retweet[1])] = 1
	edges = list(temp.items())
	f = open(filename, 'w')
	for edge in edges:
		f.write('{}\t{}\t{}\n'.format(edge[0][0], edge[0][1], edge[1]))
	f.close()

def mentiongraph(data, filename, num = 5):
	# Find all mention history
	mentions = []
	for line in data:
		line = line.strip()
		if line == '':
			continue
		line = line.split(',')
		if len(line) < 4:
			continue
		if line[3] == '':
			continue
		if line[0] == 'name':
			continue
		mtns = line[3].split('-')
		for mtn in mtns:
			mentions.append([line[0], mtn])

	# Find out nodes with more than 'num' weighted degree
	nodes = dict()
	for line in mentions:
		if line[0] not in nodes:
			nodes[line[0]] = 0
		nodes[line[0]] += 1
		if line[1] not in nodes:
			nodes[line[1]] = 0
		nodes[line[1]] += 1

	for i in list(nodes):
		if nodes[i] <= num:
			del nodes[i]
	# Find undirected weighted edges without self loop
	temp = dict()
	for mention in mentions:
		if mention[0] == mention[1]:
			continue
		if mention[0] in nodes and mention[1] in nodes:
			if (mention[0], mention[1]) in temp:
				temp[(mention[0], mention[1])] += 1
			elif (mention[1], mention[0]) in temp:
				temp[(mention[1], mention[0])] += 1
			else:
				temp[(mention[0], mention[1])] = 1
	edges = list(temp.items())
	f = open(filename, 'w')
	for edge in edges:
		f.write('{}\t{}\t{}\n'.format(edge[0][0], edge[0][1], edge[1]))
	f.close()

def main(argv):
	if len(argv) < 2:
		print('You must pass some parameters.')
		return
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', type = argparse.FileType('r'))
	parser.add_argument('--graphtype', dest = 'graphtype')
	parser.add_argument('--output', dest = 'output')
	args = parser.parse_args()
	if args.graphtype == 'mention':
		mentiongraph(args.infile, args.output)
	elif args.graphtype == 'retweet':
		retweetgraph(args.infile, args.output)
	elif args.graphtype == 'similarity':
		create_similarity_graph(args.infile, args.output)
	


if __name__ == '__main__':
	main(sys.argv[1:])