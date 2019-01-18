import json
from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

facebook_keywords = [
    "facebook",
    "facebook pages",
    "facebook posts",
    "facebook users",
    "facebook likes"
]

facebook_types = [
    "page",
    "pages",
    "public page",
    "public pages",
    "profile",
    "profiles",
    "user",
    "users",
    "post",
    "posts",
    "like",
    "likes"
]

# Instantiate an IntentDeterminationEngine
facebook_engine = IntentDeterminationEngine()

# Register each keyword with the engine
for tk in facebook_keywords:
    facebook_engine.register_entity(tk, "FacebookKeyword")

# Register each type with the engine
for ft in facebook_types:
    facebook_engine.register_entity(ft, "FacebookType")

# Create a regex to parse out the search query
facebook_engine.register_regex_entity("(page|pages|public page|public pages|profile|profiles|user|users|post|posts|like|likes) (?P<FacebookSearchQuery>(\w+))")

# Construct the intent parser
facebook_intent = IntentBuilder("FacebookIntent")\
    .require("FacebookKeyword")\
    .require("FacebookType")\
    .optionally("FacebookSearchQuery")\
    .build()

# Register the intent parser with the engine
facebook_engine.register_intent_parser(facebook_intent)


def use_facebook_intent(request):
    for intent in facebook_engine.determine_intent(request):
        if intent.get('confidence') > 0:
            return json.dumps(intent, indent=4)
        else:
            return None
