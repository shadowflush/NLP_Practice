import re

def getInformation(S):
	start,end,count =-1,0,0
	for i in range(0,len(S)):
		if S[i] =='\t' and count ==0:
			start,count =i,count+1
		elif S[i] =='\t' and count ==1:
			end =i
			break
	return S[start+1:end]
	
	
def genDict(sourceFile, outcomeFile):
	with open(sourceFile, mode='r', encoding="utf-8") as input:
		with open(outcomeFile, mode='w', encoding="utf-8") as output:
			lines =input.readlines()
			for line in lines:
				line =getInformation(line)
				#line =re.sub("[A-Z0-9\_\\t\\n\\r]","",line)#filter non-Chinese
				output.write(line+" ")


def genText(sourceFile, outcomeFile):
	with open(sourceFile, mode='r', encoding="utf-8") as input:
		with open(outcomeFile, mode='w', encoding="utf-8") as output:
			lines =input.readlines()
			sentence =""
			for line in lines:
				line =getInformation(line)
				#line =re.sub("[A-Z0-9\_\\t\\n\\r]","",line)#filter non-Chinese
				if line =="":
					output.write(sentence+"\n")
					sentence =""
				else:
					sentence =sentence+line
					
genDict("data.conll","word.dict")
genText("data.conll", "data.txt")