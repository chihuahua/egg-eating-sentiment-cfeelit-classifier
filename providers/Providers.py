#
# A list of all the providers we are using.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 11, 2013
#

import AfinnProvider, InquirerProvider, SentiWordNetProvider, \
  SubjectivityProvider

# list all of the providers.
providers = [
    AfinnProvider.AfinnProvider(),
    InquirerProvider.InquirerProvider(),
    SentiWordNetProvider.SentiWordNetProvider(),
    SubjectivityProvider.SubjectivityProvider(),
]
