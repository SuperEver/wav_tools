# coding:utf-8
import logging
import argparse
import glob
import os


def logging_config():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')


def parse_args():
    parser = argparse.ArgumentParser('Generate wav.scp for given wav dir')
    parser.add_argument('--wav_scp', required=True, help='input wav.scp path')
    parser.add_argument('--text_in', required=True, help='input text path')
    parser.add_argument('--text_out', required=True, help='output text path')
    args = parser.parse_args()
    return args


def gen_valid_text(args):
    valid_uttids = set()
    with open(args.wav_scp) as f:
        for line in f:
            word_arr = line.split(None, 1)
            uttid = word_arr[0]
            valid_uttids.add(uttid)

    fout = open(args.text_out, 'w')
    with open(args.text_in) as f:
        for line in f:
            word_arr = line.strip().split(None, 1)
            if word_arr[0] in valid_uttids:
                fout.write(line)
    fout.close()


if __name__ == '__main__':
    args = parse_args()
    logging_config()
    gen_valid_text(args)
