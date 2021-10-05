import json
from json import JSONEncoder
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

    class QueryModelEncoder(JSONEncoder):
        # overload method default
        def default(self, obj):

        # Match all the types you want to handle in your converter
            if isinstance(obj, QueryModel):
                return obj.__dict__
        # Call the default method for other types
            return json.JSONEncoder.default(self, obj)
    