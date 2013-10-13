#
# Breaks a post into a bag of words.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import re, string
import SlangParser, SpecialWords, Stemmer

# mapping from contraction to expansion.
Contractions = {
    "i'll": "is not",
    "it'?ll": "it will",
    "'?twas": "it was",
    "she'll": "she will",
    "why'?d": "why would",
    "don'?t": "do not",
    "should'?ve": "should have",
    "didn'?t": "did not",
    "they'?ve": "they have",
    "who'?ll": "who will",
    "won'?t": "will not",
    "we'd": "we would",
    "couldn'?t": "could not",
    "how'?ll": "how will",
    "why'?s": "why is",
    "shan'?t": "shall not",
    "doesn'?t": "does not",
    "might'?ve": "might have",
    "how'?s": "how is",
    "he'?s": "he is",
    "when'?s": "when is",
    "it's": "it is",
    "where'?d": "where would",
    "what'?d": "what would",
    "he'?d": "he would",
    "can'?t": "can not",
    "how'?d": "how would",
    "there'?s": "there is",
    "shouldn'?t": "should not",
    "they'?ll": "they will",
    "when'?ll": "when will",
    "where'?ll": "where will",
    "you'?re": "you are",
    "we're": "we are",
    "mightn'?t": "might not",
    "i'?ve": "i have",
    "'?tis": "it is",
    "what'?s": "what is",
    "who'?s": "who is",
    "where'?s": "where is",
    "they'?d": "they would",
    "ain'?t": "is not",
    "you'?ve": "you have",
    "would'?ve": "would have",
    "that'?ll": "that will",
    "aren'?t": "are not",
    "who'?d": "who would",
    "he'll": "he will",
    "must'?ve": "must have",
    "you'?d": "you would",
    "they'?re": "they are",
    "we'?ll": "we will",
    "why'?ll": "why will",
    "weren'?t": "were not",
    "wasn'?t": "was not",
    "wouldn'?t": "would not",
    "hasn'?t": "has not",
    "she'?d": "she would",
    "you'?ll": "you will",
    "i'd": "i would",
    "could'?ve": "could have",
    "she'?s": "she is",
    "i'm": "i am",
    "when'?d": "when would",
    "mustn'?t": "must not",
    "isn'?t": "is not",
    "that's": "that is"
}

class Breaker:

  def __init__(self):
    '''
    Creates a new breaker.
    '''

    # set of punctuation marks.
    self.transTable = string.maketrans("","")

    # used for parsing slang.
    self.slangParser = SlangParser.SlangParser()

    # used for stemming individual words.
    self.stemmer = Stemmer.Stemmer()

  def removePunctuation(self, post):
    '''
    Removes the punctuation marks from a post.
    @param post The string from which to remove punctuation.
    '''
    return post.translate(self.transTable, SpecialWords.punctuation)

  def replaceExtensions(self, post):
    '''
    Replaces extensions with just single letters. Extensions occur when letters
    are repeated in a string (appear 3 or more times) for emphasis.
    @param post The post from which extensions are replaced.
    '''

    return re.sub(
        r'\b(?P<f>\w*)(?P<l>\w)(?!\2)(?P<r>\w)(?P=r){2,}(?P<s>\w*)\b',
        r'\1\2\3\4 \1\2\3\4',
        post
    )

  def replaceContractions(self, post):
    '''
    Replaces the contractions in the string @post with their expansions.
    @param post The post from which contractions are replaced.
    '''

    for contraction in Contractions:
      post = re.sub(contraction, Contractions[contraction], post)
    return post

  def separate(self, post):
    '''
    Breaks a post into a bag of words.
    @param post The string to break. This string could be say a raw tweet.
    @return a list of strings denoting the words.
    '''

    # trim the post, replace any slang.
    post = post.strip(' \t\n\r')
    post = self.slangParser.removeSlang(post)

    # replace any extensions and duplicate them for emphasis.
    post = self.replaceExtensions(post)

    # replace any contractions such as don't with their expansions.
    post = self.replaceContractions(post)

    # remove punctuation.
    post = self.removePunctuation(post)

    # make lowercase.
    post = post.lower()

    # split into spaces, get rid of empty strings.
    bag = filter(None, post.split(' '))

    # remove stop words.
    bag = filter(lambda word: word not in SpecialWords.stopWords, bag)

    # stem words.
    bag = map(self.stemmer.stem, bag)

    # return bag of words.
    return bag
