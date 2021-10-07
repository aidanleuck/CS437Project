import os
import sys

import constants as constant
from Models.Query import QueryModel

# Adds the modules inside the project directory to the system path
sys.path.append(constant.PROJECTDIR)

from QLog.QuerySuggester import QuerySuggester


if(__name__ == "__main__"):
    query = "how to buy a"
    suggester = QuerySuggester()
    suggestions = suggester.getQuerySuggestions(query)
    print(suggestions)
    
    