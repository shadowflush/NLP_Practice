

def loadDict(filePath):
	dict ={}
	with open(filePath,mode ='r',encoding='utf-8') as input:
		allWord =input.readline()
		wordList =allWord.split(' ')
		for i in wordList:
			dict[i] =1
	return dict

def backwardSeg(dict, sentence, wordMaxLength):
	end =len(sentence)-1
	outcome =[]
	while end >=0:
		for i in range(1,wordMaxLength+1)[::-1]:
			if end -i+1 >=0 and (sentence[end-i+1:end+1] in dict) or i ==1:
				outcome.append(sentence[end-i+1:end+1])
				end -=i
				break
	outcome.reverse()
	return outcome
	

def main(sourceFile,outcomeFile,wordMaxLength):
	dict =loadDict("word.dict")
	with open(sourceFile, mode='r', encoding="utf-8") as input:
		lines =input.readlines()
		with open(outcomeFile, mode='w', encoding="utf-8") as output:
			for line in lines:
				segSentence =backwardSeg(dict,line[:-1],wordMaxLength)
				for i in segSentence:
					output.write(i+"\n")
	eva =evaluate(dict,"data.out")
	print("Precision: %f\n" %eva[0])
	print("Recall: %f\n" %eva[1])
	print("F-measure: %f\n" %eva[2])
	
def evaluate(standardDict, evaluatedFile):
	standardDictCopy =standardDict.copy()
	with open(evaluatedFile, mode='r', encoding="utf-8") as file:
		words =file.readlines()
		countAll,countRight1,countRight2 =0,0,0
		for word in words:
			countAll +=1
			word =word[:-1]
			if word in standardDict:
				countRight1+=1
				if standardDictCopy[word] ==1:
					countRight2+=1
					standardDictCopy[word] =0
	P =countRight1/countAll
	R =countRight2/len(standardDict)
	return (P,R,2*P*R/(P+R))
	
main("data.txt","data.out",3)


	