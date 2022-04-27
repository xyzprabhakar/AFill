from cgitb import text
from dataclasses import field
from pickle import NONE
import tkinter as tk
from tkinter import ttk
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
                
            self.varTotalDataCount.set(len(str(self.varAllDataFile)) ) 
            self.varTotalTemplateCount.set(str(len(self.varAllTemplate)))
            self.varTotalPendingDataCount.set("0")
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
            self.varCurrentMonthDataCount.set(str(currentMonthCounter) )
        except Exception as ex:
            messagebox.showerror("Error", ex)


    def fncCreateItems(self):
        self.varActionType.set("Add Template")
        
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
        btnReffreshData = tk.Button ( frmbtn1,name="btnReffreshData", text =fa.icons['sync'], relief='groove', width=3,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command = lambda :self.LoadAllJsonData() )                
        btnReffreshData.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        

        self.treev = ttk.Treeview(frmBody, selectmode ='browse')
        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(frmBody,orient ="vertical",command = self.treev.yview)
        horscrlbar = ttk.Scrollbar(frmBody,orient ="horizontal",command = self.treev.xview)

        # Calling pack method w.r.to vertical
        # scrollbar
        verscrlbar.pack(side ='right', fill ='y')
        horscrlbar.pack(side ='bottom', fill ='x')
        self.treev.pack(fill=tk.BOTH,expand=True,pady=(10,10))
        # Configuring treeview
        self.treev.configure(xscrollcommand = verscrlbar.set, yscrollcommand=horscrlbar.set)

        # Defining number of columns
        self.treev["columns"] = ("FileName", "ApplicantType", "TemplateType","CreationDt","ModifyDt")
        # Defining heading
        self.treev['show'] = 'headings'
        # Assigning the width and anchor to the
        # respective columns
        self.treev.column("FileName", width = 50, anchor ='center')
        self.treev.column("ApplicantType", width = 50, anchor ='center')
        self.treev.column("TemplateType", width = 50, anchor ='center')
        self.treev.column("CreationDt", width = 70, anchor ='nw')
        self.treev.column("ModifyDt", width = 70, anchor ='nw')
        # Assigning the heading names to the
        # respective columns
        self.treev.heading("FileName", text ="File Name")
        self.treev.heading("ApplicantType", text ="Applicant Type")
        self.treev.heading("TemplateType", text ="Template Type")
        self.treev.heading("CreationDt", text ="Creation Dt")
        self.treev.heading("ModifyDt", text ="Modify Dt")        

    
    def fncRemove(self):
        rowselected=False
        selected_items = self.treev.selection()        
        for ind,selected_item in enumerate(selected_items) :          
            if(ind==0):
                answer = messagebox.askyesno(title="Confirmation", message="Are you sure want to delete??")
                if(not answer):
                    return
                else:
                    rowselected=True
            if os.path.exists(os.path.join(self.config.FilePath, self.treev.item(selected_item)["values"][0]+".json")):
                os.remove(os.path.join(self.config.FilePath, self.treev.item(selected_item)["values"][0]+".json"))
            self.treev.delete(selected_item)
        if(rowselected):
            AllData=[]        
            for item in self.treev.get_children():            
                aDict = {"FileName":self.treev.item(item)["values"][0] , "ApplicantType":self.treev.item(item)["values"][1],
                "TemplateType":self.treev.item(item)["values"][2],"CreationDt":self.treev.item(item)["values"][3],"ModifyDt":self.treev.item(item)["values"][4]}
                AllData.append(aDict)
            with open(os.path.join(self.config.FilePath, self.config.DataFileName), 'w', encoding='utf-8') as f1:
                    json.dump(AllData, f1, ensure_ascii=False, indent=4,separators=(',',': '))                
                    tk.messagebox.showinfo("showinfo", "Deleted Successfully")
            self.BindExistingTreeview()
        
       
            
    def fncOpenChildForm(self):            
        selected_items = self.treev.selection()        
        for index,selected_item in enumerate(selected_items) :          
            if(index==0):
                self.varCurrentFileName.set(self.treev.item(selected_item)["values"][0])
                self.varCurrentApplicantType.set(self.treev.item(selected_item)["values"][1])
                self.varCurrentTemplateType.set(self.treev.item(selected_item)["values"][2])
                if os.path.exists(os.path.join(self.config.FilePath, self.varCurrentFileName.get()+".json")):
                    with io.open(os.path.join(self.config.FilePath, self.varCurrentFileName.get()+".json")) as fp:
                        self.varCurrentData=fp.read()             
        
        containter = tk.Toplevel(self.ContainerFrame)        
        containter.title("Update Data")
        containter.geometry("600x400")
        chdFrm=ttk.Frame(containter)        
        chdFrm.pack(expand=tk.TRUE,fill=tk.BOTH)
        chdFrm.columnconfigure(0, weight=1)
        chdFrm.columnconfigure(1, weight=1)
        chdFrm.columnconfigure(2, weight=100)
        chdFrm.rowconfigure(0, weight=1)
        chdFrm.rowconfigure(1, weight=1)
        chdFrm.rowconfigure(2, weight=1)
        chdFrm.rowconfigure(3, weight=1)        
        chdFrm.rowconfigure(4, weight=100)
        ttk.Label(chdFrm,text = "File Name :").grid(row=0,column = 0,padx=(10, 10), pady=(20, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Entry(chdFrm, width = 26, textvariable = self.varCurrentFileName,state=tk.DISABLED).grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(chdFrm,text = "Applicant Type :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Entry(chdFrm, width = 26, textvariable = self.varActionType,state=tk.DISABLED).grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(chdFrm,text = "Template Type :" ).grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(chdFrm, width = 26, textvariable = self.varCurrentTemplateType,state=tk.DISABLED).grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(chdFrm,text = "Data :",).grid(row=3,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Button (chdFrm, text ="Save", width=10, command =lambda: self.fncAddAction(chdFrm)).grid(row=3,column = 1 , padx=(10,0),pady=(3,5),sticky=tk.N+tk.W)
        txtData=tk.Text(chdFrm, name="txtData")        
        txtData.grid(row=4,column = 0,columnspan=3 ,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W+tk.E)
        txtData.insert(tk.END, self.varCurrentData)
        chdFrm.grab_set()
    

    def fncAddAction(self,chdFrm):
        if(self.varCurrentFileName==None or self.varCurrentFileName.get()=="" ):
            messagebox.showerror("Required", "Required File Name")
            return
        FileData=None
        try:            
            FileData=json.loads((chdFrm.children["txtData"]).get("1.0",tk.END))
        except:
            messagebox.showerror("Required", "Invalid JSON")
            return

        with open(os.path.join(self.config.FilePath, self.varCurrentFileName.get()+".json"), 'w', encoding='utf-8') as f:
            json.dump(FileData, f, ensure_ascii=False, indent=4,separators=(',',': '))

            AllData=[] 
            for item in self.treev.get_children():            
                if(self.treev.item(item)["values"][0]==self.varCurrentFileName.get()):
                    aDict = {"FileName":self.treev.item(item)["values"][0] , "ApplicantType":self.treev.item(item)["values"][1],
                    "TemplateType":self.treev.item(item)["values"][2],"CreationDt":self.treev.item(item)["values"][3],"ModifyDt":datetime.now().strftime("%d-%b-%Y %H:%M:%S")}
                else:
                    aDict = {"FileName":self.treev.item(item)["values"][0] , "ApplicantType":self.treev.item(item)["values"][1],
                    "TemplateType":self.treev.item(item)["values"][2],"CreationDt":self.treev.item(item)["values"][3],"ModifyDt":self.treev.item(item)["values"][4]}
                AllData.append(aDict)
            print(AllData)
            with open(os.path.join(self.config.FilePath, self.config.DataFileName), 'w', encoding='utf-8') as f1:
                    json.dump(AllData, f1, ensure_ascii=False, indent=4,separators=(',',': '))                
                    tk.messagebox.showinfo("showinfo", "Save Successfully")

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
    DataReport(myframe,config)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
