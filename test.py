#
# Tests the classifier.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import Classifier
import csv, re

def filterTweet(tweet):
  '''
  Filters a tweet.
  '''
  return re.sub(
    r'(@\w+)\b|(\[link\])|(\[\d+ comment\])',
    '',
    tweet
  )

if __name__ == '__main__':
  # create a classifier.
  c = Classifier.Classifier()

  # open the file containing our testing data.
  testFile = open('data/testing.csv', 'r')

  # read the data through a csv parser.
  reader = csv.reader(testFile)

  # each row contains a testing item.
  for row in reader:
    print filterTweet(row[1])

