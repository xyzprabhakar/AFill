from cgitb import text
from dataclasses import field
from pickle import NONE
import tkinter as tk
from tkinter import NW, ttk
from tkinter import messagebox
import GenerateConfig as Gc
import json,io,os
import fontawesome as fa
from ttkthemes import ThemedStyle
from datetime import datetime


class Dashboard:
    config=None    
    ContainerFrame=None    
    displayFont = ( "Verdana", 10)
    combostyle=None
    treeViewStyle=None
    varAllDataFile,varAllTemplate=[],[]    
    varTotalDataCount,varTotalTemplateCount,varCurrentMonthDataCount,varTotalPendingDataCount=None,None,None,None
    varLastModifyFileName,varLastModifyApplicantType,varLastModifyTemplateType,varLastModifyModifyDt=None,None,None,None

    def __init__(self,Container,config):
        self.config=config        
        self.varTotalDataCount,self.varTotalTemplateCount,self.varCurrentMonthDataCount,self.varTotalPendingDataCount= tk.StringVar() ,tk.StringVar() ,tk.StringVar() ,tk.StringVar() 
        self.varLastModifyFileName,self.varLastModifyApplicantType,self.varLastModifyTemplateType,self.varLastModifyModifyDt= tk.StringVar() ,tk.StringVar() ,tk.StringVar() ,tk.StringVar() 
        #self.varCurrentData=tk.StringVar()                
        self.ContainerFrame=Container        
        self.LoadAllJsonData()
        self.fncCreateItems()
    
    
    def LoadAllJsonData(self):
        try:
            if not os.path.exists(self.config.FilePath):
                os.makedirs(self.config.FilePath)        
            if os.path.isfile(os.path.join(self.config.FilePath, self.config.DataFileName)) is False:
                with io.open(os.path.join(self.config.FilePath, self.config.DataFileName), 'w') as fp:
                    print('Empty File Created')
            else:
                with io.open(os.path.join(self.config.FilePath, self.config.DataFileName)) as fp:
                    self.varAllDataFile = json.load(fp)
            if os.path.isfile(os.path.join(self.config.FilePath, self.config.TemplateFileName)) is False:
                with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName), 'w') as fp:
                    print('Empty File Created')
            else:
                with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName)) as fp1:
                    self.varAllTemplate = json.load(fp1)
                
            self.varTotalDataCount.set("Total Data ="+str(len(self.varAllDataFile)) ) 
            self.varTotalTemplateCount.set("Total Template ="+str(len(self.varAllTemplate)))
            self.varTotalPendingDataCount.set("Coming Soon")
            LastMonthdate=datetime.strptime( datetime.now().strftime("01-%b-%Y"),"%d-%b-%Y")
            MaxModifyDate=datetime.strptime( "01-Jan-2000","%d-%b-%Y")
            currentMonthCounter=0
            for allData in  self.varAllDataFile:
                currentDate=datetime.strptime( allData["ModifyDt"],"%d-%b-%Y %H:%M:%S")
                if(currentDate>=MaxModifyDate):                    
                    MaxModifyDate=currentDate
                    self.varLastModifyFileName.set(allData["FileName"])
                    self.varLastModifyApplicantType.set(allData["ApplicantType"])
                    self.varLastModifyTemplateType.set(allData["TemplateType"])
                    self.varLastModifyModifyDt.set(allData["ModifyDt"])
                if(currentDate>LastMonthdate):
                    currentMonthCounter=currentMonthCounter+1
            self.varCurrentMonthDataCount.set("Current Month Data = "+str(currentMonthCounter) )
        except Exception as ex:
            messagebox.showerror("Error", ex)

    def checkKey(self,dict, key):      
        if key in dict.keys():
            return True
        else:
            return False
            
    def fncCreateItems(self):              
        self.frmHeader = ttk.Frame(self.ContainerFrame)        
        frmBody = ttk.Frame(self.ContainerFrame)
        self.ContainerFrame.grid_columnconfigure(0, weight=100)
        self.ContainerFrame.grid_rowconfigure(0, weight=1)
        self.ContainerFrame.grid_rowconfigure(1, weight=100)

        self.frmHeader.grid(row=0,column = 0, sticky=tk.N+tk.S+tk.W+tk.E)
        frmBody.grid(row=1,column = 0,  sticky=tk.N+tk.S+tk.W+tk.E)

        self.frmHeader.columnconfigure(0, weight=100)                
        self.frmHeader.rowconfigure(0, weight=1)
        self.frmHeader.rowconfigure(1, weight=100)        
        
        frmbtn1 = ttk.Frame(self.frmHeader,name="frmTreeviewhandler1")        
        frmbtn1.grid(row=3,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnReffreshData = tk.Button ( frmbtn1,name="btnReffreshData", image=self.config.ico_sync, relief='groove', width=3,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command = lambda :self.LoadAllJsonData() )                
        btnReffreshData.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        
        frmBody.columnconfigure(0, weight=1)
        frmBody.columnconfigure(1, weight=1)        
        frmBody.rowconfigure(0, weight=1)
        frmBody.rowconfigure(1, weight=1)
        frmBody.rowconfigure(2, weight=1)
        frmBody.rowconfigure(3, weight=1)        
        
        frmPanel1=ttk.Frame(frmBody,height=50,style="Dashboard1.TFrame")
        frmPanel2=ttk.Frame(frmBody,height=50,style="Dashboard2.TFrame")
        frmPanel3=ttk.Frame(frmBody,height=50,style="Dashboard3.TFrame")
        frmPanel4=ttk.Frame(frmBody,height=50,style="Dashboard4.TFrame")
        frmPanel5=ttk.LabelFrame(frmBody,text="Last Data",style="Details.TLabelframe")
        frmPanel6=ttk.Frame(frmPanel5,style="TFrame")
        
        frmPanel1.grid(row=0,column = 0, padx=(25,25),pady=(15,10),sticky=tk.N+tk.W+tk.E+tk.S)
        frmPanel2.grid(row=0,column = 1, padx=(25,25),pady=(15,10),sticky=tk.N+tk.W+tk.E+tk.S)
        frmPanel3.grid(row=1,column = 0, padx=(25,25),pady=(15,10),sticky=tk.N+tk.W+tk.E+tk.S)
        frmPanel4.grid(row=1,column = 1, padx=(25,25),pady=(15,10),sticky=tk.N+tk.W+tk.E+tk.S)
        frmPanel5.grid(row=2,column = 0,columnspan=2, padx=(25,25),pady=(15,10),sticky=tk.N+tk.W+tk.E+tk.S)
        frmPanel6.pack(fill=tk.BOTH,expand=tk.TRUE,anchor=NW)
        ttk.Label(frmPanel1,style="Dashboard1.TLabel",textvariable=self.varTotalDataCount).place(relx=.5, rely=.5,anchor= tk.CENTER)#.grid(row=0,column = 0, padx=(25,25),pady=(25,25),sticky=tk.N+tk.W+tk.E+tk.S)
        ttk.Label(frmPanel2,style="Dashboard2.TLabel",textvariable=self.varTotalTemplateCount).place(relx=.5, rely=.5,anchor= tk.CENTER)#.grid(row=0,column = 0, padx=(25,25),pady=(25,25),sticky=tk.N+tk.W+tk.E+tk.S)
        ttk.Label(frmPanel3,style="Dashboard3.TLabel",textvariable=self.varCurrentMonthDataCount).place(relx=.5, rely=.5,anchor= tk.CENTER)#.grid(row=0,column = 0, padx=(25,25),pady=(25,25),sticky=tk.N+tk.W+tk.E+tk.S)
        ttk.Label(frmPanel4,style="Dashboard4.TLabel",textvariable=self.varTotalPendingDataCount).place(relx=.5, rely=.5,anchor= tk.CENTER)#.grid(row=0,column = 0, padx=(25,25),pady=(25,25),sticky=tk.N+tk.W+tk.E+tk.S)

        ttk.Label(frmPanel6,text="File Name : ").grid(row=0,column = 0, padx=(5,5),pady=(5,5),sticky=tk.N+tk.W+tk.S)
        ttk.Label(frmPanel6,textvariable=self.varLastModifyFileName).grid(row=0,column = 1, padx=(5,5),pady=(5,5),sticky=tk.N+tk.W+tk.S)
        ttk.Label(frmPanel6,text="Applicant Type : ").grid(row=0,column = 3, padx=(25,5),pady=(5,5),sticky=tk.N+tk.W+tk.S)
        ttk.Label(frmPanel6,textvariable=self.varLastModifyApplicantType).grid(row=0,column = 4, padx=(25,5),pady=(5,5),sticky=tk.N+tk.W+tk.S)

        ttk.Label(frmPanel6,text="Template Type : ").grid(row=1,column = 0, padx=(5,5),pady=(5,5),sticky=tk.N+tk.W+tk.S)
        ttk.Label(frmPanel6,textvariable=self.varLastModifyTemplateType).grid(row=1,column = 1, padx=(5,5),pady=(5,5),sticky=tk.N+tk.W+tk.S)
        ttk.Label(frmPanel6,text="Modify Dt : ").grid(row=1,column = 3, padx=(25,5),pady=(5,5),sticky=tk.N+tk.W+tk.S)
        ttk.Label(frmPanel6,textvariable=self.varLastModifyModifyDt).grid(row=1,column = 4, padx=(25,5),pady=(5,5),sticky=tk.N+tk.W+tk.S)

        
    
if __name__ == '__main__':
    config= Gc.GenerateConfig()        
    
    root = tk.Tk()
    sizex = 600
    sizey = 400
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    config.set_theme(None,root)
    myframe=tk.Frame(root,relief=tk.GROOVE,width=500,height=600,bd=1)
    myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
    Dashboard(myframe,config)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
