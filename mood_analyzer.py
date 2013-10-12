# assume we have a tweet, 4 lexicon dictionaries stored in lexicons
# 0-neg 1-pos 2-neutral

words = tweet.split()
lexCounts = [[0] for i in range(3)] for j in range(4)
for word in words:
    for num,lexicon in enumerate(lexicons):
	pol = lexicon.get(word)
	if pol:
	    lexCounts[num][pol] += 1
	else:
	    lexCounts[num][2] += 1

tweetLabels = [2]*4
for num,lexCount in enumerate(lexCounts):
    tweetLabels[num] = lexCount.index(max(lexCount))
    if lexCount[0]==lexCount[1] and lexCount[0]>lexCount[2]:
	tweetLabels[num] = 2

tweetLabel = max(set(tweetLabels), key=tweetLabels.count)
if tweetLabels.count(0)==2 and tweetLabels.count(1)==2:
    tweetLabel = 2
