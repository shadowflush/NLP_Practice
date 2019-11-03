from collections import defaultdict,Counter
import math
constant =10000

def viterbi(S,emission,transfer):
	outcome =[]
	score,backpointer=[],[]
	tags =set(emission.keys())
	tags.remove('*')
	
	vtb,bp ={},{}
	for i in tags:#first
		e =emission['*'][i] if emission['*'][i] >0 else emission['*']['_']
		t =transfer[i][S[0]] if transfer[i][S[0]] >0 else transfer[i]['_']
		vtb[i] =e*t
		bp[i] ='*'
	score.append(vtb)
	backpointer.append(bp)
	for i in range(1,len(S)):
		vtb,bp ={},{}
		pre_vtb =score[-1]
		for tag in tags:
			Max ,bestPreTag =0,'_'
			for key in pre_vtb.keys():
				e =emission[key][tag] if emission[key][tag] >0 else emission[key]['_']
				t =transfer[tag][S[i]] if transfer[tag][S[i]] >0 else transfer[tag]['_']
				if pre_vtb[key]*e*t*constant > Max:#乘常数避免因为精度问题导致出错
					bestPreTag =key
					Max = pre_vtb[key]*e*t*constant
			vtb[tag] =Max
			bp[tag] =bestPreTag
		score.append(vtb)
		backpointer.append(bp)
	
	Max ,bestPreTag =0,'_'
	for key in score[-1].keys():
		if score[-1][key]*emission[key]['$'] > Max:
			bestPreTag =key 
			Max =score[-1][key]*emission[key]['$']
	outcome.append(bestPreTag)
	
	backpointer.reverse()
	for bp in backpointer:
		outcome.append(bp[outcome[-1]])
	outcome.reverse()
	return outcome[1:]

def loadModel(FilePath):
	dict =defaultdict(Counter)
	with open(FilePath,mode='r',encoding="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			info =line.split(' ')
			dict[info[0]][info[1]] =float(info[2])
	return dict

def loadData(sourceFile):#载入数据
	sentences =[]
	def getInformation(S):
		start,end,count =-1,0,0
		for i in range(0,len(S)):
			if S[i] =='\t' and count ==0:
				start,count =i,count+1
			elif S[i] =='\t' and count ==1:
				end =i
				break
		return S[start+1:end]
		
	outcome =[]
	with open(sourceFile,mode ='r',encoding="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			line =getInformation(line)
			if not line:
				sentences.append(outcome[:])
				outcome.clear()
			else:
				outcome.append(line)
	return sentences

def tag(sourceFile,emissionModelFile,transferModelFile,outcome):
	tags =[]
	sentences =loadData(sourceFile)
	emissionDict =loadModel(emissionModelFile)
	transferDict =loadModel(transferModelFile)
	
	with open(outcome,mode='w',encoding ="utf-8") as output:
		for i in sentences:
			tag =viterbi(i,emissionDict,transferDict)
			for j in range(len(i)):
				output.write(i[j]+' '+tag[j]+' \n')
	
#tag("dev.conll","emission","transfer","tags")
	
	