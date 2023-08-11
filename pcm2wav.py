# coding:utf-8
import struct
import numpy as np
import os
import argparse


def gen_wav_header(num_samples: int):
    # 16K 16bits mono signed-integer
    wav_header = bytearray(
        b'RIFF$\xff\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\xff\x00\x00'
    )
    byte_len = 2 * num_samples
    len1 = byte_len
    len2 = len1 + 36
    str1 = struct.pack('i', len1)
    str2 = struct.pack('i', len2)
    wav_header[4:8] = str2
    wav_header[40:44] = str1
    return bytes(wav_header)


def pcm_to_wav(pcm_filepath, wav_filepath):
    '''
    Only Support 16K 16bits mono signed-integer pcm
    '''
    if not os.path.exists(pcm_filepath):
        print('File %s not exists')
        return
    pcm_data = np.fromfile(pcm_filepath, dtype=np.int16)
    wav_header = gen_wav_header(pcm_data.shape[0])
    with open(wav_filepath, 'wb') as f:
        f.write(wav_header)
        f.write(pcm_data.tobytes())


def parse_args():
    parser = argparse.ArgumentParser(description='Format pcm(16K,16bits,mono,signed-integer) file to wav file')
    parser.add_argument('pcm_file', type=str, action='store', help='pcm file path(input)')
    parser.add_argument('wav_file', type=str, action='store', help='wav file path(output)')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    pcm_to_wav(args.pcm_file, args.wav_file)
