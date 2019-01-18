import os
from sys import exit
import atexit
from scutils.log_factory import LogFactory
from intents import twitter, facebook
import json
import re
import es_query_generator as esqg


class MLSearch:
    """MLSearch class"""
    def __init__(self):
        """Initialize the MLSearch class."""
        self.logger = self._create_logger()
        self.es_use_ssl = os.getenv('ES_USE_SSL', 'false')
        self.es_host = os.getenv('ES_HOST')
        self.es_index = os.getenv('ES_INDEX')
        self.es_doc_type = os.getenv('ES_DOC_TYPE', 'document')
        self.from_date_search = None
        self.to_date_search = None
        self.rule_tag_search = None
        self.app_id_search = None
        self.campaign_id_search = None
        self.project_id_search = None
        self.project_version_id_search = None
        self.node_id_search = None

        def send_exit_message():
            """Send an exit message when ML Search stops running."""
            self.logger.info("ML Search closing down.")

        atexit.register(send_exit_message)

    # Utility Functions
    # =================

    @staticmethod
    def _create_logger():
        """
        Create a logger.

        :return: logger
        """
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        log_dir = os.getenv('LOG_DIR', './logs')
        log_file_name = os.getenv('LOG_FILE_NAME', 'ml_search.log')

        logger = LogFactory.get_instance(json=True,
                                         stdout=False,
                                         name='ml-search',
                                         level=log_level,
                                         dir=log_dir,
                                         file=log_file_name)
        return logger

    # Ops Functions
    # =============

    def _compile_search_patterns(self):
        """Compile the regex search patterns"""
        self.logger.info("Compiling search patterns")

        # From date
        self.from_date_search = re.compile(r"(from (\d+/\d+/\d+))")

        # From date
        self.to_date_search = re.compile(r"(to (\d+/\d+/\d+))")

        # Rule tag
        self.rule_tag_search = re.compile(r"(\btag\b|\brule tag\b|\btagged with\b|\bwith rule tag\b) (\b+)")

        # App ID
        self.app_id_search = re.compile("(appid|app id) (\b+)")

        # Campaign ID
        self.campaign_id_search = re.compile("(campaignid|campaign id|campaign_id) (\b+)")

        # Project ID
        self.project_id_search = re.compile("(projectid|project id|project_id) (\b+)")

        # Project Version ID
        self.project_version_id_search = re.compile("(projectversionid|project version id|project_version_id) (\b+)")

        # Node ID
        self.node_id_search = re.compile("(nodeid|node id|node_id) (\b+)")

    def determine_users_intent(self, query):
        self.logger.info("Determining the users intent")

        intent = twitter.use_twitter_intent(query)

        if intent is None:
            intent = facebook.use_facebook_intent(query)

            if intent is None:
                self.logger.warning("Unable to determine intent for query: {}".format(query))
                intent = "I don't understand what you're asking for"

        return intent

    def get_additional_intent_entities(self, query, intent):
        """
        Add additional extracted entities to the provided intent.

        :param query: user's query to parse
        :param intent: intent object
        :return: enriched_intent: original intent enriched with additional entities
        """
        self.logger.info("Adding additional entities to the intent")
        # Load the intent as a dict for appending
        enriched_intent = json.loads(intent.encode('utf-8'))

        # From Date
        from_date = re.findall(self.from_date_search, query)
        if from_date:
            enriched_intent['FromDate'] = from_date[0][1]

        # To Date
        to_date = re.findall(self.to_date_search, query)
        if to_date:
            enriched_intent['ToDate'] = to_date[0][1]

        # Rule Tag
        rule_tag = re.findall(self.rule_tag_search, query)
        if rule_tag:
            enriched_intent['RuleTag'] = rule_tag[0][1]

        # Appid
        app_id = re.findall(self.app_id_search, query)
        if app_id:
            enriched_intent['AppID'] = app_id[0][1]

        # CampaignID
        campaign_id = re.findall(self.campaign_id_search, query)
        if campaign_id:
            enriched_intent['CampaignID'] = campaign_id[0][1]

        # Project ID
        project_id = re.findall(self.project_id_search, query)
        if project_id:
            enriched_intent['ProjectID'] = project_id[0][1]

        # Project Version ID
        project_version_id = re.findall(self.project_version_id_search, query)
        if project_version_id:
            enriched_intent['ProjectVersionID'] = project_version_id[0][1]

        # Node ID
        node_id = re.findall(self.node_id_search, query)
        if node_id:
            enriched_intent['NodeID'] = node_id[0][1]

        return enriched_intent

    def run(self):
        """
        Run the MLSearch
        """
        self.logger.info("ML Search initializing.")
        self._compile_search_patterns()
        # Accept input
        query = input("What would you like to search for: ")

        if query in ['exit', 'goodbye', 'finished', 'done']:
            exit(1)
        else:
            # Get the intent
            intent = self.determine_users_intent(query)

            if intent:
                # Add any additional extracted information
                intent = self.get_additional_intent_entities(query, intent)

                # Log the query and the intent for future training
                self.logger.info("User query input", extra={
                    'user_query': query,
                    'intent': intent
                })

                # Print out the intent
                print("Intent found: \n{}".format(json.dumps(intent, indent=4)))

                # Create an ElasticSearch query from the intent
                es_query = esqg.create_twitter_es_query(intent)

                # Print out the query
                print("ES Query: \n{}".format(json.dumps(es_query, indent=4)))
            else:
                # If we can't figure out what they want, redirect the user to a form that's pre-filled with what
                # we think they were looking for. Keep the original query and what the user typed into the form
                # so we can make it more better
                pass


if __name__ == '__main__':
    # Create an instance of MLSearch
    _ml_search = MLSearch()
    _ml_search.run()
