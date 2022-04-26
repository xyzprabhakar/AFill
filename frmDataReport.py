from dataclasses import field
from pickle import NONE
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import GenerateConfig as Gc
import json,io,os
import fontawesome as fa
from ttkthemes import ThemedStyle


class DataReport:
    config=None    
    ContainerFrame=None    
    displayFont = ( "Verdana", 10)
    combostyle=None
    treeViewStyle=None
    varAllDataFile=[]
    
    varActionType= None
    varCurrentFileName=None
    varCurrentApplicantType=None
    varCurrentTemplateType=None    
    varCurrentCreationDt=None
    varCurrentModifyDt=None
    varCurrentFileData=None

    treev=None;

    def __init__(self,Container,config):
        self.config=config        
        self.varActionType= tk.StringVar()        
        self.varCurrentFileName= tk.StringVar()
        self.varCurrentApplicantType= tk.StringVar() 
        self.varCurrentTemplateType= tk.StringVar()
        self.varCurrentCreationDt= tk.StringVar()
        self.varCurrentModifyDt= tk.StringVar()
        self.varCurrentFileData= tk.StringVar()                
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
                    
        except Exception as ex:
            messagebox.showerror("Error", ex)


    def BindExistingTreeview(self):
        self.varCurrentTemplate=None        
        self.clear_all_gridview()        
        self.LoadAllJsonData()        
        if(self.varAllDataFile != None):            
            for actions in self.varAllDataFile:                
                self.treev.insert("", 'end',values =(actions["FileName"], actions["ApplicantType"],actions["TemplateType"],actions["CreationDt"],actions["CreationDt"]))
    
    def clear_all_gridview(self):
        for item in self.treev.get_children():
            self.treev.delete(item)

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
        
        frmbtn1 = ttk.Frame(self.frmHeader,name="frmTreeviewhandler")        
        frmbtn1.grid(row=3,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnReffreshData = tk.Button ( frmbtn1,name="btnReffreshData", text =fa.icons['sync'], relief='groove', width=3,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command = lambda :self.BindExistingTreeview() )
        btnUpdateData = tk.Button ( frmbtn1,name="btnUpdateData" ,text =fa.icons['pencil-alt'], relief='groove', width=3, font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda : self.fncOpenChildForm() )        
        btnRemoveData = tk.Button ( frmbtn1,name="btnRemoveData", text =fa.icons['trash'], relief='groove', width=3, font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda : self.fncRemove() )
        
        btnReffreshData.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        btnUpdateData.grid(row=0,column = 1, padx=(10,0),pady=(3,5))
        btnRemoveData.grid(row=0,column =2, padx=(10,0),pady=(3,5))        

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

        

    def fnc_Select_Record(self):
        selected=self.treev.focus()
        values= self.treev.item(selected,'values')
        print(values)
        self.frmHeader.children["frmTreeviewhandler"].children["btnRemoveAction"]["state"]=tk.NORMAL
        self.frmHeader.children["frmTreeviewhandler"].children["btnMoveUpAction"]["state"]=tk.NORMAL
        self.frmHeader.children["frmTreeviewhandler"].children["btnMoveDownAction"]["state"]=tk.NORMAL


    
    def fncRemove(self):
        selected_items = self.treev.selection()        
        for selected_item in selected_items:          
            self.treev.delete(selected_item)    
                
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
        for item in self.treev.get_children():            
            aDict = {"action_type":self.treev.item(item)["values"][0] , "action_on":self.treev.item(item)["values"][1],
             "control":self.treev.item(item)["values"][2],"io_name":self.treev.item(item)["values"][3],"control_value":self.treev.item(item)["values"][4]}
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

            
    def fncOpenChildForm(self):    
        containter = tk.Toplevel(self.ContainerFrame)        
        containter.title("Add Action")
        containter.geometry("300x210")
        chdFrm=ttk.Frame(containter)        
        chdFrm.pack(expand=tk.TRUE,fill=tk.BOTH)
        chdFrm.columnconfigure(0, weight=1)
        chdFrm.columnconfigure(1, weight=1)
        chdFrm.columnconfigure(2, weight=100)
        chdFrm.rowconfigure(0, weight=1)
        chdFrm.rowconfigure(1, weight=1)
        chdFrm.rowconfigure(2, weight=1)
        chdFrm.rowconfigure(3, weight=1)
        chdFrm.rowconfigure(4, weight=1)
        chdFrm.rowconfigure(5, weight=1)
        chdFrm.rowconfigure(6, weight=100)
        ttk.Label(chdFrm,text = "Action Type :").grid(row=0,column = 0,padx=(10, 10), pady=(20, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Combobox(chdFrm, width = 24,state="readonly" , textvariable = self.var_action_type, values=self.config.Action_Types).grid(row=0,column = 1,padx=(10, 10), pady=(20, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(chdFrm,text = "Action On :").grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        ttk.Combobox(chdFrm, width = 24,state="readonly", textvariable = self.var_action_on, values=self.config.Action_On).grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(chdFrm,text = "Control :",name="txtControl" ).grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(chdFrm, width = 26, textvariable = self.var_control).grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(chdFrm,text = "IO Name :",).grid(row=3,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(chdFrm, width = 24,state="readonly", textvariable = self.var_io_name, values=self.config.IO_Name).grid(row=3,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Label(chdFrm,text = "Default Value :" ).grid(row=4,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        ttk.Entry(chdFrm, width = 26, textvariable = self.var_control_value).grid(row=4,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        ttk.Button ( chdFrm, text ="Save", width=10, command =lambda: self.fncAddAction(chdFrm)).grid(row=5,column = 1 , padx=(10,0),pady=(3,5),sticky=tk.N+tk.W)
        chdFrm.grab_set()
    
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
        
        self.treev.insert("", 'end',values =(self.var_action_type.get(), self.var_action_on.get(),self.var_control.get(),self.var_io_name.get(),self.var_control_value.get()))
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
    DataReport(myframe,config)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
