import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

twitter_engine = IntentDeterminationEngine()

twitter_intent_keywords = [
    "twitter",
    "tweets",
    "tweet messages",
    "twitter messages"
]

for tik in twitter_intent_keywords:
    twitter_engine.register_entity(tik, "TwitterIntentKeyword")
    
# Hashtag
hashtag_pattern = r"(\bwith hashtag\b|\bwith hashtags\b|\bhashtagged\b|\bhashtag\b|\bhashtags\b) (?P<Hashtag>(\w+(?:,\w+)?))"
twitter_engine.register_regex_entity(hashtag_pattern)

# Construct the intent parser
twitter_intent = IntentBuilder("TwitterIntent")\
    .require("TwitterIntentKeyword")\
    .optionally("Hashtag")\
    .build()
    
# Register the intent parser with the engine
twitter_engine.register_intent_parser(twitter_intent)

request = "find twitter by user rdempsey to user kingjames with hashtags python,ruby in jordan tagged with ist.dev from 11/12/13 to 11/13/13"

for intent in twitter_engine.determine_intent(request):
    if intent.get('confidence') > 0:
        print(json.dumps(intent, indent=4))
    else:
        print("")
