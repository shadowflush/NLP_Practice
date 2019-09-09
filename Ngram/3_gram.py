# -*- coding: utf-8 -*- 
from collections import defaultdict 
from collections import Counter

def getInformation(S):
	start,end,count =-1,0,0
	for i in range(0,len(S)):
		if S[i] =='\t' and count ==0:
			start,count =i,count+1
		elif S[i] =='\t' and count ==1:
			end =i
			break
	return S[start+1:end]
	
def loadTrainData(sourceFile,N):#载入分词文件，句首添加 START token，返回list
	outcome =[START for i in range(N-1)]
	with open(sourceFile, mode='r', encoding="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			line =getInformation(line)
			if not line:
				outcome.extend([START for i in range(N-1)])
			outcome.append(line)
	return outcome

			
def countNgram(trainData,N):#trainData为list具体内容如下 [*,*,戴相龙,说,....,*,*]  **表示句首
	dict =defaultdict(int)
	
	for i in range(len(trainData)):#统计出现在trainData中的所有三元组出现次数
		if trainData[i] =='*':
			continue
		gram =tuple(trainData[i-N+1:i+1])
		dict[gram] +=1
	
	setW,setUV =set(trainData),set(trainData)#trainData 词语去重
	setUV.remove('。')
	setW.remove('*')
	
	for word1 in setUV:#统计所有三元组出现的次数（问题在这儿，运行时间长，且内存占用巨大）
		for word2 in setUV:
			if word1 !='*' and word2 =='*':
				continue
			for word3 in setW:
				gram =tuple([word1,word2,word3])
				dict[gram]#若gram在dict中，则不改变值（已经统计过了），若不在，则为0
	return dict

def genmodel_GT(trainData,dict,outcomeFile,threshold):#概率计算 good-turing 平滑
	setW,setUV =set(trainData),set(trainData)
	setUV.remove('。')
	setW.remove('*')
	
	tmp =[]
	for i in dict:
		tmp.append(dict[i])
	countC =Counter(tmp)#统计出现C 次的Ngram个数
	
	N_all =sum(countC.values())
	
	with open(outcomeFile, mode='w', encoding="utf-8") as output:
		for word1 in setUV:
			for word2 in setUV:
				if word1 !='*' and word2 =='*':
					continue
				for word3 in setW:
					P =0
					gram =tuple([word1,word2,word3])
					if dict[gram] <threshold:
						P =((dict[gram]+1) *countC[dict[gram]+1] /countC[dict[gram]])/N_all
					else:
						P =dict[gram] /N_all
					for i in gram:
						output.write(i+" ")
					output.write(P)
					output.write("\n")

START ='*'
def main():
	sentences =loadTrainData("train.conll",3)
	dict =countNgram(sentences,3)
	genmodel_GT(sentences,dict,"outcome",2)
	
main()

