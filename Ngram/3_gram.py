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
			if not line :#为空，表示一句话结束。添加下一句START token
				outcome.extend([START for i in range(N-1)])
			else:
				outcome.append(line)
	return outcome

			
def countNgram(trainData,N):#N元组统计。trainData为loadTrainData返回的list。
	dict =defaultdict(int)
	
	for i in range(len(trainData)):#统计出现在trainData中的所有三元组出现次数
		if trainData[i] =='*':
			continue
		gram =tuple(trainData[i-N+1:i+1])
		dict[gram] +=1
	return dict

def genModel_GT(trainData,dict,outcomeFile,N,threshold):#统计结果转化为概率 good-turing 平滑
	tmp =[]
	for i in dict:
		tmp.append(dict[i])
	countC =Counter(tmp)#统计出现C 次的N元组个数
	
	N_all =0
	for i in countC:#所有N元组出现次数总和
		N_all +=i*countC[i]
	
	flag =defaultdict(int)#记录已经计算过的N元组，避免重复计算
	with open(outcomeFile, mode='w', encoding="utf-8") as output:#计算概率，保存
		for i in range(len(trainData)):#计算在训练集中出现过的N元组
			if trainData[i] =='*':
				continue
			gram =tuple(trainData[i-N+1:i+1])#截取N元组
			if flag[gram] ==0:
				flag[gram] =1
				if dict[gram] <threshold:#N元组出现次数 < 阈值，平滑处理
					P =((dict[gram]+1) *countC[dict[gram]+1] /countC[dict[gram]])/N_all
				else:
					P =dict[gram] /N_all
				for i in gram:
					output.write(i+' ')
				output.write(' '+str(P)+"\n")
		setWords =set(trainData)#训练集词去重
		P = ( countC[1]/((len(setWords) -1)**3-N_all) ) /N_all#平滑处理 在训练集中未出现的N元组
		output.write("- - -"+' '+str(P))
		
START ='*'
STOP =["？","。","！"]
def main():
	sentences =loadTrainData("train.conll",3)#载入训练数据
	dict =countNgram(sentences,3)#获取统计结果
	genModel_GT(sentences,dict,"outcome",3,10)#统计结果转化为概率（平滑处理），保存
	
main()

