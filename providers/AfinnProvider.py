#
# The provider for the Afinn lexicon. Provides a dictionary
# mapping from stemmed word -> 0, 1, 2 (NEG, POS, NEU)
# @author Dan
# Oct. 11, 2013
#

import Provider

class AfinnProvider(Provider.Provider):

  def __init__(self):
    '''
    Creates a new provider for Subjectivity
    '''
    Provider.Provider.__init__(self, 'afinn')

  def makeDictionary(self):
    '''
    Makes the dictionary.
    @return the dictionary.
    '''

    afinn_lexicon = dict(map(lambda (k,v): (self.stemmer.stem(k),
                                            self.num_to_polar(int(v))),
        [line.split('\t') for line in open("data/afinn_lexicon.txt")]))
    self.dict = afinn_lexicon

  def num_to_polar(self, x):
    '''
    Helper function for making dictionary.
    @x The number for which to obtain the polarity.
    '''
    if x > 0:
      return Provider.POSITIVE
    elif x < 0:
      return Provider.NEGATIVE
    else:
      return Provider.NEUTRAL
