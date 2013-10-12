
f = open('providers/data/subjectivity_lexicon.tff', 'rb')
rows = f.readlines()
subjectivity_lexicon = {}
for row in rows:
    cols = row.split(' ')
    i = cols[2].index('=')
    word = cols[2][i+1:]
    if subjectivity_lexicon.get(word):
	continue
    j = cols[5].index('=')
    polar = cols[5][j+1:j+9]
    if polar == "positive":
	subjectivity_lexicon[word] = 1
    elif polar == "negative":
	subjectivity_lexicon[word] = 0
    else:
	subjectivity_lexicon[word] = 2
print subjectivity_lexicon
