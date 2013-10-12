#
# Script that uses the providers to generate the lexicons.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import AfinnProvider, InquirerProvider, SentiWordNetProvider, \
    SubjectivityProvider

if __name__ == '__main__':

  # list all of the providers.
  providers = [
      AfinnProvider.AfinnProvider(),
      InquirerProvider.InquirerProvider(),
      SentiWordNetProvider.SentiWordNetProvider(),
      SubjectivityProvider.SubjectivityProvider(),
  ]

  # have all the providers create a new lexicon (dictionary) to be stored in
  # the providers/lexicons directory.
  for provider in providers:
    provider.makeDictionary()
    provider.saveLexicon()
