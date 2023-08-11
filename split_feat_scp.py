#coding: utf-8
import re
import logging
import argparse
import os
import numpy as np


def logging_config():
    logger_level = logging.INFO
    logging.basicConfig(level=logger_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def parse_args():
    parser = argparse.ArgumentParser('Split feats.scp to train_feats.scp and test_feats.scp')
    parser.add_argument('feats_scp', type=str, help='input feats.scp')
    parser.add_argument('train_feats_scp', type=str, help='train_feats.scp')
    parser.add_argument('test_feats_scp', type=str, help='test_feats.scp')
    parser.add_argument('--test_ratio', type=float, default=0.02, help='ratio of utterances to use as test part')
    args = parser.parse_args()
    return args


def process(args):
    logger = logging.getLogger(__name__)
    pattern = re.compile('^(rev[0-9]_)?(noise[0-9]-)?(sp[0-9.]+)-(.*) .*$')
    assert os.path.exists(args.feats_scp)
    key_set = set()
    with open(args.feats_scp) as f:
        ori_lines = f.readlines()

    ori_key_list = []
    for line in ori_lines:
        line = line.strip()
        match = pattern.match(line)
        if match is None:
            logger.error('match error: %s' % line)
            exit(1)
        str_key = match.group(4)
        ori_key_list.append(str_key)
        key_set.add(str_key)
    key_list = list(key_set)
    logger.info('length of key_list: %d' % len(key_list))
    num_test = round(len(key_list) * args.test_ratio)
    logger.info('split test utt number: %d' % num_test)
    np.random.seed(1331)
    np.random.shuffle(key_list)
    key_test_set = set(key_list[0:num_test])
    key_train_set = set(key_list[num_test:])
    outf_train = open(args.train_feats_scp, 'w')
    outf_test = open(args.test_feats_scp, 'w')
    for i, ori_line in enumerate(ori_lines):
        if ori_key_list[i] in key_train_set:
            outf_train.write(ori_line)
        else:
            assert ori_key_list[i] in key_test_set
            outf_test.write(ori_line)
    outf_train.close()
    outf_test.close()


if __name__ == '__main__':
    logging_config()
    args = parse_args()
    process(args)
