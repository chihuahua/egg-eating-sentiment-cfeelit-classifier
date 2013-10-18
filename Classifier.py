#
# Sentiment Classifier for +, neutral, or - based on CFeelIt.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import Breaker, SpecialWords, providers.Providers
import re

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
        '(:': True,
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
        '=-)': True,
        '@5': True, # high 5.
        'hi5': True,
        ':]': True,
        ';]': True,

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
        ':/': False,
        'D;': False,
    }

    # initialize lexicon.
    provs = providers.Providers.providers
    self.lexicons = [provider.fetchLexicon() for provider in provs]

    # matches only letters.
    self.punctuationRegex = re.compile('\W+')

    # matches only question marks
    self.questionMarkRegex = re.compile('\?')

    # matches only exclamation marks.
    self.exclamationRegex = re.compile('!')

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

    if not words:
      # nothing to latch off of. we can only say neutral.
      return providers.Provider.NEUTRAL

    # store votes of the lexicons.
    lexCounts = [[0 for i in range(3)] for j in range(4)]
    lexicons = self.lexicons
    numLexicons = len(lexicons)

    # whether we should currently negate.
    negationStatus = False

    # the factor to multiply all the sentiment-laden scores.
    moodEmphasis = 1

    exclamations = re.findall(self.exclamationRegex, post)
    if exclamations:
      # exclamation mark found. emphasize sentiments based on how many.
      moodEmphasis = len(exclamations) * 5

    for i, word in enumerate(words):
      if word in SpecialWords.negationWords:
        # possibly negate subsequent words if the current one is a negator.
        negationStatus = True
        for j in range(i, len(words)):
          if self.punctuationRegex.match(words[j]) or words[j] in SpecialWords.reverseWords:
            # found either a punctuation mark or a special word.
            if re.findall(self.questionMarkRegex, words[j]):
              # we end with a question mark. don't negate.
              negationStatus = False

            # we found a stopping point.
            break

        # don't evaluate negators.
        continue

      if self.punctuationRegex.match(word) or word in SpecialWords.reverseWords:
        # only punctuation and no words. or reversal word. end negation.
        negationStatus = False
        continue

      for num, lexicon in enumerate(lexicons):
        # get the sentiment for the word.
        pol = lexicon.get(word, -1)

        # this word is in dictionary, so we'll incorporate its rating.
        if pol > -1:
          if negationStatus:
            # negate sentiment since a negator was recently encountered.
            if pol == providers.Provider.NEGATIVE:
              pol = providers.Provider.POSITIVE
            elif pol == providers.Provider.POSITIVE:
              pol = providers.Provider.NEGATIVE

          # if this sentiment is non-neutral, potentially apply emphasis.
          scoreAddend = 1
          if pol != providers.Provider.NEUTRAL:
            # emphasize the sentiment of this word.
            scoreAddend *= moodEmphasis

          lexCounts[num][pol] += scoreAddend
        else:
          lexCounts[num][providers.Provider.NEUTRAL] += 1

    tweetLabels = [providers.Provider.NEUTRAL] * numLexicons
    for num, lexCount in enumerate(lexCounts):
      tweetLabels[num] = lexCount.index(max(lexCount))
      if lexCount[providers.Provider.NEGATIVE] == \
         lexCount[providers.Provider.POSITIVE] and \
            lexCount[providers.Provider.NEGATIVE] > \
                lexCount[providers.Provider.NEUTRAL]:
        # if tie, label tweet as neutral.
        tweetLabels[num] = providers.Provider.NEUTRAL

    tweetLabel = max(set(tweetLabels), key=tweetLabels.count)
    halfNumLexicons = numLexicons / 2
    if tweetLabels.count(providers.Provider.NEGATIVE) == halfNumLexicons and \
        tweetLabels.count(providers.Provider.POSITIVE) == halfNumLexicons:
      # if 2 positives and 2 negatives, then tweet is neutral.
      tweetLabel = providers.Provider.NEUTRAL

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
