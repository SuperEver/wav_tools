# coding:utf-8
import logging
import argparse
import glob
import os


def logging_config():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')


def parse_args():
    parser = argparse.ArgumentParser('Generate wav.scp for given wav dir')
    parser.add_argument('--wav_dir', required=True, help='wav directory')
    parser.add_argument('--wav_scp', required=True, help='output wav.scp path')
    parser.add_argument('--split', type=int, default=1, help='split number for wav.scp')
    args = parser.parse_args()
    return args


def gen_wav_scp(args):
    abs_wav_dir = os.path.abspath(args.wav_dir)
    wav_files = glob.glob('%s/*.wav' % abs_wav_dir)
    wav_dict = {}
    for wav_file in wav_files:
        _, wav_filename = os.path.split(wav_file)
        uttid, _ = os.path.splitext(wav_filename)
        wav_dict[uttid] = wav_file
    wav_list = sorted(wav_dict.items())
    if args.split > 1:
        part_num = (len(wav_list) + args.split - 1) // args.split
        wav_scp_prefix, _ = os.path.splitext(args.wav_scp)
        for i in range(0, args.split):
            index = i + 1
            st = i * part_num
            ed = index * part_num
            with open('%s_%d.scp' % (wav_scp_prefix, index), 'w') as f:
                for ele in wav_list[st:ed]:
                    f.write('%s\t%s\n' % (ele[0], ele[1]))
    else:
        with open(args.wav_scp, 'w') as f:
            for ele in wav_list:
                f.write('%s\t%s\n' % (ele[0], ele[1]))


if __name__ == '__main__':
    args = parse_args()
    logging_config()
    gen_wav_scp(args)
