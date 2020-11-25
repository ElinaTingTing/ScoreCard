# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 09:31:59 2020

@author: secoo
"""
import os
import time
import pickle
import datetime
import pandas as pd
import tkinter as tk
from pandastable import Table
from pandas import DataFrame as df
from tkinter import ttk,Toplevel,Frame,Label,Entry,INSERT,E,W
from tkinter import filedialog


class inputdata():
    def __init__(self,mainfram,project_info):

        self.data_set = df()
        self.data_name = None
        self.data_path = None
        self.data_role = None
        self.data_coding = None
        self.first_load = 'Y'
        
        self.save = 'N'
        self.data_variable_setting = df()

        
        self.node_setting = {'node_type': 'DATA',
                               'node_name': self.data_name,
                               'node_save_path': None,
                               'data_name': self.data_name,
                               'data_path': self.data_path,
                               'data_role': self.data_role,
                               'data_coding': self.data_coding,
                               'data_variable_setting': self.data_variable_setting.copy(),
                               'time': None,
                                 
                               'check_change': [],
                               'use_node': []}  ##不清楚下面这三个的用意
        
        self.project_path =os.path.split(project_info[project_info['模块类型'] == 'project']['保存地址'][0])[0]
        self.exist_data = list(project_info['模块名字'])
        self.master = mainfram
    
    
    
    def load(self, node_info):

        self.data_path = node_info[0]['data_path']
        self.data_role = node_info[0]['data_role']
        self.data_variable_setting = node_info[0]['data_variable_setting']
        self.data_coding = node_info[0]['data_coding']
        self.data_name = node_info[0]['data_name']
        self.data_time = node_info[0]['time']
        self.check_time = node_info[0]['check_change']
        node_save_path = node_info[0]['node_save_path']
        self.data_set = node_info[1]
        self.node_setting = {'node_type': 'DATA',
                             'data_path': self.data_path,
                             'data_role': self.data_role,
                             'data_variable_setting': self.data_variable_setting.copy(),
                             'data_coding': self.data_coding,
                             'data_name': self.data_name,
                             'node_name': self.data_name,
                             'time': self.data_time,
                             'check_change': self.check_time,
                             'node_save_path': node_save_path,
                             'use_node': [],
                             'use_node_path':[]}

        self.first_load = 'N'
        self.save = 'Y'
    
    
  
    
    
    def newdatainput(self):  ##生成导入数据集的界面
        width = 500
        height = 250
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.master.geometry(alignstr)
 
        def selectExcelfile():
            sfname=filedialog.askopenfilename(title="选择CSV文件",filetypes=[('csv', '*.csv')])
            self.E1.delete(0,'end')
            self.E1.insert(INSERT, sfname)
            file_name = os.path.basename(sfname).replace('.csv','')
            self.E2.delete(0,'end')
            self.E2.insert(INSERT,file_name)

        
        L1 = Label(self.master,text="数据集路径")    
        L1.grid(row=0,column=0,columnspan=2,sticky=(W))
        self.E1 = Entry(self.master,width=50,bd=1)
        self.E1.grid(row=0,column=1,sticky=(W))
        button1 = ttk.Button(self.master,text="浏览",command=selectExcelfile,width=8)
        button1.grid(row=0,column=2,sticky=(W))
        
        L1 = Label(self.master,text="数据集名称")
        L1.grid(row=1,column=0,columnspan=2,sticky=(W))
        self.E2 = Entry(self.master,width=20,bd=1)
        self.E2.grid(row=1,column=1,sticky=(W))
        
        L3 = Label(self.master,text="数据集编码")
        L3.grid(row=2,column=0,sticky=(W)) 
        self.combox1 = ttk.Combobox(self.master)
        self.combox1['value']=["utf-8","gbk"]
        self.combox1.current(0)
        self.combox1.grid(row=2,column=1,sticky=(W))
        
        
        L4 = Label(self.master,text="数据集角色")
        L4.grid(row=3,column=0,sticky=(W)) 
        self.combox2 = ttk.Combobox(self.master)
        self.combox2['value']=["Training model","Reject","Out Of Time Sample","Score"]
        self.combox2.current(0)
        self.combox2.grid(row=3,column=1,sticky=(W))
           
        button2 = ttk.Button(self.master,text="确定")
        button2.grid(row=4,column=1,sticky=(W))
        button2.bind("<Button-1>", self.readdata)
        
        
    def readdata(self,event):
        path = self.E1.get()
        name = self.E2.get()
        coding = self.combox1.get()
        datarole = self.combox2.get()
        
        try:
            data = pd.read_csv(path,encoding=coding,low_memory=False)
            if data.empty == True:
                tk.messagebox.showwarning('错误', "错误：数据集为空")
            else:
                settingdata=df()
                settingdata['变量名称']=data.columns
                self.colnum = list(data.select_dtypes(include=['float', 'int8', 'int16', 'int32', 'int64']).columns)
                self.colchar = list(data.select_dtypes(include=['object']).columns)
                settingdata['变量类型'] = settingdata.apply(lambda x: '数值型' if x['变量名称'] in self.colnum else '字符型', axis=1)
                
                remove = []  ##针对字符型的变量有个初判
                remove_char=[]
                for col in list(data.columns):
                    if len(data[col].unique()) < 2:
                        remove.append(col)
                    if (len(data[col].unique()) >50) and (list(settingdata[settingdata['变量名称']==col]['变量类型'])[0]=='字符型'):
                        remove_char.append(col)
                settingdata['是否使用'] = settingdata.apply(lambda x: '不使用' if x['变量名称'] in remove+remove_char else '使用', axis=1)
                settingdata['变量角色'] = settingdata.apply(lambda x: '拒绝' if x['变量名称'] in remove+remove_char else '自变量', axis=1)
                settingdata['备注'] = settingdata.apply(lambda x: '只有一个值' if x['变量名称'] in remove else None, axis=1)
                settingdata['备注'] = settingdata.apply(lambda x: '字符值太多' if x['变量名称'] in remove_char else x['备注'], axis=1)
                
                self.data_path = path
                self.data_set = data
                self.data_role = datarole
                self.data_name = name
                self.data_variable_setting = settingdata
                self.data_coding = coding
                self.variable_seting_ui()
        except Exception as e:
            tk.messagebox.showwarning('错误',e)
            
            
    def variable_seting_ui(self):
        
        for child in self.master.winfo_children(): 
            child.destroy()
        
        self.data_variable_set_ui = self.master
        self.data_variable_set_ui.withdraw()  ##隐藏窗体
        self.data_variable_set_ui.title(self.data_name)
        self.data_variable_set_ui.update()  ##显示窗体
        self.data_variable_set_ui.deiconify()  ##为什么隐藏了窗体后又显示，这个不明白
        
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (
            screenwidth * 0.8, screenheight * 0.8, (screenwidth * 0.2) / 2, (screenheight * 0.2) / 2)
        self.data_variable_set_ui.geometry(alignstr)
        
        test_button4 = ttk.Button(self.data_variable_set_ui, text='保存')
        test_button4.grid(row=0, column=0, sticky=(W))
        test_button4.bind("<Button-1>", self.variable_role_check)
        
        test_button5 = ttk.Button(self.data_variable_set_ui, text='关闭')
        test_button5.grid(row=0, column=1, sticky=(W))
        test_button5.bind("<Button-1>", self.closeall)

        test_button6 = ttk.Button(self.data_variable_set_ui, text='数据探索')
        test_button6.grid(row=0, column=2, sticky=(W))
        test_button6.bind("<Button-1>", self.data_explore)

        test_button7 = ttk.Button(self.data_variable_set_ui, text='数据预览')
        test_button7.grid(row=0, column=3, sticky=(W))
        test_button7.bind("<Button-1>", self.data_preview)

        test_button8 = ttk.Button(self.data_variable_set_ui, text='数据介绍')
        test_button8.grid(row=0, column=4, sticky=(W))
        test_button8.bind("<Button-1>", self.data_detail)
        
        self.refresh_df(mianfram=self.data_variable_set_ui, dfd=self.data_variable_setting)
        
    
    def refresh_df(self, mianfram, dfd):
        f = Frame(mianfram)
        f.grid(row=1, column=0, rowspan=len(dfd),columnspan=6, sticky=(E, W))
        screen_width = f.winfo_screenwidth() * 0.8
        screen_height = f.winfo_screenheight() * 0.8
        self.table = self.ptm = Table(f, dataframe=dfd, colspan=7, height=screen_height, width=screen_width)
        self.table.show()
        self.table.bind("<Button-3>", self.modify_variable_role)
        self.table.bind("<Button-2>", self.modify_variable_role)
        self.table.bind("<Button-1>", self.table.handle_left_click)
        self.table.bind("<Double-Button-3>", self.modify_variable_role)
        self.table.bind("<Double-Button-1>", self.modify_variable_role)
        self.table.bind("<Double-Button-2>", self.modify_variable_role)
        self.table.bind("<Triple-Button-3>", self.modify_variable_role)
        self.table.bind("<Triple-Button-1>", self.modify_variable_role)
        self.table.bind("<Triple-Button-2>", self.modify_variable_role)    
        
        
    def variable_role_check(self,event):
        error=0 ##针对一些以后用到的字段名称有所限制,,这个地方提示错误但是没有办法进行修改？？？？？？？？？？
        if 'SCORE' in self.data_variable_setting['变量名称']:
            error=1
            tk.messagebox.showwarning('错误', "SCORE 将用在以好打分中请更改变量名")
        elif 'SCORECARD_LR_p_1' in self.data_variable_setting['变量名称']:
            error = 1
            tk.messagebox.showwarning('错误', "SCORECARD_LR_p_1 将用在以好打分中请更改变量名")
        elif 'const' in self.data_variable_setting['变量名称']:
            error = 1
            tk.messagebox.showwarning('错误', "const 将用在以后模型训练中请更改变量名")
        elif len(self.data_variable_setting[self.data_variable_setting['变量角色'] == 'TimeID']) == 1:
                timeid=list(self.data_variable_setting[self.data_variable_setting['变量角色'] == 'TimeID']['变量名称'])[0]
                if len(list(self.data_set[timeid].unique()))>30:
                    error=1
                    tk.messagebox.showwarning('错误', "Timeid 数量太多请合并日期")
                    
        if error==0 and len(self.data_variable_setting[self.data_variable_setting['变量角色'] == '目标']) == 0:  ##没有Y
            if self.data_role == 'Training model':
                tk.messagebox.showwarning('错误', "训练集中必须有且只有一个目标")
            else:
                if len(self.data_variable_setting[self.data_variable_setting['变量角色'] == 'TimeID']) > 1:
                    tk.messagebox.showwarning('错误', "最多只有一个TimeID")
                else:
                    self.save_d()
        elif error==0 and len(self.data_variable_setting[self.data_variable_setting['变量角色'] == '目标']) == 1:
            target = list(self.data_variable_setting[self.data_variable_setting['变量角色'] == '目标']['变量名称'])[0]
            if set(self.data_set[target].unique()) != set([0, 1]):
                tk.messagebox.showwarning('错误', "目标角色只能有【0，1】两个值")
            else:
                if self.data_role == 'Training model':
                    if (len(self.data_variable_setting[self.data_variable_setting['变量角色'] == '自变量']) == 0) | (
                            len(self.data_variable_setting[self.data_variable_setting['是否使用'] == '使用']) == 0):
                        tk.messagebox.showwarning('错误', "训练集中至少有一个是可以使用的自变量")
                    else:
                        if len(self.data_variable_setting[self.data_variable_setting['变量角色'] == 'TimeID']) > 1:
                            tk.messagebox.showwarning('错误', "最多只有一个TimeID")
                        else:
                            self.save_d()
                else:
                    if len(self.data_variable_setting[self.data_variable_setting['变量角色'] == 'TimeID']) > 1:
                        tk.messagebox.showwarning('错误', "最多只有一个TimeID")
                    else:
                        self.save_d()
        else:
            tk.messagebox.showwarning('错误', "变量角色中必须有且只有一个目标")
            
        
    def save_d(self):
        colnum = list(self.data_variable_setting[self.data_variable_setting['变量类型'] == '数值型']['变量名称'])
        colchar = list(self.data_variable_setting[self.data_variable_setting['变量类型'] == '字符型']['变量名称'])
        try:
            for col in colnum:
                self.data_set['var'] = self.data_set[col].astype('float')
            for col in colchar:
                self.data_set['var'] = self.data_set[col].astype('object')
              
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            node_save_path = self.project_path + '/' + self.data_name+'.dataset'

            self.node_setting = {'node_type': 'DATA',
                               'node_name': self.data_name,
                               'node_save_path': node_save_path,
                               'data_name': self.data_name,
                               'data_path': self.data_path,
                               'data_role': self.data_role,
                               'data_coding': self.data_coding,
                               'data_variable_setting': self.data_variable_setting.copy(),
                               'time': nowTime,
                                 
                               'check_change': [{'node_name': self.data_name, 'node_time': nowTime}],
                               'use_node': [self.data_name],
                               'use_node_path':[self.data_path]}  ##不清楚下面这三个的用意
            data_save = (self.node_setting, self.data_set)  ##存储了所有的描述信息以及数据集
        
            error2 = Toplevel(self.data_variable_set_ui)
            screenwidth = self.data_variable_set_ui.winfo_screenwidth()
            screenheight = self.data_variable_set_ui.winfo_screenheight()
            
            error2.geometry('%dx%d+%d+%d' % (150, 100, (screenwidth - 150) / 2, (screenheight - 100) / 2))
            L2 = Label(error2, text="保存中")
            L2.grid()
            
            self.data_variable_set_ui.update()
            filename = node_save_path + '.dataset'
            fw = open(filename, 'wb')
            pickle.dump(data_save, fw, 1)
            fw.close()
            
            self.save = 'Y'  ##已经保存的标志
            try:
                time.sleep(2)
                error2.destroy()
            except:
                pass
            self.data_variable_set_ui.update()
  
        except Exception as e:
            tk.messagebox.showwarning('错误', e)
            
        
        
    def closeall(self,event):  
        def final_close(event):
                try:
                    self.tt.destroy() ##数据探索的窗口
                except:
                    pass
                try:
                    self.tt1.destroy()  ##数据预览窗口
                except:
                    pass
                try:
                    self.data_variable_set_ui.destroy()  ##数据展示窗口
                except:
                    pass
                try:
                    self.master.destroy()  ##不知道这个是为了关闭谁？？？？？
                except:
                    pass
                
        if self.save != 'Y':
            tk.messagebox.showwarning('错误', "错误：请先保存您的设置")
        elif self.data_variable_setting.equals(self.node_setting['data_variable_setting'])==False:  ##前后存储，中间有修改
            self.close_tip = Toplevel(self.data_variable_set_ui)
            screenwidth = self.data_variable_set_ui.winfo_screenwidth()
            screenheight = self.data_variable_set_ui.winfo_screenheight()
            self.close_tip.geometry('%dx%d+%d+%d' % (400, 100, (screenwidth - 150) / 2, (screenheight - 100) / 2))
            def close_save(event):
                try:
                    self.close_tip.destroy()
                except:
                    pass
        
                self.save_d()  ##这里不是针对部分修改的就行修改后save,而是全部重新的save,也许日后这里可以优化

            
            L2 = Label(self.close_tip, text="参数设置以更改，是否保存更改")
            L2.grid(column=0, row=0, columnspan=3)
            test_button4 = ttk.Button(self.close_tip, text='保存')
            test_button4.grid(row=1,column=0, sticky=(W))
            test_button4.bind("<Button-1>", close_save)  ##没有保存，采用关闭保存
            
            
    
            test_button4 = ttk.Button(self.close_tip, text='不保存(关闭)')
            test_button4.grid(row=1, column=2, sticky=(W))
            test_button4.bind("<Button-1>", final_close)  ##不保存，维持原来的
            
        else:
            final_close(event)
    
    def data_explore(self,event):
        dd = self.data_set.describe()
        de = dd.T
        de['变量名称'] = de.index
        self.tt = Toplevel()
        self.tt.title(self.data_name)
        f = Frame(self.tt)
        f.grid(column=0, row=1, rowspan=len(de), sticky=(E, W))
        screen_width = f.winfo_screenwidth() * 0.8
        screen_height = f.winfo_screenheight() * 0.8
        ptm = Table(f, dataframe=de, height=screen_height, width=screen_width)
        ptm.show()
         
    def data_preview(self,event):
        data_len = min(200, len(self.data_set))
        self.tt1 = Toplevel()
        self.tt1.title(self.data_name)
        f = Frame(self.tt1)
        f.grid(column=0, row=1, rowspan=data_len, sticky=(E, W))
        screen_width = f.winfo_screenwidth() * 0.8
        screen_height = f.winfo_screenheight() * 0.8
        ptm = Table(f, dataframe=self.data_set.iloc[:data_len,:], height=screen_height, width=screen_width)
        ptm.show()
            
         
    def data_detail(self, event):
        tt = Toplevel(self.master)
        tt.title(self.data_name)
        width = 500
        height = 200
        screenwidth = tt.winfo_screenwidth()
        screenheight = tt.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        tt.geometry(alignstr)


        L1 = Label(tt, width=20, text="数据集路径（CSV):")
        L1.grid(row=0,column=0, sticky=(W))
        L2 = Label(tt, text=self.data_path)
        L2.grid(row=0,column=1, sticky=(W))

        L3 = Label(tt, width=20, text="数据集名称:")
        L3.grid(row=1, column=0, sticky=(W))
        L4 = Label(tt, text=self.data_name)
        L4.grid(row=1, column=1, sticky=(W))

        L5 = Label(tt, width=20, text="数据集编码:")
        L5.grid(row=2, column=0, sticky=(W))
        L6 = Label(tt, text=self.data_coding)
        L6.grid(row=2, column=1, sticky=(W))

        L7 = Label(tt, width=20, text="数据集角色:")
        L7.grid(row=3, column=0, sticky=(W))
        L8 = Label(tt, text=self.data_role)
        L8.grid(row=3, column=1, sticky=(W))

        L9 = Label(tt, width=20, text="数据集样本数:")
        L9.grid(row=4, column=0, sticky=(W))
        L10 = Label(tt, text=len(self.data_set))
        L10.grid(row=4, column=1, sticky=(W))

        L11 = Label(tt, width=20, text="数据集列数:")
        L11.grid(row=5, column=0, sticky=(W))
        L12 = Label(tt, text=self.data_set.shape[1])
        L12.grid(row=5, column=1, sticky=(W))

        L12 = Label(tt, width=20, text="数值型自变量:")
        L12.grid(row=6, column=0, sticky=(W))
        L13 = Label(tt, text=len(self.data_variable_setting[(self.data_variable_setting['变量角色'] == '自变量') & (
                self.data_variable_setting['变量类型'] == '数值型')]))
        L13.grid(row=6, column=1, sticky=(W))

        L14 = Label(tt, width=20, text="字符型自变量:")
        L14.grid(row=7, column=0, sticky=(W))
        L15 = Label(tt, text=len(self.data_variable_setting[(self.data_variable_setting['变量角色'] == '自变量') & (
                self.data_variable_setting['变量类型'] == '字符型')]))
        L15.grid(row=7, column=1, sticky=(W))

        if len(self.data_variable_setting[self.data_variable_setting['变量角色'] == '目标']) == 1:
            target = list(self.data_variable_setting[self.data_variable_setting['变量角色'] == '目标']['变量名称'])[0]
            L11 = Label(tt, width=20, text="坏样本数:")
            L11.grid(row=8, column=0, sticky=(W))
            L12 = Label(tt, text=self.data_set[target].sum())  ##认定1为坏客户
            L12.grid(row=8, column=1, sticky=(W))
            
            
            
    
    
    
    def modify_variable_role(self, event):
        try:
            self.comboxlist_modify_f_group.destroy()
        except:
            pass
        self.rowclicked = self.ptm.get_row_clicked(event)
        self.colclicked = self.ptm.get_col_clicked(event)

        if list(self.data_variable_setting.columns)[self.colclicked] == '是否使用':
            try:
                self.comboxlist_modify_f_group = ttk.Combobox(self.data_variable_set_ui)
                self.comboxlist_modify_f_group["value"] = ['使用', '不使用']
                self.data_variable_set_ui.update()
                self.comboxlist_modify_f_group.place(x=event.x_root - self.data_variable_set_ui.winfo_rootx(),
                                                     y=event.y_root - self.data_variable_set_ui.winfo_rooty())
                self.comboxlist_modify_f_group.bind("<<ComboboxSelected>>", self.variable_role_update)

            except:
                pass

        elif list(self.data_variable_setting.columns)[self.colclicked] == '变量角色':
            try:
                self.comboxlist_modify_f_group = ttk.Combobox(self.data_variable_set_ui)

                self.comboxlist_modify_f_group["value"] = ['自变量', 'ID', 'TimeID', '目标', '以前模型分数']
                self.data_variable_set_ui.update()
                self.comboxlist_modify_f_group.place(x=event.x_root - self.data_variable_set_ui.winfo_rootx(),
                                                     y=event.y_root - self.data_variable_set_ui.winfo_rooty())
                self.comboxlist_modify_f_group.bind("<<ComboboxSelected>>", self.variable_role_update)

            except:
                pass
        elif list(self.data_variable_setting.columns)[self.colclicked] == '变量类型':
            try:
                self.comboxlist_modify_f_group = ttk.Combobox(self.data_variable_set_ui)

                self.comboxlist_modify_f_group["value"] = ['数值型', '字符型']
                self.data_variable_set_ui.update()
                self.comboxlist_modify_f_group.place(x=event.x_root - self.data_variable_set_ui.winfo_rootx(),
                                                     y=event.y_root - self.data_variable_set_ui.winfo_rooty())
                self.comboxlist_modify_f_group.bind("<<ComboboxSelected>>", self.variable_role_update)

            except:
                pass
        else:
            pass
        
        
    def variable_role_update(self, event):
        if (self.comboxlist_modify_f_group.get() == '自变量') & (
                self.data_variable_setting.iloc[self.rowclicked]['备注'] == '只有一个值') & (
                list(self.data_variable_setting.columns)[self.colclicked] == '变量角色'):
            self.comboxlist_modify_f_group.destroy()
            tk.messagebox.showwarning('错误', "该变量只有一个值，不能设置为自变量")
        else:
            value = self.comboxlist_modify_f_group.get()
            self.data_variable_setting.iloc[self.rowclicked, self.colclicked] = value
            self.comboxlist_modify_f_group.destroy()

            self.refresh_df(mianfram=self.data_variable_set_ui, dfd=self.data_variable_setting)
            
