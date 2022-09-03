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
    varLocation,varTemplateFile,varDataFile,varWrapperFile=None,None,None,None
    def __init__(self,Container,config):  
        self.config=config   
        self.ContainerFrame=Container
        self.displayFont = ( "Verdana", 10)       
        self.varName,self.varContactNo,self.varEmail = tk.StringVar(), tk.StringVar(), tk.StringVar()        
        self.varLocation,self.varTemplateFile,self.varDataFile,self.varWrapperFile ,self.varDriverName= tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.LoadData()
        self.fncCreateItems()        

    def LoadData(self):
        
        self.varName.set(self.config.Name)
        self.varContactNo.set(self.config.ContactNo)
        self.varEmail.set(self.config.Email)
        self.varLocation.set(self.config.FilePath)
        self.varTemplateFile.set(self.config.TemplateFileName)
        self.varDataFile.set(self.config.DataFileName)
        self.varWrapperFile.set(self.config.WrapperFileName)
        self.varDriverName.set(self.config.DriverName)

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
        btnReffreshData = tk.Button ( frmbtn1,name="btnReffreshData", text =fa.icons['sync'],image=self.config.ico_sync,  command = lambda :self.LoadData() )
        btnReffreshData.grid(row=0,column = 0,sticky=tk.E ,padx=(10,0),pady=(3,5))
        
        frmUserDetails=ttk.LabelFrame(frmBody,text="User Details",style="Details.TLabelframe")
        frmUserDetails.columnconfigure(0, weight=100) 
        frmUserDetails.rowconfigure(0, weight=100) 
        frmUserDetails.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        frmUserDetailsInnerData=ttk.Frame(frmUserDetails)
        frmUserDetailsInnerData.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        
        ttk.Label(frmUserDetailsInnerData,text="Name").grid(row=0,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmUserDetailsInnerData,text="Contact No").grid(row=1,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmUserDetailsInnerData,text="Email").grid(row=2,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Entry(frmUserDetailsInnerData,textvariable=self.varName, width=50 ).grid(row=0,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmUserDetailsInnerData,textvariable=self.varContactNo, width=50).grid(row=1,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmUserDetailsInnerData,textvariable=self.varEmail, width=50).grid(row=2,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))


        frmFileDetails=ttk.LabelFrame(frmBody,text="File Setting",style="Details.TLabelframe",)
        frmFileDetails.columnconfigure(0, weight=100) 
        frmFileDetails.rowconfigure(0, weight=100) 
        frmFileDetails.grid(row=1,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        frmFileDetailsInnerData=ttk.Frame(frmFileDetails)
        frmFileDetailsInnerData.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        
        ttk.Label(frmFileDetailsInnerData,text="Location").grid(row=0,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmFileDetailsInnerData,text="Template File").grid(row=1,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmFileDetailsInnerData,text="Data File").grid(row=2,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmFileDetailsInnerData,text="Wrapper File").grid(row=3,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Label(frmFileDetailsInnerData,text="Web Driver").grid(row=4,column=0,sticky=tk.E+tk.N+tk.S, padx=(30,10),pady=(8,3))
        ttk.Entry(frmFileDetailsInnerData,textvariable=self.varLocation, width=50).grid(row=0,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmFileDetailsInnerData,textvariable=self.varTemplateFile, width=50).grid(row=1,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmFileDetailsInnerData,textvariable=self.varDataFile, width=50).grid(row=2,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmFileDetailsInnerData,textvariable=self.varWrapperFile, width=50).grid(row=3,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Combobox(frmFileDetailsInnerData,textvariable = self.varDriverName,values=["Chrome","FireFox","IE","Edge"],width=47).grid(row=4,column=1,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Button( frmFileDetailsInnerData, text ="Save", width=10,command =lambda: self.fncSaveData()).grid(row=5,column=1, padx=(10,10),pady=(8,3))

    def fncSaveData(self):
        if(self.varName==None or self.varName.get()=="" ):
            messagebox.showerror("Required", "Required Name")
            return
        if(self.varEmail==None or self.varEmail.get()=="" ):
            messagebox.showerror("Required", "Required Email")
            return
        if(self.varContactNo==None or self.varContactNo.get()==""):
            messagebox.showerror("Required", "Required Contact")
            return

        
        if(self.varLocation==None or self.varLocation.get()=="" ):
            messagebox.showerror("Required", "Required Location")
            return
        if(self.varTemplateFile==None or self.varTemplateFile.get()=="" ):
            messagebox.showerror("Required", "Required TemplateFile")
            return
        if(self.varDataFile==None or self.varDataFile.get()==""):
            messagebox.showerror("Required", "Required Data")
            return
        if(self.varWrapperFile==None or self.varWrapperFile.get()=="" ):
            messagebox.showerror("Required", "Required Wrapper File")
            return
        if(self.varDriverName==None or self.varDriverName.get()==""):
            messagebox.showerror("Required", "Required DriverName")
            return
        self.config.fnc_RegisterUser(self.varName.get(),self.varEmail.get(),self.varContactNo.get())
        self.config.fnc_SaveSetting(self.varLocation.get(),self.varTemplateFile.get(),self.varDataFile.get(),self.varWrapperFile.get(),self.varDriverName.get())
        messagebox.showinfo("Success", "Save successfully")


if __name__ == '__main__':
    config= Gc.GenerateConfig()         
    root = tk.Tk()
    sizex = 600
    sizey = 400
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    config.set_theme(None,root)
    config.set_icons()
    myframe=ttk.Frame(root,relief=tk.GROOVE,width=500,height=600)
    myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
    Setting(myframe,config)
    #root.eval('tk::PlaceWindow . center')
    root.mainloop()

        

