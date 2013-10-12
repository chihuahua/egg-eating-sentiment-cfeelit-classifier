#
# The provider for the subjectivity lexicon. Provides a dictionary
# mapping from stemmed word -> 0, 1, 2 (NEG, POS, NEU)
# @author Dan
# Oct. 11, 2013
#

import Provider

class SubjectivityProvider(Provider.Provider):

  def __init__(self):
    '''
    Creates a new provider for Subjectivity
    '''
    Provider.Provider.__init__(self, 'subjectivity')

  def makeDictionary(self):
    '''
    Makes the dictionary.
    @return the dictionary.
    '''

    f = open('data/subjectivity_lexicon.tff', 'rb')
    rows = f.readlines()
    subjectivity_lexicon = {}
    for row in rows:
      cols = row.split(' ')
      i = cols[2].index('=')
      word = cols[2][i+1:]

      # stem the word.
      word = self.stemmer.stem(word)

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

    self.dict = subjectivity_lexicon
