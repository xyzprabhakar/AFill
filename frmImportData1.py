#import PyPDF2 as pdf
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage

import ctypes
import os
import tabula 
#from tabula import read_pdf
#from tabulate import tabulate
import pandas as pd
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

        self.scrollbar_y=tk.Scrollbar(Container,orient= tk.VERTICAL,command=self.ContainerCanvas.yview)
        scrollbar_x=tk.Scrollbar(Container,orient=tk.HORIZONTAL ,command=self.ContainerCanvas.xview)        
        self.scrollbar_y.pack(side=tk.RIGHT ,fill="y")
        scrollbar_x.pack(side=tk.BOTTOM,fill="x")
        self.ContainerCanvas.configure(yscrollcommand=self.scrollbar_y.set,xscrollcommand=scrollbar_x.set)
        self.ContainerCanvas.pack(expand=tk.TRUE, fill="both")
        self.ContainerCanvas.create_window((0,0),window=self.ContainerFrame,anchor='n')
        self.ContainerFrame.bind("<Configure>",self.fnc_resizeScroll)
        self.ContainerCanvas.bind_all("<MouseWheel>", self.OnMouseWheel)
        self.fncCreateItems()


    def OnMouseWheel(self,event):
        self.ContainerCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
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
            #Contact Details
            frmContactDetailFrame = ttk.LabelFrame(ParentContainer,text="Contact Details",style="Details.TLabelframe")
            frmContactDetailFrame.grid(row=3, column=0, sticky=tk.N+tk.W+tk.E, pady=(10,10),padx=(10,10))
            self.fnc_Read_ContactDetails_IO_Template(frmContactDetailFrame,Applicantid)
            #Bank Details
            frmBankDetailFrame = ttk.LabelFrame(ParentContainer,text="Bank Details",style="Details.TLabelframe")
            frmBankDetailFrame.grid(row=4, column=0, sticky=tk.N+tk.W+tk.E, pady=(10,10),padx=(10,10))
            self.fnc_Read_BankAccountDetails_IO_Template(frmBankDetailFrame,Applicantid)

            #Bank Details
            frmIDVerificationFrame = ttk.LabelFrame(ParentContainer,text="ID Verification",style="Details.TLabelframe")
            frmIDVerificationFrame.grid(row=6, column=0, sticky=tk.N+tk.W+tk.E, pady=(10,10),padx=(10,10))
            self.fnc_Read_IDVerification_IO_Template(frmIDVerificationFrame,Applicantid)

            

    def fnc_GenrateControl(self,ParentContainer,DetailTable,FindingColumnIndex,FromPosition,IO_Name,IO_Template_Name,Suffix):
        if(self.IsEvenColumn):
            self.IsEvenColumn=False
            self.gridcolumnindex=2
        else:
            self.IsEvenColumn=True
            self.gridcolumnindex=0
            self.gridrowindex=self.gridrowindex+1
        FindingValue=""
        if (not("[M]" in IO_Name)):            
            for i, j in DetailTable.iterrows():
                if(i<FromPosition):
                    continue
                try:
                    if(j[0]==IO_Template_Name):
                        FindingValue=j[FindingColumnIndex]
                        if(str(FindingValue) =="nan"):
                            FindingValue=""
                        break;

                except Exception as ex:
                    print("Error", ex)
        ttk.Label(ParentContainer,text = IO_Name.replace('[M]','')).grid(row=self.gridrowindex,column = self.gridcolumnindex, sticky=tk.N+tk.S+tk.E,padx=(10,10),pady=(5,2))
        txtboxname=Suffix+IO_Name.strip().replace(' ', '_').replace('[M]','')
        entrybox=ttk.Entry(ParentContainer, name=txtboxname)                            
        entrybox.insert(0,FindingValue)
        entrybox.grid(row=self.gridrowindex,column =(self.gridcolumnindex + 1) , sticky=tk.N+tk.S+tk.W,padx=(10,10),pady=(5,2))

    def fnc_GenrateControl_Vertical(self,ParentContainer,DetailTable,FindingColumnIndex,FindingRowIndex,IO_Name,IO_Template_Name,Suffix):
        if(self.IsEvenColumn):
            self.IsEvenColumn=False
            self.gridcolumnindex=2
        else:
            self.IsEvenColumn=True
            self.gridcolumnindex=0
            self.gridrowindex=self.gridrowindex+1
        FindingValue=""
        if (not("[M]" in IO_Name) and FindingRowIndex>0):            
            for i, j in DetailTable.iterrows():
                if(i<FindingRowIndex):
                    continue
                try:
                    FindingValue=j[FindingColumnIndex]                    
                    if(str(FindingValue) =="nan"):
                        FindingValue=""
                    break
                except Exception as ex:
                    print("Error", ex)
        ttk.Label(ParentContainer,text = IO_Name.replace('[M]','')).grid(row=self.gridrowindex,column = self.gridcolumnindex, sticky=tk.N+tk.S+tk.E,padx=(10,10),pady=(5,2))
        txtboxname=Suffix+IO_Name.strip().replace(' ', '_').replace('[M]','')
        entrybox=ttk.Entry(ParentContainer, name=txtboxname)                            
        entrybox.insert(0,FindingValue)
        entrybox.grid(row=self.gridrowindex,column =(self.gridcolumnindex + 1) , sticky=tk.N+tk.S+tk.W,padx=(10,10),pady=(5,2))
                                
                                
    def fun_mergetables(self,table,IsPrentTable):
        currentColumnLength=len(table.columns) 
        if(IsPrentTable):
            self.tableData=[]
            self.tableDataColumnLength=len(table.columns) 
            self.tableDataColumnName=[]
            for colindex in range(self.tableDataColumnLength):
                self.tableDataColumnName.append("columns"+str(colindex))
        else:
            subrow1=[] 
            for colindex in range(self.tableDataColumnLength):
                if(colindex>=currentColumnLength):
                   subrow1.append("") 
                else:
                   subrow1.append(table.columns[colindex]) 
            self.tableData.append(subrow1)        
              
        for i, j in table.iterrows():
            subrow2=[]
            for colindex in range(self.tableDataColumnLength):
                if(colindex>=currentColumnLength):
                   subrow2.append("") 
                else:
                    try:
                        subrow2.append(j[colindex])
                    except:
                        subrow2.append("")            
            self.tableData.append(subrow2)
            
    def fnc_Read_PersonalDetails_IO_Template(self,ParentContainer,Applicantid):        
        self.IsEvenColumn=False
        self.gridrowindex=-1
        self.gridcolumnindex=0
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
                break
            
            for ioindex,x in enumerate(self.config.IO_Name_PersonalDetail):
                self.fnc_GenrateControl(ParentContainer,PersonalDetailTable,Applicantid,0,x,self.config.IO_Template_PersonalDetail[ioindex],"txt_PersonalDetails_"+str(Applicantid))

    def fnc_Read_Address_GetRowColumnIndex(self,DetailTable,PreviousRowIndex,PreviousColumnIndex,Adressee, IsCurrentAddress ):        
        FoundApplicant=False
        IsFound=False
        columnLength=len(DetailTable.columns)
        if(PreviousColumnIndex>=columnLength-1):
            PreviousColumnIndex=0
            PreviousRowIndex=PreviousRowIndex+10

        RowIndex=PreviousRowIndex
        ColumnIndex=PreviousColumnIndex+1
        

        CurrentIndex={"row":RowIndex,"column":ColumnIndex,"IsFound":IsFound}        
        self.CurrentDepthCount+=1
        if(self.RecursionDepthCount<self.CurrentDepthCount):
            return CurrentIndex
        for i, row in DetailTable.iterrows():
            try:
                if(i<PreviousRowIndex):
                    continue
                if(row[0]=="Addressee" and (not FoundApplicant)):
                    RowIndex=i
                    if( row[ColumnIndex]==Adressee):
                        FoundApplicant=True
                    else:
                        if(ColumnIndex+1<=columnLength-1):
                            return self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex,ColumnIndex,Adressee, IsCurrentAddress )
                        else:
                            return self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex+10,0,Adressee, IsCurrentAddress )
                if(FoundApplicant):
                    if(row[0]=="Address Status" and ((IsCurrentAddress and  row[ColumnIndex]=="Current Address") or ( row[ColumnIndex]=="Previous Address") )):
                        IsFound=True
                        break
                    if(row[0]=="Addressee" and i>RowIndex):
                        break
            except Exception as ex:
                print("Error", ex)
        if(IsFound):
            CurrentIndex["row"]=RowIndex 
            CurrentIndex["column"]=ColumnIndex
            CurrentIndex["IsFound"]=True
        else:
            if(self.RecursionDepthCount>self.CurrentDepthCount):            
                if(ColumnIndex+1<=columnLength-1):
                    return self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex,ColumnIndex,Adressee, IsCurrentAddress )
                else :
                    return self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex+10,0,Adressee, IsCurrentAddress )
        return CurrentIndex
    
    def fnc_Read_Bank_GetRowColumnIndex(self,DetailTable,PreviousRowIndex,PreviousColumnIndex,Adressee,ApplicantId ):        
        FoundApplicant=False
        IsFound=False
        columnLength=len(DetailTable.columns)
        if(PreviousColumnIndex>=columnLength-1):
            PreviousColumnIndex=0
            PreviousRowIndex=PreviousRowIndex+10

        RowIndex=PreviousRowIndex
        ColumnIndex=PreviousColumnIndex+1
        

        CurrentIndex={"row":RowIndex,"column":ColumnIndex,"IsFound":IsFound}        
        self.CurrentDepthCount+=1
        if(self.RecursionDepthCount<self.CurrentDepthCount):
            return CurrentIndex
        for i, row in DetailTable.iterrows():
            try:
                if(i<PreviousRowIndex):
                    continue
                if(row[0]=="Owner"):
                    RowIndex=i
                    if( row[ColumnIndex]==Adressee or (ApplicantId==1 and row[ColumnIndex]=="Joint")):                        
                        IsFound=True
                        break
                    else:
                        if(ColumnIndex+1<=columnLength-1):
                            return self.fnc_Read_Bank_GetRowColumnIndex(DetailTable,PreviousRowIndex,ColumnIndex,Adressee,ApplicantId )
                        else:
                            return self.fnc_Read_Bank_GetRowColumnIndex(DetailTable,PreviousRowIndex+10,0,Adressee, ApplicantId )                
            except Exception as ex:
                print("Error", ex)
        if(IsFound):
            CurrentIndex["row"]=RowIndex 
            CurrentIndex["column"]=ColumnIndex
            CurrentIndex["IsFound"]=True
        else:
            if(self.RecursionDepthCount>self.CurrentDepthCount):            
                if(ColumnIndex+1<=columnLength-1):
                    return self.fnc_Read_Bank_GetRowColumnIndex(DetailTable,PreviousRowIndex,ColumnIndex,Adressee, ApplicantId )
                else :
                    return self.fnc_Read_Bank_GetRowColumnIndex(DetailTable,PreviousRowIndex+10,0,Adressee, ApplicantId )
        return CurrentIndex
    

    def fnc_Read_Vertical_GetRowColumnIndex(self,DetailTable,PreviousRowIndex,PreviousColumnIndex,Adressee, KeyData,KeyColumn ):        
        IsFound=False        
        RowIndex=PreviousRowIndex
        ColumnIndex=PreviousColumnIndex
        CurrentIndex={"row":RowIndex,"column":ColumnIndex,"IsFound":IsFound}        
        for i, row in DetailTable.iterrows():
            try:
                if(i<PreviousRowIndex):
                    continue
                if((row[ColumnIndex]==Adressee or row[ColumnIndex]=="Joint") and  row[KeyColumn]==KeyData):
                    RowIndex=i
                    IsFound=True
                    break
            except Exception as ex:
                print("Error", ex)
        if(IsFound):
            CurrentIndex["row"]=RowIndex 
            CurrentIndex["column"]=ColumnIndex
            CurrentIndex["IsFound"]=True        
        return CurrentIndex
    

    def fnc_Read_CurrentAddress_IO_Template(self,ParentContainer,Applicantid):                
        self.gridrowindex,self.gridcolumnindex=-1,0        
        columnIndex,rowIndex =0,0
        DetailTable=None        
        foundTable,foundItem=False ,False          
        self.RecursionDepthCount,self.CurrentDepthCount=15,0                 
        for tableindex ,table in enumerate(self.tables) :
            if(table.columns[0]=="ontact Address"):
                self.fun_mergetables(table,True)
                #check Next Table is on Next Page
                if (not (self.tables[tableindex+1].columns[0]=="ontact Details")):
                    self.fun_mergetables(self.tables[tableindex+1],False)
                    #check Next Table is on Next to Next Page
                    if (not (self.tables[tableindex+2].columns[0]=="ontact Details")):
                        self.fun_mergetables(self.tables[tableindex+2],False)                
                DetailTable=pd.DataFrame(self.tableData, columns = self.tableDataColumnName)
                foundTable=True
                self.CurrentAddressFound=True
                break
                    
                
        if(foundTable):                
            PreviousAddressCounter=0
            PreviousColumnIndex=0
            PreviousRowIndex=0
            Addressee= self.varApplicant1.get() if (Applicantid==1)  else self.varApplicant2.get() if (Applicantid==2) else ""
            while PreviousAddressCounter < 1:
                self.IsEvenColumn=False
                foundItem=False
                tempData=self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex,PreviousColumnIndex,Addressee,True )
                foundItem=tempData["IsFound"]                
                if(foundItem):
                    PreviousColumnIndex=tempData["column"]
                    PreviousRowIndex=tempData["row"]
                    rowIndex=PreviousRowIndex
                    columnIndex=PreviousColumnIndex

                    for ioindex,x in enumerate(self.config.IO_Name_CurrentAddress):
                        self.fnc_GenrateControl(ParentContainer,DetailTable,columnIndex,rowIndex,x,self.config.IO_Template_CurrentAddress[ioindex],"txt_CurrentAddress_"+str(Applicantid))

                    self.gridrowindex=self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(row=self.gridrowindex, column=0,columnspan=4, sticky=tk.E+tk.W, pady=(5,5))
                PreviousAddressCounter+=1
         
    def fnc_Read_PreviousAddress_IO_Template(self,ParentContainer,Applicantid):                
        self.gridrowindex,self.gridcolumnindex=-1,0        
        columnIndex,rowIndex =0,0
        DetailTable=None        
        foundTable,foundItem=False ,False          
        self.RecursionDepthCount,self.CurrentDepthCount=15,0              
        
        if(self.CurrentAddressFound):
            DetailTable=pd.DataFrame(self.tableData, columns = self.tableDataColumnName)
            foundTable=True
        else:            
            for tableindex ,table in enumerate(self.tables) :
                if(table.columns[0]=="ontact Address"):
                    self.fun_mergetables(table,True)
                    #check Next Table is on Next Page
                    if (not (self.tables[tableindex+1].columns[0]=="ontact Details")):
                        self.fun_mergetables(self.tables[tableindex+1],False)
                        #check Next Table is on Next to Next Page
                        if (not (self.tables[tableindex+2].columns[0]=="ontact Details")):
                            self.fun_mergetables(self.tables[tableindex+2],False)                
                    DetailTable=pd.DataFrame(self.tableData, columns = self.tableDataColumnName)
                    foundTable=True
                    self.CurrentAddressFound=True
                    break
        if(foundTable):                        
            PreviousAddressCounter=0
            PreviousColumnIndex=0
            PreviousRowIndex=0
            Addressee= self.varApplicant1.get() if (Applicantid==1)  else self.varApplicant2.get() if (Applicantid==2) else ""
            while PreviousAddressCounter < 4:
                self.IsEvenColumn=False
                foundItem=False
                tempData=self.fnc_Read_Address_GetRowColumnIndex(DetailTable,PreviousRowIndex,PreviousColumnIndex,Addressee,False )
                foundItem=tempData["IsFound"]                
                if(foundItem):
                    PreviousColumnIndex=tempData["column"]
                    PreviousRowIndex=tempData["row"]
                    rowIndex=PreviousRowIndex
                    columnIndex=PreviousColumnIndex
                    for ioindex,x in enumerate(self.config.IO_Name_PreviousAddress):  
                        self.fnc_GenrateControl(ParentContainer,DetailTable,columnIndex,rowIndex,x,self.config.IO_Template_PreviousAddress[ioindex],"txt_PreviousAddress_"+ str(PreviousAddressCounter+1)+"_" +str(Applicantid))
                    
                    self.gridrowindex=self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(row=self.gridrowindex, column=0,columnspan=4, sticky=tk.E+tk.W, pady=(5,5))
                PreviousAddressCounter+=1
    
    def fnc_Read_ContactDetails_IO_Template(self,ParentContainer,Applicantid):                
        self.gridrowindex,self.gridcolumnindex=-1,0                
        DetailTable=None        
        foundTable,foundItem=False ,False          
        self.RecursionDepthCount,self.CurrentDepthCount=15,0              
        for tableindex ,table in enumerate(self.tables) :
            if(table.columns[0]=="ontact Details"):
                self.fun_mergetables(table,True)
                #check Next Table is on Next Page
                if (not (self.tables[tableindex+1].columns[0]=="rofessional Contacts")):
                    self.fun_mergetables(self.tables[tableindex+1],False)
                    #check Next Table is on Next to Next Page
                    if (not (self.tables[tableindex+2].columns[0]=="rofessional Contacts")):
                        self.fun_mergetables(self.tables[tableindex+2],False)                
                DetailTable=pd.DataFrame(self.tableData, columns = self.tableDataColumnName)
                foundTable=True
                self.CurrentAddressFound=True
                break
        if(foundTable):                                    
            
            Addressee= self.varApplicant1.get() if (Applicantid==1)  else self.varApplicant2.get() if (Applicantid==2) else ""            
            for ioindex,x in enumerate(self.config.IO_Name_ContactDetails):  
                foundItem=False
                PreviousRowIndex=0
                if (not("[M]" in x)):            
                    tempData=self.fnc_Read_Vertical_GetRowColumnIndex(DetailTable,0,0,Addressee,self.config.IO_Template_ContactDetails[ioindex],1)
                    foundItem=tempData["IsFound"]
                    if(foundItem):                        
                        PreviousRowIndex=tempData["row"]
                self.fnc_GenrateControl_Vertical(ParentContainer,DetailTable,2,PreviousRowIndex,x,self.config.IO_Template_ContactDetails[ioindex],"txt_ContactDetails_"+str(Applicantid))

    def fnc_Read_BankAccountDetails_IO_Template(self,ParentContainer,Applicantid):                
        self.gridrowindex,self.gridcolumnindex=-1,0        
        columnIndex,rowIndex =0,0
        DetailTable=None        
        foundTable,foundItem=False ,False          
        self.RecursionDepthCount,self.CurrentDepthCount=15,0              
        for tableindex ,table in enumerate(self.tables) :
            if(table.columns[0]=="ank Account Details"):
                self.fun_mergetables(table,True)
                #check Next Table is on Next Page
                if (not (self.tables[tableindex+1].columns[0]=="amily And Dependants")):
                    self.fun_mergetables(self.tables[tableindex+1],False)
                    #check Next Table is on Next to Next Page
                    if (not (self.tables[tableindex+2].columns[0]=="amily And Dependants")):
                        self.fun_mergetables(self.tables[tableindex+2],False)                
                DetailTable=pd.DataFrame(self.tableData, columns = self.tableDataColumnName)
                foundTable=True
                self.CurrentAddressFound=True
                break
        if(foundTable):                        
            PreviousAddressCounter=0
            PreviousColumnIndex=0
            PreviousRowIndex=0
            Addressee= self.varApplicant1.get() if (Applicantid==1)  else self.varApplicant2.get() if (Applicantid==2) else ""
            while PreviousAddressCounter < 4:
                self.IsEvenColumn=False
                foundItem=False
                tempData=self.fnc_Read_Bank_GetRowColumnIndex(DetailTable,PreviousRowIndex,PreviousColumnIndex,Addressee,Applicantid )
                foundItem=tempData["IsFound"]                
                if(foundItem):
                    PreviousColumnIndex=tempData["column"]
                    PreviousRowIndex=tempData["row"]
                    rowIndex=PreviousRowIndex
                    columnIndex=PreviousColumnIndex
                    for ioindex,x in enumerate(self.config.IO_Name_BankAccountDetails):  
                        self.fnc_GenrateControl(ParentContainer,DetailTable,columnIndex,rowIndex,x,self.config.IO_Template_BankAccountDetails[ioindex],"txt_BankAccountDetails_"+ str(PreviousAddressCounter+1)+"_" +str(Applicantid))
                    
                    self.gridrowindex=self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(row=self.gridrowindex, column=0,columnspan=4, sticky=tk.E+tk.W, pady=(5,5))
                PreviousAddressCounter+=1
    

    def fnc_Read_IDVerification_IO_Template(self,ParentContainer,Applicantid):                
        self.gridrowindex,self.gridcolumnindex=-1,0        
        columnIndex,rowIndex =0,0
        DetailTable=None        
        foundTable,foundItem=False ,False          
        self.RecursionDepthCount,self.CurrentDepthCount=15,0              
        for tableindex ,table in enumerate(self.tables) :
            if(table.columns[0]=="D Verification"):
                self.fun_mergetables(table,True)
                #check Next Table is on Next Page
                if (not (self.tables[tableindex+1].columns[0]=="lectronic ID Verification")):
                    self.fun_mergetables(self.tables[tableindex+1],False)
                    #check Next Table is on Next to Next Page
                    if (not (self.tables[tableindex+2].columns[0]=="lectronic ID Verification")):
                        self.fun_mergetables(self.tables[tableindex+2],False)                
                DetailTable=pd.DataFrame(self.tableData, columns = self.tableDataColumnName)
                foundTable=True
                self.CurrentAddressFound=True
                break
        if(foundTable):                        
            PreviousAddressCounter=0
            PreviousColumnIndex=0
            PreviousRowIndex=0
            Addressee= self.varApplicant1.get() if (Applicantid==1)  else self.varApplicant2.get() if (Applicantid==2) else ""
            while PreviousAddressCounter < 1:
                self.IsEvenColumn=False
                foundItem=False
                tempData=self.fnc_Read_Bank_GetRowColumnIndex(DetailTable,PreviousRowIndex,PreviousColumnIndex,Addressee,Applicantid )
                foundItem=tempData["IsFound"]                
                if(foundItem):
                    PreviousColumnIndex=tempData["column"]
                    PreviousRowIndex=tempData["row"]
                    rowIndex=PreviousRowIndex
                    columnIndex=PreviousColumnIndex
                    for ioindex,x in enumerate(self.config.IO_Name_IDVerification):  
                        self.fnc_GenrateControl(ParentContainer,DetailTable,columnIndex,rowIndex,x,self.config.IO_Template_IDVerification[ioindex],"txt_IDVerification_"+ str(PreviousAddressCounter+1)+"_" +str(Applicantid))
                    
                    self.gridrowindex=self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(row=self.gridrowindex, column=0,columnspan=4, sticky=tk.E+tk.W, pady=(5,5))
                PreviousAddressCounter+=1
    

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
            self.CurrentAddressFound=False
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
    
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
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

    