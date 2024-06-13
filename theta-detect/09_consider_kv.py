import win32gui
import win32api
import time
from math import sin, cos, sqrt, log, tan,exp
import numpy as np
import scipy.optimize as opt
def findTitle(window_title):
    '''
    查找指定标题窗口句柄
    @param window_title: 标题名
    @return: 窗口句柄
    '''
    hWndList = []
    # 函数功能：该函数枚举所有屏幕上的顶层a窗口，办法是先将句柄传给每一个窗口，然后再传送给应用程序定义的回调函数。
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for hwnd in hWndList:
        # 函数功能：该函数获得指定窗口所属的类的类名。
        # clsname = win32gui.GetClassName(hwnd)
        # 函z数功能：该函数将指定窗口的标题条文本（如果存在）拷贝到一个缓存区内
        title = win32gui.GetWindowText(hwnd)
        if (title == window_title):
            print("标题：", title, "句柄：", hwnd)
            break
    return hwnd


window_title = '这不是TNT - MuMu模拟器'
hwnd = findTitle(window_title)
print(hwnd)

#小于3.3
def solve_v(v, x, y, theta,k,g):
    # print(1-(k*x)/(v*cos(theta)))
    return y - (g/(k**2))*log(1-(k*x)/(v*cos(theta))) - (g/(k*v*cos(theta))+tan(theta))*x

# def solve_theta_v(X, arg):
#
#     x = [arg(0), 13150]
#     y = [arg(1), 120]
#     k = arg(2)
#     g = arg(3)
#     def h(theta,v, x, y,k,g):
#         return y - (g / (k ** 2)) * log(1 - (k * x) / (v * cos(theta))) - (g / (k * v * cos(theta)) + tan(theta)) * x
#
#
#     return [X,  px, py, k, g]

while True:
    #   zxcGezczxzxcctCursorPos 获取鼠标指针的当前位置
    p = win32api.GetCursorPos()
    # print(p[0], p[1])
    #  GetWindowRect 获得整个窗口的范围矩形，窗口的边框、标题栏、滚动条及菜单等都在这个矩形内
    x, y, w, h = win32gui.GetWindowRect(hwnd)
    # 鼠标坐标减去指定窗口坐标为鼠标在窗口中的坐标值
    pos_x = p[0] - x
    pos_y = p[1] - y
    # print(pos_x, pos_y)
    z_last_state = win32api.GetKeyState(ord('Z'))
    x_last_state = win32api.GetKeyState(ord('X'))
    c_last_state = win32api.GetKeyState(ord('C'))
    time.sleep(0.3)
    if win32api.GetKeyState(ord('Z')) != z_last_state and win32api.GetKeyState(ord('X')) == x_last_state :            # 只能检测到系统内的状态，开模拟器的话没检测到
        # print("z_last_state:", z_last_state, "now_state:", win32api.GetKeyState(ord('Z')))
        my_pos_x = pos_x-45
        my_pos_y = 810+39-pos_y
        print("锁定我方坐标为：{},{}".format(my_pos_x, my_pos_y) )
    if win32api.GetKeyState(ord('X')) != x_last_state and win32api.GetKeyState(ord('Z')) == z_last_state:
        target_pos_x = pos_x-45
        target_pos_y = 810+39-pos_y
        print("锁定敌方坐标为:{},{}".format(target_pos_x, target_pos_y))
    if win32api.GetKeyState(ord('C')) != c_last_state:
        p1_p2_dis = abs(target_pos_x - my_pos_x)  # 不清楚为啥乘了2，但是乘了2是正确的
        y_dis = (target_pos_y - my_pos_y)                #  12022.3/67.5/12
        theta0 = 9 * 3.141592657 / 180
        theta1 = 20 * 3.141592657 / 180
        theta2 = 30 * 3.141592657 / 180
        theta3 = 40 * 3.141592657 / 180
        theta4 = 50 * 3.141592657 / 180
        theta45 = 45 * 3.141592657 / 180
        theta5 = 60 * 3.141592657 / 180
        theta6 = 65 * 3.141592657 / 180
        theta7 = 70 * 3.141592657 / 180
        theta8 = 73 * 3.141592657 / 180
        theta9 = 78 * 3.141592657 / 180
        theta10 = 55 * 3.141592657 / 180
        theta35 = 35 * 3.141592657 / 180
        theta48 = 48 * 3.141592657 / 180
        theta80 = 80 * 3.141592657 / 180
        theta85 = 80 * 3.141592657 / 180

        k = 0.1709
        g = 216.6324
        # k = 0.1726
        # g=209.6544

        # k = 0.1503
        # g = 283.1753
        # v2 = (p1_p2_dis * sqrt(g / (2 * cos(theta2) * (p1_p2_dis * sin(theta2) - y_dis * cos(theta2)))))
        # v3 = (p1_p2_dis * sqrt(g / (2 * cos(theta3) * (p1_p2_dis * sin(theta3) - y_dis * cos(theta3)))))
        # v4 = (p1_p2_dis * sqrt(g / (2 * cos(theta4) * (p1_p2_dis * sin(theta4) - y_dis * cos(theta4)))))
        # v5 = (p1_p2_dis * sqrt(g / (2 * cos(theta5) * (p1_p2_dis * sin(theta5) - y_dis * cos(theta5)))))
        # result_v = fsolve(solve_theta_v, x0 = [theta1,v], args=(p1_p2_dis, y_dis,  k, g))
        # print("v:", v)
        try:
            v0 = (p1_p2_dis * sqrt(g / (2 * cos(theta0) * (p1_p2_dis * sin(theta0) - y_dis * cos(theta0)))))

            result_v1 = opt.fsolve(solve_v, x0=v0, args=(p1_p2_dis, y_dis, theta0, k, g))
            print("9度打{}".format(result_v1/10))
        except:
            print('9度无解')


        try:
            v1 = (p1_p2_dis * sqrt(g / (2 * cos(theta1) * (p1_p2_dis * sin(theta1) - y_dis * cos(theta1)))))

            result_v1 = opt.fsolve(solve_v, x0=v1, args=(p1_p2_dis, y_dis, theta1, k, g))
            print("20度打{}".format(result_v1 / 10))
        except:
            print('20度无解')

        try:
            v2 = (p1_p2_dis * sqrt(g / (2 * cos(theta2) * (p1_p2_dis * sin(theta2) - y_dis * cos(theta2)))))

            result_v2 = opt.fsolve(solve_v, x0=v2, args=(p1_p2_dis, y_dis, theta2, k, g))
            print("30度打{}".format(result_v2 / 10))
        except:
            print('30度无解')
        try:
            v35 = (p1_p2_dis * sqrt(g / (2 * cos(theta35) * (p1_p2_dis * sin(theta35) - y_dis * cos(theta35)))))

            result_v35 = opt.fsolve(solve_v, x0=v35, args=(p1_p2_dis, y_dis, theta35, k, g))
            print("35度打{}".format(result_v35 / 10))
        except:
            print('35度无解')

        try:
            v3 = (p1_p2_dis * sqrt(g / (2 * cos(theta3) * (p1_p2_dis * sin(theta3) - y_dis * cos(theta3)))))

            result_v3 = opt.fsolve(solve_v, x0=v3, args=(p1_p2_dis, y_dis, theta3, k, g))
            print("40度打{}".format(result_v3 / 10))
        except:
            print('40度无解')
        try:
            v45 = (p1_p2_dis * sqrt(g / (2 * cos(theta45) * (p1_p2_dis * sin(theta45) - y_dis * cos(theta45)))))

            result_v45 = opt.fsolve(solve_v, x0=v45, args=(p1_p2_dis, y_dis, theta45, k, g))
            print("45度打{}".format(result_v45 / 10))
        except:
            print('45度无解')

        try:
            v48 = (p1_p2_dis * sqrt(g / (2 * cos(theta48) * (p1_p2_dis * sin(theta48) - y_dis * cos(theta48)))))
            result_v48 = opt.fsolve(solve_v, x0=v48, args=(p1_p2_dis, y_dis, theta48, k, g))
            print("48度打{}".format(result_v48 / 10))
        except:
            print('48度无解')
        try:
            v4 = (p1_p2_dis * sqrt(g / (2 * cos(theta4) * (p1_p2_dis * sin(theta4) - y_dis * cos(theta4)))))
            result_v4 = opt.fsolve(solve_v, x0=v4, args=(p1_p2_dis, y_dis, theta4, k, g))
            print("50度打{}".format(result_v4 / 10))
        except:
            print('50度无解')

        try:
            v10 = (p1_p2_dis * sqrt(g / (2 * cos(theta10) * (p1_p2_dis * sin(theta10) - y_dis * cos(theta10)))))
            result_v10 = opt.fsolve(solve_v, x0=v10, args=(p1_p2_dis, y_dis, theta10, k, g))
            print("55度打{}".format(result_v10 / 10))
        except:
            print('55度无解')
        try:
            v5 = (p1_p2_dis * sqrt(g / (2 * cos(theta5) * (p1_p2_dis * sin(theta5) - y_dis * cos(theta5)))))
            result_v5 = opt.fsolve(solve_v, x0=v5, args=(p1_p2_dis, y_dis, theta5, k, g))
            print("60度打{}".format(result_v5 / 10))
        except:
            print('60度无解')
        try:
            v6 = (p1_p2_dis * sqrt(g / (2 * cos(theta6) * (p1_p2_dis * sin(theta6) - y_dis * cos(theta6)))))
            result_v6 = opt.fsolve(solve_v, x0=v6, args=(p1_p2_dis, y_dis, theta6, k, g))
            print("65度打{:.2f}飞{:.2f}".format(result_v6[0] / 10, v6/10))
        except:
            print('65度无解')
        try:
            v7 = (p1_p2_dis * sqrt(g / (2 * cos(theta7) * (p1_p2_dis * sin(theta7) - y_dis * cos(theta7)))))
            result_v7 = opt.fsolve(solve_v, x0=v7, args=(p1_p2_dis, y_dis, theta7, k, g))
            print("70度打{}".format(result_v7 / 10))
        except:
            print('70度无解')
        try:
            v8 = (p1_p2_dis * sqrt(g / (2 * cos(theta8) * (p1_p2_dis * sin(theta8) - y_dis * cos(theta8)))))
            result_v8 = opt.fsolve(solve_v, x0=v8, args=(p1_p2_dis, y_dis, theta8, k, g))
            print("73度打{}".format(result_v8 / 10))
        except:
            print('73度无解')

        try:
            v9 = (p1_p2_dis * sqrt(g / (2 * cos(theta9) * (p1_p2_dis * sin(theta9) - y_dis * cos(theta9)))))
            result_v9 = opt.fsolve(solve_v, x0=v9, args=(p1_p2_dis, y_dis, theta9, k, g))
            print("78度打{}".format(result_v9 / 10))
        except:
            print('78度无解')

        try:
            v80 = (p1_p2_dis * sqrt(g / (2 * cos(theta80) * (p1_p2_dis * sin(theta80) - y_dis * cos(theta80)))))
            result_v80 = opt.fsolve(solve_v, x0=v80, args=(p1_p2_dis, y_dis, theta80, k, g))
            print("80度打{}".format(result_v80 / 10))
        except:
            print('80度无解')

        try:
            v85 = (p1_p2_dis * sqrt(g / (2 * cos(theta85) * (p1_p2_dis * sin(theta85) - y_dis * cos(theta85)))))
            result_v85 = opt.fsolve(solve_v, x0=v85, args=(p1_p2_dis, y_dis, theta85, k, g))
        except:
            print('85度无解')




        # print("距离（{}，{}）".format(p1_p2_dis, y_dis), result_v/10)
        # result_v1 = result_v1/10
        # result_v2 = result_v2/10
        # result_v3 = result_v3 / 10
        # result_v4 = result_v4 / 10
        # print("50度打{}".format(result_v1))
        # print("65度打{}".format(result_v2))
        # print("20度打{}".format(result_v3))
        # print("73度打{}".format(result_v4))