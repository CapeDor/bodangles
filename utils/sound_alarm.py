import pygame, alarm_lib, time

def play_alarm(alarm):
    if alarm == True:
        pygame.mixer.init()
        pygame.mixer.music.load("beepBeepLettuce.ogg")
        pygame.mixer.music.play()
        while pygame.mixer.get_busy():
            continue
    else:
        return None

while True:
    alarm = alarm_lib.get_alarm_flag()
    play_alarm(alarm)
    print(alarm)
    time.sleep(3)