import serial, sqlite3, re, minimalmodbus, time, sys, alarm_lib
cursor = None
con = None
alarm_lib.set_alarm_flag(False)

def db_con():
	try:
		global con
		con = sqlite3.connect("../data.db")
	except:
		print("Unable to connect to database :'( ")
		return None
	else:
		with con:
			print("Connected to database :)")
			global cursor
			cursor = con.cursor()
			cursor.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' ")
			table_count = cursor.fetchall()
			return table_count

def index_table_count(table_count):
	table_count = table_count[0]
	table_count = table_count[0]
	return table_count

def slave_create(num_slave):
	try:
		slaveid_list = []
		for i in range(2, num_slave + 2):
			slave_device = minimalmodbus.Instrument('/dev/serial/by-path/pci-0000:00:14.0-usb-0:12:1.0-port0', i)
			print("Connecting to slave" + str(i))

			slave_device.serial.baudrate = 9600
			slave_device.serial.bytesize = 8
			slave_device.serial.parity = serial.PARITY_NONE
			slave_device.serial.stopbits = 1
			slave_device.serial.timeout = 1

			slave_device.mode = minimalmodbus.MODE_RTU
			slaveid_list.append(slave_device)
		return slaveid_list
	except OSError as e:
		print("Unable to connect to modbus: Retrying")
		print("Error: " + str(e))
		alarm_lib.set_alarm_flag(True)
		sys.exit()

def modbus_read(slave, num_reg):
	try:
		slave_data = []
		for i in range(num_reg):
			slave_data.append(slave.read_register(i,0,3,False))
		slave_data[0] = slave_data[0]/100.00
		return slave_data
	except IOError as e:
		print("Read Failed: " + str(e))
		slave_data = [0, 0, 0, 0, 0, 0]
		return slave_data
	except ValueError as e:
		print("Read Failed: " + str(e))
		slave_data = [0, 0, 0, 0, 0, 0]
		return slave_data

def populate_db(all_slave_data):
	alarm_list = []
	for i in all_slave_data:
		for j in i:
			#[tank_num, sat, pressure, online, sol_state, o2_alarm, float_alarm]
			tank_num = str(i[0])
			sat = str(i[1])
			pressure = str(i[2])
			online = str(i[3])
			sol_state = str(i[4])
			o2_alarm = str(i[5])
			float_alarm = str(i[6])
		alarm_list.append(o2_alarm)
		alarm_list.append(float_alarm)
		sql_entry = "INSERT INTO Tank" + tank_num + "Data VALUES(datetime('now', 'localtime'), " + sat + ", " + online + ", " + float_alarm + ", " + o2_alarm + ", " + sol_state.rstrip() + ")"
		try:
			global cursor
			global con
			cursor.execute(sql_entry)
			con.commit()
			print("Writing to database succesful")
		except:
			print("Insert Failed")
			return alarm_list
	return alarm_list

def main():
	print("Main Loop")
	table_count = index_table_count(db_con())
	slaveid_list = slave_create(table_count)
	all_slave_data = []

	for index in range(table_count):
		print("Reading from slave " + str(index + 2))
		raw_slave_data = (modbus_read(slaveid_list[index], 6))
		raw_slave_data.insert(0, index)
		all_slave_data.append(raw_slave_data)
		time.sleep(1)
	alarm_list = populate_db(all_slave_data)
	print(alarm_list)
	if "1" in alarm_list:
		alarm_lib.set_alarm_flag(True)
	else:
		alarm_lib.set_alarm_flag(False)

while True:
	main()