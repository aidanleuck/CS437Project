from Models.Query import QueryModel
import os
import constants
import pickle;


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
        self.qLogIndex = {}
        if(not(os.path.exists(self.frequencyDir))):
            os.makedirs(self.frequencyDir)

        

    # Merges the query logs together into a dictionary
    def __mergeQueryLogs(self):
        # Gets the query log text files
        logFiles = [file for file in os.listdir(self.qLogDir) if(os.path.isfile(os.path.join(self.qLogDir, file)))]

        if(len(logFiles) == 0):
            raise FileNotFoundError("Please download the Query Log Files and place them in the Data/QLog folder")

        # Goes through each query log file and converts into a query model
        for logFile in logFiles:
            logPath = os.path.join(self.qLogDir, logFile)
            fdesc = open(logPath, 'r')
            logContent = fdesc.read()
            self.__convertFileToIndex(logContent)
        self.__writeToFrequencyFile()


    # Converts each line into a query model
    #
    # Params: text, the file text to convert into a query model
    def __convertFileToIndex(self, text):
        lines = text.split("\n")
        lines = lines[1:]
        for line in lines:
            logEntry = line.split("\t")

            # Makes sure we haven't found an empty line
            if(logEntry[0] != ''):
                logEntryLength = len(logEntry[1].split(" "))
                query = logEntry[1].lower()
                args = [logEntry[0], query, logEntry[2]]

                query = QueryModel(args)
                

                if logEntryLength in self.qLogIndex.keys():
                    self.qLogIndex[logEntryLength].append(query)
                else:
                    self.qLogIndex[logEntryLength] = [query]

    def __writeToFrequencyFile(self):
        for key in self.qLogIndex.keys():
            frequencyFile = os.path.join(self.frequencyDir, f"frequency-file{key}.pkl")
            frequencyFileDescriptor = open(frequencyFile, "w+b")
            pickle.dump(self.qLogIndex[key], frequencyFileDescriptor)
        self.qLogIndex.clear()
    
    def __getCandidates(self, query, queryRange):
        queryLength = len(query.split(" "))
        startIndex = queryLength
        endIndex = startIndex + queryRange + 1

        candidateList = []
        for length in range(startIndex, endIndex):
            filePath = os.path.join(self.frequencyDir, f"frequency-file{length}.pkl")
            if(os.path.exists(filePath)):
                openFileDesc = open(filePath, 'rb')
                candidateList.append(pickle.load(openFileDesc))
        return candidateList
        
    def loadQueryLog(self, query, queryRange=3):
        test = os.listdir(self.frequencyDir)
        fileCount = len([file for file in os.listdir(self.frequencyDir) if not(os.path.isdir(file))])
        if((os.path.exists(self.frequencyDir) and fileCount > 0)):
            return self.__getCandidates(query, queryRange)
            
        else:
            self.__mergeQueryLogs()
            return self.__getCandidates(query,queryRange)

        
        
        
            


       

