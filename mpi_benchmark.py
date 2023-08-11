# coding:utf-8

import os
import shutil
import sys
import glob
import multiprocessing
import argparse
import logging
import datetime
import uuid

# prefix s
today = datetime.date.today().strftime('%y%m%d')
logger_level = logging.INFO
#logger_level = logging.DEBUG
logging.basicConfig(level=logger_level, format='%(asctime)s - %(name)s -%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

snowboy_path = '/home/zhangyongchao/snowboy/'
eval_path = snowboy_path + '/src/bin/snowboy-universal-eval'
resource_path = snowboy_path + '/scripts/python_api/resources/universal/universal_detect.res'


## 解析参数
def parse_args():
    parser = argparse.ArgumentParser('run snowboy-unversal-detect multi-processing')
    parser.add_argument('wav_list', type=str, help='wav list to be benchmark')
    parser.add_argument('model', type=str, help='model file to be benchmark')
    parser.add_argument('log_dir', type=str, help='output log dir for result of benchmark')
    parser.add_argument('--tmp_dir', type=str, default='./tmps')
    parser.add_argument('-nj', '--multiprocessing', type=int, default=24, help='number of parallel thread')
    parser.add_argument('--sen', type=str, default='0.5', help='sensitivity')
    parser.add_argument('--hi_sen', type=str, default='0.5', help='high sensitivity')

    args = vars(parser.parse_args())

    if os.path.exists(args['log_dir']):
        shutil.rmtree(args['log_dir'])
    os.makedirs(args['log_dir'], exist_ok=True)
    os.makedirs(args['tmp_dir'], exist_ok=True)
    print(args)
    return args


def task(part_id, idx_st, idx_ed, total_part):
    global arguments, str_uuid, today, model_list_fn
    tmp_dir = arguments['tmp_dir']
    cur_list_fn = '%s/%s_%d.list' % (arguments['tmp_dir'], str_uuid, part_id)
    for i in range(idx_st, idx_ed):
        with open(cur_list_fn, 'w') as f:
            f.write(total_part[i])
        wav_fn = os.path.split(total_part[i])[1]
        wav_fn_pre = os.path.splitext(wav_fn)[0]
        log_fn = '%s/%s.log' % (arguments['log_dir'], wav_fn_pre)
        str_cmd = '%s --verbose=1 ' % eval_path + \
                '--wa.process-as-one-file=false ' + \
                '--detectp.gc.audio-gain=1 ' + \
                '--detectp.apply-frontend=true '  + \
                '--sensitivity-str="%s" ' % arguments['sen'] + \
                '--high-sensitivity-str="%s" ' % arguments['hi_sen'] + \
                '--resource-filename=%s %s %s > %s 2>&1' % (resource_path,
                        model_list_fn, cur_list_fn, log_fn)
        #print(str_cmd)
        os.system(str_cmd)


if __name__ == '__main__':

    ## 系统环境和参数读取
    arguments = parse_args()
    str_uuid = uuid.uuid4().hex
    model_list_fn = '%s/%s_model.list' % (arguments['tmp_dir'], str_uuid)
    with open(model_list_fn, 'w') as f:
        f.write(arguments['model'])

    ## 加载wav_list
    with open(arguments['wav_list'], 'r') as fp:
        wav_list_lines = fp.readlines()

    logger.info('%d wav files in feat_scp' % len(wav_list_lines))

    # assign multiprocessing task
    pool = multiprocessing.Pool(processes=arguments['multiprocessing'])
    part_number = (len(wav_list_lines) + arguments['multiprocessing'] - 1) // arguments['multiprocessing']
    for i in range(arguments['multiprocessing']):
        idx_st = i * part_number
        idx_ed = min((i + 1) * part_number, len(wav_list_lines))

        pool.apply_async(task, (i, idx_st, idx_ed, wav_list_lines))
    pool.close()
    pool.join()
    # clean temp folder
    #str_cmd = 'rm -rf %s' % arguments['tmp_dir']
    #os.system(str_cmd)
