#
# Sentiment Classifier for +, neutral, or - based on CFeelIt.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import json
import Breaker, providers.Providers

class Classifier:

  def __init__(self):
    '''
    Creates a new classifier.
    '''
    self.breaker = Breaker.Breaker()

    # mapping of emoticons to mood.
    # False is negative, True is positive.
    self.emoticons = {
        # positive moods.
        '__/__': True, # applause
        '<>': True, # clap
        ':)': True,
        ':-)': True,
        ':D': True,
        ';D': True,
        ':-{}': True, # blowing a kiss.
        ':*)': True, # clowning.
        ':\')': True, # crying with joy.
        ':\'-)': True, # crying with joy.
        ':-9': True, # delicious.
        ':->': True, # devilish.
        ';->': True, # devilish wink.
        ':->*<-:': True, # french kiss.
        ':-)*(-:': True, # kiss.
        'XD': True, # laughing.
        'XO': True, # laughing.
        '(Y)': True, # liking.
        '=)': True,
        '@5': True, # high 5.
        'hi5': True,

        # negative moods.
        ':(': False,
        ':-(': False,
        ':-|': False,
        ':@': False, # angry
        ':-@': False, # angry
        'D:': False,
        '\-O': False, # bored.
        ':-C': False,
        ':C': False,
        ':\'(': False, # crying.
        ':\'-(': False, # crying.
        '(//_\')': False, # emo.
        'd//_-b': False, # emo with headset.
        ':-6': False, # exhausted.
        ':-\\': False,
        ':\\': False,
        'D;': False,
    }

    # initialize lexicon.
    ps = providers.Providers.providers
    self.lexicons = []
    for provider in ps:
      # add in dictionary for this provider.
      rawFile = open('providers/lexicons/' + provider.name + '.json')
      dictionary = json.load(rawFile)
      self.lexicons.append(dictionary)

  def classify(self, post):
    '''
    Takes a post and classifies its mood.
    @param post A string to classify. For instance, maybe it's a sentence.
    @return 1 for positive, 0 for neutral, -1 for negative.
    '''

    # if emoticon found, we can classify post immediately.
    emoticonMood = self.detectMoodByEmoticon(post)
    if emoticonMood != 0:
      return emoticonMood

    # turn the post into a bag of words.
    words = self.breaker.separate(post)

    lexCounts = [[0 for i in range(3)] for j in range(4)]
    lexicons = self.lexicons
    for word in words:
      for num, lexicon in enumerate(lexicons):
        pol = lexicon.get(word, -1)

        # this word is in dictionary, so we'll incorporate its rating.
        if pol > -1:
          lexCounts[num][pol] += 1
        else:
          lexCounts[num][2] += 1

    tweetLabels = [2]*4
    for num,lexCount in enumerate(lexCounts):
      tweetLabels[num] = lexCount.index(max(lexCount))
      if lexCount[0] == lexCount[1] and lexCount[0] > lexCount[2]:
        tweetLabels[num] = 2

      # print tweet labels
      print tweetLabels[num]

    tweetLabel = max(set(tweetLabels), key=tweetLabels.count)
    if tweetLabels.count(0)==2 and tweetLabels.count(1)==2:
      tweetLabel = 2

    return tweetLabel

  def detectMoodByEmoticon(self, post):
    '''
    Detects the mood of a post based solely from the emoticon.
    @param post The post to parse.
    @return 1 if positive, 0 if not sure, -1 if negative.
    '''
    for emoticon in self.emoticons:
      if post.find(emoticon) != -1:
        # Feeling found.
        return 1 if self.emoticons[emoticon] else -1

    # no emoticon found.
    return 0
