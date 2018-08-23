import pygame, alarm_lib, time

while True:
    alarm = alarm_lib.get_alarm_flag()
    print(alarm)
    time.sleep(3)