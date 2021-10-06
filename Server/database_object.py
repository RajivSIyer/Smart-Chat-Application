import pyodbc
import logging
from Session import Session, ServerSession
from User import User
from datetime import datetime
from dateutil.relativedelta import relativedelta
class Database_Object(object):
    def __init__(self, logger):
        self.logger = logger
        self.connection = None

    def connect(self, connection_string):
        try:
            self.connection = pyodbc.connect(connection_string)
        except Exception as e:
            self.logger.critical("Could not establish connection! ", str(e))
            raise e

#Users Table Access Methods Start

    def add_User(self, user):
        try:
            cursor = self.connection.cursor()
            insert_query = '''INSERT INTO Users(ID, Username, Passwd, Email, FirstName, LastName) VALUES (?,?,?,?,?,?);'''
            tuple_data =  (user.ID, user.Username, user.Passwd, user.Email, user.FirstName, user.LastName)
            cursor.execute(insert_query, tuple_data)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.logger.error("Error occured while trying to add user! " + user + "Exception:\n" + str(e))
        return False

    def query_user_byname(self, uname):
        try:
            cursor = self.connection.cursor()
            query = '''SELECT ID, Username, Passwd, Email, FirstName, LastName FROM Users WHERE Username=(?)'''
            cursor.execute(query, (uname))
            ulist = []
            for row in cursor:
                u = User(row[0], row[1], row[2], row[3], row[4], row[5])
                ulist.append(u)
            cursor.close()
            return ulist
        except Exception as e:
            self.logger.error("Error occured while trying to query user! " + uname + "Exception:\n" + str(e))

    def query_oneUser_byname(self, uname):
        ul = self.query_user_byname(uname)
        if len(ul) > 0:
            return ul[0]
        else:
            return None

    def delete_user_byid(self, uid):
        try:
            cursor = self.connection.cursor()
            query = '''DELETE FROM Users WHERE ID=(?)'''
            cursor.execute(query, (uid))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.logger.error("Error occured while trying to delete user! " + str(uid) + "Exception:\n" + str(e))
        return False

    def update_user(self, user):
        try:
            cursor = self.connection.cursor()
            query = '''UPDATE Users SET Username=(?), Passwd=(?), Email=(?), FirstName=(?), LastName=(?) WHERE ID=(?)'''
            tuple_data =  (user.Username, user.Passwd, user.Email, user.FirstName, user.LastName, user.ID)
            cursor.execute(query, tuple_data)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.logger.error("Error occured while trying to update user! " + str(user) + "Exception:\n" + str(e))
        return False
#Users Table Access Methods End

#Session Table Access Methods Start

    def insert_Session(self, SessionID, UID):
        try:
            cursor = self.connection.cursor()
            Start = datetime.utcnow()
            Expire = Start + relativedelta(minutes=30)
            query = '''INSERT INTO SessionLog (SessionID, UID, Start, Expire) VALUES (?,?,?,?);'''
            tuple_data = (SessionID, UID, Start, Expire)
            cursor.execute(query, tuple_data)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.logger.error("Error occured while trying to ADD a Session! " + str(SessionID) + "Exception:\n" + str(e))
        return False

    def update_Session(self, SessionID):
        try:
            cursor = self.connection.cursor()
            Start = datetime.utcnow()
            Expire = Start + relativedelta(minutes=30)
            query = '''UPDATE SessionLog SET Start = (?), Expire = (?) WHERE SessionID = (?);'''
            tuple_data = (Start, Expire, SessionID)
            cursor.execute(query, tuple_data)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.logger.error("Error occured while trying to UPDATE an existing Session! " + str(SessionID) + "Exception:\n" + str(e))
        return False

    def getSession_byUID(self, UID):
        try:
            sesh = None
            cursor = self.connection.cursor()
            query = '''SELECT SessionID, UID, Start, Expire FROM SessionLog WHERE UID = (?)'''
            tuple_data = (UID)
            cursor.execute(query, tuple_data)
            results = list(cursor)
            if len(results) > 0:
                row = results[0]
                sesh = ServerSession(row[0], row[1], row[2], row[3])
            cursor.close()
        except Exception as e:
            self.logger.error("Error occured while trying to GET a Session! " + str(UID) + "Exception:\n" + str(e))
        return sesh

    def getSession_byUIDExpire(self, UID):
        try:
            sesh = None
            cursor = self.connection.cursor()
            Start = datetime.utcnow()
            query = '''SELECT SessionID, UID, Start, Expire FROM SessionLog WHERE UID = (?) AND Expire > (?)'''
            tuple_data = (UID, Start)
            cursor.execute(query, tuple_data)
            results = list(cursor)
            if len(results) > 0:
                row = results[0]
                sesh = ServerSession(row[0], row[1], row[2], row[3])
            cursor.close()
        except Exception as e:
            self.logger.error("Error occured while trying to GET a Session! " + str(UID) + "Exception:\n" + str(e))
        return sesh

    def getSession_bySessionID(self, SessionID):
        try:
            sesh = None
            cursor = self.connection.cursor()
            query = '''SELECT SessionID, UID, Start, Expire FROM SessionLog WHERE SessionID = (?)'''
            tuple_data = (SessionID)
            cursor.execute(query, tuple_data)
            results = list(cursor)
            if len(results) > 0:
                row = results[0]
                sesh = ServerSession(row[0], row[1], row[2], row[3])
            cursor.close()
        except Exception as e:
            self.logger.error("Error occured while trying to GET a Session! " + str(SessionID) + "Exception:\n" + str(e))
        return sesh

    def deleteSession_bySessionID(self, SessionID):
        try:
            cursor = self.connection.cursor()
            query = '''DELETE FROM SessionLog WHERE SessionID = (?);'''
            tuple_data = (SessionID)
            cursor.execute(query, tuple_data)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.logger.error("Error occured while trying to DELETE Session(s)! " + str(SessionID) + "Exception:\n" + str(e))
        return False

    def deleteSession_byExpire(self):
        try:
            cursor = self.connection.cursor()
            Start = datetime.utcnow()
            query = '''DELETE FROM SessionLog WHERE Expire < (?);'''
            tuple_data = (Start)
            cursor.execute(query, tuple_data)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.logger.error("Error occured while trying to DELETE Session(s)! " + str(Start) + "Exception:\n" + str(e))
        return False

if __name__ == "__main__":
    #Logging Setup
    #logging.basicConfig(filename='smartchat.log', encoding='utf-8', level=logging.DEBUG)
    logger = logging.getLogger('SmartChatServer')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('smartchat.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(thread)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info("Logger Created")

    #Database Connection
    db_obj = Database_Object(logger)
    connection_string = "DRIVER={ODBC Driver 17 for SQL Server};\
    SERVER=BALROG;\
    DATABASE=SmartChat;\
    UID=sa;\
    PWD=Technobase2021;\
    Trusted_Connection=no;"
    logger.info("Connection String:"+connection_string)
    db_obj.connect(connection_string)

    userlist = db_obj.query_user_byname('Rajiv')
    for u in userlist:
        logger.info(u)

    u1 = User(5, "Jesus", "Bevda99", "MaryMe@gmail.com", "Unknown", "Virgin")
    db_obj.add_User(u1)
    user = db_obj.query_oneUser_byname(u1.Username)
    logger.info(user)

    u1.LastName = "God"
    u1.Username = "Mr.X"
    db_obj.update_user(u1)
    print(db_obj.delete_user_byid(u1.ID))