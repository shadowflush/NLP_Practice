from collections import defaultdict,Counter

def loadStandardData(standardFile):
	standard =[]
	with open(standardFile,mode='r',encoding ="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			info =line.split('\t')
			if len(info) >3:
				standard.append(info[3])
	return standard
	
def loadTestData(testFile):
	test =[]
	with open(testFile,mode='r',encoding ="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			info =line.split(' ')
			test.append(info[1])
	return test
	
def precision(testFile,standardFile):
	test =loadTestData(testFile)
	standard =loadStandardData(standardFile)
	rightCount =0
	for i in range(len(test)):
		if test[i] ==standard[i]:
			rightCount +=1
	print(rightCount/len(test))

precision("tags","dev.conll")
	