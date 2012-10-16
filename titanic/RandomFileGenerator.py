''' RandomFileGenerator
	Given training file, and number of lines when prompted, it generates a sub training and test file(test file will still have the class labelled).

@author: Vivek Hariharan	'''

import sys
import csv as csv
import random

def writeOutputFileWithHead(headLine, outputWriter, output):
	outputWriter.write(str(headLine))
	for line in output:
		outputWriter.write(str(line))
	outputWriter.close()

def writeOutputFile(outputWriter, output):
	for line in output:
		outputWriter.write(str(line))
	outputWriter.close()

if len(sys.argv) < 2:
	print "give filename as arguement"
	print "python RandomFileGenerator <fileName>"
	exit(1)

fileName = str(sys.argv[1])

headerResponse = raw_input('Is First line of file the header? (y/n)')
headerLine = ""
data = []
if headerResponse == "y":
	inputFile = open(fileName,'r')
	fileData = inputFile.readlines()
	headerLine = fileData[0]
	print headerLine
	for i in range(1,len(fileData)):
		data.append(fileData[i])	

else:
	data = open(fileName, 'r').readlines()
	
print "number of lines in file is " + str(len(data))
numberOfLines = raw_input("How many lines of data do you want in new random file (remaining lines will be put in test)? ")
print numberOfLines

randomNumbersForTrain = []


for i in range(0,int(numberOfLines)):
	numberGenerated = random.randint(0,int(len(data))-1)
	while(numberGenerated in randomNumbersForTrain):
		numberGenerated = random.randint(0,int(len(data))-1)
	randomNumbersForTrain.append(numberGenerated)
		
	

trainData = []
testData = []
testTestData = []
for i in range(0,len(data)):
	if i in randomNumbersForTrain:
		trainData.append(data[i])
	else:
		testTestData.append(data[i].replace('\"',''))
		testData.append(','.join(data[i].split(',')[1::]))

outputTrainFile = open("train"+str(numberOfLines),'w+')
outputTestFile = open("test"+str(numberOfLines), 'w+')
outputTestTestFile = open("testSolution"+str(numberOfLines), 'w+')

if len(headerLine) != 0:
	writeOutputFileWithHead(headerLine,outputTrainFile, trainData)
	writeOutputFileWithHead(','.join(headerLine.split(',')[1::]), outputTestFile, testData)
	writeOutputFile(outputTestTestFile, testTestData) 
else:
	writeOutputFile(outputTrainFile, trainData)
	writeOutputFile(outputTestFile, testData)
	writeOutputFile(outputTestTestFile, testTestData)


