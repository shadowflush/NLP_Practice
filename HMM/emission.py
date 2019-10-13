from collections import defaultdict,Counter

alpha =0.5

def getPart_of_speech(S):#截取词性
	start,end,count =-1,0,-3
	for i in range(0,len(S)):
		if S[i] == '\t':
			count +=1
		if count ==0 and start == -1:
			start =i
		if count ==1:
			end =i
			break
	return S[start+1:end]

def loadTrainData(sourceFile):#载入训练数据
	outcome =['*']
	with open(sourceFile,mode ='r',encoding="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			line =getPart_of_speech(line)
			if not line:
				outcome.extend(['$','*'])
			else:
				outcome.append(line)
	return outcome
	
def count2tuple(trainData):#统计2元模型
	dict =defaultdict(Counter)
	
	for i in range(len(trainData)):
		if trainData[i] !='*':
			context =trainData[i-1]
			data =trainData[i]
			dict[context][data] +=1
		
	return dict
	
	
def smoothAndSave(modeDict, outcomeFile):#平滑统计结果，保存至文件
	
	V =[]#统计不同词性
	for i in modeDict:
		V.append(i)
	setV =set(V)
	
	all =len(setV)
	with open(outcomeFile,mode='w',encoding="utf-8") as output:
		for i in modeDict:
			for j in modeDict[i]:
				p =(modeDict[i][j] + alpha) / ( sum(modeDict[i].values()) + alpha*all)
				output.write(i+' '+j+' '+str(p)+'\n')

def emission(trainFile,outcomeFile):
	trainData =loadTrainData(trainFile)
	trainDict =count2tuple(trainData)
	smoothAndSave(trainDict,outcomeFile)

emission("train.conll","emission")
		