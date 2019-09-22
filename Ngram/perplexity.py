from collections import defaultdict, Counter
import math
def getInformation(S):#获取有效信息：例如从（1	戴相龙	_	NR	_	_	2	VMOD	_	_）中获取 “戴相龙”
	start,end,count =-1,0,0
	for i in range(0,len(S)):
		if S[i] =='\t' and count ==0:
			start,count =i,count+1
		elif S[i] =='\t' and count ==1:
			end =i
			break
	return S[start+1:end]
	
def loadData(sourceFile,N):#载入以分词文件，生成句子
	outcome =[]
	sentence =[START for i in range(N-1)]
	with open(sourceFile, mode='r', encoding="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			line =getInformation(line)#获取有效信息
			if not line :#为空，表示一句话结束。添加下一句START token
				outcome.append(sentence)
				sentence =[START for i in range(N-1)]
			else:
				sentence.append(line)
	return outcome

def loadModel(modelFile):#载入模型
	dict =defaultdict(Counter)
	with open(modelFile, mode='r', encoding="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			info =line.split()
			context =info[:-2]#上文
			word =info[-2]#词
			value =info[-1]#概率
			dict[tuple(context)][word] =float(value)
	return dict
		
def sentencePer(modelDict,N,sentence):#计算单句perplexity
	P =1
	for i in range(2,len(sentence)):
		context =tuple(sentence[i-N+1:i])
		word =sentence[i]
		if context not in modelDict:#测试N元组未出现在模型中
			P *= 1
		elif context in modelDict and word not in modelDict[context]:
			P *= modelDict[('-','-')]['-'] / sum(modelDict[context].values())
		else:
			P *= modelDict[context][word] / sum(modelDict[context].values())
	return math.log(P,2)

def perplexity(testDataFile,modelFile):
	sentences =loadData(testDataFile,3)
	modelDict =loadModel(modelFile)
	
	per,wordCount =0,0
	for i in sentences:
		wordCount +=len(i)
		per +=sentencePer(modelDict,3,i)
	
	per /=wordCount
	per = 1/(2**per)
	print(per)
	
	
	
	
	
START ='*'
perplexity("dev.conll","outcome")