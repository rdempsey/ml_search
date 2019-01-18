import json
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

# Instantiate an IntentDeterminationEngine
twitter_engine = IntentDeterminationEngine()

twitter_intent_keywords = [
    "twitter",
    "tweets",
    "tweet messages",
    "twitter messages"
]

for tik in twitter_intent_keywords:
    twitter_engine.register_entity(tik, "TwitterIntentKeyword")

# Keyword
twitter_engine.register_regex_entity("(with keyword|with keywords|keyword|keywords) (?P<Keyword>(\b+(?:,\b+)?))")

# Hashtag
hashtag_pattern = r"(\bwith hashtag\b|\bwith hashtags\b|\bhashtagged\b|\bhashtag\b|\bhashtags\b) (?P<Hashtag>(\b+))"
twitter_engine.register_regex_entity(hashtag_pattern)

# Author
author_pattern = r"(\bby user\b|\bby username\b|\bby user name\b|\bby userid\b|\bby user id\b|\bfrom user\b|\bfrom username\b|\bfrom user name\b|\bfrom userid\b|\bfrom user id\b) (?P<Author>(\b+))"
twitter_engine.register_regex_entity(author_pattern)

# Recipient
recipient_pattern = r"(\bto user\b|\bto username\b|\bto user name\b|\bto userid\b|\bto user id\b|\bto user\b|\bto username\b|\bto user name\b|\bto userid\b|\bto user id\b) (?P<Recipient>(\b+))"
twitter_engine.register_regex_entity(recipient_pattern)

# Mentioning
mentioned_user_pattern = r"(\babout user\b|\babout username\b|\babout user name\b|\babout userid\b|\babout user id\b|\babout user\b|\babout username\b|\babout user name\b|\babout userid\b|\babout user id\b) (?P<MentionedUser>(\b+))"
twitter_engine.register_regex_entity(mentioned_user_pattern)

# Location
twitter_engine.register_regex_entity("in (?P<Location>(\b+))")

# TextSearch
twitter_engine.register_regex_entity("(containing|with text) (?P<TextSearch>(\b+))")


# Construct the intent parser
twitter_intent = IntentBuilder("TwitterIntent")\
    .require("TwitterIntentKeyword")\
    .optionally("Keyword")\
    .optionally("Hashtag")\
    .optionally("Author")\
    .optionally("Recipient")\
    .optionally("MentionedUser")\
    .optionally("Location")\
    .optionally("TextSearch")\
    .build()

# Register the intent parser with the engine
twitter_engine.register_intent_parser(twitter_intent)


def use_twitter_intent(request):
    for intent in twitter_engine.determine_intent(request):
        if intent.get('confidence') > 0:
            return json.dumps(intent, indent=4)
        else:
            return None
