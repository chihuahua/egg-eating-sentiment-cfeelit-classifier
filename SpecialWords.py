#
# Lists words that harbor special meaning.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

negationWords = frozenset([
    'ain\'t', 'aren\'t', 'cannot', 'can\'t', 'cant', 'didnt', 'didn\'t' 'dont',
    'doesn\'t', 'don\'t', 'hadn\'t', 'hasn\'t', "haven't", "isn't", "mustn't",
    'no', 'neither', 'nor', 'not', "shan't", "shouldn't", "wasn't", "weren't"
])

punctuation = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'

stopWords = frozenset(['a', 'about', 'above', 'after', 'again', 'against',
                      'all',
                'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because',
                'been', 'before', 'being', 'below', 'between', 'both', 'but',
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
                'very', 'was', 'we', "we'd", "we'll", "we're", "we've",
                'were', 'what', "what's", 'when', "when's", 'where',
                "where's", 'which', 'while', 'who', "who's", 'whom', 'why',
                "why's", 'with', "won't", 'would', "wouldn't", 'you',
                "you'd", "you'll", "you're", "you've", 'your', 'yours',
                'yourself', 'yourselves'])
