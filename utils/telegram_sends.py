import telegram_send, alarm_lib, time

while True:
    if alarm_lib.get_alarm_flag() == True:
        telegram_send.send(messages=["TANKS ARE ALARMING! FISH ARE GONNA DIEEE!"])
        with open("image.jpg", "rb") as f:
            telegram_send.send(images=[f])
        time.sleep(300)