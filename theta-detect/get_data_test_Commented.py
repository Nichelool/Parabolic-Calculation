import cv2 as cv
import numpy as np
import win32con
import win32gui
from PIL import ImageGrab
import pyautogui


class GetData():
    def __init__(self):
        pass

    def get_window_pos(self, name):
        name = name
        handle = win32gui.FindWindow(0, name)
        # 获取窗口句柄
        if handle == 0:
            return None
        else:
            # 返回坐标值和handle
            return win32gui.GetWindowRect(handle), handle

    def get_data(self):
        (x1, y1, x2, y2), handle = self.get_window_pos('大号')
        try:
            # 发送还原最小化窗口的信息
            win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
            # 设为高亮
            win32gui.SetForegroundWindow(handle)
        except:
            return

        while x1 + x2 + y1 + y2 < 0:  # 有时候截取的尺寸不对，全是负值，故而做了一个坐标的判断
            (x1, y1, x2, y2), handle = get_data.get_window_pos('大号')

        img = pyautogui.screenshot(region=(x1, y1+35,  1800, 1080))  # 截取tnt屏幕的照片   需要转化为np数组  37指的是上边框的厚度

        image_array = np.array(img)
        img = cv.cvtColor(image_array, cv.COLOR_BGR2GRAY)
        cv.imshow("img", img)             # tnt屏幕（单通道）

        box = (130, 608, 184, 631)  # box代表需要剪切图片的位置格式为:xmin ymin xmax ymax

        # cv.imshow("img1", img[841:890,168:270])  # 截取到的角度长55 高23
        # theta = self.get_theta(img[841:890,168:270])
        # print(theta)

    def get_wind(self):
        pass

    def sequence_contours(self, image, width, height):  # 在模板上分割图像
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

    def get_theta(self,pic_theta):
        # 10model_test 是负号
        pic_theta = cv.imread("./model_theta/0_gray.png")  # 游戏中获取到的图片

        pic_theta = cv.resize(pic_theta, (5 * pic_theta.shape[1], 5 * pic_theta.shape[0]))

        # gray = cv.cvtColor(pic_theta, cv.COLOR_BGR2GRAY)  # 转成单通道的灰度图
        retval, thresh = cv.threshold(pic_theta, 185, 255, cv.THRESH_BINARY)

        # cv.imshow("thresh", thresh)

        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # print(len(contours))
        if len(contours) >= 1:
            for i in range(len(contours)):
                # print(cv.contourArea(contours[i]))
                if cv.contourArea(contours[i]) > 190:
                    adaptiveThresh = cv.drawContours(thresh, contours, i, (255, 255, 255), 1)  # 轮廓绘制
                    # cv.imshow('adaptiveThresh2', adaptiveThresh)

                    RectBoxes, ImgBoxes = self.sequence_contours(adaptiveThresh, 80, 95)  # 把游戏中获取到的图片中的数字做分割
                    # cv.imshow("game_num", ImgBoxes[0])  # 游戏中获取并分割后的数字
                    # cv.imshow("game_num1", ImgBoxes[1])
                    # print(RectBoxes[0])    # x y w h
                    # #
                    ## 准备模板
                    ImgBoxes_Temp = [[] for i in range(11)]
                    for i in range(11):
                        ImgBoxes_Temp[i] = cv.imread("./model_theta/{}_model_large.png".format(i))
                        ImgBoxes_Temp[i] = cv.cvtColor(ImgBoxes_Temp[i], cv.COLOR_BGR2GRAY)
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
                    for i in range(len(ImgBoxes_Temp)):  # 循环10次 0-10  10代表负数
                        score[i] = cv.matchTemplate(ImgBoxes[0], ImgBoxes_Temp[i], cv.TM_CCORR)
                    min_val, max_val, min_indx, max_indx = cv.minMaxLoc(score)
                    print(score)
                    print(max_indx[1])
            # score = np.zeros(len(ImgBoxes_Temp), dtype=int)
            # print(score)
            # print(len(ImgBoxes_Temp))
            #         result = []
            #         print(len(ImgBoxes))
            #
            #         for i in range(len(ImgBoxes)):   # 游戏中的图片
            #             score = np.zeros(len(ImgBoxes_Temp), dtype=int)
            #             for j in range(len(ImgBoxes_Temp)):
            #                 score[j] = cv.matchTemplate(ImgBoxes[i], ImgBoxes_Temp[j], cv.TM_CCOEFF )  # 图片各对应位置的像素点对比
            #             # print(score)
            #
            #             min_val, max_val, min_indx, max_indx = cv.minMaxLoc(score)
            #             result.append(max_indx[1])
            #         print(result)
            #     #     result[i] = max_indx[1]
            #     print(result)
            #     print(result)
        #     theta = result
        # theta = result[0]
        # theta = result[2]*100+result[1]*10+result[0]

        # for i in range(len(result)):

        #     theta =
        # print(theta)
        # return theta

        # cv.imshow("game_num", ImgBoxes[1])  # 游戏中获取并分割后的数字
        # cv.imshow("game_num", ImgBoxes_Temp[1])
        # print(contours)           # 打印出来看看

        # kernel = np.ones((5, 5), np.uint8)
        # dilation = cv.dilate(adaptiveThresh, kernel, iterations=1)
        # cv.imshow('dilation', dilation)


get_data = GetData()
# get_data.get_data()
# while True:
#     get_data.get_data()
get_data.get_theta()

cv.waitKey(0)
cv.destroyAllWindows()
