#
# Stems a word using Lovins algorithm.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import stemming.lovins

class Stemmer:
  
  def __init__(self):
    '''
    Creates a new stemmer.
    '''
    self.exceptions = {
      'fucking': 'fucking',
      'freaking': 'freaking'
    }

  def stem(self, word):
    '''
    Stems a single word.
    '''
    if not word:
      # word is empty.
      return ''

    if word in self.exceptions:
      # respect exceptions.
      return self.exceptions[word]

    return stemming.lovins.stem(word)
