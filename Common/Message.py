import json
import time

class Message(object):
    def __init__(self, datetime, from_user, to_user, msg_str):
        self.datetime = datetime
        self.from_user = from_user
        self.to_user = to_user
        self.msg_str = msg_str

    def to_Json(self):
        return json.dumps(self, indent=4, default=self.encode_Json)

    def encode_Json(self, msg):
        return {"datetime":self.datetime, "from_user":self.from_user, "to_user":self.to_user, "msg_str":self.msg_str}

    @classmethod
    def from_Json(self, jsonStr):
        jsonDict = json.loads(jsonStr)
        return Message(**jsonDict)

    def __str__(self):
        return self.to_Json() 
