#
# The provider for the SentiWordNet lexicon. Provides a dictionary
# mapping from stemmed word -> 0, 1, 2 (NEG, POS, NEU)
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import re
import Provider

class SentiWordNetProvider:

  def __init__(self):
    '''
    Creates a new provider for SentiWordNet
    '''
    self.dataFile = open("providers/data/SentiWordNet_3.0.0_20130122.txt")
    self.dict = self.makeDictionary()

  def getDictionary(self):
    '''
    Returns a dictionary.
    '''
    pass

  def makeDictionary(self):
    '''
    Makes the dictionary.
    @return the dictionary.
    '''

    # our dictionary.
    dict = {}

    # ignore the first line.
    self.dataFile.readline()

    for line in self.dataFile:

      # find all words in line.
      words = re.findall(r'([a-z\']+)#\d+', line)

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
        if word in dict:
          # add up the scores.
          dict[word] = [a + b for (a,b) in zip(dict[word], scores)]
        else:
          # assign initial values.
          dict[word] = scores

    # convert dict to neg, pos, neu.
    for key in dict:
      values = dict[key]
      minIndex = 0
      min = values[minIndex]
      for i in range(1, 3):
        if values[i] < min:
          min = values[i]
          minIndex = i
      dict[key] = minIndex

    print dict
    return dict


