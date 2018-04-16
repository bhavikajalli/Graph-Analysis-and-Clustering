crawl: 
	pip install tweepy==3.3.0
	python data_utils/crawl_metoo.py --hashtag '#Metoo' --since 2018-03-10 --until 2018-03-19 --outputFile metoo_rawTweets.txt
preprocess:
	python data_utils/data_preprocess.py --input metoo_rawTweets.txt --output metoo_processedTweets.txt
creategraph:
	python creategraph.py metoo_processedTweets.txt --graphtype mention --output mentionGraph.txt
	python creategraph.py metoo_processedTweets.txt --graphtype retweet --output retweetGraph.txt
	python creategraph.py metoo_processedTweets.txt --graphtype similarity --output similarityGraph.txt
detectcommunities:
	python detectcommunities.py mentionGraph.txt --model LPA --output LPA_mention.txt
	python detectcommunities.py mentionGraph.txt --model LM --output LM_mention.txt
	./Infomap mentionGraph.txt output/ -N 5 --clu
	python detectcommunities.py retweetGraph.txt --model LPA --output LPA_retweet.txt
	python detectcommunities.py retweetGraph.txt --model LM --output LM_retweet.txt
	./Infomap retweetGraph.txt output/ -N 5 --clu
	python detectcommunities.py similarityGraph.txt --model LPA --output LPA_similarity.txt
	python detectcommunities.py similarityGraph.txt --model LM --output LM_similarity.txt
	./Infomap similarityGraph.txt output/ -N 5 --clu
Sentiment:
	python3 sentiment_analysis/sentiment_analysis.py similarityGraph.clu tweets_graph.txt
topwords:
	python3 topwords.py clus_sentiment.csv
evaluation:
	python evaluation.py mentionGraph.txt LPA_mention.txt
	python evaluation.py mentionGraph.txt LM_mention.txt
	python evaluation.py mentionGraph.txt mentionGraph.clu
	python evaluation.py retweetGraph.txt LPA_retweet.txt
	python evaluation.py retweetGraph.txt LM_retweet.txt
	python evaluation.py retweetGraph.txt retweetGraph.clu
	python evaluation.py similarityGraph.txt LPA_similarity.txt
	python evaluation.py similarityGraph.txt LM_similarity.txt
	python evaluation.py similarityGraph.txt similarityGraph.clu

