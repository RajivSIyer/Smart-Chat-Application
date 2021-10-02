import json

class ClientInfo(object):
    def __init__(self, version, devicetype, ostype):
        self.version = version
        self.devicetype = devicetype #In config file, each number will be a value to keys defining systems.
        self.ostype = ostype

    def to_Json(self):
        return json.dumps(self, indent=4, default=self.encode_Json)

    def encode_Json(self, cliinfo):
        return {"version":self.version, "devicetype":self.devicetype, "ostype":self.ostype}

    @classmethod
    def from_Json(self, jsonStr):
        jsonDict = json.loads(jsonStr)
        return ClientInfo(**jsonDict)

    def __str__(self):
        return self.to_Json()