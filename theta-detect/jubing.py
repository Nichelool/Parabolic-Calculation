import numpy as np
import win32gui
from PIL import ImageGrab
import cv2 as cv
import pyautogui

# name = '大号'
# handle = win32gui.FindWindow(0, name)
# # print(handle)
# # win32gui.SetForegroundWindow(handle)
# rect = win32gui.GetWindowRect(handle)
# # rect = [int(x * 1.5+1) for x in rect]
# # print(rect)
# # img = ImageGrab.grab(rect)  # 截取tnt屏幕的照片   需要转化为np数组  37指的是上边框的厚度
# img = pyautogui.screenshot(region=(rect[0]+183, rect[1]+35+840,  87, 41))
# image_array = np.array(img)
# img = cv.cvtColor(image_array, cv.COLOR_BGR2GRAY)
# cv.imshow("img", img)
# cv.waitKey(0)
# cv.destroyAllWindows()

a = 10**(3-1)
print(a)