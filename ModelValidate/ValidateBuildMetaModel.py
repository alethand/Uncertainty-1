# -*- coding: utf-8 -*-
import ValidateRealModel as rm
import ValidateDoubleLoop
import get_sample as gs
import data_related as dr
import distance as dis

def import_model_data(n_id):
    # 认知参数
    cog_p = gs.get_samp(nid=n_id, arg_type=2)  # 根据你选择的模型导入相应的数据
    # 固有参数
    inh_p = gs.get_samp(nid=n_id, arg_type=1)
    # 自变量
    input_X = gs.get_samp(nid=n_id, arg_type=0)
    # print cog_p
    # print inh_p
    # print input_v

    # 生成真实数据
    real_d = rm.run_real_model(inh_p, input_X)
    cog_real = rm.cog_p_real

    # 生成模型数据
    model_d = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, input_X)

    return model_d, real_d
    # 直接用生成的数据
    # return dr.model_d,dr.real_d

def build_euc_dis(model_d, real_d):
    cog_sim = {}
    cog_sim['euc'] = dr.cal_simiarity(model_d, real_d, dis.euclidean)
    cog_df = dr.get_dataframe(model_d, cog_sim)
    return cog_df


def build_mah_dis(model_d, real_d):
    cog_sim = {}
    cog_sim['mah'] = dr.cal_simiarity(model_d, real_d, dis.mahalanobis)
    cog_df = dr.get_dataframe(model_d, cog_sim)
    return cog_df


def build_che_dis(model_d, real_d):
    cog_sim = {}
    cog_sim['che'] = dr.cal_simiarity(model_d, real_d, dis.chebyshev)
    cog_df = dr.get_dataframe(model_d, cog_sim)
    return cog_df


def build_man_dis(model_d, real_d):
    cog_sim = {}
    cog_sim['man'] = dr.cal_simiarity(model_d, real_d, dis.manhattan)
    cog_df = dr.get_dataframe(model_d, cog_sim)
    return cog_df


def build_KL_dis(model_d, real_d):
    cog_sim = {}
    cog_sim['KL'] = dr.cal_simiarity(model_d, real_d, dis.KL)
    cog_df = dr.get_dataframe(model_d, cog_sim)
    return cog_df
