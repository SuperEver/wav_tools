# coding:utf-8
import cv2
import os
import glob
import numpy as np
import argparse
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser('pics to video')
    parser.add_argument('pic_dirs', type=str, help='jpgs dir, use "," to split')
    parser.add_argument('video_out', type=str, help='output video path')
    parser.add_argument('--fps', type=int, required=True, help='fps of video')
    args = parser.parse_args()
    return args


def main(args):
    pic_dirs = args.pic_dirs.split(',')
    pics = []
    for pic_dir in pic_dirs:
        temp_list = glob.glob(os.path.join(pic_dir, '*.jpg'))
        temp_list.sort()
        pics += temp_list
    print(f'{len(pics)} pics found')
    img = cv2.imread(pics[0])
    height, width, layers = img.shape
    size = (width,height)

    out = cv2.VideoWriter(args.video_out,cv2.VideoWriter_fourcc(*'mp4v'), args.fps, size)
    for pic in  tqdm(pics):
        img = cv2.imread(pic)
        if img is None:
            raise ValueError('img is None')
            continue
        height, width, layers = img.shape
        size = (width,height)
        out.write(img)
     
    out.release()



if __name__ == '__main__':
    args = parse_args()
    main(args)

