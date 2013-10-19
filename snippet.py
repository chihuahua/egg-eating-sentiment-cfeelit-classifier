#
# A snippet for running whatever.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import Breaker, Classifier

if __name__ == '__main__':
  post = '  Great Stanford course. Thanks for making it available to the ' \
         'public! Really helpful and informative for starting off!'
  # post = 'not bad'

  b = Breaker.Breaker()
  c = Classifier.Classifier()
  print c.classify(post)

  # print the classification of each word.
  # words = b.separate(post)
  # for word in words:
  #   print word + ': ' + `c.classify(word)`
