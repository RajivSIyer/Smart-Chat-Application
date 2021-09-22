import json

class User(object):
    '''def __init__(self):
        self.ID = None
        self.Username = ''
        self.Passwd = ''
        self.Email = ''
        self.FirstName = ''
        self.LastName = ''
    '''    

    def __init__(self, ID, Username, Passwd, Email='', FirstName='', LastName=''):
        self.initialize(ID, Username, Passwd, Email, FirstName, LastName)

    #def __init__(self, row:tuple):
            #self.initialize(row)

    def initialize(self, ID, Username, Passwd, Email='', FirstName='', LastName=''):
        self.ID = ID
        self.Username = Username
        self.Passwd = Passwd
        self.Email = Email
        self.FirstName = FirstName
        self.LastName = LastName
        
    #def initialize_tup(self, row:tuple):
        #self.initialize(row[0], row[1], row[2], row[3], row[4], row[5])

    def to_Json(self):
        return json.dumps(self, indent=4, default=self.encode_Json)

    def encode_Json(self, u):
        return {"ID":u.ID, "Username":u.Username, "Passwd":u.Passwd, "Email":u.Email, "FirstName":u.FirstName, "LastName": u.LastName}

    @classmethod
    def from_Json(self, json_str):
        json_dict = json.loads(json_str)
        u = User(**json_dict)
        return u

    def __str__(self):
        return self.to_Json()


if __name__ == "__main__":
    u = User(1,"GregorClaw","chokra99","rajpop@gmail.com","Rajiv","Iyer")
    print(u)
    print(type(u))
    #json_str = '''{"ID": 2, "Username": "Claw", "Passwd": "chokra", "FirstName": "Raj", "LastName": "Iyer"}'''
    json_str = u.to_Json() 
    u2 = User.from_Json(json_str)
    print(u2)
    print(type(u2))