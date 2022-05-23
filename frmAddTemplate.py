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


class AddTemplate:
    config=None    
    ContainerFrame=None    
    displayFont = ( "Verdana", 10)
    combostyle=None
    treeViewStyle=None
    varAllTemlate,varAllTemlateName,varCurrentTemplate,varAllSection,varCurrentSection,varAllAction=[],[],None,[],None,[]    
    IsUpdateSection=False,False
    
    varActionType= None    
    varCurrentTemplateName=None
    varCurrentUrl=None
    

    chdFrm1,chdFrm2=None,None
    var_allSectionName,var_allSectionType,var_allSectionCategory,var_allSectionCategoryType,var_allSelectorType, var_allActionType,var_allInputType,var_allConditionType=None,None,None,None,None, None,None,None
    
    var_sectionName,var_sectionType,var_sectionCategory=None,None,None
    var_actionId,var_actionType,var_controlSelectorType,var_control,var_inputType,var_manualValue,var_ioValue,var_nextActionId,var_ActionStartupType,var_conditionType,var_leftInputType,var_leftManualValue,var_leftIOValue,var_rightInputType,var_rightManualValue,var_rightIOValue,var_trueActionId,var_falseActionId=None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None

    
    treev1,treev2=None,None;

    def __init__(self,Container,config):
        self.config=config        
        self.varActionType= tk.StringVar()        
        self.varCurrentTemplateName= tk.StringVar()
        self.varCurrentUrl= tk.StringVar()         
        self.ContainerFrame=Container        
        self.LoadFromConfig()        
        self.fncCreateItems()
    
    def LoadFromConfig(self):
        self.var_allSectionName,self.var_allSectionType,self.var_allSectionCategory,self.var_allSectionCategoryType,self.var_allSelectorType, self.var_allActionType,self.var_allInputType,self.var_allConditionType=self.config.SectionNames,self.config.SectionType,self.config.SectionCategory,self.config.SectionCategoryType,self.config.SelectorType,self.config.ActionTypes,self.config.InputType,self.config.ConditionType
        self.var_actionId,self.var_actionType,self.var_controlSelectorType,self.var_control,self.var_inputType,self.var_manualValue,self.var_ioValue,self.var_nextActionId,self.var_ActionStartupType,self.var_conditionType,self.var_leftInputType,self.var_leftManualValue,self.var_leftIOValue,self.var_rightInputType,self.var_rightManualValue,self.var_rightIOValue,self.var_trueActionId,self.var_falseActionId = tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()
        self.var_sectionName,self.var_sectionType,self.var_sectionCategory=tk.StringVar(),tk.StringVar(),tk.StringVar()
        self.var_actionType.set("Fill Input")
        self.var_ActionStartupType.set("Middle")
        
    
    def fncChangeTemplateType(self,event):
        if(self.varActionType.get()=="Add Template"):
            self.frmHeader.children["cmbTemplateName"].grid_forget()
            self.frmHeader.children["txtTemplateName"].grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)            
            self.varCurrentTemplate=None
            self.varCurrentSection=None
        elif(self.varActionType.get()=="Update Template"):
            self.frmHeader.children["txtTemplateName"].grid_forget()
            self.frmHeader.children["cmbTemplateName"].grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        self.BindDropDownTemplateName()
            
    def LoadAllJsonData(self):
        try:
            if not os.path.exists(self.config.FilePath):
                os.makedirs(self.config.FilePath)        
            if os.path.isfile(os.path.join(self.config.FilePath, self.config.TemplateFileName)) is False:
                with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName), 'w') as fp:
                    print('Empty File Created')
            else:
                with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName)) as fp:
                    self.varAllTemlate=[]
                    self.varAllTemlate = json.load(fp)
                    self.varAllTemlateName=[]
                    for x in self.varAllTemlate:
                        self.varAllTemlateName.append(x["templateName"])
        except Exception as ex:
            messagebox.showerror("Error", ex)

    
    def BindDropDownTemplateName(self ):
        self.LoadAllJsonData()
        if(self.checkKey(self.frmHeader.children,"cmbTemplateName")):
            self.frmHeader.children["cmbTemplateName"].configure(values=self.varAllTemlateName)

    def checkKey(self,dict, key):      
        if key in dict.keys():
            return True
        else:
            return False

    def BindExistingTreeview(self,event,procType=1):
        if(procType==1):
            self.varCurrentTemplate=None        
            self.var_allSectionName=[]
            self.clear_all_gridview(procType)        
            for template in self.varAllTemlate:
                if template["templateName"]==self.varCurrentTemplateName.get():
                    self.varCurrentTemplate=template
            if(self.varCurrentTemplate != None):
                self.varCurrentUrl.set(self.varCurrentTemplate["url"])
                for sections in self.varCurrentTemplate["sections"]:                
                    sectionName,sectionType,sectionCategory,actionCount='','','',0
                    if(self.checkKey(sections,"sectionName")):
                        sectionName=sections["sectionName"]
                    if(self.checkKey(sections,"sectionType")):
                        sectionType=sections["sectionType"]
                    if(self.checkKey(sections,"sectionCategory")):
                        sectionCategory=sections["sectionCategory"]
                    if(self.checkKey(sections,"actions")):
                        actionCount=len(sections["actions"]) 
                    self.treev1.insert("", 'end',values =(sectionName, sectionType,sectionCategory,actionCount))
                    self.var_allSectionName.append(sectionName)
        elif(procType==2):
            self.varCurrentSection=None        
            self.clear_all_gridview(procType)       
            if(not self.checkKey(self.varCurrentTemplate,"sections")):       
                return
            for sections in self.varCurrentTemplate["sections"]:                 
                if sections["sectionName"]==self.var_sectionName.get():
                    self.varCurrentSection=sections
            if(self.varCurrentSection != None):
                if( self.checkKey(self.varCurrentSection,"sectionCategory")) :
                    self.var_sectionCategory.set(self.varCurrentSection["sectionCategory"])
                if( self.checkKey(self.varCurrentSection,"sectionType")) :
                    self.var_sectionType.set(self.varCurrentSection["sectionType"])
                for actions in self.varCurrentSection["actions"]:                
                    ActionId,ActionType,StartupType,SelectorType,Control_,InputType,ManualValue,IOValue,NextActionId='','','','','','','','',''
                    conditionType,leftInputType,leftManualValue,leftIOValue,trueActionId,rightInputType,rightManualValue,rightIOValue,falseActionId='','','','','','','','',''
                    if(self.checkKey(actions,"actionId")):
                        ActionId=actions["actionId"]
                    if(self.checkKey(actions,"actionType")):
                        ActionType=actions["actionType"]
                    if(self.checkKey(actions,"startupType")):
                        StartupType=actions["startupType"]
                    if(self.checkKey(actions,"selectorType")):
                        SelectorType=actions["selectorType"]
                    if(self.checkKey(actions,"control")):
                        Control_=actions["control"]
                    if(self.checkKey(actions,"inputType")):
                        InputType=actions["inputType"]
                    if(self.checkKey(actions,"manualValue")):
                        ManualValue=actions["manualValue"]
                    if(self.checkKey(actions,"ioValue")):
                        IOValue=actions["ioValue"]
                    if(self.checkKey(actions,"nextActionId")):
                        NextActionId=actions["nextActionId"]

                    if(self.checkKey(actions,"conditionType")):
                        conditionType=actions["conditionType"]
                    if(self.checkKey(actions,"leftInputType")):
                        leftInputType=actions["leftInputType"]
                    if(self.checkKey(actions,"leftManualValue")):
                        leftManualValue=actions["leftManualValue"]
                    if(self.checkKey(actions,"leftIOValue")):
                        leftIOValue=actions["leftIOValue"]
                    if(self.checkKey(actions,"trueActionId")):
                        trueActionId=actions["trueActionId"]
                    if(self.checkKey(actions,"rightInputType")):
                        rightInputType=actions["rightInputType"]
                    if(self.checkKey(actions,"rightManualValue")):
                        rightManualValue=actions["rightManualValue"]
                    if(self.checkKey(actions,"rightIOValue")):
                        rightIOValue=actions["rightIOValue"]
                    if(self.checkKey(actions,"falseActionId")):
                        falseActionId=actions["falseActionId"]

                    
                    self.treev2.insert("", 'end',values =(ActionId,ActionType,StartupType,SelectorType,Control_,InputType,ManualValue,IOValue,NextActionId,
                    conditionType,leftInputType,leftManualValue,leftIOValue,trueActionId,rightInputType,rightManualValue,rightIOValue,falseActionId))
                self.treev2.pack_forget()
                self.treev2.pack(fill=tk.BOTH,expand=True,pady=(10,10))
    
    def clear_all_gridview(self,ProcType=1):
        if(ProcType==1):
            for item in self.treev1.get_children():
                self.treev1.delete(item)
            self.frmHeader.children["frmTreeviewhandler"].children["btnEditAction"]["state"]=tk.DISABLED
            self.frmHeader.children["frmTreeviewhandler"].children["btnRemoveAction"]["state"]=tk.DISABLED
            self.frmHeader.children["frmTreeviewhandler"].children["btnMoveUpAction"]["state"]=tk.DISABLED
            self.frmHeader.children["frmTreeviewhandler"].children["btnMoveDownAction"]["state"]=tk.DISABLED
        elif(ProcType==2) :
            for item in self.treev2.get_children():
                self.treev2.delete(item)
            self.frmHeader1.children["frmTreeviewhandler1"].children["btnRemoveAction"]["state"]=tk.DISABLED
            self.frmHeader1.children["frmTreeviewhandler1"].children["btnMoveUpAction"]["state"]=tk.DISABLED
            self.frmHeader1.children["frmTreeviewhandler1"].children["btnMoveDownAction"]["state"]=tk.DISABLED


    def fncCreateItems(self):
        self.varActionType.set("Add Template")
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

        ttk.Label(self.frmHeader,text = "Type").grid(row=0,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        cmbType=ttk.Combobox(self.frmHeader,state="readonly", width = 24, textvariable = self.varActionType, values=("Add Template","Update Template"))
        
        cmbType.grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        

        ttk.Label(self.frmHeader,text = "Template Name").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        cmbAllTemplate=ttk.Combobox(self.frmHeader,name="cmbTemplateName",state="readonly", width = 24, textvariable = self.varCurrentTemplateName)
        ttk.Entry(self.frmHeader,name="txtTemplateName",width = 26,textvariable = self.varCurrentTemplateName).grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        
        ttk.Label(self.frmHeader,text = "Url" ,font=self.displayFont).grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.frmHeader,name="txtUrl",textvariable =self.varCurrentUrl, width = 26).grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        

        
        frmbtn = ttk.Frame(self.frmHeader)        
        frmbtn.grid(row=0,column = 2, rowspan=3, sticky=tk.N+tk.S+tk.W)
        btnSave = ttk.Button( frmbtn, text ="Save", width=10,command =lambda: self.fncSaveData())
        btnReset = ttk.Button ( frmbtn, text ="Reset", width=10,command =lambda: self.fncResetData())
        
        btnSave.grid(row=0,column = 0 , padx=(10,0),pady=(3,5))        
        btnReset.grid(row=1,column = 0, padx=(10,0),pady=(3,5))


        frmbtn1 = ttk.Frame(self.frmHeader,name="frmTreeviewhandler")        
        frmbtn1.grid(row=3,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnAddAction = ttk.Button ( frmbtn1,name="btnAddAction" , image=self.config.ico_add ,command =lambda: self.fncOpenChildForm(False) )        
        btnEditAction = ttk.Button ( frmbtn1,name="btnEditAction" , image=self.config.ico_edit , state=tk.DISABLED,  command =lambda: self.fncOpenChildForm(True) )        
        btnRemoveAction = ttk.Button ( frmbtn1,name="btnRemoveAction",image=self.config.ico_delete ,  state=tk.DISABLED,command =lambda: self.fncRemove() )
        btnMoveUpAction = ttk.Button ( frmbtn1,name="btnMoveUpAction",image=self.config.ico_up ,  state=tk.DISABLED,command =lambda: self.fncMoveUp() )
        btnMoveDownAction = ttk.Button ( frmbtn1,name="btnMoveDownAction",image=self.config.ico_down , state=tk.DISABLED,command =lambda: self.fncMoveDown() )
        btnAddAction.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        btnEditAction.grid(row=0,column = 1, padx=(10,0),pady=(3,5))
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
        self.treev1["columns"] = ("sectionName", "sectionType", "sectionCategory","actionCount")
        # Defining heading
        self.treev1['show'] = 'headings'
        # Assigning the width and anchor to the
        # respective columns
        self.treev1.column("sectionName", width = 50, anchor ='nw')
        self.treev1.column("sectionType", width = 50, anchor ='nw')
        self.treev1.column("sectionCategory", width = 50, anchor ='nw')
        self.treev1.column("actionCount", width = 50, anchor ='center')
        
        # Assigning the heading names to the
        # respective columns
        self.treev1.heading("sectionName", text ="Section Name")
        self.treev1.heading("sectionType", text ="Type")
        self.treev1.heading("sectionCategory", text ="Category")
        self.treev1.heading("actionCount", text ="Action Count")
        
        self.treev1.bind("<ButtonRelease-1>",lambda event:self.fncMoveItems(event,1))
        cmbType.bind("<<ComboboxSelected>>", lambda event:self.fncChangeTemplateType(event))
        cmbAllTemplate.bind("<<ComboboxSelected>>",lambda event:self.BindExistingTreeview(event,1))

    def fnc_Select_Record(self,procType):
        if(procType==1):
            selected=self.treev1.focus()        
            if(len(selected)>0):
                self.frmHeader.children["frmTreeviewhandler"].children["btnEditAction"]["state"]=tk.NORMAL
                self.frmHeader.children["frmTreeviewhandler"].children["btnRemoveAction"]["state"]=tk.NORMAL
                self.frmHeader.children["frmTreeviewhandler"].children["btnMoveUpAction"]["state"]=tk.NORMAL
                self.frmHeader.children["frmTreeviewhandler"].children["btnMoveDownAction"]["state"]=tk.NORMAL
        elif (procType==2):
            selected=self.treev2.focus()        
            if(len(selected)>0):                
                self.frmHeader1.children["frmTreeviewhandler1"].children["btnRemoveAction"]["state"]=tk.NORMAL
                self.frmHeader1.children["frmTreeviewhandler1"].children["btnMoveUpAction"]["state"]=tk.NORMAL
                self.frmHeader1.children["frmTreeviewhandler1"].children["btnMoveDownAction"]["state"]=tk.NORMAL


    def fncMoveItems(self,e,procType=1):
        self.fnc_Select_Record(procType)

    def fncMoveUp(self,procType=1):
        if(procType==1):
            rows=self.treev1.selection()
            for row in rows:
                self.treev1.move(row,self.treev1.parent(row),self.treev1.index(row)-1)
        elif(procType==2):
            rows=self.treev2.selection()
            for row in rows:
                self.treev2.move(row,self.treev2.parent(row),self.treev2.index(row)-1)
            

    def fncMoveDown(self,procType=1):
        if(procType==1):
            rows=self.treev1.selection()
            for row in reversed(rows):
                self.treev1.move(row,self.treev1.parent(row),self.treev1.index(row)+1)
        if(procType==2):
            rows=self.treev2.selection()
            for row in reversed(rows):
                self.treev2.move(row,self.treev2.parent(row),self.treev2.index(row)+1)
        

    def fncRemove(self,ProcType=1):        
        if(ProcType==1):
            selected_items = self.treev1.selection()        
            if(len(selected_items)==0):
                tk.messagebox.showerror("Error", "Select the section")
            for selected_item in selected_items:          
                self.treev1.delete(selected_item)
            self.frmHeader.children["frmTreeviewhandler"].children["btnRemoveAction"]["state"]=tk.DISABLED
            self.frmHeader.children["frmTreeviewhandler"].children["btnEditAction"]["state"]=tk.DISABLED
            self.frmHeader.children["frmTreeviewhandler"].children["btnMoveUpAction"]["state"]=tk.DISABLED
            self.frmHeader.children["frmTreeviewhandler"].children["btnMoveDownAction"]["state"]=tk.DISABLED
        if(ProcType==2):
            selected_items = self.treev2.selection()        
            if(len(selected_items)==0):
                tk.messagebox.showerror("Error", "Select the section")
            for selected_item in selected_items:          
                self.treev2.delete(selected_item)
            self.frmHeader1.children["frmTreeviewhandler1"].children["btnRemoveAction"]["state"]=tk.DISABLED
            self.frmHeader1.children["frmTreeviewhandler1"].children["btnEditAction"]["state"]=tk.DISABLED
            self.frmHeader1.children["frmTreeviewhandler1"].children["btnMoveUpAction"]["state"]=tk.DISABLED
            self.frmHeader1.children["frmTreeviewhandler1"].children["btnMoveDownAction"]["state"]=tk.DISABLED

    def fncResetData(self):
        self.varActionType.set("Add Template")
        self.varCurrentTemplateName.set("")        
        self.varCurrentUrl.set("")
        self.clear_all_gridview()
        self.fncChangeTemplateType(None)
        self.BindDropDownTemplateName()
                
    def fncSaveData(self,ProcType):

        list_of_bool = [True for elem in  self.varAllTemlate
                            if self.varCurrentTemplateName.get() in elem["templateName"]]
        tempSection=None
        self.varAllSection=[]
        
        if(self.varActionType.get()=="Add Template"):
            if any(list_of_bool):
                messagebox.showerror("Already Exists", "Template Name already exists")
                return
        if(self.varActionType.get()=="Update Template"):
            if not any(list_of_bool):
                messagebox.showerror("Not Exists", "Invalid template name")
                return
            self.varAllSection=self.varCurrentTemplate["sections"]
        if(self.varCurrentUrl==None or self.varCurrentUrl.get()==""):
            messagebox.showerror("Required", "Required URL")
            return

        if(ProcType==2):
            FoundSection=False
            if(self.var_sectionName==None or self.var_sectionName.get()==""):
                messagebox.showerror("Required", "Section Section Name")
                return
            for sections in self.varAllSection:                                    
                    if(self.checkKey(sections,"sectionName")):
                        if(sections["sectionName"]==self.var_sectionName.get()): 
                            FoundSection=True
                            break
            if(self.IsUpdateSection and not FoundSection):
                messagebox.showerror("Required", "Invalid Section Name")
                return
            if(not self.IsUpdateSection and FoundSection):
                messagebox.showerror("Required", "Section Name already Exists")
                return
            if(self.var_sectionType==None or self.var_sectionType.get()==""):
                messagebox.showerror("Required", "Required Section Type")
                return
            if(self.var_sectionCategory==None or self.var_sectionCategory.get()==""):
                messagebox.showerror("Required", "Required Section Category")
                return
            if(self.treev2==None):
                messagebox.showerror("Required", "Required Actions")
                return
            AllAction=[]
            for item in self.treev2.get_children():            
                aDict = {"actionId": str(self.treev2.item(item)["values"][0])  , "actionType":str(self.treev2.item(item)["values"][1]) ,
                "startupType":str( self.treev2.item(item)["values"][2]),"selectorType":str(self.treev2.item(item)["values"][3]) ,"control":str( self.treev2.item(item)["values"][4]),
                "inputType":str(self.treev2.item(item)["values"][5]) ,"manualValue":str( self.treev2.item(item)["values"][6]),"ioValue":str(self.treev2.item(item)["values"][7]) ,
                "nextActionId":str(self.treev2.item(item)["values"][8]) ,"conditionType": str(self.treev2.item(item)["values"][9]) ,"leftInputType":str(self.treev2.item(item)["values"][10]) ,
                "leftManualValue":str(self.treev2.item(item)["values"][11]) ,"leftIOValue":str(self.treev2.item(item)["values"][12]) ,"trueActionId":str(self.treev2.item(item)["values"][13]) ,
                "rightInputType":str(self.treev2.item(item)["values"][14]) ,"rightManualValue":str(self.treev2.item(item)["values"][15]) ,"rightIOValue":str(self.treev2.item(item)["values"][16]),
                "falseActionId": str(self.treev2.item(item)["values"][17]) }
                AllAction.append(aDict)
            if(len(AllAction)==0):
                messagebox.showerror("Required", "Required Actions")
                return
            tempSection={"sectionName":str( self.var_sectionName.get()),"sectionCategory":str(self.var_sectionCategory.get()) ,
            "sectionType":str( self.var_sectionType.get()),"actions":AllAction}
            

            if(self.IsUpdateSection):
                for index,sections in  enumerate(self.varAllSection) : 
                        if(self.checkKey(sections,"sectionName")):
                            if(sections["sectionName"]==self.var_sectionName.get()): 
                                self.varAllSection[index]=tempSection
            else:
                if (self.varAllSection==None):
                    self.varAllSection=[]
                self.varAllSection.append(tempSection)
            if(len(self.varAllSection) ==0):
                messagebox.showerror("Required", "Required Section")
                return

        AllData=None
        if(self.varActionType.get()=="Add Template"):
            AllData={"templateName":str(self.varCurrentTemplateName.get()) ,"url":str(self.varCurrentUrl.get()) ,"sections":self.varAllSection}
            self.varAllTemlate.append(AllData)
        elif (self.varActionType.get()=="Update Template"): 
            AllSection=[]
            for titem in self.treev1.get_children():
                for vitem in self.varAllSection:
                    if(self.treev1.item(titem)["values"][0] ==vitem["sectionName"]):
                        AllSection.append(vitem)
            AllData={"templateName":str( self.varCurrentTemplateName.get()),"url": str(self.varCurrentUrl.get()) ,"sections":AllSection}
            for i, item in enumerate(self.varAllTemlate):
                if item["templateName"] == self.varCurrentTemplateName.get():
                    self.varAllTemlate[i] = AllData
        
        with open(os.path.join(self.config.FilePath, self.config.TemplateFileName), 'w', encoding='utf-8') as f:
            json.dump(self.varAllTemlate, f, ensure_ascii=False, indent=4,separators=(',',': '))            
            tk.messagebox.showinfo("showinfo", "Save Successfully")            
            if(ProcType==2):
                if(self.checkKey(self.frmHeader1.children,"cmbSectionName")):
                    self.frmHeader1.children["cmbSectionName"].focus_set()
                if(self.checkKey(self.frmHeader1.children,"txtSectionName")):
                    self.frmHeader1.children["txtSectionName"].focus_set()     

            
            
            
            
    def fncOpenChildForm(self,IsUpdate):    
        if(IsUpdate):
            selected_items = self.treev1.selection()        
            if(selected_items==None or len(selected_items)==0):
                tk.messagebox.showerror("Error", "Select the section")
                self.IsUpdateSection=False
                return
            else:
                for x in selected_items:
                    print(self.treev1.item(x)["values"][0])                    
                    self.var_sectionName.set(self.treev1.item(x)["values"][0])  
                    self.IsUpdateSection=True
                
        else:
            self.varCurrentSection=None
            self.IsUpdateSection=False
        containter = tk.Toplevel(self.ContainerFrame,name="frmChildForm")        
        if(IsUpdate):
            containter.title("Update Section")
        else:
            containter.title("Add Section")
        containter.geometry("600x400")
        innercontainter=ttk.Frame(containter)
        innercontainter.pack(expand=tk.TRUE,fill=tk.BOTH)
        innercontainter.columnconfigure(0, weight=1)
        innercontainter.rowconfigure(0, weight=1)
        innercontainter.rowconfigure(1, weight=100)

        self.frmHeader1=ttk.Frame(innercontainter)
        self.frmHeader1.grid(row=0,column=0)
        self.frmHeader1.columnconfigure(0, weight=1)
        self.frmHeader1.columnconfigure(1, weight=1)
        self.frmHeader1.columnconfigure(2, weight=100)
        self.frmHeader1.rowconfigure(0, weight=1)
        self.frmHeader1.rowconfigure(1, weight=1)
        self.frmHeader1.rowconfigure(2, weight=1)
        self.frmHeader1.rowconfigure(3, weight=1)
        self.frmHeader1.rowconfigure(4, weight=1)
        
        cmbSectionName=None
        ttk.Label(self.frmHeader1,text = "Section Name :").grid(row=0,column = 0,padx=(10, 10), pady=(20, 2), sticky=tk.N+tk.S+tk.E)        
        if(IsUpdate):
            cmbSectionName=ttk.Combobox(self.frmHeader1, name="cmbSectionName", width = 24,state="readonly" , textvariable = self.var_sectionName, values=self.var_allSectionName)
            cmbSectionName.grid(row=0,column = 1,padx=(10, 10), pady=(20, 2), sticky=tk.N+tk.S+tk.W)
        else:
            ttk.Entry(self.frmHeader1, width = 26, name="txtSectionName", textvariable = self.var_sectionName).grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)    

        ttk.Label(self.frmHeader1,text = "Section Type :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Combobox(self.frmHeader1, width = 24,state="readonly", textvariable = self.var_sectionType, values=self.var_allSectionType).grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        
        ttk.Label(self.frmHeader1,text = "Section Category :").grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Combobox(self.frmHeader1, width = 24,state="readonly", textvariable = self.var_sectionCategory, values=self.var_allSectionCategory).grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        ttk.Button(self.frmHeader1, text ="Save", width=10, command =lambda: self.fncSaveData(2)).grid(row=5,column = 1 , padx=(10,0),pady=(3,5),sticky=tk.N+tk.W)

        frmbtn1 = ttk.Frame(self.frmHeader1,name="frmTreeviewhandler1")
        frmbtn1.grid(row=3,column = 1, columnspan=4, sticky=tk.N+tk.W+tk.E)
        btnAddAction = ttk.Button ( frmbtn1,name="btnAddAction" , image=self.config.ico_add ,command =lambda: self.fncOpenInnerChildForm() )        
        btnRemoveAction = ttk.Button ( frmbtn1,name="btnRemoveAction", image=self.config.ico_delete, state=tk.DISABLED, command =lambda: self.fncRemove(2) )
        btnMoveUpAction = ttk.Button ( frmbtn1,name="btnMoveUpAction", image=self.config.ico_up,  state=tk.DISABLED,  command =lambda: self.fncMoveUp(2) )
        btnMoveDownAction = ttk.Button ( frmbtn1,name="btnMoveDownAction",  image=self.config.ico_down,state=tk.DISABLED,  command =lambda: self.fncMoveDown(2) )
        btnAddAction.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        btnRemoveAction.grid(row=0,column =1, padx=(10,0),pady=(3,5))
        btnMoveUpAction.grid(row=0,column =2, padx=(10,0),pady=(3,5))
        btnMoveDownAction.grid(row=0,column =3, padx=(10,0),pady=(3,5))

        frmBody=ttk.Frame(innercontainter)
        frmBody.grid(row=1,column = 0,  sticky=tk.N+tk.S+tk.W+tk.E)
        self.treev2 = ttk.Treeview(frmBody, selectmode ='browse')
        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(frmBody,orient ="vertical",command = self.treev2.yview)
        horscrlbar = ttk.Scrollbar(frmBody,orient ="horizontal",command = self.treev2.xview)

        # Calling pack method w.r.to vertical
        # scrollbar
        verscrlbar.pack(side ='right', fill ='y')
        horscrlbar.pack(side ='bottom', fill ='x')
        self.treev2.pack(fill=tk.BOTH,expand=True,pady=(10,10))
        # Configuring treeview
        self.treev2.configure(xscrollcommand = horscrlbar.set, yscrollcommand=verscrlbar.set)

        # Defining number of columns
        self.treev2["columns"] = ("actionId", "actionType", "startupType","selectorType","control","inputType","manualValue","ioValue","nextActionId",
        "conditionType","leftInputType","leftManualValue","leftIOValue","trueActionId",
        "rightInputType","rightManualValue","rightIOValue","falseActionId")
        # Defining heading
        self.treev2['show'] = 'headings'
        # Assigning the width and anchor to the
        # respective columns
        self.treev2.column("actionId",  stretch=tk.NO, width = 50, anchor ='nw')
        self.treev2.column("actionType",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("startupType",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("selectorType",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("control",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("inputType",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("manualValue",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("ioValue",  stretch=tk.NO, width = 150, anchor ='nw')
        self.treev2.column("nextActionId",  stretch=tk.NO, width = 50, anchor ='nw')
        self.treev2.column("conditionType",  stretch=tk.NO, width = 50, anchor ='nw')
        self.treev2.column("leftInputType",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("leftManualValue",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("leftIOValue",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("trueActionId",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("rightInputType",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("rightManualValue",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("rightIOValue",  stretch=tk.NO, width = 100, anchor ='nw')
        self.treev2.column("falseActionId",  stretch=tk.NO, width = 50, anchor ='nw')
        
        # Assigning the heading names to the
        # respective columns
        self.treev2.heading("actionId", text ="Id")
        self.treev2.heading("actionType", text ="Action Type")
        self.treev2.heading("startupType", text ="Startup Type")
        self.treev2.heading("selectorType", text ="Selector Type")
        self.treev2.heading("control", text ="Control")
        self.treev2.heading("inputType", text ="Input Type")
        self.treev2.heading("manualValue", text ="manualValue")
        self.treev2.heading("ioValue", text ="IO Value")
        self.treev2.heading("nextActionId", text ="Next Action")  

        self.treev2.heading("conditionType", text ="Condition Type")  
        self.treev2.heading("leftInputType", text ="Left Input Type")  
        self.treev2.heading("rightInputType", text ="Right Input Type")  
        self.treev2.heading("leftManualValue", text ="Left Manual Value")  
        self.treev2.heading("rightManualValue", text ="Right Manual Value")  
        self.treev2.heading("leftIOValue", text ="left IO Value")  
        self.treev2.heading("rightIOValue", text ="right IO Value")  
        self.treev2.heading("trueActionId", text ="True Action Id")         
        self.treev2.heading("falseActionId", text ="False Action Id")         

        self.treev2.bind("<ButtonRelease-1>", lambda event: self.fncMoveItems(event,2))
        if(cmbSectionName!=None):
            self.BindExistingTreeview(None,2)
            cmbSectionName.bind("<<ComboboxSelected>>", lambda event: self.BindExistingTreeview(event,2))
        containter.grab_set()
    
    def fncChangeActionType(self,event):
        if(self.var_actionType.get()=="Condition" or self.var_actionType.get()=="Find Index"):
            if(self.chdFrm1 != None):
                self.chdFrm1.grid_forget()
            if(self.chdFrm2 != None):
                self.chdFrm2.grid(row=3,column=0,columnspan=4)
        else:
            if(self.chdFrm2 != None):
                self.chdFrm2.grid_forget()
            if(self.chdFrm1 != None):
                self.chdFrm1.grid(row=2,column=0,columnspan=4)
    
    def fncChangeInputType(self,event):
        if(self.var_inputType.get()=="ManualValue"):
            self.txtIOValue.config(state="disabled")
            self.txtManualValue.config(state="normal")
        else:
            self.txtIOValue.config(state="normal")
            self.txtManualValue.config(state="disabled")
    
    def fncOpenInnerChildForm(self):    
        containter = tk.Toplevel(self.frmHeader1)        
        containter.title("Add Action")
        containter.geometry("650x300")
        innercontainter=ttk.Frame(containter)        
        innercontainter.pack(expand="True",fill=tk.BOTH,anchor="nw",side=tk.LEFT)
        innercontainter.columnconfigure(0, weight=1)
        innercontainter.rowconfigure(0, weight=1)
        chdFrm=ttk.Frame(innercontainter)        
        chdFrm.grid(row=0,column=0)
        chdFrm.columnconfigure(0, weight=1)
        chdFrm.columnconfigure(1, weight=1)
        chdFrm.columnconfigure(2, weight=1)
        chdFrm.columnconfigure(3, weight=1)
        chdFrm.rowconfigure(0, weight=1)
        chdFrm.rowconfigure(1, weight=1)
        chdFrm.rowconfigure(2, weight=1)
        chdFrm.rowconfigure(3, weight=1)
        chdFrm.rowconfigure(4, weight=1)        

        ttk.Label(chdFrm,text = "Action ID :").grid(row=0,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(chdFrm, width = 26, textvariable = self.var_actionId).grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(chdFrm,text = "Action Type :").grid(row=0,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        cmbActionType=ttk.Combobox(chdFrm, width = 24, textvariable = self.var_actionType, values=self.var_allActionType)
        cmbActionType.grid(row=0,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        
         
        ttk.Label(chdFrm,text = "Startup Type :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        rdoFrm=ttk.Frame(chdFrm)
        rdoFrm.grid(row=1,column = 1,padx=(10, 10),columnspan=3, pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Radiobutton(rdoFrm,text="Strat",value="Start",variable = self.var_ActionStartupType).grid(row=0,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Radiobutton(rdoFrm,text="End",value="End",variable =  self.var_ActionStartupType).grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Radiobutton(rdoFrm,text="Middle",value="Middle",variable =  self.var_ActionStartupType).grid(row=0,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        self.chdFrm1=ttk.Frame(chdFrm) 
        self.chdFrm1.grid(row=2,column=0,columnspan=4)
        self.chdFrm1.columnconfigure(0, weight=1)
        self.chdFrm1.columnconfigure(1, weight=1)
        self.chdFrm1.columnconfigure(2, weight=1)
        self.chdFrm1.columnconfigure(3, weight=1)
        self.chdFrm1.rowconfigure(0, weight=1)
        self.chdFrm1.rowconfigure(1, weight=1)
        self.chdFrm1.rowconfigure(2, weight=1)

        ttk.Label(self.chdFrm1,text = "Selector Type :").grid(row=0,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(self.chdFrm1, width = 24,state="readonly" , textvariable = self.var_controlSelectorType, values=self.var_allSelectorType).grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm1,text = "Control :" ).grid(row=0,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm1, name="txtControl",width = 26, textvariable = self.var_control).grid(row=0,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        ttk.Label(self.chdFrm1,text = "Input Type :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        cmbInputType =ttk.Combobox(self.chdFrm1, width = 24,state="readonly" , textvariable = self.var_inputType, values=self.var_allInputType)
        cmbInputType.grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm1,text = "Manual Value :" ).grid(row=1,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        self.txtManualValue=ttk.Entry(self.chdFrm1, width = 26, textvariable = self.var_manualValue)
        self.txtManualValue.grid(row=1,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        ttk.Label(self.chdFrm1,text = "IO Value :").grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        self.txtIOValue=ttk.Entry(self.chdFrm1, width = 26,state="readonly" , textvariable = self.var_ioValue)
        self.txtIOValue.grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm1,text = "Next Action Id :").grid(row=2,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm1, width = 26, textvariable = self.var_nextActionId).grid(row=2,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        self.chdFrm2=ttk.Frame(chdFrm) 
        self.chdFrm2.grid(row=3,column=0,columnspan=4)
        self.chdFrm2.columnconfigure(0, weight=1)
        self.chdFrm2.columnconfigure(1, weight=1)
        self.chdFrm2.columnconfigure(2, weight=1)
        self.chdFrm2.columnconfigure(3, weight=1)
        self.chdFrm2.columnconfigure(4, weight=1)
        self.chdFrm2.rowconfigure(0, weight=1)
        self.chdFrm2.rowconfigure(1, weight=1)
        self.chdFrm2.rowconfigure(2, weight=1)
        self.chdFrm2.rowconfigure(3, weight=1)

        ttk.Label(self.chdFrm2,text = "Condition Type :").grid(row=0,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(self.chdFrm2, width = 24, textvariable = self.var_conditionType, values=self.var_allConditionType).grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        ttk.Label(self.chdFrm2,text = "Left Input Type :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(self.chdFrm2, width = 24,state="readonly" , textvariable = self.var_leftInputType, values=self.var_allInputType).grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm2,text = "Left Manual Value :" ).grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm2, width = 26, textvariable = self.var_leftManualValue).grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm2,text = "Left IOValue :" ).grid(row=3,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm2, width = 26, textvariable = self.var_leftIOValue).grid(row=3,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm2,text = "True Next ActionId :" ).grid(row=4,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm2, width = 26, textvariable = self.var_trueActionId).grid(row=4,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        self.var_rightInputType.set("IOValue")
        ttk.Label(self.chdFrm2,text = "Right Input Type :").grid(row=1,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(self.chdFrm2, width = 24, textvariable = self.var_rightInputType, values=self.var_allInputType).grid(row=1,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm2,text = "Right Manual Value :" ).grid(row=2,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm2, width = 26, textvariable = self.var_rightManualValue).grid(row=2,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm2,text = "Right IOValue :" ).grid(row=3,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm2, width = 26, textvariable = self.var_rightIOValue).grid(row=3,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.chdFrm2,text = "False Next ActionId :" ).grid(row=4,column = 2,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.chdFrm2, width = 26, textvariable = self.var_falseActionId).grid(row=4,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        ttk.Button(chdFrm, text ="Save", width=10, command =lambda: self.fncAddAction(containter)).grid(row=5,column = 1 , padx=(10,0),pady=(3,5),sticky=tk.N+tk.W)        
        containter.grab_set()
        self.fncChangeActionType(None)        
        containter.protocol("WM_DELETE_WINDOW", lambda :self.fncCloseInnerChild(containter))
        cmbActionType.bind("<<ComboboxSelected>>", lambda event: self.fncChangeActionType(event))
        cmbInputType.bind("<<ComboboxSelected>>", lambda event: self.fncChangeInputType(event))

    def fncCloseInnerChild(self,container):        
        self.ContainerFrame.children["frmChildForm"].focus_set()
        self.ContainerFrame.children["frmChildForm"].grab_set()
        container.destroy()

    def fncAddAction(self,container):
        if(self.var_actionId==None or self.var_actionId.get()=="" ):
            messagebox.showerror("Required", "Required Action Id")
            return
        if(self.var_actionType==None or self.var_actionType.get()=="" ):
            messagebox.showerror("Required", "Required Action Type")
            return
        if(self.var_ActionStartupType==None or self.var_ActionStartupType.get()==""):
            messagebox.showerror("Required", "Required startup type")
            return
        if(self.var_actionType.get()=="Wait"):
            if(self.var_manualValue==None or self.var_manualValue.get()==""):
                    messagebox.showerror("Required", "Required Manual Value")
                    return
        elif(not (self.var_actionType.get()=="Condition" or self.var_actionType.get()=="Find Index")) :
            if(self.var_controlSelectorType==None or self.var_controlSelectorType.get()==""):
                messagebox.showerror("Required", "Required Selector Type")
                return
            if(self.var_control==None or self.var_control.get()==""):
                messagebox.showerror("Required", "Required Control")
                return
            if(self.var_inputType==None or self.var_inputType.get()==""):
                messagebox.showerror("Required", "Required Input Type")
                return
            if(self.var_inputType.get()=="ManualValue"):
                if(self.var_manualValue==None or self.var_manualValue.get()==""):
                    messagebox.showerror("Required", "Required Manual Value")
                    return
            else:
                if(self.var_ioValue==None or self.var_ioValue.get()==""):
                    messagebox.showerror("Required", "Required IO Value")
                    return
            if(self.var_nextActionId==None or self.var_nextActionId.get()==""):
                messagebox.showerror("Required", "Required Next Action Id")
                return
        else:
            if(self.var_conditionType==None or self.var_conditionType.get()==""):
                messagebox.showerror("Required", "Required Condition Type")
                return
            if(self.var_leftInputType==None or self.var_leftInputType.get()==""):
                messagebox.showerror("Required", "Required Left Input Type")
                return
            if(self.var_leftInputType.get()=="ManualValue"):
                if(self.var_leftManualValue==None or self.var_leftManualValue.get()==""):
                    messagebox.showerror("Required", "Required Left Manual Value")
                    return
            else:
                if(self.var_leftIOValue==None or self.var_leftIOValue.get()==""):
                    messagebox.showerror("Required", "Required Left IO Value")
                    return
            if(self.var_rightInputType==None or self.var_rightInputType.get()==""):
                messagebox.showerror("Required", "Required Right Input Type")
                return
            if(self.var_rightInputType.get()=="ManualValue"):
                if(self.var_rightManualValue==None or self.var_rightManualValue.get()==""):
                    messagebox.showerror("Required", "Required Right Manual Value")
                    return
            else:
                if(self.var_rightIOValue==None or self.var_rightIOValue.get()==""):
                    messagebox.showerror("Required", "Required Right IO Value")
                    return

            if(self.var_trueActionId==None or self.var_trueActionId.get()==""):
                messagebox.showerror("Required", "Required True Action Id")
                return
            if(self.var_falseActionId==None or self.var_falseActionId.get()==""):
                messagebox.showerror("Required", "Required False Action Id")
                return
        self.treev2.insert("", 'end',values =(self.var_actionId.get(), self.var_actionType.get(),self.var_ActionStartupType.get(),
        self.var_controlSelectorType.get(),self.var_control.get(),self.var_inputType.get(),self.var_manualValue.get(),self.var_ioValue.get(),self.var_nextActionId.get(),
        self.var_conditionType.get(),self.var_leftInputType.get(),self.var_leftManualValue.get(),self.var_leftIOValue.get(),self.var_trueActionId.get(),
        self.var_rightInputType.get(),self.var_rightManualValue.get(),self.var_rightIOValue.get(),self.var_falseActionId.get()
        ))
        #reset the data
        self.var_control.set("")
        self.var_manualValue.set("")
        self.var_leftManualValue.set("")
        self.var_rightInputType.set("")
        self.var_actionId.set("")
        self.var_nextActionId.set("")
        self.var_trueActionId.set("")
        self.var_falseActionId.set("")
        self.var_ActionStartupType.set("Middle")
        self.chdFrm1.children["txtControl"].focus_set()        

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
    myframe=tk.Frame(root,relief=tk.GROOVE,width=500,height=600,bd=1)
    myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
    AddTemplate(myframe,config)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
