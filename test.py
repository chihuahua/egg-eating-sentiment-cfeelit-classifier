#
# Tests the classifier.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import Classifier

if __name__ == '__main__':
  c = Classifier.Classifier()

  # post to classify.
  post = 'i am not happy and not sad.'

  print c.classify(post)
