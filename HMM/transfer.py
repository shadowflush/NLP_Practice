from collections import defaultdict,Counter

def loadTrainData(trainFile):
	dict =defaultdict(Counter)
	with open(trainFile,mode='r',encoding ="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			info =line.split('\t')#1	戴相龙	_	NR	_	_	2	VMOD	_	_
			if len(info)>3:
				dict[info[3]][info[1]] +=1
	return dict

def toPAndSave(trainDict,outcomeFile):#计算转移概率，保存
	with open(outcomeFile,mode='w',encoding ="utf-8") as output:
		for i in trainDict:
			for j in trainDict[i]:
				p =trainDict[i][j] /sum(trainDict[i].values())
				output.write(i+' '+j+' '+str(p)+'\n')

def transfer(trainData,outcome):
	dict =loadTrainData(trainData)
	toPAndSave(dict,outcome)

transfer("train.conll","transfer")
