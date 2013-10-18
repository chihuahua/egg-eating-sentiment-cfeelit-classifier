#
# Lists words that harbor special meaning.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import providers.Provider

negationWords = frozenset([
    'no', 'neither', 'nor', 'not', 'never'
])

punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'

reverseWords = frozenset(['but', 'altho', 'although', 'tho', 'though', 'yet'])

stopWords = frozenset(['a', 'about', 'above', 'after', 'again', 'against',
                      'all',
                'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because',
                'been', 'before', 'being', 'below', 'between', 'both',
                'by', 'could', 'did', 'do', 'does', 'doing', 'down',
                'during', 'each', 'few', 'for', 'from', 'further', 'had',
                'has', 'have', 'having', 'he', "he'd", "he'll", "he's",
                'her', 'here', "here's", 'hers', 'herself', 'him', 'himself',
                'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've",
                'if', 'in', 'into', 'is', 'it', "it's", 'its',
                'itself', "let's", 'me', 'more', 'most', 'my', 'myself',
                'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought',
                'our', 'ours', '', 'ourselves', 'out', 'over', 'own', 'same',
                'she', "she'd", "she'll", "she's", 'should', 'so', 'some',
                'such', 'than', 'that', "that's", 'the', 'their', 'theirs',
                'them', 'themselves', 'then', 'there', "there's", 'these',
                'they', "they'd", "they'll", "they're", "they've", 'this',
                'those', 'through', 'to', 'too', 'under', 'until', 'up',
                'very', 'was', 'we',
                'were', 'what', "what's", 'when', "when's", 'where',
                'which', 'while', 'who', "who's", 'whom', 'why',
                'with', "won't", 'would', 'you', 'your', 'yours',
                'yourself', 'yourselves', 'id', 'im', 'lets', 'heres',
                'hows', 'shes', 'thats', 'their\'s', 'weve', 'whens',
                'whats', 'whos', 'whys', 'youd', 'youll', 'wont', 'ive',
                'ever', 'take', 'took', 'taken', 'since', 'due to', 'hence',
                'will'])

# exceptions for lexicons. these exceptions override. they'll be stemmed later.
lexiconExceptions = {
    'rock': providers.Provider.POSITIVE,
    'ha': providers.Provider.POSITIVE,
    'hah': providers.Provider.POSITIVE,
    'hahah': providers.Provider.POSITIVE,
    'hahahah': providers.Provider.POSITIVE,
}
