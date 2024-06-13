import numpy as np
import win32gui
from PIL import ImageGrab
import cv2 as cv
import pyautogui


def sequence_contours(image, width, height):  # 在模板上分割图像
    contours, hierarchy = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    n = len(contours)
    RectBoxes0 = np.ones((n, 4), dtype=int)  # 2*4的  4指的是x y w h
    # print("n",n)
    for i in range(n):
        RectBoxes0[i] = cv.boundingRect(contours[i])  # x，y是矩阵左上点的坐标，w，h是矩阵的宽和高
        x, y, w, h = RectBoxes0[i]
        left_top_x = int(x + w / 2.0 - 80.0 / 2)
        if left_top_x < 0:
            left_top_x = 0
            right_bottom_x = 80

        else:
            left_top_x = int(x + w / 2.0 - 80.0 / 2)

            right_bottom_x = int(x + w / 2.0 + 80.0 / 2)
        left_top_y = int(y + h / 2.0 - 95 / 2.0)
        right_bottom_y = int(y + h / 2.0 + 95 / 2.0)
        w = 80
        h = 95
        RectBoxes0[i] = [left_top_x, left_top_y, w, h]
        # print(RectBoxes0[0])
    RectBoxes = np.ones((n, 4), dtype=int)
    for i in range(n):
        sequence = 0
        for j in range(n):
            if RectBoxes0[i][0] > RectBoxes0[j][0]:
                sequence = sequence + 1
        RectBoxes[sequence] = RectBoxes0[i]
    # print(RectBoxes[0])      #[60 22 80 95]
    ImgBoxes = [[] for i in range(n)]
    for i in range(n):  # 返回图片的区域
        x, y, w, h = RectBoxes[i]
        ROI = image[y:y + 95, x:x + 80]
        # print(y,y+h,x,x+w)

        ImgBoxes[i] = ROI
        # if np.array(ImgBoxes[i]) != (95,80):
        ImgBoxes[i] = cv.resize(ImgBoxes[i], (80, 95))

        # print("ImgBoxes:", np.array(ImgBoxes[0]).shape)
    # cv.imshow("ImgBox[0]",ImgBoxes[1])

    return RectBoxes, ImgBoxes

#
# pic_theta = cv.imread("./model_theta/42.png")  # 游戏中获取到的图片


def detect_theta(pics):
    # 有缩放记得除以缩放比例
    pic_theta = cv.resize(pics, (int(3.6 * pics.shape[1]), int(3.6 * pics.shape[0])))

    # gray = cv.cvtColor(pic_theta, cv.COLOR_BGR2GRAY)  # 转成单通道的灰度图
    gray = pic_theta
    retval, thresh = cv.threshold(gray, 185, 255, cv.THRESH_BINARY)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # print(len(contours))
    l = 0
    a = ''
    adaptiveThresh = cv.drawContours(thresh, contours, -1, (255, 255, 255), 1)  # 轮廓绘制
    RectBoxes, ImgBoxes = sequence_contours(adaptiveThresh, 80, 95)  # 把游戏中获取到的图片中的数字做分割

    if len(contours) >= 1:
        for i in range(len(contours)):
            # print(cv.contourArea(contours[i]))
            if cv.contourArea(contours[i]) > 100:
                l += 1

                # cv.imshow("game_num", ImgBoxes[0])  # 游戏中获取并分割后的数字

                # print(RectBoxes[0])    # x y w h
                # #
                ## 准备模板
                ImgBoxes_Temp = [[] for i in range(11)]
                for k in range(11):
                    ImgBoxes_Temp[k] = cv.imread("./model_theta/{}_model_large.png".format(k))
                    ImgBoxes_Temp[k] = cv.cvtColor(ImgBoxes_Temp[k], cv.COLOR_BGR2GRAY)
                # #
                # cv.imshow("ImgBoxes_Temp", ImgBoxes_Temp[10])     # 读取到的单个模板数字 一共十个 0-9
                #     # print(len(ImgBoxes_Temp))
                #     # print(ImgBoxes[0])
                #     # print(ImgBoxes[1])
                #
                # cv.imshow("ImgBoxes[0]", ImgBoxes[0])   # 源图像
                # cv.imshow("ImgBoxes_Temp", ImgBoxes_Temp[10])     # 读取到的单个模板数字 一共十个 0-9
                #
                # score = np.zeros(len(ImgBoxes_Temp), dtype=int)

                # print(ImgBoxes_Temp[2])
                # print("*"*40)
                # print(np.array(ImgBoxes[0]).shape)
                # print(np.array(ImgBoxes_Temp[9]).shape)

                score = np.zeros(len(ImgBoxes_Temp), dtype=int)
                if l <= len(ImgBoxes):
                    # cv.imshow("game_num1", ImgBoxes[l - 1])
                    # cv.waitKey(0)
                    for n in range(len(ImgBoxes_Temp)):  # 循环10次 0-10  10代表负数
                        score[n] = cv.matchTemplate(ImgBoxes[i], ImgBoxes_Temp[n], cv.TM_CCORR)
                    min_val, max_val, min_indx, max_indx = cv.minMaxLoc(score)
                    # print(score)
                    a += repr(max_indx[1])
                    # print(max_indx[1])
    print(a)
    # adaptiveThresh1 = cv.drawContours(pic_theta, contours, -1, (255, 0, 0), 3)
    # cv.imshow('adaptiveThresh2', adaptiveThresh1)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


if __name__ == '__main__':
    name = '大号'
    handle = win32gui.FindWindow(0, name)
    # print(handle)
    # win32gui.SetForegroundWindow(handle)
    rect = win32gui.GetWindowRect(handle)
    # rect = [int(x * 1.5+1) for x in rect]
    # print(rect)
    # img = ImageGrab.grab(rect)  # 截取tnt屏幕的照片   需要转化为np数组  37指的是上边框的厚度
    while True:
        img = pyautogui.screenshot(region=(rect[0] + 183, rect[1] + 35 + 840, 87, 41))
        image_array = np.array(img)
        img = cv.cvtColor(image_array, cv.COLOR_BGR2GRAY)
        # cv.imshow("img", img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        try:
            detect_theta(img)
        except:
            continue
