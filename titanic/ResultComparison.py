
import sys

if len(sys.argv)<3:
    print "Enter two input files"
    print "python ResulsComparison <result-file-1> <result-file-2>"
    exit(1)
    
fileName1 = str(sys.argv[1])
fileName2 = str(sys.argv[2])

file1 = open(fileName1, 'r')
file2 = open(fileName2, 'r')
data1 = []
data2 = []
for line in file1:
    data1.append(line)

for line in file2:
    data2.append(line)

if len(data1) != len(data2):
    print "Please make sure you have given the right file"
    exit(1)
match = 0
noMatch = 0
for i in range(0,len(data1)):
    if data1[i].split(',')[0] == data2[i].split(',')[0]:
        match+=1
    else:
        noMatch+=1

print "total match: "+str(match)
print "total notmatch: "+str(noMatch)
print "accuracy: "+str((float(match)/(float(match)+float(noMatch))))
                       