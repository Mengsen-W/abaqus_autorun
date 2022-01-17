"""
2019-12-28 15:06:25
Mengsen. Wang

"""
import math
import os

# coding = "utf-8"

# 半径
r = 0.5
# 质量
m = 300.00
# 重力加速的
g = 9.8
# 重心位置
h = 3/8 * r
# 转动惯量
Ic = 83/320 * m * r ^ 2
# [deg] 初始角度
theta = 60
# [deg/s] 初始角速度
omega = 0
# [m] 初始位移
xo = -theta*r
# 仿真步长
dt = 2e-3
# 画半球
Xb = r*cosd(180: 360)
Yb = r*sind(180: 360)
[xb, yb] = rotxy(Xb, Yb, theta)
hb = fill(xb+xo, yb, [1, 0.8, 0.8])
axis([-2.25, 2.25, -0.5, 2])
