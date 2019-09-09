import re
import sys

def contentExtract(sourceFile,sourceFileFormat,outcomeFile):
	with open(sourceFile, mode='r', encoding=sourceFileFormat) as input:
		with open(outcomeFile, mode='w', encoding="utf-8") as output:
			lines =input.readlines()
			for line in lines:
				content =re.sub("<.*?>","",line)#提取内容
				content =re.sub("[\\t\\r\\n ]","",content)#去除空格 TAB 换行
				if content:
					output.write(content+"\n")

if __name__=="__main__":
	contentExtract(sys.argv[1],sys.argv[2],sys.argv[3])