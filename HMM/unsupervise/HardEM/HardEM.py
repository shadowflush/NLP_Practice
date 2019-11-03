from collections import defaultdict,Counter
import random
from viterbi import viterbi,loadData

def loadT(file):
	T =[]
	with open(file,mode ='r',encoding="utf-8") as input:
		line =input.readline()
		T =line.split(" ")
	return T
	
def loadWords(file):
	words =[]
	with open(file,mode='r',encoding ="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			info =line.split('\t')
			if len(info)>3:
				words.append(info[1])
	words =set(words)
	return words

def initTransfer(T):#随机初始化转移概率   $ 为结束标志 *为开始标志
	dict =defaultdict(Counter)
	for i in T:
		if i !='$':
			count =0
			for j in T:
				if j =='*' or (i=='*' and j =='$'):#排除 Word* 和 *$ 的情况
					continue
				dict[i][j] =random.random()
				count +=dict[i][j]
			dict[i]['_'] =random.random()
			count +=dict[i]['_']
			for j in dict[i]:#归一化
				dict[i][j] /=count
			dict[i]['_'] /=count
	return dict

def initEmission(T,Words):#随机初始化发射概率
	dict =defaultdict(Counter)
	for i in T:
		if i !='*' and i != '$':
			count =0
			for j in Words:
				dict[i][j] =random.random()
				count +=dict[i][j]
			dict[i]['_'] =random.random()
			count +=dict[i]['_']
			for j in dict[i]:#归一化
				dict[i][j] /=count
			dict[i]['_'] /=count
	return dict

def emission(sentences,Tsequence):
	dict =defaultdict(Counter)
	for i in range(len(sentences)):
		for j in range(len(sentences[i])):
			dict[Tsequence[i][j]][sentences[i][j]] +=1
	
	all =0
	for i in dict:
		all +=len(dict[i].keys())
	for i in dict:
		for j in dict[i]:
			dict[i][j] =(dict[i][j]+1) /(sum(dict[i].values()) +all)
		dict[i]['_'] =1/(sum(dict[i].values()) +all)
	return dict
	
def transfer(Tsequence):
	dict =defaultdict(Counter)
	for T in Tsequence:#统计次数
		T =['*']+T+['$']
		for i in range(len(T)-1):
			dict[T[i]][T[i+1]] +=1
	
	all =len(dict.keys())
	for i in dict:
		for j in dict[i]:
			dict[i][j] =(dict[i][j] + 1) / ( sum(dict[i].values()) + all)
		dict[i]['_'] = 1 / ( sum(dict[i].values()) + all)
	return dict

def diff(Y,new_Y):
	count =0
	for i in range(len(Y)):
		for j in range(len(Y[i])):
			if Y[i][j] != new_Y[i][j]:
				count +=1
	return count

def HardEM(file,outcome):
	words =loadWords(file)
	T =loadT("T")
	iniT =initTransfer(T)#随机初始化转移概率
	iniE =initEmission(T,words)#随机初始化发射概率
	sentences =loadData(file)
	
	Y =[]
	for i in sentences:
		Y.append(viterbi(i,iniT,iniE))
		
	
	print(sentences[50])
	print(Y[50])
	
	for i in range(maxLoop):
		print(i)
		new_T =transfer(Y)
		new_E =emission(sentences,Y)
		new_Y =[]
		for j in sentences:
			new_Y.append(viterbi(j,new_T,new_E))
		print(sentences[50])
		print(Y[50])
		if diff(Y,new_Y) < threshold:
			Y =new_Y
			break
		Y =new_Y
	with open(outcome,mode='w',encoding ="utf-8") as output:
		for i in range(len(sentences)):
			for j in range(len(sentences[i])):
				output.write(sentences[i][j]+' '+Y[i][j]+' \n')
		
		
maxLoop =100
threshold =50
HardEM("dev.conll","outcome")

