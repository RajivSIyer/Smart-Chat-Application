import json

class ClientCredentials(object):
    def __init__(self, username, passwd):
        self.username= username
        self.passwd = passwd

    def to_Json(self):
        return json.dumps(self, indent=4, default=self.encode_Json)

    def encode_Json(self, cc):
        return {"username":self.username, "passwd":self.passwd}

    @classmethod
    def from_Json(self, jsonStr):
        jsonDict = json.loads(jsonStr)
        return ClientCredentials(**jsonDict)

    def __str__(self):
        return self.to_Json()   