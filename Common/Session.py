import json

class Session(object): #Expiry may or may not be implemented
    def __init__(self, id):
        self.id = id

    def to_Json(self):
        return json.dumps(self, indent=4, default=self.encode_Json)

    def encode_Json(self, sesh):
        return {"id":self.id}

    @classmethod
    def from_Json(self, jsonStr):
        jsonDict = json.loads(jsonStr)
        return Session(**jsonDict)

    def __str__(self):
        return self.to_Json()   
        