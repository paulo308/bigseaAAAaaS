
from collections import namedtuple

def before_all(context):
    pass

def after_all(context):
    pass

def before_feature(context, feature):
    pass

def after_feature(context, feature):
    pass

def before_tag(context, tag):
    if tag == 'rest':
        context.settings = namedtuple('settings', 'settings')
        context.settings = context.settings({'data': {}})
        context.request = namedtuple('request', 'registry params')
    

def after_tag(context, tag):
    pass
