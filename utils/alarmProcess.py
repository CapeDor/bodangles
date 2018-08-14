import serial, sqlite3, re, pygame


ser = None
# connect to database
try:
    con = sqlite3.connect('../data.db')
except:
    print("Cannot connect to database")
else:
    with con:
        print("Connected to database!")
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table'")
        count = cur.fetchall()

def BEEEEOP():
    pygame.mixer.init()
    pygame.mixer.music.load("beepBeepLettuce.ogg")
    pygame.mixer.music.play()
    print("REEEEEE!")
    while pygame.mixer.music.get_busy() == True:
        continue
    serialConnect()

def superConverter(count):
    count = str(count[0])
    numbers = re.compile('\d+(?:\.\d+)?')
    count = numbers.findall(count)
    return(int(count[0]))

def populateDatabase(data):
    tableCount = superConverter(count)
    if(len(data) == tableCount):
        for entry in data:
            tankNum = entry[0]
            sat = entry[1]
            online = entry[2]
            floatAlarm = entry[3]
            o2Alarm = entry[4]
            pressure = entry[5]
            sqlEntry = "INSERT INTO Tank" + tankNum + "Data VALUES(datetime('now', 'localtime'), " + sat + ", " + online + ", " + floatAlarm + ", " + o2Alarm + ", " + pressure.rstrip() + ")"
            print(sqlEntry)
            try:
                cur.execute(sqlEntry)
                con.commit()
            except:
                print("Read failed")
                readSerial()
    readSerial()

def serialConnect():
    try:
        global ser
        ser = serial.Serial('/dev/serial/by-id/usb-ES_Gear_Ltd._Industruino_D21G-if00', 9600, timeout=61)
        print("Connected to serial")
        readSerial()
    except:
        BEEEEOP()

def readSerial():
    global ser
    try:
        data = []
        for x in range(superConverter(count)):
            line = ser.readline()
            dec = line.decode('utf-8')
            data.append(dec.split(","))
    except serial.SerialException as e:
        print(e)
        serialConnect()
        return None
    except TypeError as e:
        print("Closing serial port")
        BEEEEOP()
        return None
    else:
        print("Reading Serial data")
        populateDatabase(data)

serialConnect()