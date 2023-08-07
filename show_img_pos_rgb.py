# -*- coding: utf-8 -*-
import cv2
import argparse


def parse_args():
    parser = argparse.ArgumentParser('Image Show')
    parser.add_argument('pic_path', help='path for pic')
    args = parser.parse_args()
    return args


def main(args):
    img= cv2.imread(args.pic_path)          #定义图片位置

    def onmouse(event, x, y, flags, param):   #标准鼠标交互函数
        if event==cv2.EVENT_MOUSEMOVE:      #当鼠标移动时
            print(f'({x},{y}):{img[y,x]}')           #显示鼠标所在像素的数值，注意像素表示方法和坐标位置的不同

    cv2.namedWindow("img")          #构建窗口
    cv2.setMouseCallback("img", onmouse)   #回调绑定窗口
    while True:               #无限循环
        cv2.imshow("img",img)        #显示图像
        # esc 退出
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()         #关闭窗口


if __name__ == '__main__':          #运行
    args = parse_args()
    main(args)
