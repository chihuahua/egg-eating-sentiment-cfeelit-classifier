#
# Script that uses the providers to generate the lexicons.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import InquirerProvider, SentiWordNetProvider

if __name__ == '__main__':

  # list all of the providers.
  providers = [
      InquirerProvider.InquirerProvider(),
      SentiWordNetProvider.SentiWordNetProvider(),
  ]

  # have all the providers create a new lexicon (dictionary) to be stored in
  # the providers/lexicons directory.
  map(lambda provider: provider.saveLexicon(), providers)
