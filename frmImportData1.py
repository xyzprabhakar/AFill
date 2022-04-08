from ast import Break
from cProfile import label
from multiprocessing.sharedctypes import Value
from tkinter import font
from typing import Text
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
    varApplicant1=None
    varApplicant2=None
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
    tables=None

    def __init__(self,Container,config):
        self.config=config        
        self.varTemplateType = tk.StringVar()
        self.varApplicantType = tk.StringVar()
        self.varApplicant1 = tk.StringVar()
        self.varApplicant2 = tk.StringVar()
        self.varId=tk.StringVar()        
        
        self.ContainerCanvas= tk.Canvas(Container,bg=self.config.COLOR_MENU_BACKGROUND, highlightthickness=0, relief='ridge')
        self.ContainerFrame=ttk.Frame(self.ContainerCanvas)

        scrollbar_y=tk.Scrollbar(Container,orient= tk.VERTICAL,command=self.ContainerCanvas.yview)
        scrollbar_x=tk.Scrollbar(Container,orient=tk.HORIZONTAL ,command=self.ContainerCanvas.xview)        
        scrollbar_y.pack(side=tk.RIGHT ,fill="y")
        scrollbar_x.pack(side=tk.BOTTOM,fill="x")
        self.ContainerCanvas.configure(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set)
        self.ContainerCanvas.pack(expand=tk.TRUE, fill="both")
        self.ContainerCanvas.create_window((0,0),window=self.ContainerFrame,anchor='n')
        self.ContainerFrame.bind("<Configure>",self.fnc_resizeScroll)
        self.fncCreateItems()



    
    def fnc_resizeScroll(self,event):        
        self.ContainerCanvas.configure(scrollregion=self.ContainerCanvas.bbox("all"),width=self.Parent_Width,height=self.Parent_Height)

    def fnc_Read_PersonalDetails(self,ParentContainer,Applicantid):  
        frmTopFrame = ttk.Frame(ParentContainer)        
        frmTopFrame.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)             
        if(self.varTemplateType.get()=="IO Template"):
            self.fnc_Read_PersonalDetails_IO_Template(frmTopFrame,Applicantid)
            #Add Current Address
            frmCurrentAddressFrame = ttk.LabelFrame(ParentContainer,text="Current Address",style="Details.TLabelframe")
            frmCurrentAddressFrame.grid(row=1, column=0, sticky=tk.N+tk.W+tk.E, pady=(10,10),padx=(10,10))             
            self.fnc_Read_CurrentAddress_IO_Template(frmCurrentAddressFrame ,Applicantid)
            #Add Previous Address
            frmPreviousAddressFrame = ttk.LabelFrame(ParentContainer,text="Previous Address",style="Details.TLabelframe")
            frmPreviousAddressFrame.grid(row=2, column=0, sticky=tk.N+tk.W+tk.E, pady=(10,10),padx=(10,10))
            self.fnc_Read_PreviousAddress_IO_Template(frmPreviousAddressFrame,Applicantid)
            
    def fnc_Read_PersonalDetails_IO_Template(self,ParentContainer,Applicantid):        
        IsEvenColumn=False
        gridrowindex=-1
        gridcolumnindex=0
        PersonalDetailTable=None        
        foundTable=False
        for tableindex,table in enumerate(self.tables):
            if(table.columns[0]=="ersonal Details"):
                PersonalDetailTable=table
                foundTable=True
                break
        if(foundTable):            
            for i, j in PersonalDetailTable.iterrows():
                if(i==0):
                    if(Applicantid==1):
                        self.varApplicant1.set(j[1]) 
                    elif(Applicantid==2):
                        self.varApplicant2.set(j[2]) 
                for ioindex,x in enumerate(self.config.IO_Name_PersonalDetail):
                    #try:
                        if(j[0]==self.config.IO_Template_PersonalDetail[ioindex]):
                            if(IsEvenColumn):
                                IsEvenColumn=False
                                gridcolumnindex=2
                            else:
                                IsEvenColumn=True
                                gridcolumnindex=0
                                gridrowindex=gridrowindex+1
                            ttk.Label(ParentContainer,text = x).grid(row=gridrowindex,column = gridcolumnindex, sticky=tk.N+tk.S+tk.E,padx=(10,10),pady=(5,2))
                            txtboxname="txt_PersonalDetails_"+str(Applicantid)+x.strip().replace(' ', '_')
                            entrybox=ttk.Entry(ParentContainer, name=txtboxname)
                            ResponseData=""
                            if(Applicantid==1):
                                ResponseData=j[1]
                            elif(Applicantid==2):
                                ResponseData=j[2]                            
                            if(str(ResponseData) =="nan"):
                                ResponseData=""
                            entrybox.insert(0, ResponseData)                            
                            entrybox.grid(row=gridrowindex,column =(gridcolumnindex + 1) , sticky=tk.N+tk.S+tk.W,padx=(10,10),pady=(5,2))
                            break
                    #except Exception as ex:
                        #print("Error", ex)

    def fnc_Read_CurrentAddress_IO_Template(self,ParentContainer,Applicantid):        
        IsEvenColumn=False
        gridrowindex=-1
        gridcolumnindex=0
        DetailTable=None        
        foundTable=False
        foundApplicant=False
        foundItem=False
        columnLength=0
        columnIndex=1
        rowIndex=0
        for table in self.tables:
            if(table.columns[0]=="ontact Address"):
                DetailTable=table
                foundTable=True
                break
        if(foundTable):
            columnLength=len(DetailTable.columns)            
            for i, row in DetailTable.iterrows():
                if(row[0]=="Addressee"):
                    foundApplicant=False
                    rowIndex=i
                    while (columnIndex<columnLength):                        
                        if((Applicantid==1 and self.varApplicant1.get()==row[columnIndex]) or (Applicantid==2 and self.varApplicant2.get()==row[columnIndex])):
                            foundApplicant=True
                            break
                        columnIndex+=1    
                if(foundApplicant):
                    if(rowIndex<i and row[0]=="Addressee"):
                        pass
                    elif(row[0]=="Address Status" and row[columnIndex]=="Current Address"):
                        foundItem=True
                        break
                else:
                    columnIndex=1
            if(foundItem):   
                for ioindex,x in enumerate(self.config.IO_Name_CurrentAddress):
                    for i, j in DetailTable.iterrows():                    
                        if(i<=rowIndex):
                            continue
                        else:
                        #try:
                            if(j[0]==self.config.IO_Template_CurrentAddress[ioindex]):
                                if(IsEvenColumn):
                                    IsEvenColumn=False
                                    gridcolumnindex=2
                                else:
                                    IsEvenColumn=True
                                    gridcolumnindex=0
                                    gridrowindex=gridrowindex+1
                                ttk.Label(ParentContainer,text = x).grid(row=gridrowindex,column = gridcolumnindex, sticky=tk.N+tk.S+tk.E,padx=(10,10),pady=(5,2))
                                txtboxname="txt_CurrentAddress_"+str(Applicantid)+x.strip().replace(' ', '_')
                                entrybox=ttk.Entry(ParentContainer, name=txtboxname)                            
                                ResponseData=j[columnIndex]
                                if(str(ResponseData) =="nan"):
                                    ResponseData=""
                                entrybox.insert(0,ResponseData)
                                entrybox.grid(row=gridrowindex,column =(gridcolumnindex + 1) , sticky=tk.N+tk.S+tk.W,padx=(10,10),pady=(5,2))
                                break
                        #except Exception as ex:
                            #print("Error", ex)

    def fnc_Read_Address_GetRowColumnIndex(self,DetailTable,PreviousRowIndex,PreviousColumnIndex,Adressee, IsCurrentAddress ):        
        FoundApplicant=False
        IsFound=False
        columnLength=len(DetailTable.columns)
        RowIndex=PreviousRowIndex+1
        ColumnIndex=PreviousColumnIndex+1
        CurrentIndex={"row":RowIndex,"column":ColumnIndex,"IsFound":IsFound}        
        self.CurrentDepthCount+=1
        if(self.RecursionDepthCount<self.CurrentDepthCount):
            return CurrentIndex
        for i, row in DetailTable.iterrows():
            if(i<PreviousRowIndex):
                continue
            if(row[0]=="Addressee"):
                RowIndex=i
                if( row[ColumnIndex]==Adressee):
                    FoundApplicant=True
                else:
                    if(ColumnIndex+1<=columnLength-1):
                        return self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex,ColumnIndex+1,Adressee, IsCurrentAddress )
                    else:
                        return self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex+1,0,Adressee, IsCurrentAddress )
            if(FoundApplicant):
                if(row[0]=="Address Status" and ((IsCurrentAddress and  row[ColumnIndex]=="Current Address") or ( row[ColumnIndex]=="Previous Address") )):
                    IsFound=True
                    break
                if(row[0]=="Addressee"):
                    break        
        if(IsFound):
            CurrentIndex["row"]=RowIndex 
            CurrentIndex["column"]=ColumnIndex
            CurrentIndex["IsFound"]=True
        if(self.RecursionDepthCount>self.CurrentDepthCount):            
            return self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex+1,PreviousColumnIndex,Adressee, IsCurrentAddress )
        return CurrentIndex
            
        

    def fnc_Read_PreviousAddress_IO_Template(self,ParentContainer,Applicantid):        
        IsEvenColumn=False
        gridrowindex,gridcolumnindex=-1,0        
        columnIndex,rowIndex =0,0
        DetailTable=None        
        foundTable,foundItem=False ,False          
        self.RecursionDepthCount,self.CurrentDepthCount=15,0              
        for table in self.tables:
            if(table.columns[0]=="ontact Address"):
                DetailTable=table
                foundTable=True
                break
        if(foundTable):            
            #columnLength=len(DetailTable.columns)            
            PreviousAddressCounter=0
            PreviousColumnIndex=0
            PreviousRowIndex=0
            Addressee= self.varApplicant1.get() if (Applicantid==1)  else self.varApplicant2.get() if (Applicantid==2) else ""
            if PreviousAddressCounter < 4:
                columnIndex=PreviousColumnIndex+1
                foundItem=False
                tempData=self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex,PreviousColumnIndex,Addressee,False )
                foundItem=tempData["IsFound"]
                

                
                # for i, row in DetailTable.iterrows():
                #     if(row[0]=="Addressee"):
                #         foundApplicant=False
                #         rowIndex=i
                #         while (columnIndex<columnLength):                        
                #             if((Applicantid==1 and self.varApplicant1.get()==row[columnIndex]) or (Applicantid==2 and self.varApplicant2.get()==row[columnIndex])):
                #                 foundApplicant=True
                #                 break
                #             columnIndex+=1    
                #     if(foundApplicant):
                #         if(rowIndex<i and row[0]=="Addressee"):
                #             pass
                #         elif(row[0]=="Address Status" and row[columnIndex]=="Previous Address"):
                #             foundItem=True
                #             PreviousColumnIndex=columnIndex
                #             break
                #     else:
                #         columnIndex=1
                #         PreviousColumnIndex=0

                if(foundItem):
                    PreviousColumnIndex=tempData["column"]
                    PreviousRowIndex=tempData["row"]
                    rowIndex=PreviousColumnIndex
                    columnIndex=PreviousColumnIndex
                    for ioindex,x in enumerate(self.config.IO_Name_CurrentAddress):                    
                        for i, j in DetailTable.iterrows():
                            if(i<=rowIndex):
                                continue
                            else:
                            #try:
                                if(j[0]==self.config.IO_Template_CurrentAddress[ioindex]):
                                    if(IsEvenColumn):
                                        IsEvenColumn=False
                                        gridcolumnindex=2
                                    else:
                                        IsEvenColumn=True
                                        gridcolumnindex=0
                                        gridrowindex=gridrowindex+1
                                    ttk.Label(ParentContainer,text = x).grid(row=gridrowindex,column = gridcolumnindex, sticky=tk.N+tk.S+tk.E,padx=(10,10),pady=(5,2))
                                    txtboxname="txt_PreviousAddress_"+ str(PreviousAddressCounter+1)+"_" +str(Applicantid)+x.strip().replace(' ', '_')
                                    entrybox=ttk.Entry(ParentContainer, name=txtboxname)                            
                                    ResponseData=j[columnIndex]
                                    if(str(ResponseData) =="nan"):
                                        ResponseData=""
                                    entrybox.insert(0,ResponseData)
                                    entrybox.grid(row=gridrowindex,column =(gridcolumnindex + 1) , sticky=tk.N+tk.S+tk.W,padx=(10,10),pady=(5,2))
                                    break
                            #except Exception as ex:
                                #print("Error", ex)
                #add Seprator
                gridrowindex=gridrowindex+1
                ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(row=gridrowindex, column=0,columnspan=4, sticky=tk.E+tk.W, pady=(5,5))
                PreviousAddressCounter+1
    

    def hide_unhide_applicant(self,event,ParentFrame):
        yaxis= self.varStarttingPoint
        if(self.varApplicantType.get()=="Single"):
            for x in self.config.IO_Name:
               ParentFrame.children["txtCoApplicant"+ x.strip().replace(' ', '_')].place_forget() 
        else:
            for x in self.config.IO_Name:
               ParentFrame.children["txtCoApplicant"+ x.strip().replace(' ', '_')].place(x = 400,y = (10+yaxis), anchor=tk.NW)
               yaxis=yaxis+40
    
    def clear_frame(self,frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def open_file(self):
        open_file = askopenfilename(initialdir="d:",title="Open Template" , filetypes =[('Pdf Files', '*.pdf')])
        if open_file: 
            self.tables = tabula.read_pdf(open_file,pages="all") 
            frm_Applicant1=None
            frm_Applicant2=None
            if "frm_Applicant1" in self.ContainerFrame.children.keys():
                frm_Applicant1=self.ContainerFrame.children["frm_Applicant1"]
                self.clear_frame(frm_Applicant1)
            else:
                frm_Applicant1=ttk.Frame(self.ContainerFrame)
            if "frm_Applicant2" in self.ContainerFrame.children.keys():
                frm_Applicant2=self.ContainerFrame.children["frm_Applicant2"]
                self.clear_frame(frm_Applicant2)
            else:
                frm_Applicant2=ttk.Frame(self.ContainerFrame)
            
            frm_Applicant1.columnconfigure(0, weight=1)
            frm_Applicant1.rowconfigure(0, weight=1)
            frm_Applicant1.rowconfigure(1, weight=1)
            frm_Applicant1.rowconfigure(2, weight=100)
            frm_Applicant1.grid_forget()
            frm_Applicant2.columnconfigure(0, weight=1)
            frm_Applicant2.rowconfigure(0, weight=1)
            frm_Applicant2.rowconfigure(1, weight=1)
            frm_Applicant2.rowconfigure(2, weight=100)
            frm_Applicant2.grid_forget()
            ttk.Label(frm_Applicant1,text="Applicant 1", textvariable=self.varApplicant1,style="H1.TLabel").grid(row=0, column=0, sticky=tk.N+tk.W, pady=(5,3),padx=(10,10))
            ttk.Frame(frm_Applicant1, style="Separator.TFrame", height=1).grid(row=1, column=0, sticky=tk.E+tk.W, pady=(5,5))
            frmInnerContentFrame1=ttk.Frame(frm_Applicant1)
            frmInnerContentFrame1.grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S, pady=(10,10),padx=(10,10))

            ttk.Label(frm_Applicant2,text="Applicant 2", textvariable=self.varApplicant2,style="H1.TLabel").grid(row=0, column=0, sticky=tk.N+tk.W, pady=(5,3), padx=(10,10))
            ttk.Frame(frm_Applicant2, style="Separator.TFrame", height=1).grid(row=1, column=0, sticky=tk.E+tk.W, pady=(5,5))
            frmInnerContentFrame2=ttk.Frame(frm_Applicant2)
            frmInnerContentFrame2.grid(row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S,pady=(10,10),padx=(10,10))

            frm_Applicant1.grid(row=4, column=0,columnspan=3 ,sticky=tk.E+tk.W+tk.N+tk.S)
            self.fnc_Read_PersonalDetails(frmInnerContentFrame1,1)
            
            if(self.varApplicantType.get()=="Co Applicant"):
                frm_Applicant2.grid(row=5, column=0,columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)
                self.fnc_Read_PersonalDetails(frmInnerContentFrame2,2)
                
                
           
    

    def fncCreateItems(self):
        self.ContainerFrame.columnconfigure(0, weight=1)
        self.ContainerFrame.columnconfigure(1, weight=1)        
        self.ContainerFrame.columnconfigure(2, weight=100)
        self.ContainerFrame.rowconfigure(0, weight=1)
        self.ContainerFrame.rowconfigure(1, weight=1)
        self.ContainerFrame.rowconfigure(2, weight=1)
        self.varApplicantType.set("Co Applicant")
        self.varTemplateType.set("IO Template")
        ttk.Label(self.ContainerFrame,text = "Id").grid(row=0,column = 0, sticky=tk.N+tk.S+tk.E,pady=(5, 2),padx=(10, 10))
        ttk.Entry(self.ContainerFrame,name="txt__Id",textvariable = self.varId ,width = 25).grid(row=0,column = 1, sticky=tk.N+tk.S+tk.W,pady=(5, 2),padx=(10, 10))
        ttk.Label(self.ContainerFrame,text = "Template Type").grid(row=1,column = 0, sticky=tk.N+tk.S+tk.E,pady=(5, 2),padx=(10, 10))        
        cmbTemplateType = ttk.Combobox(self.ContainerFrame, width = 23, textvariable =self.varTemplateType)
        # Adding combobox drop down list
        cmbTemplateType['values'] = ('IO Template', 'Fact Find')
        cmbTemplateType.grid(row=1,column = 1, sticky=tk.N+tk.S+tk.W,pady=(5, 2),padx=(10, 10))
        ttk.Label(self.ContainerFrame,text = "Applicant Type").grid(row=2,column = 0, sticky=tk.N+tk.S+tk.E,pady=(5, 2),padx=(10, 10))
        
        cmbApplicantType = ttk.Combobox(self.ContainerFrame, width = 23, textvariable = self.varApplicantType)
        cmbApplicantType['values'] = ('Single', 'Co Applicant')
        cmbApplicantType.grid(row=2,column = 1, sticky=tk.N+tk.S+tk.W,pady=(5, 2),padx=(10, 10))	
        cmbApplicantType.bind("<<ComboboxSelected>>", lambda:self.hide_unhide_applicant(self.ContainerFrame))
        
        btnFrame=ttk.Frame(self.ContainerFrame)
        btnFrame.grid(row=0,rowspan=3,column=2,sticky=tk.N+tk.S+tk.W)
        

        # yaxis=3
        # self.varStarttingPoint=yaxis
        # for x in self.config.IO_Name:
        #     ttk.Label(self.ContainerFrame,  text = x.strip()).grid(row=yaxis,column =0, sticky=tk.N+tk.S+tk.E)
        #     ttk.Entry(self.ContainerFrame,name="txtApplicant"+ x.strip().replace(' ', '_'), width = 25).grid(row=yaxis,column = 1, sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))
        #     ttk.Entry(self.ContainerFrame,name="txtCoApplicant"+ x.strip().replace(' ', '_'), width = 25).grid(row=yaxis,column = 2, sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))	
        #     yaxis=yaxis+1
        
        btnImport = ttk.Button (btnFrame, text ="Import",width=10,  command =lambda:self.open_file() )
        btnLoad = ttk.Button (btnFrame, text ="Load",width=10,  command =lambda:self.open_file() )
        btnSave = ttk.Button ( btnFrame, text ="Save", width=10,  command =lambda: self.save_data())
        btnReset = ttk.Button ( btnFrame, text ="Reset", width=10, command =lambda: self.reset_data())
        # btnImport.bind('<Enter>', self.config.on_enter_button)
        # btnImport.bind('<Leave>', self.config.on_leave_button)
        # btnSave.bind('<Enter>', self.config.on_enter_button)
        # btnSave.bind('<Leave>', self.config.on_leave_button)
        # btnReset.bind('<Enter>', self.config.on_enter_button)
        # btnReset.bind('<Leave>', self.config.on_leave_button)
        btnImport.grid(row=0,column = 0, sticky=tk.N+tk.S+tk.W, padx=(5,5), pady=(5,5))	
        btnLoad.grid(row=0,column = 1, sticky=tk.N+tk.S+tk.W, padx=(5,5), pady=(5,5))	
        btnSave.grid(row=1,column = 0, sticky=tk.N+tk.S+tk.W, padx=(5,5), pady=(5,5))	
        btnReset.grid(row=1,column = 1, sticky=tk.N+tk.S+tk.W, padx=(5,5), pady=(5,5))	
        
        
if __name__ == '__main__':
    config= Gc.GenerateConfig()        
    
    root = tk.Tk()
    sizex = 700
    sizey = 500
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    myframe=tk.Frame(root,relief=tk.GROOVE,width=500,height=600,bd=1)
    myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
    config.set_theme(None,myframe)
    ImportData(myframe,config)
    root.mainloop()

    