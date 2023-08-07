# coding:utf-8
import cv2
import os
import glob
import numpy as np
import argparse
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser('video to pics')
    parser.add_argument('video_in', type=str, help='video path')
    parser.add_argument('pics_dir', type=str, help='output pic dir')
    args = parser.parse_args()
    return args


def main(args):
    os.makedirs(args.pics_dir, exist_ok=True)
    str_cmd = f'rm -rf {args.pics_dir}/*.*'
    os.system(str_cmd)
    vidcap = cv2.VideoCapture(args.video_in)
    num_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS)
    print(f'num_frames = {num_frames}, fps = {fps}')
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    for i in tqdm(range(num_frames)):
        _,image = vidcap.read()
        cv2.imwrite(os.path.join(args.pics_dir, f'{i:04d}.jpg'), image)


if __name__ == '__main__':
    args = parse_args()
    main(args)

