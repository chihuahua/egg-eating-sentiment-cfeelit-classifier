#
# The provider for the Inquirer lexicon.
# @author Dan
# Oct. 11, 2013
#

import csv
import Provider

class InquirerProvider(Provider.Provider):

  def __init__(self):
    '''
    Creates a new provider for the Inquirer
    '''
    Provider.Provider.__init__(self, 'inquirer')

  def makeDictionary(self):
    '''
    Makes the dictionary.
    @return the dictionary.
    '''

    inquirer_lexicon = {}
    with open('data/inquirerbasic.csv', 'rb') as f:
      csvreader = csv.reader(
          f, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONE)
      for row in csvreader:
        word = row[0]
        if len(word) > 2:
          if word[-2:] == "#1":
            word = word[:-2]
          if len(word) > 2 and word[-2] == "#":
            continue

        # stem the word after lower casing it.
        word = self.stemmer.stem(word.lower())
        if row[1]:
          inquirer_lexicon[word] = 1
        elif row[2]:
          inquirer_lexicon[word] = 0

    self.dict = inquirer_lexicon
