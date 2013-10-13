#
# A snippet for running whatever.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import Classifier

if __name__ == '__main__':
  post = 'i lam so in love with Bobby Flay... he is my favorite. RT :  ' \
         'you need a place in Phoenix. We have great peppers here!'

  c = Classifier.Classifier()
  c.classify(post)
