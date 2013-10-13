#
# Creates providers. Providers offer dictionaries.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import json
import Stemmer

class Provider:

  def __init__(self, lexiconName):
    '''
    Creates a new provider.
    @param lexiconName The name of the lexicon. Can't contain spaces.
    '''

    # name of the lexicon we're generating. can't contain spaces.
    self.name = lexiconName

    # generate this dictionary.
    self.dict = {}

    # for stemming words.
    self.stemmer = Stemmer.Stemmer()

  def fetchLexicon(self):
    '''
    Fetches the lexicon for the provider. A lexicon is a mapping from stemmed
    word to the sentiment score.
    '''
    rawFile = open('providers/lexicons/' + self.name + '.json')
    return json.load(rawFile)

  def saveLexicon(self):
    '''
    Saves the lexicon.
    @param lexiconName The short name of the lexicon. No spaces allowed.
    '''
    # create new file.
    newFile = open('lexicons/' + self.name + '.json', 'w')

    # write json of dictionary to file.
    rawJson = json.dumps(self.dict)
    newFile.write(rawJson)

# constants for negative, positive, neutral.
NEGATIVE = 0
POSITIVE = 1
NEUTRAL = 2
