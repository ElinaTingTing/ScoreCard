# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:51:13 2020

@author: secoo
"""
import os
import pickle
import datetime
import pandas as pd
from pandas import DataFrame as df
import tkinter as tk
from tkinter import filedialog
from os.path import exists
from pandastable import Table
from tkinter import Tk,Toplevel,LabelFrame,Frame,Label,Entry,INSERT,Menu,E,W,ttk
from load_node import import_node 
from inputdata import inputdata
from split import spliting



class scorecard():
    def __init__(self):
        self.row = 0
        self.col = 0  ##目前不清楚是干什么的
        
        self.project_name = None
        self.project_path = None
        self.project_seting = {}
        self.project_detail = df(columns=['模块类型', '模块名字', '引用模块', '保存地址', '状态','创建时间'])
       
        self.root = Tk()
        self.Start_UI()
        self.root.withdraw()
        self.root.mainloop()
    

    
    def Start_UI(self):
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        winWidth = 500
        winHeight = 200
        x = int((self.screenWidth - winWidth) / 2)
        y = int((self.screenHeight - winHeight) / 2)
        
        self.start_window_base = Toplevel(self.root)  ##不明白为什么使用toplevel，是否是别的都消失这个也会存在
        self.start_window_base.title('项目')
        self.start_window_base.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        
        def selectExcelfold():
            sfname = filedialog.askdirectory()
            self.project_path_E.insert(INSERT, sfname)
            
        self.start_window = LabelFrame(self.start_window_base, text='创建新项目')
        L1 = Label(self.start_window, text="项目路径")
        L1.grid(row=0,column=0, sticky=(W))
        self.project_path_E = Entry(self.start_window, width=50, bd=1)
        self.project_path_E.grid(row=0,column=1,sticky=(W))
        button1 = ttk.Button(self.start_window, text='浏览', width=8, command=selectExcelfold)
        button1.grid(row=0,column=2, sticky=(W))

        L2 = Label(self.start_window, text="项目名称")
        L2.grid(row=1,column=0,sticky=(W))
        name = tk.StringVar(value='scorecard1')
        self.project_name_E = Entry(self.start_window, textvariable=name, bd=1)
        self.project_name_E.grid(row=1,column=1,sticky=(W))

        test_button4 = ttk.Button(self.start_window, text='确定',command=self.new_project)
        test_button4.grid(row=2,column=1, sticky=(W))
        
        self.start_window.grid(row=0,column=0, columnspan=2, rowspan=3)


        def selectExcelfile():
            sfname = filedialog.askopenfilename(title='选择project文件', filetypes=[('project', '*.project')])
            self.project_path_Ex.insert(INSERT, sfname)

        self.start_window_ex = LabelFrame(self.start_window_base, text='导入现有项目')
        L5 = Label(self.start_window_ex, text="项目路径")
        L5.grid(row=4,column=0, sticky=(W))
        self.project_path_Ex = Entry(self.start_window_ex, width=50, bd=1)
        self.project_path_Ex.grid(row=4,column=1, sticky=(W))
        button1 =ttk.Button(self.start_window_ex, text='浏览', width=8, command=selectExcelfile)
        button1.grid(row=4,column=2,sticky=(W))

        test_button5 =ttk.Button(self.start_window_ex, text='导入',command=self.load_project)
        test_button5.grid(row=5,column=1, sticky=(W))
        self.start_window_ex.grid()
    
    
    def new_project(self,event):
        self.project_name = self.project_name_E.get()
        self.project_path = self.project_path_E.get()+ '/' + '%s.project' % self.project_name
        if exists(self.project_path)==False:
            self.project_seting = {'project_name': self.project_name, 'project_path': self.project_path}
            tt = [{'模块类型': 'project',
                   '模块名字': self.project_name,
                   '引用模块': [],
                   '保存地址': self.project_path,
                   '状态': 'Good',
                   '创建时间':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') }]
            mm = df(tt)
            self.project_detail = self.project_detail.append(mm)

            try:
                self.save_project()
            except Exception as e:
                tk.messagebox.showwarning('错误', e)
                self.start_window_base.destroy()
                self.root.destroy() 
                self.__init__()  ##出错后重新调用了一遍
            self.start_window_base.destroy()
            self.base_UI()
        else:
            tk.messagebox.showwarning('错误', '在文件夹下有同名项目')
        

    def save_project(self):
        filename = self.project_path
        fw = open(filename, 'wb')
        pickle.dump(self.project_detail, fw)  ##项目里面存的是项目的名称以及数据集的路径，并没有存储数据
        fw.close()  
        
                 
    def load_project(self):
        try:
            project_add = self.project_path_Ex.get()
            fr = open(project_add, 'rb')
            project_info = pickle.load(fr)
            fr.close()
            self.project_detail = project_info
            
            self.project_path = project_add
            self.project_name = self.project_detail[self.project_detail['模块类型'] == 'project']['模块名字'][0]
            self.project_detail['保存地址'][self.project_detail['模块类型'] == 'project']=self.project_path
            self.start_window_base.destroy()
            self.base_UI()
        except Exception as e:
            tk.messagebox.showwarning('错误', e)
    
    
    def base_UI(self):

        self.root.update()
        self.root.deiconify()  ##显示窗口
        
        winWidth = 1000
        winHeight = 600
        x = int((self.screenWidth - winWidth) / 2)
        y = int((self.screenHeight - winHeight) / 2)
        self.root.title(self.project_name)
        self.root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

        
        menubar = Menu(self.root)  ##顶级菜单
        sysmenu_save = Menu(menubar, tearoff=False)
        sysmenu_load_node = Menu(menubar, tearoff=False)
        sysmenu_inputdata = Menu(menubar, tearoff=False)
        sysmenu_data_deal = Menu(menubar, tearoff=False)
        sysmenu_IGN = Menu(menubar, tearoff=False)
        sysmenu_model = Menu(menubar, tearoff=False)
        
        
        menubar.add_cascade(label='保存/刷新',menu=sysmenu_save)
        sysmenu_save.add_command(label='保存项目',command=self.save_project)
        sysmenu_save.add_command(label='刷新', command=lambda: self.refresh_df(self.root, self.project_detail))

        menubar.add_cascade(label='导入模块', menu=sysmenu_load_node)
        sysmenu_load_node.add_command(label='导入', command=lambda: self.func_menu('load_node'))

        menubar.add_cascade(label='导入数据集', menu=sysmenu_inputdata)
        sysmenu_inputdata.add_command(label='添加', command=lambda: self.func_menu('importdata'))

        menubar.add_cascade(label='数据集处理', menu=sysmenu_data_deal)
        sysmenu_data_deal.add_command(label='分区', command=lambda: self.func_menu('split'))
        sysmenu_data_deal.add_command(label='抽样', command=lambda: self.func_menu('sampling'))

        menubar.add_cascade(label='交互分组', menu=sysmenu_IGN)
        sysmenu_IGN.add_command(label='单变量分组', command=lambda: self.func_menu('IGN'))

        menubar.add_cascade(label='评分卡', menu=sysmenu_model)
        sysmenu_model.add_command(label='训练模型', command=lambda: self.func_menu('model'))
        sysmenu_model.add_command(label='数据集打分', command=lambda: self.func_menu('Scoring'))

        self.root.grid()
        self.root.config(menu=menubar)
        self.refresh_df(self.root, self.project_detail)
        self.root.update()
        
        
    def refresh_df(self, mianfram, project_detail):
        try:
            self.save_project()
        except Exception as e:
            tk.messagebox.showwarning('错误', e)
        project_detail['状态'] = project_detail.apply(lambda x: 'Good' if x['模块类型'] == 'project' else self.refresh_check(x['保存地址']), axis=1)
#        project_detail = project_detail[['模块类型', '模块名字', '引用模块', '保存地址', '状态','创建时间']]
        f = Frame(mianfram)
        f.grid(row=1, column=0, rowspan=1,columnspan=5, sticky=(E, W))
        screen_width = f.winfo_screenwidth() * 0.8
        screen_height = f.winfo_screenheight() * 0.8
        self.table = self.ptm = Table(f, dataframe=project_detail, height=screen_height, width=screen_width)
        ##Table本身为tkinter的class
        self.table.show()
        self.table.grid()
        self.table.bind("<Button-2>", self.right_click_menu)  ##使用bind原因为保证相应的事件发生后调用相应的函数
        self.table.bind("<Button-3>", self.right_click_menu)
        self.table.bind("<Double-Button-1>", self.right_click_menu)
        self.table.bind("<Double-Button-2>", self.right_click_menu)
        self.table.bind("<Double-Button-3>", self.right_click_menu)


    def refresh_check(self, node_save_path):  ##检查保存的项目信息是否有问题，能否正常打开
        p2 = Label(self.root, text='checking.... \n wait.....')
        p2.grid(row=0, column=0)
        self.root.update()
        try:
            fr = open(node_save_path, 'rb')
            fr.close()
            p2.destroy()
            return 'Good'
        except Exception as e:
            p2.destroy()
            return 'error'   
   

    def right_click_menu(self, event):
        rowclicked = self.ptm.get_row_clicked(event)
        colclicked = self.ptm.get_col_clicked(event)
        menu = Menu(self.root)
        sysmenu_inputdata = Menu(menu, tearoff=False)
        menu.add_command(label="设置", command=lambda: self.ope(rowclicked, colclicked,'setting'))
        menu.add_separator() ##分割线
        menu.add_command(label="结果", command=lambda: self.ope(rowclicked, colclicked,'result'))
        menu.add_separator()
        menu.add_command(label="删除", command=lambda: self.delet(rowclicked, colclicked))
        menu.post(event.x_root, event.y_root) ##弹出菜单栏


    
    def ope(self, rowclicked, colclicked,ty):
        node_type = self.project_detail.iloc[rowclicked]['模块类型']
        node_name = self.project_detail.iloc[rowclicked]['模块名字']
        node_save_path = self.project_detail.iloc[rowclicked]['保存地址']
        try:
            fr = open(node_save_path, 'rb')
            node_info = pickle.load(fr)
            fr.close()
            flag_error = 0
        except Exception as e:
            flag_error = 1
            tk.messagebox.showwarning('错误', e)
        if flag_error != 1:
            try:
                if self.root2.state() == 'normal':
                    tk.messagebox.showwarning('错误', "请先处理当前打开窗口")
            except:
                self.root2 = Toplevel(self.root)
                self.root2.title(node_name)
                # try:
                if node_type == 'DATA':
                    new_node = inputdata(self.root2, self.project_detail)
                    new_node.load(node_info)
                    new_node.variable_seting_ui()
                elif node_type == 'SPLIT':
                    new_node = spliting(self.root2, self.project_detail)
                    new_node.load_node(node_data=node_info, ac=ty)
                elif node_type == 'SAMPLE':
                    new_node = sample(self.root2, self.project_detail)
                    new_node.load_node(node_data=node_info, ac=ty)
                elif node_type == 'IGN':
                    new_node = IGN(self.root2, self.project_detail)
                    new_node.load_node(node_info,ac=ty)
                elif node_type == 'SCR':
                    new_node = model(self.root2, self.project_detail)
                    new_node.import_node(node_info,ac=ty)
                elif node_type == 'Scoring':
                    new_node = scoreing(self.root2, self.project_detail)
                    new_node.load_node(node_info,ac=ty)

                self.root.wait_window(self.root2)
                try:
                    tt = [{'模块类型': new_node.node_setting['node_type'],
                           '模块名字': new_node.node_setting['node_name'],
                           '引用模块': new_node.node_setting['use_node'],
                           '保存地址': new_node.node_setting['node_save_path'],
                           '创建时间': new_node.node_setting['time'],
                           '状态': 'Good'}]

                    mm = pd.DataFrame(tt)
                    self.project_detail = self.project_detail[self.project_detail['模块名字'] != node_name]
                    self.project_detail = self.project_detail.append(mm)
                    self.refresh_df(self.root, self.project_detail)
                except:
                    pass
    

    
    def delet(self, rowclicked, colclicked):
        node_name = self.project_detail.iloc[rowclicked]['模块名字']
        node_save_path = self.project_detail.iloc[rowclicked]['保存地址']
        try:
            os.remove(node_save_path)
            self.project_detail = self.project_detail[self.project_detail['模块名字'] != node_name]
            self.refresh_df(self.root, self.project_detail)
        except  Exception as e:
            tk.messagebox.showwarning('错误', e)
            self.project_detail = self.project_detail[self.project_detail['模块名字'] != node_name]
            self.refresh_df(self.root, self.project_detail)
    
    
    def func_menu(self, func):
        try:
            if self.root2.state() == 'normal':
                tk.messagebox.showwarning('错误', "请先处理当前打开窗口")
        except:
            self.root2 = Toplevel(self.root)
            if func == 'importdata':
                self.root2.title('导入数据集')
                new_node = inputdata(self.root2, self.project_detail)
                new_node.newdatainput()
                tip = '导入数据集'
            elif func == 'split':
                self.root2.title('数据集分区')
                new_node = spliting(self.root2, self.project_detail)
                new_node.ui_start()
                tip = '数据集分区'
            elif func == 'sampling':
                self.root2.title('数据集抽样')
                new_node = sample(self.root2, self.project_detail)
                new_node.ui_start()
                tip = '数据集抽样'
            elif func == 'IGN':
                self.root2.title('交互式分组')
                new_node = IGN(self.root2, self.project_detail)
                new_node.Start_UI()
                new_node.adjustsetting()
                tip = '交互式分组'
            elif func == 'model':
                self.root2.title('评分卡模型')
                new_node = model(self.root2, self.project_detail)
                new_node.Start_UI()
                new_node.adjustsetting()
                tip = '评分卡模型'
            elif func == 'Scoring':
                self.root2.title('数据集打分')
                new_node = scoreing(self.root2, self.project_detail)
                new_node.Start_UI()
                new_node.adjustsetting()
                tip = '数据集打分'
            elif func == 'load_node':
                new_node = import_node(self.root2, self.project_detail)
                tip = '导入模块'
            self.root.wait_window(self.root2)

            if new_node.save != 'Y':
                tk.messagebox.showwarning('错误', "%s未完成" % tip)
            else:
                try:
                    print(new_node.save)
                    tt = [{'模块类型': new_node.node_setting['node_type'],
                           '模块名字': new_node.node_setting['node_name'],
                           '引用模块': new_node.node_setting['use_node'],
                           '保存地址': new_node.node_setting['node_save_path'],
                           '创建时间': new_node.node_setting['time'],
                           '状态': 'Good'}]

                    mm = pd.DataFrame(tt)
                    print(mm)
                    self.project_detail = self.project_detail.append(mm)
                    # del new_node
                    self.refresh_df(self.root, self.project_detail)
                except Exception as e:
                    tk.messagebox.showwarning('错误', "%s未完成%s" % (tip, e))

