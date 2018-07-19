import sqlite3

def getInput():
    # ask for user input and store to tankNum
    tankNum = input("Enter the tank number you are setting up: ")
    # create a string that will be the name of the table in the DB
    # example table name: Tank0Data
    tableName = "Tank" + str(tankNum) + "Data"
    return tableName

# connect to the sqlite database
con = sqlite3.connect('/home/merlinq/O2Data/data.db')
with con:
    # call getInput() to get the name of the table to be created
    tableName = getInput()
    # create string to drop table if it already exists
    sqlDropTable = "DROP TABLE IF EXISTS " + tableName
    # create a string to create a table
    sqlCreateTable = "CREATE TABLE " + tableName + "(timestamp DATETIME, sat NUMERIC, bypass NUMERIC, floatAlarm NUMERIC, o2Alarm NUMERIC, solenoid NUMERIC)"
    # get the db cursor
    cur = con.cursor()
    # execute the sqlite commands
    cur.execute(sqlDropTable)
    cur.execute(sqlCreateTable)
    # commit current transaction
    con.commit()
# close db connection
con.close()