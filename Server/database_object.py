import pyodbc
import logging
from User import User

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