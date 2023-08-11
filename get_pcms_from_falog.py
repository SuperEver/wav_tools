# coding:utf-8
import os
import argparse
import glob
import numpy as np
import re
import datetime

pattern = re.compile("^.*SampleStart: (\d+), SampleEnd: (\d+).*")
str_prefix = datetime.date.today().strftime("%y%m%d")


def parse_args():
    parser = argparse.ArgumentParser("Extract false wakeup segments to pcm files")
    parser.add_argument("wav_list", type=str, help="wav list")
    parser.add_argument("log_dir", type=str, help="input false wakeup log for wav_list")
    parser.add_argument("out_dir", type=str, help="output pcm dir")
    args = parser.parse_args()
    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)
    return args


def process(args):
    with open(args.wav_list) as f:
        wav_files = f.readlines()

    global str_prefix
    out_index = 0
    for wav_file in wav_files:
        wav_file = wav_file.strip()
        wav_file_fname = os.path.split(wav_file)[1]
        log_file_fname = os.path.splitext(wav_file_fname)[0] + ".log"
        log_file = os.path.join(args.log_dir, log_file_fname)
        if not os.path.exists(log_file):
            print("File %s not exists" % log_file)
            continue
        pcm_data = np.fromfile(wav_file, dtype=np.int16)
        pcm_data = pcm_data[22:]
        f = open(log_file)
        for line in f:
            mat = pattern.match(line.strip())
            if mat is None:
                continue
            smp_st = max(int(mat.group(1)) - 8000, 0)
            smp_ed = int(mat.group(2)) + 8000

            seg_data = pcm_data[smp_st:smp_ed]
            out_index += 1
            outf = open(
                os.path.join(args.out_dir, "fa_%s_%05d.pcm" % (str_prefix, out_index)),
                "wb",
            )
            outf.write(bytes(seg_data))
            outf.close()
        f.close()


if __name__ == "__main__":
    args = parse_args()
    process(args)
