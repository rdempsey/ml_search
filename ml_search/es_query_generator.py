"""
ElasticSearch Query Generator

Use these methods to create Elasticsearch queries from intents
"""
from collections import defaultdict

# Twitter Doc Types
twitter_doc_type = 'tweet_traptor'

# Facebook Doc Types
fbgraph_entity = 'fbgraph_entity'
fbgraph_feed_item = 'fbgraph_feed_item'
fbgraph_post = 'fbgraph_post'
fbgraph_comment = 'fbgraph_comment'
fbgraph_like = 'fbgraph_like'

# Document Fields - Global
doc_type_field = '_type'
author_field = 'norm.author'
created_at_field = 'norm.timestamp'
text_search_field = 'norm.body'
domain = 'norm.domain'
url = 'norm.url'

# Document Fields - SMData
rule_tag_field = 'meta.rule_matcher.results.rule_tag'
appid_field = 'meta.rule_matcher.results.appid'
campaign_id_field = 'meta.rule_matcher.results.campaign_id'
project_id_field = 'meta.rule_matcher.results.project_id'
project_version_id_field = 'meta.rule_matcher.results.project_version_id'
node_id_field = 'meta.rule_matcher.results.node_id'


def create_twitter_es_query(twitter_intent):
    """
    Create an ElasticSearch query for Twitter data

    :param twitter_intent: the Twitter intent to create the query from
    :return: es_query: ElasticSearch query
    """
    # Twitter-Specific Fields
    recipient_field = 'doc.in_reply_to_screen_name'
    mentioned_user_field = 'meta.username'
    hashtag_field = 'meta.hashtag.results'
    keyword_field = 'meta.rule_matcher.results.value'
    location_field = 'doc.place'

    # Extract the values from the intent
    keyword = twitter_intent.get('Keyword', None)
    hashtag = twitter_intent.get('Hashtag', None)
    author = twitter_intent.get('Author', None)
    recipient = twitter_intent.get('Recipient', None)
    mentioned_user = twitter_intent.get('MentionedUser', None)
    location = twitter_intent.get('Location', None)
    text_search = twitter_intent.get('TextSearch', None)

    # Additional intents
    from_date = twitter_intent.get('FromDate', None)
    to_date = twitter_intent.get('ToDate', None)
    rule_tag = twitter_intent.get('RuleTag', None)
    appid = twitter_intent.get('AppID', None)
    campaign_id = twitter_intent.get('CampaignID', None)
    project_id = twitter_intent.get('ProjectID', None)
    project_version_id = twitter_intent.get('ProjectVersionID', None)
    node_id = twitter_intent.get('NodeID', None)

    # Continue building the filter based on the presence of an intent
    intent_list = ['keyword', 'hashtag', 'author', 'recipient', 'mentioned_user', 'location', 'text_search',
                   'rule_tag', 'appid', 'campaign_id', 'project_id', 'project_version_id', 'node_id']

    additional_intents = dict()

    for intent in intent_list:
        additional_intents[intent] = eval(intent + "_field")

    nested_dict = lambda: defaultdict(nested_dict)

    es_query = nested_dict()
    es_query['type']['value'] = twitter_doc_type
    es_query['query']['bool']['should'] = list()
    es_query['query']['filter'] = list()

    for value, field_value in additional_intents.items():
        d = nested_dict()
        if eval(value):
            d['match'][field_value] = eval(value)
            es_query['query']['bool']['should'].append(d)

    # Dates - a special case
    if from_date and to_date:
        date_dict = nested_dict()
        date_dict['range'][created_at_field]['gte'] = from_date
        date_dict['range'][created_at_field]['lte'] = to_date
        es_query['query']['filter'].append(date_dict)

    return es_query

def create_fb_es_query(facebook_intent):
    """
    Create an ElasticSearch query for Facebook data

    :param facebook_intent: the Facebook intent to create the query from
    :return: es_query: ElasticSearch query
    """
    # Facebook-specific fields
    recipient_field = 'doc.in_reply_to_screen_name'
    mentioned_user_field = 'meta.username'
    location_field = 'doc.place'

    # Extract the values from the intent
    author = facebook_intent.get('Author', None)
    recipient = facebook_intent.get('Recipient', None)
    mentioned_user = facebook_intent.get('MentionedUser', None)
    location = facebook_intent.get('Location', None)
    text_search = facebook_intent.get('TextSearch', None)

    # Additional intents
    from_date = facebook_intent.get('FromDate', None)
    to_date = facebook_intent.get('ToDate', None)
    rule_tag = facebook_intent.get('RuleTag', None)
    appid = facebook_intent.get('AppID', None)
    campaign_id = facebook_intent.get('CampaignID', None)
    project_id = facebook_intent.get('ProjectID', None)
    project_version_id = facebook_intent.get('ProjectVersionID', None)
    node_id = facebook_intent.get('NodeID', None)

    # Continue building the filter based on the presence of an intent
    intent_list = ['author', 'recipient', 'mentioned_user', 'location', 'text_search',
                   'rule_tag', 'appid', 'campaign_id', 'project_id', 'project_version_id', 'node_id']

    additional_intents = dict()

    for intent in intent_list:
        additional_intents[intent] = eval(intent + "_field")

    # Build the query
    nested_dict = lambda: defaultdict(nested_dict)

    es_query = nested_dict()
    es_query['type']['value'] = fbgraph_entity # TODO: replace this with a type lookup
    es_query['query']['bool']['should'] = list()
    es_query['query']['filter'] = list()

    for value, field_value in additional_intents.items():
        d = nested_dict()
        if eval(value):
            d['match'][field_value] = eval(value)
            es_query['query']['bool']['should'].append(d)

    # Dates - a special case
    if from_date and to_date:
        date_dict = nested_dict()
        date_dict['range'][created_at_field]['gte'] = from_date
        date_dict['range'][created_at_field]['lte'] = to_date
        es_query['query']['filter'].append(date_dict)

    return es_query