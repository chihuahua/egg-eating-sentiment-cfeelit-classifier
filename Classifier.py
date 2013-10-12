#
# Sentiment Classifier for +, neutral, or - based on CFeelIt.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import Breaker

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
    bag = self.breaker.separate(post)

    return 0

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
