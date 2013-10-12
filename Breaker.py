#
# Breaks a post into a bag of words.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import re, string
import SlangParser, SpecialWords, Stemmer

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
