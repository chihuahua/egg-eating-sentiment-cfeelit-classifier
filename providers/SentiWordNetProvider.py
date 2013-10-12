#
# The provider for the SentiWordNet lexicon. Provides a dictionary
# mapping from stemmed word -> 0, 1, 2 (NEG, POS, NEU)
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import re
import Provider

class SentiWordNetProvider(Provider.Provider):

  def __init__(self):
    '''
    Creates a new provider for SentiWordNet
    '''
    Provider.Provider.__init__(self, 'sentiWordNet')
    self.dict = self.makeDictionary()

  def makeDictionary(self):
    '''
    Makes the dictionary.
    @return the dictionary.
    '''

    # open dictionary file.
    self.dataFile = open("providers/data/SentiWordNet_3.0.0_20130122.txt")

    # our dictionary.
    lexicon = {}

    # ignore the first line.
    self.dataFile.readline()

    for line in self.dataFile:

      # find all words in line.
      words = re.findall(r'\b([a-z\']+)#\d+\b', line)
      words = map(self.stemmer.stem, words)

      # if no words, ignore line.
      if not words:
        continue

      # break up line into useful pieces.
      line = line.split('\t')

      # get the scores.
      scores = [0., 0., 0.]

      # get the SentiWordNet scores.
      scores[Provider.NEGATIVE] = float(line[3])
      scores[Provider.POSITIVE] = float(line[2])
      scores[Provider.NEUTRAL] = 1. - \
          scores[Provider.NEGATIVE] - scores[Provider.POSITIVE]

      # update the scores of each word.
      for word in words:
        if word in lexicon:
          # add up the scores.
          lexicon[word] = [a + b for (a,b) in zip(lexicon[word], scores)]
        else:
          # assign initial values.
          lexicon[word] = scores

    # convert dict to neg, pos, neu.
    for key in lexicon:
      values = lexicon[key]
      maxIndex = 0
      max = values[maxIndex]
      for i in range(1, 3):
        if values[i] > max:
          max = values[i]
          maxIndex = i
      lexicon[key] = maxIndex

    return lexicon
