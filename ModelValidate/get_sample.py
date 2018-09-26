# -*- coding: utf-8 -*-

import Sql
import numpy as np

#arg_type = 0取自变量   1取固有  2是认知
def get_samp(nid = 9, arg_type = 2):
    count = Sql.selectSql((nid, arg_type), Sql.get_sampling_count)
    # print 'count: %s' %count
    count = count[0][0]
    records = Sql.selectSql((nid, arg_type), Sql.get_samp1)
    records = [record[1] for record in records]
    samps = [records[i:i + count] for i in range(0, len(records), count)]
    # print samps
    flag = 0
    for samp in samps:
        if flag == 0:
            mat = samp
            flag = 1
        else:
            mat = np.row_stack((mat, samp))

    mat = np.mat(mat)
    # print mat.shape
    #这就是参数数据，每列代表一个参数，每行代表观测次数
    mat = mat.T
    # print mat.shape
    # print mat
    return mat

def get_samp2(nid = 9, arg_type = 1):
    records = Sql.selectSql((nid, arg_type), Sql.get_samp2)
    flag = 0
    for record in records:
        samps = record[1].decode('utf-8')
        samps = samps.split(',')
        print len(samps)
        samps = [float(samp) for samp in samps]
        if flag == 0:
            mat = samps
            flag = 1
        else:
            mat = np.row_stack((mat, samps))
    mat = np.mat(mat)
    print mat.shape
    mat = mat.T
    print mat.shape
    return mat

if __name__ == '__main__':
    get_samp(76,1)