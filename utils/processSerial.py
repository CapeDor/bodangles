import  serial, sqlite3, re, pygame

# connect to database
con = sqlite3.connect('../data.db')
ser = None
with con:
    # get the db cursor
    cur = con.cursor()
    # get the count of tables in the db
    # returns a tuple in the format [(2,)]
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table'")
    # assign the table count to a variable
    count = cur.fetchall()

def BEEEEOP():
    global ser
    pygame.mixer.init()
    pygame.mixer.music.load("beepBeepLettuce.ogg")
    pygame.mixer.music.play()
    print("REEEEEEEE!")
    while pygame.mixer.music.get_busy() == True:
        continue
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=61)
    except:
        BEEEEOP()

def superConverter(count):
    #convert the first element of the list to a string
    count = str(count[0])
    # create a regular expression to strip all but numbers from the string
    numbers = re.compile('\d+(?:\.\d+)?')
    # create a list containing only the numbers in the string
    count = numbers.findall(count)
    # return the number at list element 0 as an int
    return(int(count[0]))

# open a serial port with a baudrate of 9600 and a timeout of 61 seconds
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=61)
except:
    BEEEEOP()
# initialize an empty list named data
data = []
reee = []
# initialize tableCount to the number of tables in the db
tableCount = superConverter(count)
if ser != None:
    while ser.isOpen():
        print(ser)
        # read from serial until a '\n' and store it in line
        line = ser.readline()
        # decode the serial input to utf-8
        dec = line.decode('utf-8')
        # append the serial input into data[] and seperate the input by commas
        data.append(dec.split(","))
        if(len(data) == tableCount):
            # for every element in data[]
            for entry in data:
                # set varaibles to the elements in entry[]
                tankNum = entry[0]
                sat = entry[1]
                online = entry[2]
                floatAlarm = entry[3]
                o2Alarm = entry[4]
                pressure = entry[5]
                reee.append(entry[3])
                # create a string to insert vales into the specified table
                sqlEntry = "INSERT INTO Tank" + tankNum + "Data VALUES(datetime('now', 'localtime'), " + sat + ", " + online + ", " + floatAlarm + ", " + o2Alarm + ", " + pressure.rstrip() + ")"
                print(sqlEntry)
                #print(reee)
                for num in reee:
                    if num == 1:
                        #BEEEEOP()
                        print("ASDUAISFA")
                # actually insert the values into the db
                cur.execute(sqlEntry)
                # commit the transaction
                con.commit()
            # reset data[] to empty
            data = []
if ser == None:
    print("closed")