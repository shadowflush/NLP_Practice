from collections import defaultdict,Counter

def viterbi(S,emission,transfer):
	outcome =[]
	score,backpointer=[],[]
	tags =set(emission.keys())
	tags.remove('*')
	
	vtb,bp ={},{}
	for i in tags:#first
		vtb[i] =emission['*'][i]*transfer[i][S[0]]
		bp[i] ='*'
	score.append(vtb)
	backpointer.append(bp)
	
	for i in range(1,len(S)):
		vtb,bp ={},{}
		pre_vtb =score[-1]
		
		for tag in tags:
			Max =0
			bestPreTag ='_'
			for key in pre_vtb.keys():
				if pre_vtb[key]*emission[key][tag]*transfer[tag][S[i]] > Max:
					bestPreTag =key
			vtb[tag] =pre_vtb[bestPreTag]*emission[bestPreTag][tag]*transfer[tag][S[i]]
			bp[tag] =bestPreTag
		score.append(vtb)
		backpointer.append(bp)
	
	Max =0
	bestPreTag ='_'
	for key in score[-1].keys():
		if score[-1][key]*emission[key]['$'] > Max:
			bestPreTag =key 
	outcome.append(bestPreTag)
	
	backpointer.reverse()
	for bp in backpointer:
		outcome.append(bp[outcome[-1]])
	return outcome

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
				sentences.append(outcome)
				outcome.clear()
			else:
				outcome.append(line)
	return sentences

def tag(sourceFile,emissionModelFile,transferModelFile,outcome):
	tags =[]
	sentences =loadData(sourceFile)
	emissionDict =loadModel(emissionModelFile)
	transferDict =loadModel(transferModelFile)
	
	for i in sentences:
		tags.append(viterbi(i,emissionDict,transferDict))
	
	with open(outcome,mode='w',encoding ="utf-8") as output:
		for sentence,tag in sentences,tags:
			for i,j in sentence,tag:
				output.write(i+' '+j+'\n')

tag("dev.conll","emission","transfer","tags")
	
	