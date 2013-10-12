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
    pass

  def stem(self, word):
    '''
    Stems a single word.
    '''
    return stemming.lovins.stem(word)
