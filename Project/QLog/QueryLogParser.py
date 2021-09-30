from Models.Query import QueryModel
import os
import constants

# Parses the query logs into a model that can be used for query parsing
class QueryLogParser:

    # Directory for query logs
    qLogDir = None

    # Keeps index of query log terms
    qLogIndex = {}

    # Initializes the log directory by joining paths together
    def __init__(self):
        self.qLogDir = os.path.join(constants.BASEDIR, constants.PROJECTDIR, constants.QUERYLOGDIR)

    # Merges the query logs together into a dictionary
    def mergeQueryLogs(self):

        # Gets the query log text files
        logFiles = os.listdir(self.qLogDir)

        # Goes through each query log file and converts into a query model
        for logFile in logFiles:
            logPath = os.path.join(self.qLogDir, logFile)
            fdesc = open(logPath, 'r')
            logContent = fdesc.read()
            self.__convertFileToModel(logContent)

    # Converts each line into a query model
    #
    # Params: text, the file text to convert into a query model
    def __convertFileToModel(self, text):
        lines = text.split("\n")
        lines = lines[1:]
        for line in lines:
            logEntry = line.split("\t")

            # Makes sure we haven't found an empty line
            if(logEntry[0] != ''):

                # Creates arguments to create a query model
                args = [logEntry[0], logEntry[1], logEntry[2]]
                query = QueryModel(args)
                self.qLogIndex[logEntry[1]] = query
            


       

