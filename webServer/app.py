from flask import Flask, render_template, request, redirect
from datetime import date, timedelta
import sqlite3

app = Flask(__name__)

# create a global variable for the tank number that defaults to 0
tankNum = "0"
# create global variable for the number of tables in the db
numTables = 1

# method to get date from the db
def getHistData(startDate, endDate, tankNum):
    # create a string to send to the db to retreive data from a specified table between 2 dates
    sqlTableString = "SELECT * FROM Tank" + tankNum + "Data WHERE timestamp BETWEEN '" + startDate + "' AND '" + endDate + "'"
    # create a connection to the db
    con = sqlite3.connect("../data.db")
    # get the db cursor
    curs = con.cursor()
    # get data from the db
    curs.execute(sqlTableString)
    # store the data from the db into data[]
    data = curs.fetchall()
    # create lists for each row in the table
    dates = []
    sats = []
    online = []
    floatAlarm = []
    o2Alarm = []
    pressure = []
    for row in data:
        # append the data in each row to their corresponding list
        dates.append(row[0])
        sats.append(row[1])
        online.append(row[2])
        floatAlarm.append(row[3])
        o2Alarm.append(row[4])
        pressure.append(row[5])
    # commit the transaction
    con.commit()
    # close the db connection
    con.close()
    # return all the lists
    return dates, sats, online, floatAlarm, o2Alarm, pressure

# when at the root of the url (this is the overview page)
@app.route("/")
# mex how do i luk in mai new pants
def beepBeepLettuce():
    # initialize an empty dictionary to store tank data
    tanks = {
    }
    # get the global varaible numTables
    global numTables
    # set startDate to yesterday
    startDate = str(date.today() - timedelta(1))
    # set endDate to tomorrow
    endDate = str(date.today() + timedelta(1))
    for x in range(numTables):
        # set tankNum to the iteration of the loop
        tankNum = str(x)
        # retreive data from table for specified start date, end date, and tank number
        dates, sats, online, floatAlarm, o2Alarm, pressure = getHistData(startDate, endDate, tankNum)
        # add the last value of each list to the dictionary with their corresponding keys
        # example entry: tanks[sat0 : 100]
        tanks["sat" + str(x)] = sats[-1]
        tanks["online" + str(x)] = online[-1]
        tanks["floatAlarm" + str(x)] = floatAlarm[-1]
        tanks["o2Alarm" + str(x)] = o2Alarm[-1]
        tanks["pressure" + str(x)] = pressure[-1]
    # return the page 'main.html' along with access to the tanks dictionary
    return render_template("main.html", data = tanks)

# when the user clicks on 'Show Detail'
@app.route("/", methods=["POST"])
def sendTank():
    # get the global tankNum
    global tankNum
    # set tankNum to the value retreived from the html form
    tankNum = str(request.form["tankNum"])
    # redirect the user to route '/detail'
    return redirect("/detail")

# when the user submits the date form on the details page
@app.route("/detail", methods=["POST"])
def formPost():
    # set startDate to the date selected from the date form
    startDate = str(request.form["startDate"])
    # set the endDate to the date selected from the date form
    endDate = str(request.form["endDate"])
    # get the global tankNum
    global tankNum
    # retreive data from table for specified start date, end date, and tank number
    dates, sats, online, floatAlarm, o2Alarm, pressure = getHistData(startDate, endDate, tankNum)
    # set legend to 'Tank x Saturation (%)' where x is the tankNum + 1
    # example string if tankNum were equal to 0: Tank 1 Saturation
    legend = "Tank " + str(int(tankNum) + 1) + " Saturation (%)"
    # just reassigning variables for use in the html templating
    labels = dates
    values = sats
    # set maxDate to tomorrow
    maxDate = date.today() + timedelta(1)
    # return 'data.html' with access to allllllll the variables
    # any that have a [-1] are a list and only the last element is being returned
    return render_template("detail.html", online = online, floatAlarm = floatAlarm, o2Alarm = o2Alarm, values = values, labels = labels, legend = legend, tankNum = str(int(tankNum) + 1), startDate = startDate, endDate = endDate, maxDate = maxDate, pressure = pressure)

# do the same as the previous method but automatically set the start and end date rather then getting them from a form
@app.route("/detail")
def detail():
    # set startDate to 2 days ago
    startDate = str(date.today() - timedelta(3))
    # set endDate to tomorrow
    endDate = str(date.today() + timedelta(1))
    global tankNum
    dates, sats, online, floatAlarm, o2Alarm, pressure = getHistData(startDate, endDate, tankNum)
    legend = "Tank " + str(int(tankNum) + 1) + " Saturation (%)"
    labels = dates
    values = sats
    return render_template("detail.html", values = values, labels = labels, legend = legend, tankNum = str(int(tankNum) + 1), maxDate = endDate, startDate = startDate, endDate = endDate, online = online, o2Alarm = o2Alarm, floatAlarm = floatAlarm, pressure = pressure)

if __name__ == "__main__":
    app.run(debug=True)