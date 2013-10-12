#
# Tests the classifier.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import SlangParser, providers.SentiWordNetProvider

if __name__ == '__main__':
  p = providers.SentiWordNetProvider.SentiWordNetProvider()
  for key in p.dict:
    if p.dict[key] != 2:
      print key, p.dict[key]
  p.saveLexicon('sentiWordNet')
