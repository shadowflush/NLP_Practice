from collections import defaultdict, Counter
import random

def loadModel(modelFile):#载入模型
	dict =defaultdict(Counter)
	words =[]
	with open(modelFile, mode='r', encoding="utf-8") as input:
		lines =input.readlines()
		for line in lines:
			info =line.split()
			context =info[:-2]#上文
			word =info[-2]#词
			value =info[-1]#概率
			dict[tuple(context)][word] =float(value)
			words =words+ info[:-1]
	words =set(words)
	words.remove('*')
	words.remove('-')
	words =list(words)
	return (dict,words)

def genNextWord(context,dict):#利用上文获取概率最大的下一个词
	if context not in dict:
		return "。"
	else:
		max,word=0,""
		for i in dict[context]:
			if dict[context][i] > max:
				max =dict[context][i]
				word =i
		return word
	
def genSentence(dict,words):
	word =words[random.randint(0,len(words))]
	context =('*','*')
	sentence =word
	for i in range(30):#最大句子长度
		context =(context[1],word)
		word =genNextWord(context,dict)#获取下一词
		sentence = sentence+word
		if word in STOP:
			break
	return sentence

def genSentences(outcomeFile,max):
	dict,words =loadModel("outcome")
	with open(outcomeFile, mode='w', encoding="utf-8") as output:
		for i in range(max):
			sentence =genSentence(dict,words)
			output.write(sentence+'\n')

STOP =["？","。","！"]		
genSentences("sentences",100)	
