# -*- coding: utf-8 -*- 
from collections import defaultdict 
from collections import Counter

def getInformation(S):#获取train.conll有效信息：例如从（1	戴相龙	_	NR	_	_	2	VMOD	_	_）中获取 “戴相龙”
	start,end,count =-1,0,0
	for i in range(0,len(S)):
		if S[i] =='\t' and count ==0:
			start,count =i,count+1
		elif S[i] =='\t' and count ==1:
			end =i
			break
	return S[start+1:end]
	
def loadTrainData(sourceFile,N):#载入以分词文件，句首添加 START token，返回list。返回结果例如 [*,*,戴相龙,说,....,*,*]
	outcome =[START for i in range(N-1)]
	with open(sourceFile, mode='r', encoding="utf-8") as input:
		lines =input.readlines()#读入分词文件一行内容
		for line in lines:
			line =getInformation(line)#获取有效信息
			if not line:#为空，表示一句话结束。添加下一句START token
				outcome.extend([START for i in range(N-1)])
			outcome.append(line)
	return outcome

			
def countNgram(trainData,N):#N元组统计。trainData为loadTrainData返回的list。（待改进）
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

def genModel_GT(trainData,dict,outcomeFile,threshold):#统计结果转化为概率 good-turing 平滑 （待改进）
	setW,setUV =set(trainData),set(trainData)
	setUV.remove('。')
	setW.remove('*')
	
	tmp =[]
	for i in dict:
		tmp.append(dict[i])
	countC =Counter(tmp)#统计出现C 次的N元组个数
	
	N_all =0
	for i in countC:#所有N元组出现次数总和
		N_all +=i*countC[i]
	
	with open(outcomeFile, mode='w', encoding="utf-8") as output:#计算概率，保存
		for word1 in setUV:
			for word2 in setUV:
				if word1 !='*' and word2 =='*':
					continue
				for word3 in setW:
					P =0
					gram =tuple([word1,word2,word3])
					if dict[gram] <threshold:#N元组出现次数 < 阈值，平滑处理
						P =((dict[gram]+1) *countC[dict[gram]+1] /countC[dict[gram]])/N_all
					else:
						P =dict[gram] /N_all
					for i in gram:
						output.write(i+" ")
					output.write(P)
					output.write("\n")

START ='*'
def main():
	sentences =loadTrainData("train.conll",3)#载入训练数据
	dict =countNgram(sentences,3)#获取统计结果
	genmodel_GT(sentences,dict,"outcome",2)#统计结果转化为概率（平滑处理），保存
	
main()

