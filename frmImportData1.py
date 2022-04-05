from multiprocessing.sharedctypes import Value
from tkinter import font
import PyPDF2 as pdf
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os

import tabula 
#from tabula import read_pdf
#from tabulate import tabulate

import io
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import RAISED, ttk
import GenerateConfig as Gc
import json

import tkinter as tk
 
 
class ImportData:
    config=None
    varTemplateType = None
    varApplicantType = None
    varStarttingPoint=0
    varAllJsonData=[]
    varId=None
    canvas=None
    frame=None
    ContainerCanvas=None
    ContainerFrame=None
    Parent_Height=500
    Parent_Width=600

    def __init__(self,Container,config):
        self.config=config        
        self.varTemplateType = tk.StringVar()
        self.varApplicantType = tk.StringVar()
        self.varId=tk.StringVar()        
        
        self.ContainerCanvas=tk.Canvas(Container,bg=self.config.COLOR_MENU_BACKGROUND)
        self.ContainerFrame=ttk.Frame(self.ContainerCanvas)

        scrollbar_y=tk.Scrollbar(Container,orient= tk.VERTICAL,command=self.ContainerCanvas.yview)
        scrollbar_x=tk.Scrollbar(Container,orient=tk.HORIZONTAL ,command=self.ContainerCanvas.xview)        
        scrollbar_y.pack(side=tk.RIGHT ,fill="y")
        scrollbar_x.pack(side=tk.BOTTOM,fill="x")
        self.ContainerCanvas.configure(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set)
        self.ContainerCanvas.pack(expand=tk.TRUE, fill="both")
        self.ContainerCanvas.create_window((0,0),window=self.ContainerFrame,anchor='nw')
        self.ContainerFrame.bind("<Configure>",self.fnc_resizeScroll)

        self.fncCreateItems()


    
    def fnc_resizeScroll(self,event):
        #print('Hello World')
        #self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=self.Parent_Width,height=self.Parent_Height)
        self.ContainerCanvas.configure(scrollregion=self.ContainerCanvas.bbox("all"),width=self.Parent_Width,height=self.Parent_Height)


    def hide_unhide_applicant(self,event,ParentFrame):
        yaxis= self.varStarttingPoint
        if(self.varApplicantType.get()=="Single"):
            for x in self.config.IO_Name:
               ParentFrame.children["txtCoApplicant"+ x.strip().replace(' ', '_')].place_forget() 
        else:
            for x in self.config.IO_Name:
               ParentFrame.children["txtCoApplicant"+ x.strip().replace(' ', '_')].place(x = 400,y = (10+yaxis), anchor=tk.NW)
               yaxis=yaxis+40
    
    def fncCreateItems(self):

        self.ContainerFrame.columnconfigure(0, weight=1)
        self.ContainerFrame.columnconfigure(1, weight=1)
        self.ContainerFrame.columnconfigure(2, weight=1)
        self.ContainerFrame.columnconfigure(3, weight=1)
        self.ContainerFrame.columnconfigure(4, weight=1)
        self.ContainerFrame.columnconfigure(5, weight=100)
        self.ContainerFrame.rowconfigure(0, weight=1)
        self.ContainerFrame.rowconfigure(1, weight=1)
        self.ContainerFrame.rowconfigure(2, weight=1)
        self.varApplicantType.set("Co Applicant")
        self.varTemplateType.set("IO Template")
        ttk.Label(self.ContainerFrame,text = "Id").grid(row=0,column = 0, sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.ContainerFrame,name="txt__Id",textvariable = self.varId ,width = 25).grid(row=0,column = 1, sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.ContainerFrame,text = "Template Type").grid(row=1,column = 0, sticky=tk.N+tk.S+tk.E)        
        cmbTemplateType = ttk.Combobox(self.ContainerFrame, width = 23, textvariable =self.varTemplateType)
        # Adding combobox drop down list
        cmbTemplateType['values'] = ('IO Template', 'Fact Find')
        cmbTemplateType.grid(row=1,column = 1, sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.ContainerFrame,text = "Applicant Type").grid(row=2,column = 0, sticky=tk.N+tk.S+tk.E)
        
        cmbApplicantType = ttk.Combobox(self.ContainerFrame, width = 23, textvariable = self.varApplicantType)
        cmbApplicantType['values'] = ('Single', 'Co Applicant')
        cmbApplicantType.grid(row=2,column = 1, sticky=tk.N+tk.S+tk.W)	
        cmbApplicantType.bind("<<ComboboxSelected>>", lambda:self.hide_unhide_applicant(self.ContainerFrame))
        
        yaxis=3
        self.varStarttingPoint=yaxis
        for x in self.config.IO_Name:
            ttk.Label(self.ContainerFrame,  text = x.strip()).grid(row=yaxis,column =0, sticky=tk.N+tk.S+tk.E)
            ttk.Entry(self.ContainerFrame,name="txtApplicant"+ x.strip().replace(' ', '_'), width = 25).grid(row=yaxis,column = 1, sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))
            ttk.Entry(self.ContainerFrame,name="txtCoApplicant"+ x.strip().replace(' ', '_'), width = 25).grid(row=yaxis,column = 2, sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))	
            yaxis=yaxis+1
        
        btnImport = ttk.Button (self.ContainerFrame, text ="Import",width=10,  command =lambda:self.open_file() )
        btnSave = ttk.Button ( self.ContainerFrame, text ="Save", width=10,  command =lambda: self.save_data())
        btnReset = ttk.Button ( self.ContainerFrame, text ="Reset", width=10, command =lambda: self.reset_data())
        # btnImport.bind('<Enter>', self.config.on_enter_button)
        # btnImport.bind('<Leave>', self.config.on_leave_button)
        # btnSave.bind('<Enter>', self.config.on_enter_button)
        # btnSave.bind('<Leave>', self.config.on_leave_button)
        # btnReset.bind('<Enter>', self.config.on_enter_button)
        # btnReset.bind('<Leave>', self.config.on_leave_button)
        btnImport.grid(row=0,column = 2, sticky=tk.N+tk.S+tk.W)	
        btnSave.grid(row=1,column = 2, sticky=tk.N+tk.S+tk.W)	
        btnReset.grid(row=2,column = 2, sticky=tk.N+tk.S+tk.W)	
        
        
        

if __name__ == '__main__':
    config= Gc.GenerateConfig()        
    root = tk.Tk()
    sizex = 600
    sizey = 400
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    myframe=tk.Frame(root,relief=tk.GROOVE,width=500,height=600,bd=1)
    myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
    ImportData(myframe,config)
    root.mainloop()

    