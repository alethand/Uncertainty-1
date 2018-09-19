# -*- coding: utf-8 -*-

import Sql
import numpy as np

#arg_type = 0取自变量   1取固有  2是认知
def get_samp(nid = 9, arg_type = 2):
    count = Sql.selectSql((nid, arg_type), Sql.get_sampling_count)
    count = count[0][0]
    records = Sql.selectSql((nid, arg_type), Sql.get_samp1)
    records = [record[1] for record in records]
    samps = [records[i:i + count] for i in range(0, len(records), count)]
    flag = 0
    for samp in samps:
        if flag == 0:
            mat = samp
            flag = 1
        else:
            mat = np.row_stack((mat, samp))

    mat = np.mat(mat)
    print mat.shape
    mat = mat.T
    print mat.shape

    # print mat
    # mat = np.transpose(mat)
    # print mat
    # mat = np.mat(mat)
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
    # mat = np.transpose(mat)
    #
    # mat = np.mat(mat)
#     print mat
#     print mat.shape
    # print type(mat)
    # print mat.shape
    # tmat =  mat[:, 0:1]
    # print type(tmat)
    # print tmat.shape
    # shape = tmat.shape
    # print shape[0]
    return mat

if __name__ == '__main__':
    get_samp()