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
	      ';)': True,
        '(:': True,
	      '(;': True,
        ':-)': True,
	      '(-:': True,
	      ';-)': True,
	      '(-;': True,
        ':D': True,
        ':-D': True,
        ';D': True,
        ':-{}': True, # blowing a kiss.
        ':*)': True, # clowning.
        ':\')': True, # crying with joy.
        ':\'-)': True, # crying with joy.
        ':-9': True, # delicious.
        ':->': True, # devilish.
        ';->': True, # devilish wink.
        ':->*<-:': True, # french kiss.
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
      # moodEmphasis = len(exclamations) * 5
      moodEmphasis = 3

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
        scoreAddend = 1
        pol = providers.Provider.NEUTRAL
        isStrongNegative = re.match(SpecialWords.strongNegRegex, word)
        isStrongPositive = re.match(SpecialWords.strongPosRegex, word)
        if word in SpecialWords.lexiconExceptions:
          # for this word, override what the lexicons say.
          pol = SpecialWords.lexiconExceptions[word]
        else:
          # get the sentiment for the word.
          pol = lexicon.get(word, providers.Provider.NEUTRAL)

          # now, possibly override the lexicon.
          if isStrongNegative:
            # we have a strong negative word.
            pol = providers.Provider.NEGATIVE
          if isStrongPositive:
            # we have a strong positive word.
            pol = providers.Provider.POSITIVE

          if negationStatus and not isStrongPositive and not isStrongNegative:
            # negate sentiment since a negator was recently encountered.
            if pol == providers.Provider.NEGATIVE:
              pol = providers.Provider.POSITIVE
            elif pol == providers.Provider.POSITIVE:
              pol = providers.Provider.NEGATIVE

        scoreAddend = 1
        # if this sentiment is non-neutral, potentially apply emphasis.
        if pol != providers.Provider.NEUTRAL:
          # emphasize the sentiment of this word.
          scoreAddend *= moodEmphasis

        if isStrongNegative or isStrongPositive:
          # if we have a strong word, add more to its polarity.
          scoreAddend *= 5
        if i != 0 and re.match(SpecialWords.strongAdverbRegex, words[i - 1]):
          # if the word is preceded by a strong adverb, add more to its polarity.
          scoreAddend *= 5

        # update the vote by this lexicon.
        lexCounts[num][pol] += scoreAddend

    tweetLabels = [providers.Provider.NEUTRAL] * numLexicons
    for num, lexCount in enumerate(lexCounts):

      highestCategory = max(lexCount)
      if 3 * highestCategory == sum(lexCount):
        # all the categories have equal numbers of votes. neutral.
        tweetLabels[num] = providers.Provider.NEUTRAL
      else:
        # chose the category with the most votes.
        tweetLabels[num] = lexCount.index(highestCategory)

      if lexCount[providers.Provider.NEGATIVE] == \
         lexCount[providers.Provider.POSITIVE] and \
            lexCount[providers.Provider.NEGATIVE] > \
                lexCount[providers.Provider.NEUTRAL]:
        # if tie, label tweet as neutral.
        tweetLabels[num] = providers.Provider.NEUTRAL

    tweetLabel = max(set(tweetLabels), key=tweetLabels.count)
    if tweetLabels.count(providers.Provider.NEGATIVE) == \
        tweetLabels.count(providers.Provider.POSITIVE):
      # if same number of positives and negatives, then tweet is neutral.
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
