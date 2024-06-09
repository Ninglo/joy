import threading
import pygame
# 参考文档 https://www.pygame.org/docs/ref/joystick.html?highlight=gamepad

import json


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

with open("config.json",'r') as f:
    config  = json.load(f)
    print(config)

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
print(joystick_count)
# stick = pygame.joystick.Joystick(0)
# stick.init()

from pynput.keyboard import Key, Controller
from pynput.mouse import Controller as Mouse, Button
keyboard = Controller()
mouse = Mouse()
# 用于映射一些键盘不能按出来的按键
def getKeyByStr(str):
    keyMap = {
        'page_up':Key.page_up,
        'page_down':Key.page_down,
        'up':Key.up,
        'down':Key.down,
        'left':Key.left,
        'right':Key.right,
    }

    if str in keyMap.keys():
        return keyMap[str]
    
    # 没找到就给个ese吧
    return str

timer = None
# clock = pygame.time.Clock()
done = False

# while True:
#     if 
#     pass

while not done:
    try:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.JOYDEVICEADDED:
                stick = pygame.joystick.Joystick(0)
                stick.init()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button >= len(config['button']):
                    continue
                k = config['button'][event.button]
                if k != "":
                    keyboard.press(getKeyByStr(k))
            if event.type == pygame.JOYBUTTONUP:
                if event.button >= len(config['button']):
                    continue
                k = config['button'][event.button]
                if k != "":
                    keyboard.release(getKeyByStr(k))
            if event.type == pygame.JOYAXISMOTION:
                if event.axis >= len(config['axis']):
                    continue
                if event.axis <= 3:
                    continue
                
                print(event)
                if event.value < -0.5:
                    k = config['axis'][event.axis][0]
                    keyboard.press(getKeyByStr(k))
                    # keyboard.release(getKeyByStr(k))
                if event.value > 0.5:
                    k = config['axis'][event.axis][1]
                    # keyboard.press(getKeyByStr(k))
                    keyboard.release(getKeyByStr(k))
                if event.value == 0:
                    for k in config['axis'][event.axis]:
                        keyboard.release(getKeyByStr(k))
            if event.type == pygame.JOYHATMOTION:
                x,y = event.value 
                
                if x == -1:
                    kStr = config['hat'][0][0]
                    k = getKeyByStr(kStr)
                    keyboard.press(getKeyByStr(k))
                if x == 1:
                    kStr = config['hat'][0][1]
                    k = getKeyByStr(kStr)
                    keyboard.press(getKeyByStr(k))
                if x == 0:
                    for kStr in config['hat'][0]:
                        k = getKeyByStr(kStr)
                        keyboard.release(getKeyByStr(k))
                
                if y == -1:
                    kStr = config['hat'][1][0]
                    k = getKeyByStr(kStr)
                    keyboard.press(getKeyByStr(k))
                if y == 1:
                    kStr = config['hat'][1][1]
                    k = getKeyByStr(kStr)
                    keyboard.press(getKeyByStr(k))
                if y == 0:
                    for kStr in config['hat'][1]:
                        k = getKeyByStr(kStr)
                        keyboard.release(getKeyByStr(k))

                
    except KeyboardInterrupt:
        done = True
pygame.quit()

