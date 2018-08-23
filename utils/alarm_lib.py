
def set_alarm_flag(flag):
    f = open("alarm_flag.txt", "w+")
    f.write(str(flag))
    f.close()

def get_alarm_flag():
    f = open("alarm_flag.txt", "r")
    alarm = f.read()
    if alarm == "True":
        return True
    elif alarm == "False":
        return False
    else:
        raise ValueError("Cannot convert {} to a bool".format(alarm))
    

    



    

