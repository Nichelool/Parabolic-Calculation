import sys
import win32api
from math import sin, cos, sqrt, log, tan, exp, atan, pi

import scipy.optimize as opt
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QColor, QCursor, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
# from qtpy import QtCore

music_path_my_pos = "C:\\Users\\18175\\Music\\mypos.mp3"

class Line(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = uic.loadUi("compact.ui", self)
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
        self.strength9 = 0
        self.strength20 = 0
        self.strength25 = 0
        self.strength30 = 0
        self.strength35 = 0
        self.strength40 = 0
        self.strength45 = 0
        self.strength48 = 0
        self.strength50 = 0
        self.strength55 = 0
        self.strength60 = 0
        self.strength65 = 0
        self.strength70 = 0
        self.strength73 = 0
        self.strength75 = 0
        self.strength78 = 0
        self.strength80 = 0
        self.strength85 = 0
        self.initUI()
        self.pushbutton_close.setStyleSheet("QPushButton{background:#F76677;border-radius:10px;}\n        QPushButton:hover{background:red;}")
        self.pushButton_2.setStyleSheet("QPushButton{background:#F7D674;border-radius:10px;}\n        QPushButton:hover{background:yellow;}")
        self.pushbutton_mini.setStyleSheet("QPushButton{background:#6DDF6D;border-radius:10px;}\n        QPushButton:hover{background:green;}")
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
        self.wind.valueChanged.connect(self.value_change_wind)
        self.angle.valueChanged.connect(self.value_change_angle)
        self.strength.valueChanged.connect(self.value_change_strength)
        self.transaction.valueChanged.connect(self.value_change_transaction)
        self.MyPosbutton.clicked.connect(self.get_my_pos)
        self.Originbutton.clicked.connect(self.get_origin)
        self.Leftbutton.clicked.connect(self.get_left)
        self.Rightbutton.clicked.connect(self.get_right)
        self.EnemyPosbutton.clicked.connect(self.get_enemy_pos)
        self.calculatebutton.clicked.connect(self.calculate)
        self.cb9.stateChanged.connect(self.change_cb9)
        self.cb20.stateChanged.connect(self.change_cb20)
        self.cb25.stateChanged.connect(self.change_cb25)
        self.cb30.stateChanged.connect(self.change_cb30)
        self.cb35.stateChanged.connect(self.change_cb35)
        self.cb40.stateChanged.connect(self.change_cb40)
        self.cb45.stateChanged.connect(self.change_cb45)
        self.cb48.stateChanged.connect(self.change_cb48)
        self.cb50.stateChanged.connect(self.change_cb50)
        self.cb55.stateChanged.connect(self.change_cb55)
        self.cb60.stateChanged.connect(self.change_cb60)
        self.cb65.stateChanged.connect(self.change_cb65)
        self.cb70.stateChanged.connect(self.change_cb70)
        self.cb73.stateChanged.connect(self.change_cb73)
        self.cb75.stateChanged.connect(self.change_cb75)
        self.cb78.stateChanged.connect(self.change_cb78)
        self.cb80.stateChanged.connect(self.change_cb80)
        self.cb85.stateChanged.connect(self.change_cb85)

        self.cb45.setChecked(True)
        self.strength.setValue(self.strength45)
        self.angle.setValue(45)
        self.my_pos_x = 300
        self.my_pos_y = 400
        self.enemy_pos_x = 301
        self.enemy_pos_y = 401

        self.windcleanbutton.clicked.connect(self.clean_wind)

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

    def clean_wind(self):
        self.wind.setValue(0)

    def change_cb9(self):
        if self.cb9.checkState() == Qt.Checked:
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb20(self):
        if self.cb20.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb25(self):
        if self.cb25.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb30(self):
        if self.cb30.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb35(self):
        if self.cb35.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb40(self):
        if self.cb40.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb45(self):
        if self.cb45.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb48(self):
        if self.cb48.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb50(self):
        if self.cb50.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb55(self):
        if self.cb55.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb60(self):
        if self.cb60.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb65(self):
        if self.cb65.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb70(self):
        if self.cb70.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb73(self):
        if self.cb73.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb75(self):
        if self.cb75.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb78(self):
        if self.cb78.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb80.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb80(self):
        if self.cb80.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb85.setChecked(False)

    def change_cb85(self):
        if self.cb85.checkState() == Qt.Checked:
            self.cb9.setChecked(False)
            self.cb20.setChecked(False)
            self.cb25.setChecked(False)
            self.cb30.setChecked(False)
            self.cb35.setChecked(False)
            self.cb40.setChecked(False)
            self.cb45.setChecked(False)
            self.cb48.setChecked(False)
            self.cb50.setChecked(False)
            self.cb55.setChecked(False)
            self.cb60.setChecked(False)
            self.cb65.setChecked(False)
            self.cb70.setChecked(False)
            self.cb73.setChecked(False)
            self.cb75.setChecked(False)
            self.cb78.setChecked(False)
            self.cb80.setChecked(False)

    def value_change_transaction(self):
        self.setWindowOpacity(self.transaction.value() / 100)

    def value_change_wind(self):
        self.acc = self.wind.value() / 10
        self.label_wind.setText("Wind:  " + str(self.wind.value() / 10))

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

    def uncheck_all(self):
        self.cb9.setChecked(False)
        self.cb20.setChecked(False)
        self.cb25.setChecked(False)
        self.cb30.setChecked(False)
        self.cb35.setChecked(False)
        self.cb40.setChecked(False)
        self.cb45.setChecked(False)
        self.cb48.setChecked(False)
        self.cb50.setChecked(False)
        self.cb55.setChecked(False)
        self.cb60.setChecked(False)
        self.cb65.setChecked(False)
        self.cb70.setChecked(False)
        self.cb73.setChecked(False)
        self.cb75.setChecked(False)
        self.cb78.setChecked(False)
        self.cb80.setChecked(False)
        self.cb85.setChecked(False)

    def calculate(self):

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
        try:
            v0 = p1_p2_dis * sqrt(g / (2 * cos(theta0) * (p1_p2_dis * sin(theta0) - y_dis * cos(theta0))))
            result_v0 = opt.fsolve(solve_v, x0=v0, args=(p1_p2_dis, y_dis, theta0, k, g))
            self.strength9 = int(result_v0[0])
            self.st9.setText("{:.1f}".format(result_v0[0] / 10))
        except:
            self.st9.setText("无解")

        try:
            v1 = p1_p2_dis * sqrt(g / (2 * cos(theta1) * (p1_p2_dis * sin(theta1) - y_dis * cos(theta1))))
            result_v1 = opt.fsolve(solve_v, x0=v1, args=(p1_p2_dis, y_dis, theta1, k, g))
            self.strength20 = int(result_v1[0])
            self.st20.setText("{:.1f}".format(result_v1[0] / 10))
        except:
            self.st20.setText("无解")

        try:
            v25 = p1_p2_dis * sqrt(g / (2 * cos(theta25) * (p1_p2_dis * sin(theta25) - y_dis * cos(theta25))))
            result_v25 = opt.fsolve(solve_v, x0=v25, args=(p1_p2_dis, y_dis, theta25, k, g))
            self.strength25 = int(result_v25[0])
            self.st25.setText("{:.1f}".format(result_v25[0] / 10))
        except:
            self.st25.setText("无解")

        try:
            v2 = p1_p2_dis * sqrt(g / (2 * cos(theta2) * (p1_p2_dis * sin(theta2) - y_dis * cos(theta2))))
            result_v2 = opt.fsolve(solve_v, x0=v2, args=(p1_p2_dis, y_dis, theta2, k, g))
            self.strength30 = int(result_v2[0])
            self.st30.setText("{:.1f}".format(result_v2[0] / 10))
        except:
            self.st30.setText("无解")

        try:
            v35 = p1_p2_dis * sqrt(g / (2 * cos(theta35) * (p1_p2_dis * sin(theta35) - y_dis * cos(theta35))))
            result_v35 = opt.fsolve(solve_v, x0=v35, args=(p1_p2_dis, y_dis, theta35, k, g))
            self.strength35 = int(result_v35[0])
            self.st35.setText("{:.1f}".format(result_v35[0] / 10))
        except:
            self.st35.setText("无解")

        try:
            v3 = p1_p2_dis * sqrt(g / (2 * cos(theta3) * (p1_p2_dis * sin(theta3) - y_dis * cos(theta3))))
            result_v3 = opt.fsolve(solve_v, x0=v3, args=(p1_p2_dis, y_dis, theta3, k, g))
            self.strength40 = int(result_v3[0])
            self.st40.setText("{:.1f}".format(result_v3[0] / 10))
        except:
            self.st40.setText("无解")

        try:
            v45 = p1_p2_dis * sqrt(g / (2 * cos(theta45) * (p1_p2_dis * sin(theta45) - y_dis * cos(theta45))))
            result_v45 = opt.fsolve(solve_v, x0=v45, args=(p1_p2_dis, y_dis, theta45, k, g))
            self.strength45 = int(result_v45[0])
            self.st45.setText("{:.1f}".format(result_v45[0] / 10))
        except:
            self.st45.setText("无解")

        try:
            v48 = p1_p2_dis * sqrt(g / (2 * cos(theta48) * (p1_p2_dis * sin(theta48) - y_dis * cos(theta48))))
            result_v48 = opt.fsolve(solve_v, x0=v48, args=(p1_p2_dis, y_dis, theta48, k, g))
            self.strength48 = int(result_v48[0])
            self.st48.setText("{:.1f}".format(result_v48[0] / 10))
        except:
            self.st48.setText("无解")

        try:
            v4 = p1_p2_dis * sqrt(g / (2 * cos(theta4) * (p1_p2_dis * sin(theta4) - y_dis * cos(theta4))))
            result_v4 = opt.fsolve(solve_v, x0=v4, args=(p1_p2_dis, y_dis, theta4, k, g))
            self.strength50 = int(result_v4[0])
            self.st50.setText("{:.1f}".format(result_v4[0] / 10))
        except:
            self.st50.setText("无解")

        try:
            v10 = p1_p2_dis * sqrt(g / (2 * cos(theta10) * (p1_p2_dis * sin(theta10) - y_dis * cos(theta10))))
            result_v10 = opt.fsolve(solve_v, x0=v10, args=(p1_p2_dis, y_dis, theta10, k, g))
            self.strength55 = int(result_v10[0])
            self.st55.setText("{:.1f}".format(result_v10[0] / 10))
        except:
            self.st55.setText("无解")

        try:
            v5 = p1_p2_dis * sqrt(g / (2 * cos(theta5) * (p1_p2_dis * sin(theta5) - y_dis * cos(theta5))))
            result_v5 = opt.fsolve(solve_v, x0=v5, args=(p1_p2_dis, y_dis, theta5, k, g))
            self.strength60 = int(result_v5[0])
            self.st60.setText("{:.1f}".format(result_v5[0] / 10))
        except:
            self.st60.setText("无解")

        try:
            v6 = p1_p2_dis * sqrt(g / (2 * cos(theta6) * (p1_p2_dis * sin(theta6) - y_dis * cos(theta6))))
            result_v6 = opt.fsolve(solve_v, x0=v6, args=(p1_p2_dis, y_dis, theta6, k, g))
            self.strength65 = int(result_v6[0])
            self.st65.setText("{:.1f}".format(result_v6[0] / 10))
        except:
            self.st65.setText("无解")

        try:
            v7 = p1_p2_dis * sqrt(g / (2 * cos(theta7) * (p1_p2_dis * sin(theta7) - y_dis * cos(theta7))))
            result_v7 = opt.fsolve(solve_v, x0=v7, args=(p1_p2_dis, y_dis, theta7, k, g))
            self.strength70 = int(result_v7[0])
            self.st70.setText("{:.1f}".format(result_v7[0] / 10))
        except:
            self.st70.setText("无解")

        try:
            v8 = p1_p2_dis * sqrt(g / (2 * cos(theta8) * (p1_p2_dis * sin(theta8) - y_dis * cos(theta8))))
            result_v8 = opt.fsolve(solve_v, x0=v8, args=(p1_p2_dis, y_dis, theta8, k, g))
            self.strength73 = int(result_v8[0])
            self.st73.setText("{:.1f}".format(result_v8[0] / 10))
        except:
            self.st73.setText("无解")

        try:
            v75 = p1_p2_dis * sqrt(g / (2 * cos(theta75) * (p1_p2_dis * sin(theta75) - y_dis * cos(theta75))))
            result_v75 = opt.fsolve(solve_v, x0=v75, args=(p1_p2_dis, y_dis, theta75, k, g))
            self.strength75 = int(result_v75[0])
            self.st75.setText("{:.1f}".format(result_v75[0] / 10))
        except:
            self.st75.setText("无解")

        try:
            v9 = p1_p2_dis * sqrt(g / (2 * cos(theta9) * (p1_p2_dis * sin(theta9) - y_dis * cos(theta9))))
            result_v9 = opt.fsolve(solve_v, x0=v9, args=(p1_p2_dis, y_dis, theta9, k, g))
            self.strength78 = int(result_v9[0])
            self.st78.setText("{:.1f}".format(result_v9[0] / 10))
        except:
            self.st78.setText("无解")

        try:
            v80 = p1_p2_dis * sqrt(g / (2 * cos(theta80) * (p1_p2_dis * sin(theta80) - y_dis * cos(theta80))))
            result_v80 = opt.fsolve(solve_v, x0=v80, args=(p1_p2_dis, y_dis, theta80, k, g))
            self.strength80 = int(result_v80[0])
            self.st80.setText("{:.1f}".format(result_v80[0] / 10))
        except:
            self.st80.setText("无解")

        try:
            v85 = p1_p2_dis * sqrt(g / (2 * cos(theta85) * (p1_p2_dis * sin(theta85) - y_dis * cos(theta85))))
            result_v85 = opt.fsolve(solve_v, x0=v85, args=(p1_p2_dis, y_dis, theta85, k, g))
            self.strength85 = int(result_v85[0])
            self.st85.setText("{:.1f}".format(result_v85[0] / 10))
        except:
            self.st85.setText("无解")

    def paintEvent(self, ev):
        p = win32api.GetCursorPos()
        self.pos_x = p[0]
        self.pos_y = p[1]
        painter = QPainter(self)
        painter.save()
        painter.setPen(QColor(255, 255, 255))
        if self.opencurve.isChecked() & self.modifycurve.isChecked() == False:
            if self.cb9.isChecked():
                self.strength.setValue(self.strength9)
                self.angle.setValue(9)
            if self.cb20.isChecked():
                self.strength.setValue(self.strength20)
                self.angle.setValue(20)
            if self.cb25.isChecked():
                self.strength.setValue(self.strength25)
                self.angle.setValue(25)
            if self.cb30.isChecked():
                self.strength.setValue(self.strength30)
                self.angle.setValue(30)
            if self.cb35.isChecked():
                self.strength.setValue(self.strength35)
                self.angle.setValue(35)
            if self.cb40.isChecked():
                self.strength.setValue(self.strength40)
                self.angle.setValue(40)
            if self.cb45.isChecked():
                self.strength.setValue(self.strength45)
                self.angle.setValue(45)
            if self.cb48.isChecked():
                self.strength.setValue(self.strength48)
                self.angle.setValue(48)
            if self.cb50.isChecked():
                self.strength.setValue(self.strength50)
                self.angle.setValue(50)
            if self.cb55.isChecked():
                self.strength.setValue(self.strength55)
                self.angle.setValue(55)
            if self.cb60.isChecked():
                self.strength.setValue(self.strength60)
                self.angle.setValue(60)
            if self.cb65.isChecked():
                self.strength.setValue(self.strength65)
                self.angle.setValue(65)
            if self.cb70.isChecked():
                self.strength.setValue(self.strength70)
                self.angle.setValue(70)
            if self.cb73.isChecked():
                self.strength.setValue(self.strength73)
                self.angle.setValue(73)
            if self.cb75.isChecked():
                self.strength.setValue(self.strength75)
                self.angle.setValue(75)
            if self.cb78.isChecked():
                self.strength.setValue(self.strength78)
                self.angle.setValue(78)
            if self.cb80.isChecked():
                self.strength.setValue(self.strength80)
                self.angle.setValue(80)
            if self.cb85.isChecked():
                self.strength.setValue(self.strength85)
                self.angle.setValue(85)
        if self.opencurve.isChecked():
            for i in range(1000):
                x = int(((1 - exp(-self.k * i / 100)) * (self.k * self.v * cos(self.theta) - self.acc) + self.acc * self.k * i / 100) / self.k ** 2)
                y = int(((1 - exp(-self.k * i / 100)) * (self.k * self.v * sin(self.theta) + self.g) - self.g * self.k * i / 100) / self.k ** 2)
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
                painter.drawPoint(int(x_right), int(y_right))
                painter.setPen(QColor(255, 0, 0))
                painter.drawPoint(int(x_left), int(y_left))
                brush = QBrush(QColor(0,125,125))
                painter.setBrush(brush)
                painter.setPen(QColor(0, 125, 125))
                painter.drawEllipse(QPoint(int(self.delta_x), int(self.delta_y)), 10, 10)
                painter.setPen(QColor(255, 0, 0))
                brush = QBrush(QColor(255, 0, 0))
                painter.setBrush(brush)
                painter.drawEllipse(QPoint(int(self.delta_x-self.my_pos_x+self.enemy_pos_x), int(self.delta_y-self.my_pos_y+self.enemy_pos_y)), 10, 10)


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
    MainWindows.show()
    sys.exit(app.exec_())

# okay decompiling compact.cpython-37.pyc
