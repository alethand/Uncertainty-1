# -*- coding: utf-8 -*-

import wx
import Sql


class ComnTree(wx.TreeCtrl):
    
    def __init__(self, parent = None):
        
        wx.TreeCtrl.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS)
        
        self.updateTree()
        
#更新导航栏树
    def updateTree(self):
        # Create an image list
        il = wx.ImageList(16,16)

        # Get some standard images from the art provider and add them
        # to the image list
        self.fldridx = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        self.fldropenidx = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, (16,16)))
        self.fileidx = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16,16)))

        self.DeleteAllItems()
        
        record = Sql.selectSql(sql=Sql.modelSql)
        
        self.AssignImageList(il)
            
        """左侧树状图"""
        root = self.AddRoot('模型', data=0)
        self.SetItemImage(root, self.fldridx,
                               wx.TreeItemIcon_Normal)
        self.SetItemImage(root, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
        tree = [0]*100
        treeMap = {}
        i = 0
        for model in record:
            if(model[2] == 0):    #最上层节点
                tree[i] = self.AppendItem(root, model[1], data=model[0])
            else:    #子节点
                tree[i] = self.AppendItem(treeMap[model[2]], model[1], data=model[0])
                self.SetItemImage(treeMap[model[2]], self.fldridx,
                               wx.TreeItemIcon_Normal)
                self.SetItemImage(treeMap[model[2]], self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
            self.SetItemImage(tree[i], self.fileidx,
                                       wx.TreeItemIcon_Normal)
            treeMap[model[0]] = tree[i]
            i += 1
#         self.m_treeCtrl4.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)


# -*- coding: utf-8 -*-

# import wx
#
# import config
# import Sql
# import UPShowPanel
# import mysql.connector
# import UTNotebook
#
#
# class NavPanel(wx.Panel):
#
#     def __init__(self, parent=None):
#
#         wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
#                           wx.DefaultSize, wx.TAB_TRAVERSAL)
#
#         self.bSizer = wx.BoxSizer(wx.VERTICAL)
#
#         self.m_treeCtrl4 = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
#                                        wx.TR_DEFAULT_STYLE)
#
#         db_config = config.datasourse
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor()
#             args = ()
#             cursor.execute(Sql.modelSql, args)
#             record = cursor.fetchall()
#         except mysql.connector.Error as e:
#             print(e)
#         finally:
#             cursor.close()
#             conn.close()
#
#         """左侧树状图"""
#         root = self.m_treeCtrl4.AddRoot('选择模型实验')
#         tree = [[0] * len(record)] * len(record)
#         i = 0
#         for par in record:
#             tree[i] = self.m_treeCtrl4.AppendItem(root, par[1])
#             i += 1
#         self.bSizer.Add(self.m_treeCtrl4, 1, wx.ALL | wx.EXPAND, 5)

#
#     def SelectModel(self, event):
#         item = self.m_treeCtrl4.GetSelection()
#         select_name = self.m_treeCtrl4.GetItemText(item)
#         """不是根节点再进行数据库操作"""
#         if self.m_treeCtrl4.RootItem != item:
#             db_config = config.datasourse
#             try:
#                 conn = mysql.connector.connect(**db_config)
#                 cursor = conn.cursor()
#                 # FIXME:此处用模型名称查询 目前没有找到获取到树编号的方法 后期需要修改 以应对名称重复的情况
#                 cursor.execute((Sql.get_arg_Sql + " '" + select_name + "';"))
#                 record = cursor.fetchall()
#             except mysql.connector.Error as e:
#                 print(e)
#             finally:
#                 cursor.close()
#                 conn.close()
#
#             """"模型ID"""""
#             model_id = record[0][6]
#             print(">>>>>>>>>>>>>>>>>>>>>>>>>>", model_id)
#
#             """"得到分布类型"""""
#             dtype = []
#             for t in record:
#                 dtype.append(t[2])
#             """"得到分布参数"""
#             paras = []
#             for par in record:
#                 args = par[3].split(" ")
#                 a = []
#                 for p in args:
#                     a.append(float(p))  # 每个a是每一个参数的分布参数
#                 paras.append(a)  # paras 包含所有参数的分布参数
#             """"参数名称"""""
#             parname = []
#             """"参数ID"""""
#             parid = []
#             """"参数类型"""""
#             partype = []
#             for par in record:
#                 parname.append(par[1])
#                 parid.append(par[4])
#                 partype.append(par[5])
#             """"传参到抽样方法选择模块"""
#             UTN = UTNotebook.UTNotebook()
#             UTN.Para = Para(dtype, paras, parname, parid, partype, model_id)
#             UTN.ShowArg(record)
#
#
# # 将传参集中在一个类中
# # 对于同一个模型的参数 参数名字是不会重复的 每次抽出来的都是同一个模型的参数 则参数名可以唯一确定一行记录
# class Para:
#     def __init__(self, dtype=None, paras=None, parname=None, parid=None, partype=None, modelid=None):
#         self.dtype = dtype
#         self.para = tuple(paras)
#         self.name = parname
#         self.parid = parid
#         self.partype = partype
#         self.model_id = modelid