import json

class Session(object): #Expiry may or may not be implemented
    def __init__(self, id):
        self.id = id

    def to_Json(self):
        return json.dumps(self, indent=4, default=self.encode_Json)

    def encode_Json(self, sesh):
        return {"id":str(self.id)}

    @classmethod
    def from_Json(self, jsonStr):
        jsonDict = json.loads(jsonStr)
        return Session(**jsonDict)

    def __str__(self):
        return self.to_Json()   

class ServerSession(Session):
    def __init__(self, id, uid, start, expire):
        Session.__init__(self, id)
        self.uid = uid
        self.start = start
        self.expire = expire