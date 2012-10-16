''' 
this file will calculate missing cabin room(boolean),no. of cabins the ticket holder had rented(0,1,...), the level of deck their cabin was in (A,B,...), has family (boolean), is adult (>18) 
'''

from sklearn.ensemble import RandomForestClassifier
import csv as csv
import numpy as np
import re
import sys



def loadData(trainData, mode):       
    
    dataForModelling = np.zeros((trainData.shape[0], 9))
    #1st column is survived
    for i in range(0,trainData.shape[0]):
        dataForModelling[i,0] = float(trainData[i,0])
    #2nd columns if pclass
    dataForModelling[:, 1] = trainData[:, 1]
    #3rd column is sex 0 - male, 1 - female
    if all(trainData[:, 3] == "female"):
        dataForModelling[:, 2] = 1.0
    else:
        dataForModelling[:, 2] = 0.0

    #4th column age present 0 if not present, 1 if present, 5th column is age
    for i in range(0, trainData.shape[0]):
        if trainData[i, 4] == "":
            dataForModelling[i, 3] = 0.0
#            dataForModelling[i, 4] = 0.0
        else:
            dataForModelling[i, 3] = 1.0
#            dataForModelling[i, 4] = float(trainData[i, 4])

    #6th column: number of siblings trainData
#    dataForModelling[:, 5] = trainData[:, 5]

    #7th column: number of parents
#    dataForModelling[:, 6] = trainData[:, 6]

    #8th column: isadult <18 - 0, >=18 - 1
    for i in range(0, trainData.shape[0]):
        if trainData[i, 4].strip('') != "":
            if float(trainData[i, 4]) < 18:
                dataForModelling[i, 4] = 0.0
            else:
                dataForModelling[i, 4] = 1.0
        else:
        #    check male or female
            if dataForModelling[i, 2] == 0.0:
                name = trainData[i, 2]
                if re.match(".*master.*", name.lower()):
                    dataForModelling[i, 4] = 0.0
                else:
                    dataForModelling[i, 4] = 1.0
            else:
                if re.match(".*mrs.*", trainData[i, 2].lower()):
                    dataForModelling[i, 4] = 1.0
                else:
                    dataForModelling[i, 4] = 0.0
            
    #9th column no of cabins, 10th column is deck
#    for i in range(0, trainData.shape[0]):
#        if trainData[i, 9].strip('') == "":
#            dataForModelling[i, 6] = 0.0
#            dataForModelling[i, 7] = 0.0
#        else:
#            split = trainData[i, 9].split(' ')
#            dataForModelling[i, 6] = len(split)
#            deck = split[0][0]
#            if deck == "A":
#                dataForModelling[i, 7] = 1.0
#            elif deck == "B":
#                dataForModelling[i, 7] = 2.0
#            elif deck == "C":
#                dataForModelling[i, 7] = 3.0
#            elif deck == "D":
#                dataForModelling[i, 7] = 4.0
#            elif deck == "E":
#                dataForModelling[i, 7] = 5.0
#            elif deck == "F":
#                dataForModelling[i, 7] = 6.0
#            elif deck == "G":
#                dataForModelling[i, 7] = 7.0
#            elif deck == "T":
#                dataForModelling[i, 7] = 8.0

    # 11th column: embarked location
    for i in range(0, trainData.shape[0]):
        if trainData[i, 10].strip('') == "C": 
            dataForModelling[i, 5] = 1.0
        elif trainData[i, 10].strip('') == "Q":
            dataForModelling[i, 5] = 2.0
        elif trainData[i, 10].strip('') == "S":
            dataForModelling[i, 5] = 3.0
    
    return dataForModelling
    

if len(sys.argv) < 3:
	print "Please give an input file name"
	print "python FeatureComputer <train-filename> <test-filename>"
	exit(1)
trainFileName = str(sys.argv[1])
testFileName = str(sys.argv[2])

trainFileReader = csv.reader(open(trainFileName, 'rb'))
testFileReader = csv.reader(open(testFileName, 'rb'))
# remove trainHeader line from csv

trainHeader = trainFileReader.next()
testHeader = testFileReader.next()
trainData = []
for row in trainFileReader:
	trainData.append(row)

trainData = np.array(trainData)

testData = []
resultData = []

for row in testFileReader:
    newRow = []
    newRow.append(0)
    resultData.append(row)
    for item in row:
        newRow.append(item)    
    testData.append(newRow)
    
testData = np.array(testData)

trainData = loadData(trainData,"train")

testData = loadData(testData, "test")

#now run random forets

forest = RandomForestClassifier(n_estimators = 100)
forestModel = forest.fit(trainData[:,1::], trainData[:,0])

output = forestModel.predict(testData[:,1::])

print output
print len(testData)
print len(output)

resultWriter = open('../data/result.csv', 'w+')
for i in range(0,len(resultData)):    
    resultWriter.write(str(int(output[i]))+",")
    for j in range(0,len(resultData[i])):
        if j == len(resultData[i]) -1:
            resultWriter.write(resultData[i][j])
        else:
            resultWriter.write(resultData[i][j]+",")
    resultWriter.write("\n")
    
resultWriter.close()
    



