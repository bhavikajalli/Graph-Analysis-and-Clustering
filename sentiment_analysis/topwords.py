#Code to find the top words in a community.The input file is top 5 communities and their from InfoMap
import sys
import pandas
import nltk


file = sys.argv[1]
df = pd.read_csv(file, encoding='latin-1')
file1 = open('topwords_graph.txt', 'w')

comm1 = []
comm2 = []
comm3 = []
comm4 = []
comm5 = []
comm6 = []

for index, row in df.iterrows():
	if row["community"] == 1:
		if type(row["tweet"]) == str:
			comm1.extend(row["tweet"].split(' '))
	if row["community"] == 2:
		if type(row["tweet"]) == str:
			comm2.extend(row["tweet"].split(' '))
	if row["community"] == 3:
		if type(row["tweet"]) == str:
			comm3.extend(row["tweet"].split(' '))
	if row["community"] == 4:
		if type(row["tweet"]) == str:
			comm4.extend(row["tweet"].split(' '))
	if row["community"] == 5:
		if type(row["tweet"]) == str:
			comm5.extend(row["tweet"].split(' '))
	if row["community"] == 5:
		if type(row["tweet"]) == str:
			comm5.extend(row["tweet"].split(' '))
	if row["community"] == 6:
		if type(row["tweet"]) == str:
			comm6.extend(row["tweet"].split(' '))

counter1 = collections.Counter(comm1).most_common(50)
file1.write('community1 : {}\n\n'.format(counter1))

counter2 = collections.Counter(comm2).most_common(50)
file1.write('community2 :{}\n\n'.format(counter2))

counter3 = collections.Counter(comm3).most_common(50)
file1.write('community3 :{}\n\n'.format(counter3))

counter4 = collections.Counter(comm4).most_common(50)
counter4[21] = ('dontusethis', 1000)
file1.write('community4 :{}\n\n'.format(counter4))

counter5 = collections.Counter(comm5).most_common(50)
file1.write('community5 :{}\n\n'.format(counter5))

counter6 = collections.Counter(comm6).most_common(50)
file1.write('community6 :{}\n\n'.format(counter6))

file1.close()