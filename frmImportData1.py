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
 
 
class MainWindow:
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
        
        self.Parent_Height=Container["height"]-20
        self.Parent_Width=Container["width"]-20

        self.ContainerCanvas=tk.Canvas(Container, bg=Container["bg"])
        self.ContainerFrame=tk.Frame(self.ContainerCanvas, bg=Container["bg"])

        scrollbar_y=tk.Scrollbar(Container,orient= tk.VERTICAL,command=self.ContainerCanvas.yview)
        scrollbar_x=tk.Scrollbar(Container,orient=tk.HORIZONTAL ,command=self.ContainerCanvas.xview)        
        scrollbar_y.pack(side=tk.RIGHT ,fill="y")
        scrollbar_x.pack(side=tk.BOTTOM,fill="x")
        self.ContainerCanvas.configure(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set)
        self.ContainerCanvas.pack(expand=tk.TRUE, fill="both")
        self.ContainerCanvas.create_window((0,0),window=self.ContainerFrame,anchor='nw')
        self.ContainerFrame.bind("<Configure>",self.myfunction)

        self.fncCreateItems()



    def __init__1(self,Container,config):
        self.canvas=tk.Canvas(Container, bg="red")
        self.frame=tk.Frame(self.canvas, bg="yellow")
        myscrollbar=tk.Scrollbar(Container,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left", fill="both")
        self.canvas.create_window((0,0),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>",self.myfunction)
        

        self.config=config
        self.varTemplateType = tk.StringVar()
        self.varApplicantType = tk.StringVar()
        self.varId=tk.StringVar()
        #self.data()
        #self.pack(expand=True, fill=tk.BOTH)                
        self.fncCreateItems()
         
    
    def myfunction(self,event):
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
    def data(self):
        for i in range(50):
            tk.Label(self.frame,text=i).grid(row=i,column=0)
            tk.Label(self.frame,text="my text"+str(i)).grid(row=i,column=1)
            tk.Label(self.frame,text="..........").grid(row=i,column=2)

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
        tk.Label(self.ContainerFrame,text = "Id",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).grid(row=0,column = 0, sticky=tk.N+tk.S+tk.E)
        tk.Entry(self.ContainerFrame,bg=self.config.COLOR_BACKGROUND,name="txt__Id",textvariable = self.varId ,width = 25,font=self.config.displayFont).grid(row=0,column = 1, sticky=tk.N+tk.S+tk.W)
        tk.Label(self.ContainerFrame,text = "Template Type",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).grid(row=1,column = 0, sticky=tk.N+tk.S+tk.E)
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'fieldbackground': self.config.COLOR_BACKGROUND,'background': self.config.COLOR_BACKGROUND}}})
        
        combostyle.theme_use('combostyle') 
        cmbTemplateType = ttk.Combobox(self.ContainerFrame, width = 23, textvariable =self.varTemplateType,font=self.config.displayFont)
        # Adding combobox drop down list
        cmbTemplateType['values'] = ('IO Template', 'Fact Find')
        cmbTemplateType.grid(row=1,column = 1, sticky=tk.N+tk.S+tk.W)
        tk.Label(self.ContainerFrame,text = "Applicant Type",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).grid(row=2,column = 0, sticky=tk.N+tk.S+tk.E)
        cmbApplicantType = ttk.Combobox(self.ContainerFrame, width = 23, textvariable = self.varApplicantType,font=self.config.displayFont)
        cmbApplicantType['values'] = ('Single', 'Co Applicant')
        cmbApplicantType.grid(row=2,column = 1, sticky=tk.N+tk.S+tk.W)	
        cmbApplicantType.bind("<<ComboboxSelected>>", lambda:self.hide_unhide_applicant(self.ContainerFrame))
        
        yaxis=3
        self.varStarttingPoint=yaxis
        for x in self.config.IO_Name:
            tk.Label(self.ContainerFrame,  text = x.strip(),font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).grid(row=yaxis,column =0, sticky=tk.N+tk.S+tk.E)
            tk.Entry(self.ContainerFrame,name="txtApplicant"+ x.strip().replace(' ', '_'),bg=self.config.COLOR_BACKGROUND, width = 25,font=self.config.displayFont).grid(row=yaxis,column = 1, sticky=tk.N+tk.S+tk.W)
            tk.Entry(self.ContainerFrame,name="txtCoApplicant"+ x.strip().replace(' ', '_'),bg=self.config.COLOR_BACKGROUND, width = 25,font=self.config.displayFont).grid(row=yaxis,column = 2, sticky=tk.N+tk.S+tk.W)	
            yaxis=yaxis+1
        
        btnImport = tk.Button (self.ContainerFrame, text ="Import",width=10, relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND,  command =lambda:self.open_file() )
        btnSave = tk.Button ( self.ContainerFrame, text ="Save", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command =lambda: self.save_data())
        btnReset = tk.Button ( self.ContainerFrame, text ="Reset", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command =lambda: self.reset_data())
        btnImport.bind('<Enter>', self.config.on_enter_button)
        btnImport.bind('<Leave>', self.config.on_leave_button)
        btnSave.bind('<Enter>', self.config.on_enter_button)
        btnSave.bind('<Leave>', self.config.on_leave_button)
        btnReset.bind('<Enter>', self.config.on_enter_button)
        btnReset.bind('<Leave>', self.config.on_leave_button)
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
    MainWindow(myframe,config)
    root.mainloop()

    