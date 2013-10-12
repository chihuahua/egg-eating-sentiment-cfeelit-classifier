def num_to_polar(x):
    if x>0:
	return 1
    elif x<0:
	return 0
    else:
	return 2

afinn_lexicon = dict(map(lambda (k,v): (k,num_to_polar(int(v))), 
           [ line.split('\t') for line in open("providers/data/afinn_lexicon.txt") ]))
print afinn_lexicon
