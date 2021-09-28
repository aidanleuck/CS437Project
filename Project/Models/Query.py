class QueryModel():
    def __init__(self, args):
        if(len(args) == 0):
            self.anonID = ""
            self.query = ""
            self.queryTime = ""
        elif(len(args) !=3):
            raise IndexError("Length of arguments has to be 0 or 3")
        else:
            self.anonID = args[0]
            self.query = args[1]
            self.queryTime = args[2]
    
    