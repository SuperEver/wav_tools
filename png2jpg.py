# coding:utf-8
import cv2
import os
import numpy as np
import argparse
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser('png to jpg')
    parser.add_argument('png_path', type=str, help='png path')
    args = parser.parse_args()
    return args


def main(args):
    img = cv2.imread(args.png_path)
    jpg_path = os.path.splitext(args.png_path)[0] + '.jpg'
    cv2.imwrite(jpg_path, img)


if __name__ == '__main__':
    args = parse_args()
    main(args)

