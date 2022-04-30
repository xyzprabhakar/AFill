import fontawesome as fa
from multiprocessing.sharedctypes import Value
from tkinter import TOP, font
#import PyPDF2 as pdf
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
from io import StringIO
import os

import tabula 
#from tabula import read_pdf
#from tabulate import tabulate

import io
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import ttk,messagebox
import GenerateConfig as Gc
import json

# import webdriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



class Setting(ttk.Frame):
    config=None    
    varName,varContactNo,varEmail=None,None,None
    varLocation,varTemplateFile,varDataFile=None,None,None
    def __init__(self,Container,config):  
        self.config=config   
        self.ContainerFrame=Container
        self.displayFont = ( "Verdana", 10)       
        self.varName,self.varContactNo,self.varEmail = tk.StringVar(), tk.StringVar(), tk.StringVar()        
        self.varLocation,self.varTemplateFile,self.varDataFile = tk.StringVar(), tk.StringVar(), tk.StringVar()        
        self.LoadData()
        self.fncCreateItems()        

    def LoadData(self):
        
        self.varName.set(self.config.Name)
        self.varContactNo.set(self.config.ContactNo)
        self.varEmail.set(self.config.Email)
        self.varLocation.set(self.config.FilePath)
        self.varTemplateFile.set(self.config.TemplateFileName)
        self.varDataFile.set(self.config.DataFileName)

    def fncCreateItems(self):
        

        frmHeader,frmBody  = ttk.Frame(self.ContainerFrame) ,ttk.Frame(self.ContainerFrame)        
        self.ContainerFrame.grid_columnconfigure(0, weight=100)
        self.ContainerFrame.grid_rowconfigure(0, weight=1)
        self.ContainerFrame.grid_rowconfigure(1, weight=100)

        frmHeader.grid(row=0,column = 0, sticky=tk.N+tk.S+tk.W+tk.E, padx=(10,10))
        frmBody.grid(row=1,column = 0,  sticky=tk.N+tk.S+tk.W+tk.E, padx=(10,10))

        frmHeader.columnconfigure(0, weight=100)                
        frmHeader.rowconfigure(0, weight=1)        
        
        frmBody.columnconfigure(0, weight=100) 
        frmBody.rowconfigure(0, weight=1)        
        frmBody.rowconfigure(1, weight=1)        
        frmBody.rowconfigure(2, weight=1)        
        frmBody.rowconfigure(3, weight=1)        

        frmbtn1 = ttk.Frame(frmHeader)        
        frmbtn1.grid(row=0,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnReffreshData = tk.Button ( frmbtn1,name="btnReffreshData", text =fa.icons['sync'], relief='groove', width=3,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command = lambda :self.LoadData() )
        btnReffreshData.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        
        frmUserDetails=ttk.LabelFrame(frmBody,text="User Details",style="Details.TLabelframe")
        frmUserDetails.columnconfigure(0, weight=100) 
        frmUserDetails.rowconfigure(0, weight=100) 
        frmUserDetails.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        frmUserDetailsInnerData=ttk.Frame(frmUserDetails)
        frmUserDetailsInnerData.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        
        ttk.Label(frmUserDetailsInnerData,text="Name").grid(row=0,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmUserDetailsInnerData,text="Contact No").grid(row=1,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmUserDetailsInnerData,text="Email").grid(row=2,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Entry(frmUserDetailsInnerData,textvariable=self.varName,state=tk.DISABLED, width=50 ).grid(row=0,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmUserDetailsInnerData,textvariable=self.varContactNo,state=tk.DISABLED, width=50).grid(row=1,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmUserDetailsInnerData,textvariable=self.varEmail,state=tk.DISABLED, width=50).grid(row=2,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))


        frmFileDetails=ttk.LabelFrame(frmBody,text="File Setting",style="Details.TLabelframe",)
        frmFileDetails.columnconfigure(0, weight=100) 
        frmFileDetails.rowconfigure(0, weight=100) 
        frmFileDetails.grid(row=1,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        frmFileDetailsInnerData=ttk.Frame(frmFileDetails)
        frmFileDetailsInnerData.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        
        ttk.Label(frmFileDetailsInnerData,text="Location").grid(row=0,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmFileDetailsInnerData,text="Template File").grid(row=1,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmFileDetailsInnerData,text="Data File").grid(row=2,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Entry(frmFileDetailsInnerData,textvariable=self.varLocation, width=50).grid(row=0,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmFileDetailsInnerData,textvariable=self.varTemplateFile, width=50).grid(row=1,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmFileDetailsInnerData,textvariable=self.varDataFile, width=50).grid(row=2,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))

        # frmBody.columnconfigure(0, weight=1)
        # frmBody.columnconfigure(1, weight=100)  
        # frmBody.rowconfigure(0, weight=100)  
        # self.frmLeftPanel,self.frmRightPanel= ttk.Frame(frmBody,width=300),ttk.Frame(frmBody)
        
        # self.frmLeftPanel.grid(row=0,column=0,sticky=tk.N+tk.S+tk.W+tk.E,padx=(10,10))
        # self.frmRightPanel.grid(row=0,column=1,sticky=tk.N+tk.S+tk.W+tk.E,padx=(10,10))
        # self.txtData= tk.Text(self.frmRightPanel, name="txtData")
        # self.txtData.grid(row=0,column = 0,columnspan=3 ,padx=(0, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W+tk.E)

        
        # self.frmLeftPanel.columnconfigure(0, weight=1)
        # self.frmLeftPanel.columnconfigure(1, weight=100)
        # self.frmLeftPanel.rowconfigure(0, weight=1)
        # self.frmLeftPanel.rowconfigure(1, weight=1)
        # self.frmLeftPanel.rowconfigure(2, weight=1)
        # self.frmLeftPanel.rowconfigure(3, weight=1)
        # self.frmLeftPanel.rowconfigure(4, weight=1)
        # self.frmLeftPanel.rowconfigure(5, weight=1)        
        # self.frmLeftPanel.rowconfigure(6, weight=100)

        # ttk.Label(self.frmLeftPanel,text="Template").grid(row=0,column=0,sticky=tk.N+tk.S+tk.W,pady=(10,3),padx=(10,10))
        # self.ddlTemplateName=ttk.Combobox(self.frmLeftPanel,textvariable = self.varCurrentTemplateName,values=self.varAllTemlateName,width=26)
        # self.ddlTemplateName.grid(row=0,column=1,sticky=tk.N+tk.S+tk.W,pady=(10,3))
        # ttk.Label(self.frmLeftPanel,text="File Name").grid(row=1,column=0,sticky=tk.N+tk.S+tk.W,pady=(10,3),padx=(10,10))
        # self.ddlFileName=ttk.Combobox(self.frmLeftPanel,textvariable = self.varCurrentDataFileName,values=self.varAllJsonFileName,width=26)
        # self.ddlFileName.grid(row=1,column=1,sticky=tk.N+tk.S+tk.W,pady=(10,3))
        

        # self.frmInnerContentFrame1 = ttk.Frame(self.frmLeftPanel)
        # self.frmInnerContentFrame1.grid(row=6, column=0,columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)  
        # frmbtn2 = ttk.Frame(self.frmLeftPanel)        
        # frmbtn2.grid(row=2,column = 0,columnspan=2,pady=(10,3),padx=(10,10) )
        # ttk.Button (frmbtn2, text ="Open Browser", width=12, command =lambda: self.Open_Browser()).grid(row=0,column = 0,padx=(5,5) )
        # ttk.Button ( frmbtn2, text ="Load Data", width=12, command =lambda: self.load_data()).grid(row=0,column = 1 ,padx=(5,5))

        # ttk.Frame(self.frmLeftPanel, height=10).grid(row=3, column=0,columnspan=2, sticky=tk.E+tk.W)
        # ttk.Frame(self.frmLeftPanel, style="Separator.TFrame", height=1).grid(row=4, column=0,columnspan=2, sticky=tk.E+tk.W)
        # ttk.Frame(self.frmLeftPanel, height=10).grid(row=5, column=0,columnspan=2, sticky=tk.E+tk.W)
              
        
        



        # self.varApplicantType.set("")
        # self.varTemplateType.set("")
        
        # yaxis=0
        # tk.Label(self,text = "Id",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10), anchor=tk.NW)
        # tk.Entry(self,bg=self.config.COLOR_BACKGROUND,name="txt__Id",textvariable = self.varId ,width = 25,font=self.config.displayFont).place(x = 170,y = (10), anchor=tk.NW)	
        # yaxis=40
        # tk.Label(self,text = "Template",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
        # combostyle = ttk.Style()
        # combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'fieldbackground': self.config.COLOR_BACKGROUND,'background': self.config.COLOR_BACKGROUND}}})
        
        # combostyle.theme_use('combostyle') 
        # cmbTemplateType = ttk.Combobox(self, width = 23, textvariable =self.varTemplateType,font=self.config.displayFont)
        # # Adding combobox drop down list
        # cmbTemplateType['values'] = self.varAllTemlateName
        # cmbTemplateType.place(x = 170,y = (10+yaxis), anchor=tk.NW)	

        # yaxis=yaxis+40
        # tk.Label(self,text = "Data",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
        # tk.Text(self,name="txtApplicantData",bg=self.config.COLOR_BACKGROUND, width = 25, height=5,font=self.config.displayFont).place(x = 170,y = (10+yaxis), anchor=tk.NW)
        
        # btnLoadData = tk.Button ( self, text ="Get Data",width=10, relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND,  command =self.load_data )
        # btnOpenTemplate = tk.Button ( self, text ="Open Template", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command = self.Open_Template)
        # btnFillData = tk.Button ( self, text ="Fill", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command = self.fill_data)
        
        # btnLoadData.bind('<Enter>', self.config.on_enter_button)
        # btnLoadData.bind('<Leave>', self.config.on_leave_button)
        # btnFillData.bind('<Enter>', self.config.on_enter_button)
        # btnFillData.bind('<Leave>', self.config.on_leave_button)
        # btnOpenTemplate.bind('<Enter>', self.config.on_enter_button)
        # btnOpenTemplate.bind('<Leave>', self.config.on_leave_button)
        
        # btnLoadData.place(x = 400,y = 10, anchor=tk.NW)
        # btnOpenTemplate.place(x = 400,y = 50, anchor=tk.NW)
        # btnFillData.place(x = 400,y = 90, anchor=tk.NW)
        


if __name__ == '__main__':
    config= Gc.GenerateConfig()         
    root = tk.Tk()
    sizex = 600
    sizey = 400
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    config.set_theme(None,root)
    myframe=ttk.Frame(root,relief=tk.GROOVE,width=500,height=600)
    myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
    Setting(myframe,config)
    #root.eval('tk::PlaceWindow . center')
    root.mainloop()

        

