import os
import sys

import constants as constant

# Adds the modules inside the project directory to the system path
sys.path.append(constant.PROJECTDIR)

import Models.Query as Query
from QLog.QueryLogParser import QueryLogParser

if(__name__ == "__main__"):
    parser = QueryLogParser()
    parser.mergeQueryLogs()
    print("Hello")