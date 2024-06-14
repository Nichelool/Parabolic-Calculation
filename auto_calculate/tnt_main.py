import sys
import time

import win32api
from math import sin, cos, sqrt, log, tan, exp, atan, pi
import numpy as np
import win32gui
import cv2 as cv
import pyautogui
import scipy.optimize as opt
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QColor, QCursor, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QCheckBox, QSlider


# from qtpy import QtCore


class Line(QWidget):

    def __init__(self):
        super().__init__()
        self.strength = None
        self.enemy_pos_y = None
        self.enemy_pos_x = None
        self.my_pos_y = None
        self.my_pos_x = None
        self.timer = None
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.thetap = 0
        self.ui = uic.loadUi("compact1.ui", self)
        self.k = 0.1709
        self.acc = 0
        self.theta = 45 * pi / 180
        self.v = 500
        self.g = 216.6324
        self.zoom = 5
        self.delta_x = 800
        self.delta_y = 250
        self.pos_x = 0
        self.pos_y = 0
        self.i = 0
        self.theta_rotate = 0
        self.initUI()
        self.pushbutton_close.setStyleSheet("QPushButton{background:#F76677;border-radius:10px;}\n        "
                                            "QPushButton:hover{background:red;}")
        self.pushButton_2.setStyleSheet("QPushButton{background:#F7D674;border-radius:10px;}\n        "
                                        "QPushButton:hover{background:yellow;}")
        self.pushbutton_mini.setStyleSheet("QPushButton{background:#6DDF6D;border-radius:10px;}\n        "
                                           "QPushButton:hover{background:green;}")
        self.pushbutton_close.clicked.connect(self.close)
        self.pushbutton_mini.clicked.connect(self.showMinimized)
        self.label_4.lower()

    def initUI(self):
        self.setMouseTracking(True)
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update)
        self.timer.start()
        self.setWindowTitle("这不是TNT助手")
        self.center()

        self.angle.valueChanged.connect(self.value_change_angle)
        self.strength.valueChanged.connect(self.value_change_strength)
        self.transaction.valueChanged.connect(self.value_change_transaction)
        self.MyPosbutton.clicked.connect(self.get_my_pos)
        self.Originbutton.clicked.connect(self.get_origin)
        self.Leftbutton.clicked.connect(self.get_left)
        self.Rightbutton.clicked.connect(self.get_right)
        self.EnemyPosbutton.clicked.connect(self.get_enemy_pos)
        self.onTop.clicked.connect(self.onTopClick)
        # self.calculatebutton.clicked.connect(self.calculate)
        self.angle.setValue(45)
        self.my_pos_x = 300
        self.my_pos_y = 400
        self.enemy_pos_x = 301
        self.enemy_pos_y = 401

    def onTopClick(self):
        if self.onTop.isChecked():
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.show()

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

    #
    # pic_theta = cv.imread("./model_theta/42.png")  # 游戏中获取到的图片

    def detect_theta(self, pics):
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
        RectBoxes, ImgBoxes = self.sequence_contours(adaptiveThresh, 80, 95)  # 把游戏中获取到的图片中的数字做分割

        if len(contours) >= 1:
            for i in range(len(contours)):
                # print(cv.contourArea(contours[i]))
                if cv.contourArea(contours[i]) > 100:
                    l += 1

                    # cv.imshow("game_num", ImgBoxes[0])  # 游戏中获取并分割后的数字

                    # print(RectBoxes[0])    # x y w h
                    #
                    # 准备模板
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
        if a is not None:
            return int(a)
        else:
            return 0
        # adaptiveThresh1 = cv.drawContours(pic_theta, contours, -1, (255, 0, 0), 3)
        # cv.imshow('adaptiveThresh2', adaptiveThresh1)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton:
            if self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)
                QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def value_change_transaction(self):
        self.setWindowOpacity(self.transaction.value() / 100)

    def value_change_angle(self):
        self.theta = self.angle.value() * pi / 180
        self.label_angle.setText("Angle:  " + str(self.angle.value()) + "°")

    def value_change_strength(self):
        self.v = self.strength.value()
        self.label_strength.setText("Strength:  " + str(self.strength.value() / 10) + "度")

    def get_my_pos(self):
        self.my_pos_x = self.pos_x
        self.my_pos_y = self.pos_y
        self.mypos.setText(str(self.my_pos_x) + "," + str(self.my_pos_y))
        self.delta_x = self.my_pos_x - self.x()
        self.delta_y = self.my_pos_y - self.y()

    def get_enemy_pos(self):
        self.enemy_pos_x = self.pos_x
        self.enemy_pos_y = self.pos_y
        self.enemypos.setText(str(self.enemy_pos_x) + "," + str(self.enemy_pos_y))

    def get_origin(self):
        self.origin_pos_x = self.x() + 7
        self.origin_pos_y = self.y() + 31
        self.origin.setText(str(self.origin_pos_x) + "," + str(self.origin_pos_y))

    def get_left(self):
        self.left_pos_x = self.pos_x
        self.left_pos_y = 1440 - self.pos_y
        self.left.setText(str(self.left_pos_x) + "," + str(self.left_pos_y))

    def get_right(self):
        self.right_pos_x = self.pos_x
        self.right_pos_y = 1440 - self.pos_y
        self.right.setText(str(self.right_pos_x) + "," + str(self.right_pos_y))
        base_dis_x = abs(self.right_pos_x - self.left_pos_x)
        base_dis_y = abs(self.right_pos_y - self.left_pos_y)
        theta_rotate = atan(base_dis_y / base_dis_x)
        self.theta_rotate = theta_rotate
        self.anglelabel.setText("Angle:  {:.3f}".format(self.theta_rotate))
        base_horizon_length = base_dis_x * cos(theta_rotate) + base_dis_y * sin(theta_rotate)
        zoom = 810 / base_horizon_length
        self.zoom = zoom
        self.zoomlabel.setText("Zoom:  {:.3f}".format(self.zoom))

    def calculate(self, theta):
        theta = theta / 180 * pi

        def solve_v(v, x, y, theta, k, g):
            return y - g / k ** 2 * log(1 - k * x / (v * cos(theta))) - (g / (k * v * cos(theta)) + tan(theta)) * x

        x_dis_before = self.zoom * (self.enemy_pos_x - self.my_pos_x)
        y_dis_before = self.zoom * (self.my_pos_y - self.enemy_pos_y)
        p1_p2_dis = x_dis_before * cos(self.theta_rotate) + y_dis_before * sin(self.theta_rotate)
        dis = abs(p1_p2_dis) / 67.5
        p1_p2_dis = abs(p1_p2_dis)
        self.distancelabel.setText("水平屏距:{:.3f}".format(dis))
        print("你与敌方水平距离为{:.3f}".format(dis))
        y_dis = y_dis_before * cos(self.theta_rotate) - x_dis_before * sin(self.theta_rotate)
        theta0 = 0.15707963284999998
        theta1 = 0.3490658507777778
        theta2 = 0.5235987761666667
        theta3 = 0.6981317015555556
        theta4 = 0.8726646269444445
        theta45 = 0.78539816425
        theta5 = 1.0471975523333334
        theta6 = 1.1344640150277776
        theta7 = 1.2217304777222222
        theta8 = 1.2740903553388887
        theta9 = 1.3613568180333333
        theta10 = 0.9599310896388888
        theta25 = 0.43633231347222223
        theta35 = 0.6108652388611111
        theta48 = 0.8377580418666666
        theta75 = 1.3089969404166666
        theta80 = 1.3962634031111112
        theta85 = 1.4835298658055553
        k = 0.1709
        g = 216.6324
        # if theta is not None:
        #     try:
        #         v = p1_p2_dis * sqrt(g / (2 * cos(theta) * (p1_p2_dis * sin(theta) - y_dis * cos(theta))))
        #         result_v = opt.fsolve(solve_v, x0=v, args=(p1_p2_dis, y_dis, theta0, k, g))
        #         self.strength.setValue(int(result_v[0]))
        #     except:
        #         print("无解")

        try:
            v0 = p1_p2_dis * sqrt(g / (2 * cos(theta) * (p1_p2_dis * sin(theta) - y_dis * cos(theta))))
            result_v0 = opt.fsolve(solve_v, x0=v0, args=(p1_p2_dis, y_dis, theta, k, g))
            self.strength.setValue(int(result_v0[0]))
        except:
            print("无解")
            self.label_strength.setText("Strength:无解")

    def paintEvent(self, ev):
        p = win32api.GetCursorPos()
        self.pos_x = p[0]
        self.pos_y = p[1]
        painter = QPainter(self)
        painter.save()
        painter.setPen(QColor(255, 255, 255))
        name = '大号'
        handle = win32gui.FindWindow(0, name)
        rect = win32gui.GetWindowRect(handle)
        self.strength.move(rect[0] - self.x() + 428, rect[1] - self.y() + 1045)
        if self.opencurve.isChecked() & self.modifycurve.isChecked() == False:
            # name = '大号'
            # handle = win32gui.FindWindow(0, name)
            # print(handle)
            # win32gui.SetForegroundWindow(handle)
            # rect = win32gui.GetWindowRect(handle)
            img = pyautogui.screenshot(region=(rect[0] + 183, rect[1] + 35 + 840, 87, 41))
            image_array = np.array(img)
            img = cv.cvtColor(image_array, cv.COLOR_BGR2GRAY)
            # # cv.imshow("img", img)
            # # cv.waitKey(0)
            # # cv.destroyAllWindows()
            theta1 = 0
            # time.sleep(200)
            try:
                theta1 = self.detect_theta(img)
                # time.sleep(0.25)
            except:
                print(theta1)
            if theta1 > 90:
                self.thetap = 180 - theta1
            else:
                if theta1 == 0:
                    print('维持上一次值')
                else:
                    self.thetap = theta1
            self.angle.setValue(self.thetap)
            self.calculate(self.thetap)
        for i in range(1000):
            x = int(((1 - exp(-self.k * i / 100)) * (
                    self.k * self.v * cos(self.theta) - self.acc) + self.acc * self.k * i / 100) / self.k ** 2)
            y = int(((1 - exp(-self.k * i / 100)) * (
                    self.k * self.v * sin(self.theta) + self.g) - self.g * self.k * i / 100) / self.k ** 2)
            x /= self.zoom
            y /= self.zoom
            x_post_right = x * cos(self.theta_rotate) - y * sin(self.theta_rotate)
            y_post_right = y * cos(self.theta_rotate) + x * sin(self.theta_rotate)
            x_post_left = -x * cos(self.theta_rotate) - y * sin(self.theta_rotate)
            y_post_left = y * cos(self.theta_rotate) - x * sin(self.theta_rotate)
            x_right = self.delta_x + x_post_right
            x_left = self.delta_x + x_post_left
            y_right = self.delta_y - y_post_right
            y_left = self.delta_y - y_post_left
            painter.setPen(QColor(255, 255, 255))
            if (x_right <= 831) & (x_right >=30):
                if (y_right<=891) & (y_right >= 20):
                    painter.drawPoint(int(x_right), int(y_right))
            # painter.setPen(QColor(255, 0, 0))
            if (x_left <= 831) & (x_left >=30):
                if (y_left<=891) & (y_left >= 20):
                    painter.drawPoint(int(x_left), int(y_left))
            brush = QBrush(QColor(0, 125, 125))
            painter.setBrush(brush)
            painter.setPen(QColor(0, 125, 125))
            painter.drawEllipse(QPoint(int(self.delta_x), int(self.delta_y)), 10, 10)
            painter.setPen(QColor(255, 0, 0))
            brush = QBrush(QColor(255, 0, 0))
            painter.setBrush(brush)
            painter.drawEllipse(QPoint(int(self.delta_x - self.my_pos_x + self.enemy_pos_x),
                                       int(self.delta_y - self.my_pos_y + self.enemy_pos_y)), 10, 10)

        # painter.drawEllipse(2313, 733)
        painter.restore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    MainWindows = Line()
    MainWindows.move(-35, 4)
    MainWindows.show()
    sys.exit(app.exec_())

# okay decompiling compact.cpython-37.pyc
