from genericpath import isfile
from json import JSONEncoder
from Models.Query import QueryModel
import os
import constants
import pickle;
import gzip;


# Parses the query logs into a model that can be used for query parsing
class QueryLogParser:

    # Directory for query logs
    qLogDir = None
    qLogIndex = None

    # Keeps index of query log terms
    compressFilePath = os.path.join(constants.BASEDIR, constants.PROJECTDIR, constants.DATADIRECTORY, constants.GZIPFILENAME)

    # Initializes the log directory by joining paths together
    def __init__(self):
        self.qLogDir = os.path.join(constants.BASEDIR, constants.PROJECTDIR, constants.QUERYLOGDIR)
        self.frequencyDir = os.path.join(self.qLogDir, constants.FREQUENCYDIR)
        if(not(os.path.exists(self.frequencyDir))):
            os.mkdir(self.frequencyDir)

        

    # Merges the query logs together into a dictionary
    def __mergeQueryLogs(self):

        # Gets the query log text files
        logFiles = [file for file in os.listdir(self.qLogDir) if(os.path.isfile(os.path.join(self.qLogDir, file)))]

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
        
                logEntryLength = len(logEntry[1].split(" "))
                frequencyLogFile = os.path.join(self.frequencyDir, f"frequency-log-{logEntryLength}.pickle")
                currentJson = {}
                if(os.path.exists(frequencyLogFile)):
                    with open(frequencyLogFile, 'rb') as f:
                        currentJson = pickle.load(f)
                if logEntry[1] in currentJson.keys():
                    currentJson[logEntry[1]] +=1
                else:
                    currentJson[logEntry[1]] = 1

                with open(frequencyLogFile, 'w+b') as f:
                    pickle.dump(currentJson, f, pickle.HIGHEST_PROTOCOL)
        
    def loadQueryLog(self, query):
        fileCount = len([file for file in os.listdir(self.frequencyDir) if os.path.isfile(file)])
        if(os.path.exists(self.frequencyDir) and fileCount > 0):
            queryLength = len(query.split(" "))
            self.qLogIndex = pickle.load(os.path.join(self.frequencyDir, f"frequency-log-{queryLength}.pickle"))
        else:
            self.__mergeQueryLogs()

        
        
        
            


       

