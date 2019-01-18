import pytest
from mock import MagicMock, patch
from ml_search.ml_search import MLSearch
import json

# Helper fixtures and functions
# =============================

@pytest.fixture()
def ml_search(request):
    """Create an instance of the MLSearch class."""
    ml_search_instance = MLSearch()
    ml_search_instance.log_level = 'INFO'
    ml_search_instance.log_dir = './logs'
    ml_search_instance.log_file_name = 'ml_search.log'
    ml_search_instance.intents = 'twitter, facebook'
    ml_search_instance.es_use_ssl = 'false'
    ml_search_instance.es_host = 'http://fakecooperurl.com/cooper/rules/list'
    ml_search_instance.es_index = 'data'
    ml_search_instance.es_doc_type = 'document'

    return ml_search_instance

# Test functions
# ==============


class TestMLSearch(object):
    pass