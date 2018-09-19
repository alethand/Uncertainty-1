# -*- coding: utf-8 -*-

import wx

import config
import Sql
import mysql.connector
import UTNotebook

class NavPanel(wx.Panel):
    
    def __init__(self, parent = None):
        
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TAB_TRAVERSAL)

        self.bSizer = wx.BoxSizer(wx.VERTICAL)

        self.m_treeCtrl4 = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TR_DEFAULT_STYLE)

        db_config = config.datasourse
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            args = ()
            cursor.execute(Sql.modelSql, args)
            record = cursor.fetchall()
        except mysql.connector.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

        """左侧树状图"""
        root = self.m_treeCtrl4.AddRoot('选择模型实验')
        tree = [[0] * len(record)] * len(record)
        i = 0
        for par in record:
             tree[i] = self.m_treeCtrl4.AppendItem(root, par[1])
             i += 1
        self.bSizer.Add(self.m_treeCtrl4, 1, wx.ALL | wx.EXPAND, 5)
        """双击选择模型"""
        self.m_treeCtrl4.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.SelectModel)


        """"""""""""""""""""
        self.SetSizer(self.bSizer)
        self.Layout()
        self.bSizer.Fit(self)

    def SelectModel(self, event):
        item = self.m_treeCtrl4.GetSelection()
        select_name = self.m_treeCtrl4.GetItemText(item)
        """不是根节点再进行数据库操作"""
        if self.m_treeCtrl4.RootItem != item:
            db_config = config.datasourse
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                # FIXME:此处用模型名称查询 目前没有找到获取到树编号的方法 后期需要修改 以应对名称重复的情况
                cursor.execute((Sql.get_arg_Sql + " '" + select_name + "';"))
                record = cursor.fetchall()
            except mysql.connector.Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

            """"模型ID"""""
            model_id = record[0][6]
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>",model_id)

            """"得到分布类型"""""
            dtype = []
            for t in record:
                dtype.append(t[2])
            """"得到分布参数"""
            paras = []
            for par in record:
                args = par[3].split(" ")
                a = []
                for p in args:
                    a.append(float(p))# 每个a是每一个参数的分布参数
                paras.append(a) # paras 包含所有参数的分布参数
            """"参数名称"""""
            parname = []
            """"参数ID"""""
            parid = []
            """"参数类型"""""
            partype = []
            for par in record:
                parname.append(par[1])
                parid.append(par[4])
                partype.append(par[5])
            """"传参到抽样方法选择模块"""
            UTN =UTNotebook.UTNotebook()
            UTN.Para = Para(dtype, paras, parname, parid, partype, model_id)
            UTN.ShowArg(record)

# 将传参集中在一个类中
# 对于同一个模型的参数 参数名字是不会重复的 每次抽出来的都是同一个模型的参数 则参数名可以唯一确定一行记录
class Para:
    def __init__(self, dtype=None, paras=None, parname=None, parid=None, partype=None,modelid=None):
        self.dtype = dtype
        self.para = tuple(paras)
        self.name = parname
        self.parid = parid
        self.partype = partype
        self.model_id = modelid