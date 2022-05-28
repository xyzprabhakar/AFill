from dataclasses import field
from pickle import NONE
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from turtle import left
from numpy import imag

from setuptools import Command
import GenerateConfig as Gc
import json,io,os
import fontawesome as fa
from ttkthemes import ThemedStyle
import time


class IOWrapper:
    config=None    
    ContainerFrame=None    
    displayFont = ( "Verdana", 10)
    combostyle=None
    treeViewStyle=None
    varAllData,varAllTemlateName,varCurrentTemplate,varAllSectionCategory,varCurrentSectionCategory,varAllIOName,varCurrentIOName,varIOValue,varTemplateValue=[],[],None,[],None,[],None ,None,None    
    chdFrm1,chdFrm2=None,None    
    treev1=None;

    def __init__(self,Container,config):
        self.config=config        
        self.varCurrentTemplate,self.varCurrentSectionCategory,self.varCurrentIOName,self.varIOValue,self.varTemplateValue= tk.StringVar(),tk.StringVar() ,tk.StringVar(),tk.StringVar() ,tk.StringVar()         
        self.ContainerFrame=Container        
        self.LoadAllJsonData()        
        self.fncCreateItems()
    
    
    def LoadAllJsonData(self):
        try:
            if not os.path.exists(self.config.FilePath):
                os.makedirs(self.config.FilePath)        
            if os.path.isfile(os.path.join(self.config.FilePath, self.config.TemplateFileName)) is False:
                with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName), 'w') as fp:
                    print('Empty File Created')
            else:
                with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName)) as fp:                    
                    varAllTemlate = json.load(fp)
                    self.varAllTemlateName=[]
                    for x in varAllTemlate:
                        self.varAllTemlateName.append(x["templateName"])
            
            #all section 
            self.varAllSectionCategory=self.config.SectionCategory
            self.varAllIOName.append({"Category":"PersonalDetails","IOName":self.config.IO_Name_PersonalDetails})
            self.varAllIOName.append({"Category":"CurrentAddress","IOName":self.config.IO_Name_CurrentAddress})
            self.varAllIOName.append({"Category":"PreviousAddress","IOName":self.config.IO_Name_PreviousAddress})
            self.varAllIOName.append({"Category":"ContactDetails","IOName":self.config.IO_Name_ContactDetails})
            self.varAllIOName.append({"Category":"ProfessionalContacts","IOName":self.config.IO_Name_ProfessionalContacts})
            self.varAllIOName.append({"Category":"BankAccount","IOName":self.config.IO_Name_BankAccountDetails})
            self.varAllIOName.append({"Category":"FamilyAndDependants","IOName":self.config.IO_Name_FamilyAndDependants})
            self.varAllIOName.append({"Category":"IDVerification","IOName":self.config.IO_Name_IDVerification})
            self.varAllIOName.append({"Category":"CurrentEmploymentDetails","IOName":self.config.IO_Name_CurrentEmploymentDetails})
            self.varAllIOName.append({"Category":"Assets","IOName":self.config.IO_Name_Assets})
            self.varAllIOName.append({"Category":"Liabilities","IOName":self.config.IO_Name_Liabilities})
            self.varAllIOName.append({"Category":"ExistingMortgage","IOName":self.config.IO_Name_ExistingMortgage})
            self.varAllIOName.append({"Category":"MortgageRequirements","IOName":self.config.IO_Name_MortgageRequirements})
            self.varAllIOName.append({"Category":"Expenditure","IOName":self.config.IO_Name_Expenditure})

            if os.path.isfile(os.path.join(self.config.FilePath, self.config.WrapperFileName)) is False:
                with io.open(os.path.join(self.config.FilePath, self.config.WrapperFileName), 'w') as fp:
                    print('Empty File Created')
            else:
                with io.open(os.path.join(self.config.FilePath, self.config.WrapperFileName)) as fp:                    
                    tempData= json.load(fp)
                    if(self.checkKey(tempData,"allData")):
                        self.varAllData = tempData["allData"]
                    
        except Exception as ex:
            messagebox.showerror("Error", ex)

    
    
    def checkKey(self,dict, key):      
        if key in dict.keys():
            return True
        else:
            return False

    def BindExistingTreeview(self,event):                    
            self.clear_all_gridview()        
            for sections in self.varAllData:                
                varCurrentTemplate,varCurrentSectionCategory,varCurrentIOName,varIOValue,varWrapperValue='','','','',''                
                if(self.checkKey(sections,"template")):
                    varCurrentTemplate=sections["template"]
                if(self.checkKey(sections,"sectionCategory")):
                    varCurrentSectionCategory=sections["sectionCategory"]
                if(self.checkKey(sections,"ioName")):
                    varCurrentIOName=sections["ioName"]
                if(self.checkKey(sections,"ioValue")):
                    varIOValue=sections["ioValue"]
                if(self.checkKey(sections,"wrapperValue")):
                    varWrapperValue=sections["wrapperValue"]
                self.treev1.insert("", 'end',values =(varCurrentTemplate,varCurrentSectionCategory,varCurrentIOName,varIOValue,varWrapperValue))
                
        
    def clear_all_gridview(self):        
            for item in self.treev1.get_children():
                self.treev1.delete(item)            
            self.frmHeader.children["frmTreeviewhandler"].children["btnRemoveAction"]["state"]=tk.DISABLED
            self.frmHeader.children["frmTreeviewhandler"].children["btnMoveUpAction"]["state"]=tk.DISABLED
            self.frmHeader.children["frmTreeviewhandler"].children["btnMoveDownAction"]["state"]=tk.DISABLED
        


    def fncCreateItems(self):        
        self.frmHeader = ttk.Frame(self.ContainerFrame)        
        frmBody = ttk.Frame(self.ContainerFrame)
        self.ContainerFrame.grid_columnconfigure(0, weight=100)
        self.ContainerFrame.grid_rowconfigure(0, weight=1)
        self.ContainerFrame.grid_rowconfigure(1, weight=100)

        self.frmHeader.grid(row=0,column = 0, sticky=tk.N+tk.S+tk.W+tk.E)
        frmBody.grid(row=1,column = 0,  sticky=tk.N+tk.S+tk.W+tk.E)

        self.frmHeader.columnconfigure(0, weight=1)
        self.frmHeader.columnconfigure(1, weight=1)
        self.frmHeader.columnconfigure(2, weight=1)
        self.frmHeader.columnconfigure(3, weight=100)
        self.frmHeader.rowconfigure(0, weight=1)
        self.frmHeader.rowconfigure(1, weight=1)
        self.frmHeader.rowconfigure(2, weight=1)
        self.frmHeader.rowconfigure(3, weight=100)

        
        frmbtn = ttk.Frame(self.frmHeader)        
        frmbtn.grid(row=0,column = 2, rowspan=3, sticky=tk.N+tk.S+tk.W)
        btnSave = ttk.Button( frmbtn, text ="Save", width=10,command =lambda: self.fncSaveData())
        btnRefresh = ttk.Button ( frmbtn, text ="Refresh", width=10,command =lambda: self.fncReloadData())
        
        btnSave.grid(row=0,column = 0 , padx=(10,0),pady=(3,5))        
        btnRefresh.grid(row=0,column = 1, padx=(10,0),pady=(3,5))


        frmbtn1 = ttk.Frame(self.frmHeader,name="frmTreeviewhandler")        
        frmbtn1.grid(row=3,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnAddAction = ttk.Button ( frmbtn1,name="btnAddAction" , image=self.config.ico_add ,command =lambda: self.fncOpenInnerChildForm() )                
        btnRemoveAction = ttk.Button ( frmbtn1,name="btnRemoveAction",image=self.config.ico_delete ,  state=tk.DISABLED,command =lambda: self.fncRemove() )
        btnMoveUpAction = ttk.Button ( frmbtn1,name="btnMoveUpAction",image=self.config.ico_up ,  state=tk.DISABLED,command =lambda: self.fncMoveUp() )
        btnMoveDownAction = ttk.Button ( frmbtn1,name="btnMoveDownAction",image=self.config.ico_down , state=tk.DISABLED,command =lambda: self.fncMoveDown() )
        btnAddAction.grid(row=0,column = 0, padx=(10,0),pady=(3,5))        
        btnRemoveAction.grid(row=0,column =2, padx=(10,0),pady=(3,5))
        btnMoveUpAction.grid(row=0,column =3, padx=(10,0),pady=(3,5))
        btnMoveDownAction.grid(row=0,column =4, padx=(10,0),pady=(3,5))

        self.treev1 = ttk.Treeview(frmBody, selectmode ='browse')
        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(frmBody,orient ="vertical",command = self.treev1.yview)
        horscrlbar = ttk.Scrollbar(frmBody,orient ="horizontal",command = self.treev1.xview)

        # Calling pack method w.r.to vertical
        # scrollbar
        verscrlbar.pack(side ='right', fill ='y')
        horscrlbar.pack(side ='bottom', fill ='x')
        self.treev1.pack(fill=tk.BOTH,expand=True,pady=(10,10))
        # Configuring treeview
        self.treev1.configure(xscrollcommand = horscrlbar.set, yscrollcommand=verscrlbar.set)

        
        # Defining number of columns
        self.treev1["columns"] = ("Template","SectionCategory","IOName","IOValue","WrapperValue")
        # Defining heading
        self.treev1['show'] = 'headings'
        # Assigning the width and anchor to the
        # respective columns
        self.treev1.column("Template", width = 50, anchor ='nw')
        self.treev1.column("SectionCategory", width = 50, anchor ='nw')
        self.treev1.column("IOName", width = 50, anchor ='nw')
        self.treev1.column("IOValue", width = 50, anchor ='nw')
        self.treev1.column("WrapperValue", width = 50, anchor ='center')
        
        # Assigning the heading names to the
        # respective columns
        self.treev1.heading("Template", text ="Template")
        self.treev1.heading("SectionCategory", text ="Section Category")
        self.treev1.heading("IOName", text ="IO Name")
        self.treev1.heading("IOValue", text ="IO Value")
        self.treev1.heading("WrapperValue", text ="Wrapper Value")

        self.BindExistingTreeview(None)
        

    def fnc_Select_Record(self):
        selected=self.treev1.focus()        
        if(len(selected)>0):                
            self.frmHeader.children["frmTreeviewhandler"].children["btnRemoveAction"]["state"]=tk.NORMAL
            self.frmHeader.children["frmTreeviewhandler"].children["btnMoveUpAction"]["state"]=tk.NORMAL
            self.frmHeader.children["frmTreeviewhandler"].children["btnMoveDownAction"]["state"]=tk.NORMAL

    def fncMoveItems(self,e):
        self.fnc_Select_Record()

    def fncMoveUp(self):        
        rows=self.treev1.selection()
        for row in rows:
            self.treev1.move(row,self.treev1.parent(row),self.treev1.index(row)-1)
        
    def fncMoveDown(self):
        rows=self.treev1.selection()
        for row in reversed(rows):
            self.treev1.move(row,self.treev1.parent(row),self.treev1.index(row)+1)
        
    def fncRemove(self):                
        selected_items = self.treev1.selection()        
        if(len(selected_items)==0):
            tk.messagebox.showerror("Error", "Select the section")
        for selected_item in selected_items:          
            self.treev1.delete(selected_item)
        self.frmHeader.children["frmTreeviewhandler"].children["btnRemoveAction"]["state"]=tk.DISABLED            
        self.frmHeader.children["frmTreeviewhandler"].children["btnMoveUpAction"]["state"]=tk.DISABLED
        self.frmHeader.children["frmTreeviewhandler"].children["btnMoveDownAction"]["state"]=tk.DISABLED
        
    def fncReloadData(self):
        self.LoadAllJsonData()
        self.BindExistingTreeview(None)
        
                
    def fncSaveData(self):
        AllData=[]
        for titem in self.treev1.get_children():
           AllData.append({"template":self.treev1.item(titem)["values"][0],"sectionCategory":self.treev1.item(titem)["values"][1],"ioName":self.treev1.item(titem)["values"][2],"ioValue":self.treev1.item(titem)["values"][3],"wrapperValue":self.treev1.item(titem)["values"][4]})        
        with open(os.path.join(self.config.FilePath, self.config.WrapperFileName), 'w', encoding='utf-8') as f:
            json.dump({"allData":AllData}, f, ensure_ascii=False, indent=4,separators=(',',': ')) 
            tk.messagebox.showinfo("info", "Save Successfully")            
            
            
    def fncChangeSectionCategory(self,event ):       
        print(self.varCurrentSectionCategory.get()) 
        
        for section in self.varAllIOName:
            if(section["Category"]==self.varCurrentSectionCategory.get()):
                print(section["Category"])
                if(self.checkKey(self.chdFrm1.children,"cmbIOName")):
                    self.chdFrm1.children["cmbIOName"].configure(values= section["IOName"])
       
    
    def fncOpenInnerChildForm(self):    
        containter = tk.Toplevel(self.ContainerFrame)        
        containter.title("Add Wrapper value")
        containter.geometry("400x275")
        innercontainter=ttk.Frame(containter)        
        innercontainter.pack(expand="True",fill=tk.BOTH,anchor="nw",side=tk.LEFT)
        innercontainter.columnconfigure(0, weight=1)
        innercontainter.rowconfigure(0, weight=1)
        self.chdFrm1=ttk.Frame(innercontainter)        
        self.chdFrm1.grid(row=0,column=0)
        self.chdFrm1.columnconfigure(0, weight=1)
        self.chdFrm1.columnconfigure(1, weight=1)
        self.chdFrm1.rowconfigure(0, weight=1)
        self.chdFrm1.rowconfigure(1, weight=1)
        self.chdFrm1.rowconfigure(2, weight=1)
        self.chdFrm1.rowconfigure(3, weight=1)
        self.chdFrm1.rowconfigure(4, weight=1)        

        ttk.Label(self.chdFrm1, text = "Template :").grid(row=0,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(self.chdFrm1, width = 24, textvariable = self.varCurrentTemplate, values=self.varAllTemlateName).grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        
        ttk.Label(self.chdFrm1,name="cmbTemplate",text = "Section Category :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        cmbSectionCategory=ttk.Combobox(self.chdFrm1, width = 24, textvariable = self.varCurrentSectionCategory, values=self.varAllSectionCategory)
        cmbSectionCategory.grid(row=1,column =1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        
         
        ttk.Label(self.chdFrm1,text = "IO Name :").grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(self.chdFrm1, width = 24, name="cmbIOName", textvariable = self.varCurrentIOName,state="readonly").grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        ttk.Label(self.chdFrm1,text = "IO Value :").grid(row=3,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm1,width = 26, textvariable = self.varIOValue).grid(row=3,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        
        ttk.Label(self.chdFrm1,text = "Wrapper Value :" ).grid(row=4,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm1, name="txtWrapperValue",width = 26, textvariable = self.varTemplateValue).grid(row=4,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        
        ttk.Button(self.chdFrm1, text ="Save", width=10, command =lambda: self.fncAddAction(containter)).grid(row=5,column = 1 , padx=(10,0),pady=(3,5),sticky=tk.N+tk.W)        
        containter.grab_set()
        cmbSectionCategory.bind("<<ComboboxSelected>>", lambda event: self.fncChangeSectionCategory(event))
        

    
    def fncAddAction(self,container):
        if(self.varCurrentTemplate==None or self.varCurrentTemplate.get()=="" ):
            messagebox.showerror("Required", "Required Template")
            return
        if(self.varCurrentSectionCategory==None or self.varCurrentSectionCategory.get()=="" ):
            messagebox.showerror("Required", "Required Section Category")
            return
        if(self.varCurrentIOName==None or self.varCurrentIOName.get()==""):
            messagebox.showerror("Required", "Required IOName")
            return        
        if(self.varIOValue==None or self.varIOValue.get()==""):
            messagebox.showerror("Required", "Required IOValue")
            return        
        if(self.varTemplateValue==None or self.varTemplateValue.get()==""):
            messagebox.showerror("Required", "Required False Action Id")
            return
        self.treev1.insert("", 'end',values =(self.varCurrentTemplate.get(), self.varCurrentSectionCategory.get(),self.varCurrentIOName.get(),self.varIOValue.get(),self.varTemplateValue.get()))
        #reset the data
        self.varCurrentTemplate.set("")
        self.varCurrentSectionCategory.set("")
        self.varCurrentIOName.set("")
        self.varIOValue.set("")
        self.varTemplateValue.set("")        
        self.chdFrm1.children["cmbTemplate"].focus_set()      
        messagebox.showinfo("Success", "Action added successfully")


    

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
    myframe=tk.Frame(root,relief=tk.GROOVE,width=500,height=600,bd=1)
    myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
    IOWrapper(myframe,config)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
