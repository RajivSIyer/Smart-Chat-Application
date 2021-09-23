import json
CMD_CONN = 'CONNECT'
CMD_LOGIN = 'LOGIN'
CMD_SENDMSG = 'SENDMSG'
RESPCODE_OK = 200
RESPCODE_FAIL = 404

class request(object): #client to server

    def __init__(self, cmd, req_id, payload):
        self.cmd = cmd
        self.req_id = req_id
        self.payload = payload

    def to_Json(self):
        return json.dumps(self, indent=4, default=self.encode_Json)

    def encode_Json(self, req):
        return {"cmd":self.cmd, "req_id":self.req_id, "payload":self.payload}

    @classmethod
    def from_Json(self, req_jsonStr):
        req_jsonDict = json.loads(req_jsonStr)
        req = request(**req_jsonDict)
        return req

    def __str__(self):
        return self.to_Json()



class response(object): #server to client

    def __init__(self, resp_code: int, req_id, msg, payload):
        
        self.resp_code = resp_code
        self.req_id = req_id
        self.msg = msg
        self.payload = payload

    def to_Json(self):
        try:
            return json.dumps(self, indent=4, default=self.encode_Json)
        except Exception as e:
            print(str(e))

    def encode_Json(self, resp):
        print("Response: ", type(resp))
        if self.payload != '' and self.payload != 'None':
            return {"resp_code":self.resp_code, "req_id":self.req_id, "msg":json.dumps(self.msg), "payload":self.payload.encode_Json()}
        else:
            return {"resp_code":self.resp_code, "req_id":self.req_id, "msg":json.dumps(self.msg), "payload":''}

    @classmethod
    def from_Json(self, resp_jsonStr):
        resp_jsonDict = json.loads(resp_jsonStr)
        resp = request(**resp_jsonDict)
        return resp

    def __str__(self):
        return self.to_Json()