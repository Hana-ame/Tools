import pyautogui
import time

while True:
    pyautogui.moveRel(1, 0)  # 横向移动1像素
    time.sleep(60)
    pyautogui.moveRel(-1, 0) # 复位