import csv
import random
import math
import operator


def loadData(filename, split, train, test):
	with open(filename, 'rb') as csvfile:
		lines = csv.reader(csvfile)
		dataSet = list(lines)

		for x in range(len(dataSet) - 1):
			for y in range(4):
				dataSet[x][y] = float(dataSet[x][y])
			if random.random() < split:
				train.append(dataSet[x])
			else:
				test.append(dataSet[x])

def distance(instance1, instance2):
	distance = 0

	for x in range(len(instance1) - 1):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def getNeighbors(trainSet, testInstance, k):
	distances = []

	for x in range(len(trainSet)):
		eucDistance = distance(testInstance, trainSet[x])
		distances.append((trainSet[x], eucDistance))
	distances.sort(key=operator.itemgetter(1))
	neighbors =[]
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct / float(len(testSet))) * 100.0

irisData = "bezdekIris.data"
trainSet = []
testSet = []
split = 0.67

loadData(irisData, split, trainSet, testSet)

predictions = []
k = 3

for x in range(len(testSet)):
	neighbors = getNeighbors(trainSet, testSet[x], k)
	result = getResponse(neighbors)
	predictions.append(result)
	print "Predicted: " + repr(result) + ", Actual: " + repr(testSet[x][-1])

accuracy = getAccuracy(testSet, predictions)
print "Accuracy: " + repr(accuracy) + "%"
