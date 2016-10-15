import mysql.connector

creds = open("mysql.txt", "r")
db = creds.readline().split(": ")[1][:-1]
usr = creds.readline().split(": ")[1][:-1]
pw = creds.readline().split(": ")[1][:-1]
c = mysql.connector.connect(user=usr, password=pw, host="cunycalendar.cteyzoxyljy0.us-east-1.rds.amazonaws.com", database=db)
crs = c.cursor()

def dropTables():
    crs.execute("DROP TABLE names")
    crs.execute("DROP TABLE accounts")

def createTables():
    try:
        TABLES = {}
        TABLES["names"] = (
            "CREATE TABLE names ("
            "   client_id varchar(100) NOT NULL,"
            "   fname varchar(14) NOT NULL,"
            "   lname varchar(16) NOT NULL,"
            "   uname varchar(32) NOT NULL,"
            "   PRIMARY KEY (client_id), UNIQUE KEY client_id (client_id)"
            ") ENGINE=InnoDB")
        TABLES["accounts"] = (
            "CREATE TABLE accounts ("
            "   uname varchar(32) NOT NULL,"
            "   cpuser varchar(32) NOT NULL,"
            "   cppw varchar(32) NOT NULL,"
            "   cfuser varchar(32) NOT NULL,"
            "   cfpw varchar(32) NOT NULL,"
            "   serv varchar(1024) NOT NULL,"
            "   PRIMARY KEY (uname(, UNIQUE KEY uname (uname)"
            ") ENGINE=InnoDB")
        crs.execute(TABLES["names"])
        crs.execute(TABLES["accounts"])
        c.commit()
        return True
    except:
        return False

def addName(client_id, fname, lname):
    client_id = client_id[:-27]
    crs.execute("SELECT * FROM names WHERE client_id = '" + client_id + "'")
    results = crs.fetchall()
    if (len(results) > 0): # User already exists
        return False
    else:
        uname = fname + "." + lname
        crs.execute("SELECT * FROM names WHERE uname = '" + uname + "'")
        results = crs.fetchall()
        if (len(results) > 0): # Someone else has this username
            uname = uname + 0
            i = 1
            while (len(results) > 0):
                uname = uname[:-1] + i
                crs.execute("SELECT * FROM names WHERE uname = '" + uname + "'")
                results = crs.fetchall()
                i = i + 1
        crs.execute("INSERT INTO names(client_id, fname, lname, uname) VALUES ('" + client_id + "', '" + fname + "', '" + lname + "', '" + uname + "')")
        c.commit()
        return True

def getName(client_id):
    client_id = client_id[:-27]
    crs.execute("SELECT * FROM names WHERE client_id = '" + client_id + "'")
    results = crs.fetchone()
    try:
        return results[3]
    except:
        return 0

def addAccount(uname, cpuser, cppw, cfuser, cfpw, serv):
    crs.execute("SELECT * FROM accounts WHERE uname = '" + uname + "'")
    results = crs.fetchall()
    if (len(results) > 0):
        return False
    else:
        crs.execute("INSERT INTO accounts(uname, cpuser, cppw, cfuser, cfpw, serv) VALUES ('" + uname + "', '" + cpuser + "', '" + cppw + "', '" + cfuser + "', '" + cfpw + "', '" + serv + "')")
        c.commit()
        return True

def getCredentials(uname):
    crs.execute("SELECT * FROM accounts WHERE uname = '" + uname + "'")
    try:
        results = crs.fetchall()
        return [results[3], results[4]]
    except:
        return []
