import telegram_send, alarm_lib, time

print ("Telegram messenger started :)")

while True:
    if alarm_lib.get_alarm_flag() == True:
        try:
            print("Sending messages")
            telegram_send.send(messages=["TANKS ARE ALARMING! FISH ARE GONNA DIEEE!"])
            telegram_send.send(messages=["View tanks here: http://142.176.186.122"])
            with open("image.jpg", "rb") as f:
                telegram_send.send(images=[f])
            time.sleep(300)
        except:
            print("we got an issue")