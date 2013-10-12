#
# Script that uses the providers to generate the lexicons.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import Providers

if __name__ == '__main__':

  # have all the providers create a new lexicon (dictionary) to be stored in
  # the providers/lexicons directory.
  for provider in Providers.providers:
    provider.makeDictionary()
    provider.saveLexicon()
