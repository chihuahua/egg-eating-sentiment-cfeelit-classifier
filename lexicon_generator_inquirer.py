import sys
import csv

inquirer_lexicon = {}
with open('inquirerbasic.csv', 'rb') as f:
    csvreader = csv.reader(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
    for row in csvreader:
	word = row[0]
	if len(word)>2:
	    if word[-2:]=="#1":
	        word = word[:-2]
   	    if len(word)>2 and word[-2]=="#":
	        continue
	word = word.lower()
	if row[1]:
	    inquirer_lexicon[word] = 1
	elif row[2]:
	    inquirer_lexicon[word] = 0
print inquirer_lexicon
	    
        

