#
# Sentiment Classifier for +, neutral, or - based on CFeelIt.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import Breaker, SpecialWords, providers.Providers

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
    provs = providers.Providers.providers
    self.lexicons = [provider.fetchLexicon() for provider in provs]

  def classify(self, post):
    '''
    Takes a post and classifies its mood.
    @param post A string to classify. For instance, maybe it's a sentence.
    @return 1 for positive, 0 for neutral, -1 for negative.
    '''

    # if emoticon found, we can classify post immediately.
    emoticonMood = self.detectMoodByEmoticon(post)
    if emoticonMood != providers.Provider.NEUTRAL:
      return emoticonMood

    # turn the post into a bag of words.
    words = self.breaker.separate(post)

    lexCounts = [[0 for i in range(3)] for j in range(4)]
    lexicons = self.lexicons

    # if this variable is positive, then the sentiment scores of words are
    # negated since a recent negation word was encountered.
    negationStatus = 0

    for word in words:
      if word in SpecialWords.negationWords:
        # negate the subsequent 3 words if the current one is a negator.
        negationStatus = 3
        continue

      for num, lexicon in enumerate(lexicons):
        pol = lexicon.get(word, -1)

        # this word is in dictionary, so we'll incorporate its rating.
        if pol > -1:
          if negationStatus:
            # negate sentiment since a negator was recently encountered.
            if pol == providers.Provider.NEGATIVE:
              pol = providers.Provider.POSITIVE
            elif pol == providers.Provider.POSITIVE:
              pol = providers.Provider.NEGATIVE

          lexCounts[num][pol] += 1
        else:
          lexCounts[num][2] += 1

      if negationStatus:
        # decrement negation status since we've seen a word after the negator.
        negationStatus -= 1

    tweetLabels = [2] * 4
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
    @return Provider.POSITIVE if positive, PROVIDER.NEUTRAL if not sure,
        provider.NEGATIVE if negative.
    '''
    moods = providers.Provider
    for emoticon in self.emoticons:
      if post.find(emoticon) != -1:
        # Feeling found.
        return moods.POSITIVE if self.emoticons[emoticon] else moods.NEGATIVE

    # no emoticon found.
    return moods.NEUTRAL
