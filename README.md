# NLP_Practice

chinese_char_seg:（支持GB2312、UTF8）

      #gcc chinese_char_seg.c -o chinese_char_seg
      
      #./chinese_char_seg 源文件路径 编码

max-match:(后向最大匹配分词，最大词长：3)
      
      #python genDictAndSen.py //利用人工分词文件data.conll生成词典(word.dict 词之间空格隔开)，和句子（data.txt 每句一行）
      #python seg.py //对利用word.dict 对data.txt 进行后向最大匹配分词，最大词长取3。结果存于data.out，每词一行。并输出精度、召回率、F值

contentExtract:（简单本地网页内容抽取）

	  #python contentExtract.py 源文件路径 编码格式	结果文件路径
	  （例如）python contentExtract.py "Teaching by Wenliang.html" utf-8 outcome
	  
Ngram:（三元语言模型 coding）
 
	  （解决问题中...目前想法：将所有未出现的N元组作为一个整体考虑）
	  
	  
	  