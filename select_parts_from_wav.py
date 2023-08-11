# coding:utf-8
import os
import logging
import shutil
import argparse
from pcm2wav import gen_wav_header
import numpy as np
import datetime

logger_level = logging.INFO
logging.basicConfig(level=logger_level, format='%(asctime)s - %(name)s -%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser('Select wav segments from one wav file by a time label')
    parser.add_argument('wav_fn', type=str, help='wav path')
    parser.add_argument('label_fn', type=str, help='txt label file with content of st_sec ed_sec for each line')
    parser.add_argument('out_dir', type=str, help='output directory for wav segments')
    args = parser.parse_args()
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)
    return args


def process(args):
    for ele in (args.wav_fn, args.label_fn):
        if not os.path.exists(ele):
            logger.error('File %s does not exist' % ele)
            exit(1)

    file_size = os.path.getsize(args.wav_fn)

    # check if wav header is 44 bytes
    wav_stream = open(args.wav_fn, 'rb')
    assert file_size > 44
    header = wav_stream.read(44)
    data_bytes = int.from_bytes(header[40:44], byteorder='little')
    if data_bytes + 44 != file_size:
        logger.error('Wav file %s is not standard 44 bytes header wav file' % args.wav_fn)
        exit(1)

    labf = open(args.label_fn)
    seg_time_list = []
    for line in labf:
        word_arr = line.strip().split(',')
        try:
            st_sec = float(word_arr[0])
            ed_sec = float(word_arr[1])
            seg_time_list.append((st_sec, ed_sec))
        except Exception as e:
            logger.error(str(e))
            exit(1)
    labf.close()
    global_seg_index = 1
    for (st_sec, ed_sec) in seg_time_list:
        st_bytes = int((st_sec - 0.5) * 16000 * 2)
        ed_bytes = int((ed_sec + 0.5) * 16000 * 2)
        st_bytes = max(0, st_bytes)
        ed_bytes = min(ed_bytes, data_bytes)
        wav_stream.seek(st_bytes + 44, 0)
        seg_buf = wav_stream.read(ed_bytes - st_bytes)
        seg_header = gen_wav_header((ed_bytes - st_bytes) // 2)
        seg_fn = os.path.join(args.out_dir, '%05d.wav' % global_seg_index)
        outf = open(seg_fn, 'wb')
        outf.write(seg_header)
        outf.write(seg_buf)
        outf.close()
        global_seg_index += 1
    wav_stream.close()


args = parse_args()
process(args)
