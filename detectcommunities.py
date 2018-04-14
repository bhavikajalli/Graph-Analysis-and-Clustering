import sys
import argparse
import numpy as np
import copy
def lpa(edges, numOfIteration = 10):
	# Find all neighbors of each node
	neighbors = []
	dictionary = {}
	totalDegree = []
	for edge in edges:
		if edge[0] not in dictionary:
			dictionary[edge[0]] = set()
		dictionary[edge[0]].add(edge[1])
		if edge[1] not in dictionary:
			dictionary[edge[1]] = set()
		dictionary[edge[1]].add(edge[0])
	temp = list(dictionary.items())
	temp.sort()
	for line in temp:
		helper = list(line[1])
		helper.sort()
		neighbors.append(helper)
		totalDegree.append(len(helper))

	# Initialize every node a unique label
	numOfNodes = len(neighbors)
	labelsOfNodes = range(numOfNodes)
	# Do the LPA
	preLabel = copy.deepcopy(labelsOfNodes)
	for k in range(numOfIteration):
		seq = range(numOfNodes)
		np.random.shuffle(seq)
		# Change the label
		for i in seq:
			labelsOfNeighbors = []
			for neighbor in neighbors[i]:
				labelsOfNeighbors.append([labelsOfNodes[neighbor], totalDegree[neighbor]])
			tempDictionary = {}
			for element in labelsOfNeighbors:
				if element[0] not in tempDictionary:
					tempDictionary[element[0]] = 0
				tempDictionary[element[0]] += 1
			frequentLabelCount = max(tempDictionary.values())
			frequentLabel = []
			for element in labelsOfNeighbors:
				if tempDictionary[element[0]] == frequentLabelCount:
					frequentLabel.append([element[1],element[0]])
			maxDegreeLabel = []
			highestDegree = max(frequentLabel)[0]
			for element in frequentLabel:
				if element[0] == highestDegree:
					maxDegreeLabel.append(element[1])
			postion = np.random.randint(0, len(maxDegreeLabel))
			labelsOfNodes[i] = maxDegreeLabel[postion]
		if labelsOfNodes == preLabel:
			break
		else:
			preLabel = copy.deepcopy(labelsOfNodes)
	d = {}
	i = 0
	temp1 = list(set(labelsOfNodes))
	temp1.sort()
	for t in temp1:
		d[t] = i
		i += 1
	for i in range(numOfNodes):
		labelsOfNodes[i] = d[labelsOfNodes[i]]
	return labelsOfNodes

def modularity(graph, label, numofIteration = 10):
	# Recreate the graph based on label
	lengthOfLabel = len(label)
	lengthOfUniqueLabel = len(set(label))
	newgraph = []
	UniqueLabel = range(lengthOfUniqueLabel)
	if lengthOfUniqueLabel != lengthOfLabel:
		helper = dict()
		for line in graph:
			if label[line[0]] == label[line[1]]:
				continue
			if (label[line[0]], label[line[1]]) in helper:
				helper[label[line[0]], label[line[1]]] += line[2]
			elif (label[line[1]], label[line[0]]) in helper:
				helper[label[line[1]], label[line[0]]] += line[2]
			else:
				helper[label[line[0]], label[line[1]]] = line[2]
		helper2 = list(helper.items())
		for line in helper2:
			newgraph.append([line[0][0], line[0][1], line[1]])
	else:
		newgraph = copy.deepcopy(graph)
	# Find all information of neighbors
	neighbors = []
	m = 0
	K = []
	Kin = []
	sigmaTotal = dict()
	numOfNodes = lengthOfUniqueLabel
	labelsOfNodes = copy.deepcopy(UniqueLabel)
	preLabel = copy.deepcopy(labelsOfNodes)

	for i in range(numOfNodes):
		Kin.append(dict())

	for line in newgraph:
		Kin[line[0]][line[1]] = line[2]
		Kin[line[1]][line[0]] = line[2]
		m += line[2]
	neighbors = copy.deepcopy(Kin)

	for i in range(numOfNodes):
		weight = sum(Kin[i].values())
		K.append(weight)
		sigmaTotal[i] = weight
	# Do the Modularity
	for itr in range(numofIteration):
		seq = range(numOfNodes)
		np.random.shuffle(seq)
		for i in seq:
			maxdeltaQ = 0
			newLabel = labelsOfNodes[i]
			for j in Kin[i].keys():
				deltaQ = Kin[i][j] * m - sigmaTotal[j] * K[i]

				if deltaQ > maxdeltaQ:
					maxdeltaQ = deltaQ
					newLabel = j
			if maxdeltaQ > 0:
				sigmaTotal[labelsOfNodes[i]] -= K[i]
				if labelsOfNodes[i] in Kin[i]:
					sigmaTotal[labelsOfNodes[i]] += Kin[i][labelsOfNodes[i]]
				sigmaTotal[newLabel] += K[i] - Kin[i][newLabel]			
				for neighbor in neighbors[i].keys():
					weight2 = neighbors[i][neighbor]
					Kin[neighbor][labelsOfNodes[i]] -= weight2
					if Kin[neighbor][labelsOfNodes[i]] == 0:
						del Kin[neighbor][labelsOfNodes[i]]
					if newLabel not in Kin[neighbor]:
						Kin[neighbor][newLabel] = 0
					Kin[neighbor][newLabel] += weight2
				labelsOfNodes[i] = newLabel
		if labelsOfNodes == preLabel:
			break
		else:
			preLabel = copy.deepcopy(labelsOfNodes)
	d = {}
	i = 0
	temp = list(set(labelsOfNodes))
	temp.sort()
	for t in temp:
		d[t] = i
		i += 1
	for i in range(lengthOfLabel):
		label[i] = d[labelsOfNodes[label[i]]]
	return label

def runLPA(finput, flpa):
	dictInput = dict()
	i = 0
	graphlpa = []
	namelist = []
	for line in finput:
		line = line.strip()
		line = line.split('	')
		if line[0] not in dictInput:
			dictInput[line[0]] = i
			namelist.append(line[0])
			i += 1
		if line[1] not in dictInput:
			dictInput[line[1]] = i
			namelist.append(line[1])
			i += 1
		graphlpa.append([dictInput[line[0]], dictInput[line[1]]])

	# Run LPA
	labellpa = lpa(graphlpa)
	for i in range(len(namelist)):
		flpa.write('{}	{}\n'.format(namelist[i], labellpa[i]))

def runLM(finput, fmod, num = 10):
	dictInput = dict()
	i = 0
	graphmod = []
	namelist = []
	for line in finput:
		line = line.strip()
		line = line.split('	')
		if line[0] not in dictInput:
			dictInput[line[0]] = i
			namelist.append(line[0])
			i += 1
		if line[1] not in dictInput:
			dictInput[line[1]] = i
			namelist.append(line[1])
			i += 1
		graphmod.append([dictInput[line[0]], dictInput[line[1]], int(line[2])])

	# Run Louvain Modularity
	labelmod = range(len(namelist))

	for i in range(num):
		labelmod = modularity(graphmod, labelmod)
	for i in range(len(namelist)):
		fmod.write('{}	{}\n'.format(namelist[i], labelmod[i]))

def main(argv):
	if len(argv) < 2:
		print('You must pass some parameters.')
		return
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', type = argparse.FileType('r'))
	parser.add_argument('--model', dest = 'model')
	parser.add_argument('--output', dest = 'output')
	args = parser.parse_args()
	if args.model == 'LPA':
		filename = open(args.output, 'w')
		runLPA(args.infile, filename)
	elif args.model == 'LM':
		filename = open(args.output, 'w')
		runLM(args.infile, filename)

if __name__ == '__main__':
	main(sys.argv[1:])