# args: [target language] [target abbrev]

import sys
from googletrans import Translator
translator = Translator()

file = 'EnglishErrorList.txt'#sys.argv[1]
language = sys.argv[1]
langAbbrev = sys.argv[2]
f = open('LanguageData/'+file,'r')

line=f.readline()
errors = list()
#errors = line.split(',')
while line != '':
	errors.append(line.strip())
	line = f.readline()

new = open('LanguageData/'+language+'ErrorList.txt','w')

index = 0
percent = 0
for i in errors:
	translation = (translator.translate(i, dest=langAbbrev))
	new.write(str(translation.text)+'\n')
	index += 1
	percent = 100*index/len(errors)
	print(str(percent)+'% completed')
f.close()
new.close()
