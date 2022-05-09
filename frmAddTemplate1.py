from dataclasses import field
from pickle import NONE
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from turtle import left

from setuptools import Command
import GenerateConfig as Gc
import json,io,os
import fontawesome as fa
from ttkthemes import ThemedStyle


class AddTemplate:
    config=None    
    ContainerFrame=None    
    displayFont = ( "Verdana", 10)
    combostyle=None
    treeViewStyle=None
    varAllTemlate,varAllTemlateName,varCurrentTemplate,varAllSection,varCurrentSection,varAllAction=[],[],None,[],None,[]    
    
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
        self.LoadAllJsonData()
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
            
    def LoadAllJsonData(self):
        try:
            if not os.path.exists(self.config.FilePath):
                os.makedirs(self.config.FilePath)        
            if os.path.isfile(os.path.join(self.config.FilePath, self.config.TemplateFileName)) is False:
                with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName), 'w') as fp:
                    print('Empty File Created')
            else:
                with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName)) as fp:
                    self.varAllTemlate = json.load(fp)
                    self.varAllTemlateName=[]
                    for x in self.varAllTemlate:
                        self.varAllTemlateName.append(x["templateName"])
        except Exception as ex:
            messagebox.showerror("Error", ex)

    
    def BindDropDownTemplateName(self ):
        self.LoadAllJsonData()
        self.frmHeader.children["cmbTemplateName"].configure(values=self.varAllTemlateName)

    def checkKey(self,dict, key):      
        if key in dict.keys():
            return True
        else:
            return False
    def BindExistingTreeview(self,event,procType=1):
        if(procType==1):
            self.varCurrentTemplate=None        
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
        elif(procType==2):
            self.varCurrentSection=None        
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
        cmbType.bind("<<ComboboxSelected>>", self.fncChangeTemplateType)

        ttk.Label(self.frmHeader,text = "Template Name").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        cmbAllTemplate=ttk.Combobox(self.frmHeader,name="cmbTemplateName",state="readonly", width = 24, textvariable = self.varCurrentTemplateName)
        ttk.Entry(self.frmHeader,name="txtTemplateName",width = 26,textvariable = self.varCurrentTemplateName).grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        
        ttk.Label(self.frmHeader,text = "Url" ,font=self.displayFont).grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(self.frmHeader,name="txtUrl",textvariable =self.varCurrentUrl, width = 26).grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        self.BindDropDownTemplateName()

        
        frmbtn = ttk.Frame(self.frmHeader)        
        frmbtn.grid(row=0,column = 2, rowspan=3, sticky=tk.N+tk.S+tk.W)
        btnSave = ttk.Button( frmbtn, text ="Save", width=10,command =lambda: self.fncSaveData())
        btnReset = ttk.Button ( frmbtn, text ="Reset", width=10,command =lambda: self.fncResetData())
        
        btnSave.grid(row=0,column = 0 , padx=(10,0),pady=(3,5))        
        btnReset.grid(row=1,column = 0, padx=(10,0),pady=(3,5))


        frmbtn1 = ttk.Frame(self.frmHeader,name="frmTreeviewhandler")        
        frmbtn1.grid(row=3,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnAddAction = tk.Button ( frmbtn1,name="btnAddAction" ,text =fa.icons['plus'], relief='groove', width=3, font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncOpenChildForm(False) )        
        btnEditAction = tk.Button ( frmbtn1,name="btnEditAction" ,text =fa.icons['pen'], relief='groove', width=3, state=tk.DISABLED, font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncOpenChildForm(True) )        
        btnRemoveAction = tk.Button ( frmbtn1,name="btnRemoveAction", text =fa.icons['trash'], relief='groove', width=3, state=tk.DISABLED,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncRemove() )
        btnMoveUpAction = tk.Button ( frmbtn1,name="btnMoveUpAction", text =fa.icons['arrow-up'], relief='groove', width=3, state=tk.DISABLED,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncMoveUp() )
        btnMoveDownAction = tk.Button ( frmbtn1,name="btnMoveDownAction", text =fa.icons['arrow-down'], relief='groove', width=3, state=tk.DISABLED,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncMoveDown() )
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
        self.treev1.configure(xscrollcommand = verscrlbar.set, yscrollcommand=horscrlbar.set)

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
        
        self.treev1.bind("<ButtonRelease-1>",self.fncMoveItems)
        cmbAllTemplate.bind("<<ComboboxSelected>>", self.BindExistingTreeview)

    def fnc_Select_Record(self):
        selected=self.treev1.focus()
        #values= self.treev1.item(selected,'values')
        #print(values)
        self.frmHeader.children["frmTreeviewhandler"].children["btnEditAction"]["state"]=tk.NORMAL
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
            self.treev1.move(row,self.treev.parent(row),self.treev1.index(row)+1)
        

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
                
    def fncSaveData(self):
        list_of_bool = [True for elem in  self.varAllTemlate
                            if self.varCurrentTemplateName.get() in elem["templateName"]]
        if(self.varActionType.get()=="Add Template"):
            if any(list_of_bool):
                messagebox.showerror("Already Exists", "Template Name already exists")
                return
        if(self.varActionType.get()=="Update Template"):
            if not any(list_of_bool):
                messagebox.showerror("Not Exists", "Invalid template name")
                return
        if(self.varCurrentUrl==None or self.varCurrentUrl.get()==""):
            messagebox.showerror("Required", "Required URL")
            return
        
        AllAction=[]
        for item in self.treev1.get_children():            
            aDict = {"action_type":self.treev1.item(item)["values"][0] , "action_on":self.treev1.item(item)["values"][1],
             "control":self.treev1.item(item)["values"][2],"io_name":self.treev1.item(item)["values"][3],"control_value":self.treev1.item(item)["values"][4]}
            AllAction.append(aDict)
        if(len(AllAction)==0):
            messagebox.showerror("Required", "Please add actions")
            return
        
        AllData={"templateName":self.varCurrentTemplateName.get(),"url":self.varCurrentUrl.get(),"actions":AllAction}

        if(self.varActionType.get()=="Add Template"):
            self.varAllTemlate.append(AllData)
        elif (self.varActionType.get()=="Update Template"): 
            for i, item in enumerate(self.varAllTemlate):
                if item["templateName"] == self.varCurrentTemplateName.get():
                    self.varAllTemlate[i] = AllData
        
        with open(os.path.join(self.config.FilePath, self.config.TemplateFileName), 'w', encoding='utf-8') as f:
            json.dump(self.varAllTemlate, f, ensure_ascii=False, indent=4,separators=(',',': '))            
            tk.messagebox.showinfo("showinfo", "Save Successfully")
            self.fncResetData()
            
    def fncOpenChildForm(self,IsUpdate):    
        if(IsUpdate):
            selected_items = self.treev1.selection()        
            if(selected_items==None or len(selected_items)==0):
                tk.messagebox.showerror("Error", "Select the section")
                return
            else:
                print(1)
        else:
            self.varCurrentSection=None
        containter = tk.Toplevel(self.ContainerFrame)        
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
            cmbSectionName=ttk.Combobox(self.frmHeader1, width = 24,state="readonly" , textvariable = self.var_sectionName, values=self.var_allSectionName)
            cmbSectionName.grid(row=0,column = 1,padx=(10, 10), pady=(20, 2), sticky=tk.N+tk.S+tk.W)
        else:
            ttk.Entry(self.frmHeader1, width = 26, textvariable = self.var_sectionName).grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)    

        ttk.Label(self.frmHeader1,text = "Section Type :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Combobox(self.frmHeader1, width = 24,state="readonly", textvariable = self.var_sectionType, values=self.var_allSectionType).grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        
        ttk.Label(self.frmHeader1,text = "Section Category :").grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Combobox(self.frmHeader1, width = 24,state="readonly", textvariable = self.var_sectionCategory, values=self.var_allSectionCategory).grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        frmbtn1 = ttk.Frame(self.frmHeader1,name="frmTreeviewhandler1")
        frmbtn1.grid(row=3,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnAddAction = tk.Button ( frmbtn1,name="btnAddAction" ,text =fa.icons['plus'], relief='groove', width=3, font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncOpenInnerChildForm() )        
        btnRemoveAction = tk.Button ( frmbtn1,name="btnRemoveAction", text =fa.icons['trash'], relief='groove', width=3, state=tk.DISABLED,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncRemove(2) )
        btnMoveUpAction = tk.Button ( frmbtn1,name="btnMoveUpAction", text =fa.icons['arrow-up'], relief='groove', width=3, state=tk.DISABLED,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncMoveUp(2) )
        btnMoveDownAction = tk.Button ( frmbtn1,name="btnMoveDownAction", text =fa.icons['arrow-down'], relief='groove', width=3, state=tk.DISABLED,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncMoveDown(2) )
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
        self.treev2.configure(xscrollcommand = verscrlbar.set, yscrollcommand=horscrlbar.set)

        # Defining number of columns
        self.treev2["columns"] = ("action_type", "action_on", "control","io_name","control_value")
        # Defining heading
        self.treev2['show'] = 'headings'
        # Assigning the width and anchor to the
        # respective columns
        self.treev2.column("action_type", width = 50, anchor ='nw')
        self.treev2.column("action_on", width = 50, anchor ='nw')
        self.treev2.column("control", width = 50, anchor ='nw')
        self.treev2.column("io_name", width = 50, anchor ='nw')
        self.treev2.column("control_value", width = 50, anchor ='nw')        
        # Assigning the heading names to the
        # respective columns
        self.treev2.heading("action_type", text ="Action Type")
        self.treev2.heading("action_on", text ="Action on")
        self.treev2.heading("control", text ="Control")
        self.treev2.heading("io_name", text ="IO Name")
        self.treev2.heading("control_value", text ="Default Value")        

        self.treev2.bind("<ButtonRelease-1>",self.fncMoveItems)
        if(cmbSectionName!=None):
            cmbSectionName.bind("<<ComboboxSelected>>", self.BindExistingTreeview)
    
    def fncChangeActionType(self,event):
        if(self.var_actionType.get()=="Condition"):
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
        containter = tk.Toplevel(self.ContainerFrame)        
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
        
         
        ttk.Label(chdFrm,text = "StartupType :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
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
        ttk.Entry(self.chdFrm1, width = 26, textvariable = self.var_control).grid(row=0,column = 3,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

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

        ttk.Button ( chdFrm, text ="Save", width=10, command =lambda: self.fncAddAction(chdFrm)).grid(row=5,column = 1 , padx=(10,0),pady=(3,5),sticky=tk.N+tk.W)
        chdFrm.grab_set()
        self.fncChangeActionType(None)
        cmbActionType.bind("<<ComboboxSelected>>", lambda event: self.fncChangeActionType(event))
        cmbInputType.bind("<<ComboboxSelected>>", lambda event: self.fncChangeInputType(event))

    def fncAddAction(self,container):
        if(self.var_action_type==None or self.var_action_type.get()=="" ):
            messagebox.showerror("Required", "Required Action Type")
            return
        if(self.var_action_on==None or self.var_action_on.get()==""):
            messagebox.showerror("Required", "Required Action On")
            return
        if(self.var_control==None or self.var_control.get()==""):
            messagebox.showerror("Required", "Required Control")
            return
        if((self.var_io_name==None or self.var_io_name.get()=="" ) and  (self.var_control_value==None or self.var_control_value.get()=="" ) 
        and (not(self.var_action_type.get() =="Wait" or self.var_action_type.get() =="Break") )):
            messagebox.showerror("Required", "Required IO Name or Default Value")
            return
        
        self.treev1.insert("", 'end',values =(self.var_action_type.get(), self.var_action_on.get(),self.var_control.get(),self.var_io_name.get(),self.var_control_value.get()))
        self.var_io_name.set("")
        self.var_control_value.set("")
        self.var_control.set("")
        container.children["txtControl"].focus_set()
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
