from dataclasses import field
from pickle import NONE
import tkinter as tk
from tkinter import ttk
import GenerateConfig as Gc
import json,io,os
import fontawesome as fa


class AddTemplate:
    config=None
    ContainerCanvas=None
    ContainerFrame=None
    Parent_Height=500
    Parent_Width=600
    displayFont = ( "Verdana", 10)
    combostyle=None
    treeViewStyle=None
    varAllTemlateName=[]
    varAllTemlate=[]
    varCurrentTemplate=None
    varCurrentTemplateName=None
    #varCurrentTemplateName_cmb=None
    #varCurrentTemplateName_txt=None
    varActionType= None

    treev=None;

    def __init__(self,Container,config):
        self.config=config
        #self.combostyle = ttk.Style()
        #self.combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'selectbackground': self.config.COLOR_TOP_BACKGROUND,'fieldbackground': self.config.COLOR_BACKGROUND,'background': self.config.COLOR_BACKGROUND}}})
        #self.combostyle.theme_use('combostyle') 
        self.treeViewStyle= ttk.Style()
        self.treeViewStyle.theme_use("default")
        
        #self.treeViewStyle.configure("TreeView","selectbackground": ,background= self.config.COLOR_BACKGROUND,foreground="black",rowheight=20, fieldbackground= self.config.COLOR_MENU_BACKGROUND)
        #self.treeViewStyle.configure("Combobox",background= self.config.COLOR_BACKGROUND,foreground="black",rowheight=30, fieldbackground= self.config.COLOR_MENU_BACKGROUND)
        
        self.varActionType= tk.StringVar()        
        self.varCurrentTemplateName= tk.StringVar()
        #self.varCurrentTemplateName_txt= tk.StringVar()
        #self.varCurrentTemplateName_cmb= tk.StringVar()
        self.Parent_Height=Container["height"]-20
        self.Parent_Width=Container["width"]-20
        self.ContainerFrame=Container        
        
        self.LoadAllJsonData()
        self.fncCreateItems()
    
    def fncChangeTemplateType(self,event):
        if(self.varActionType.get()=="Add Template"):
            self.frmHeader.children["cmbTemplateName"].grid_forget()
            self.frmHeader.children["txtTemplateName"].grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)            
        elif(self.varActionType.get()=="Update Template"):
            self.frmHeader.children["txtTemplateName"].grid_forget()
            self.frmHeader.children["cmbTemplateName"].grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
            
            

    def LoadAllJsonData(self):
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
    
    def BindDropDownTemplateName(self ):
        self.LoadAllJsonData()
        self.frmHeader.children["cmbTemplateName"].configure(values=self.varAllTemlateName)


    def BindExistingTreeview(self,event):
        self.varCurrentTemplate=None        
        self.clear_all_gridview()
        #print (self.varCurrentTemplateName.get())
        for template in self.varAllTemlate:
            if template["templateName"]==self.varCurrentTemplateName.get():
                self.varCurrentTemplate=template
        if(self.varCurrentTemplate != None):
            for actions in self.varCurrentTemplate["actions"]:
                #print (actions)
                self.treev.insert("", 'end', text ="L1",values =(actions["action_type"], actions["action_on"],actions["control"],actions["io_name"],actions["control_value"]))
    
    def clear_all_gridview(self):
        for item in self.treev.get_children():
            self.delete(item)

    def fncCreateItems(self):
        self.varActionType.set("Add Template")
        self.frmHeader = tk.Frame(self.ContainerFrame,bg= self.config.COLOR_MENU_BACKGROUND)        
        frmBody = tk.Frame(self.ContainerFrame,bg=self.config.COLOR_MENU_BACKGROUND)
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

        
        

        tk.Label(self.frmHeader,text = "Type",font=self.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).grid(row=0,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        cmbType=ttk.Combobox(self.frmHeader, width = 24,font=self.displayFont, textvariable = self.varActionType, values=("Add Template","Update Template"))
        
        cmbType.grid(row=0,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        cmbType.bind("<<ComboboxSelected>>", self.fncChangeTemplateType)

        tk.Label(self.frmHeader,text = "Template Name",font=self.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).grid(row=1,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)        
        cmbAllTemplate=ttk.Combobox(self.frmHeader,name="cmbTemplateName", width = 24,font=self.displayFont, textvariable = self.varCurrentTemplateName)
        #cmbAllTemplate.grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)

        tk.Entry(self.frmHeader,name="txtTemplateName",bg=self.config.COLOR_BACKGROUND, width = 25,font=self.displayFont,textvariable = self.varCurrentTemplateName).grid(row=1,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        tk.Label(self.frmHeader,text = "Url" ,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND).grid(row=2,column = 0,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.E)
        tk.Entry(self.frmHeader,name="txtUrl", width = 25,bg=self.config.COLOR_BACKGROUND,font=self.displayFont).grid(row=2,column = 1,padx=(10, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W)
        self.BindDropDownTemplateName()

        #tk.Label(frmHeader,text = "Status" ,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND).grid(row=3,column = 0,padx=(10, 10), pady=(5, 10), sticky=tk.N+tk.S+tk.E)
        #tk.Label(frmHeader,text = "" ,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND).grid(row=3,column = 1,padx=(10, 10), pady=(5, 10), sticky=tk.N+tk.S+tk.W)

        frmbtn = tk.Frame(self.frmHeader,bg=self.config.COLOR_MENU_BACKGROUND)        
        frmbtn.grid(row=0,column = 2, rowspan=3, sticky=tk.N+tk.S+tk.W)
        
        btnSave = tk.Button ( frmbtn, text ="Save", width=10,relief='raised', font=self.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command =lambda: self.fncAddAction(treev))
        btnReset = tk.Button ( frmbtn, text ="Reset", width=10,relief='raised', font=self.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command =lambda: self.fncAddAction(treev))
        
        btnSave.grid(row=0,column = 0 , padx=(10,0),pady=(3,5))        
        btnReset.grid(row=1,column = 0, padx=(10,0),pady=(3,5))


        frmbtn1 = tk.Frame(self.frmHeader,bg=self.config.COLOR_MENU_BACKGROUND)        
        frmbtn1.grid(row=3,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnAddAction = tk.Button ( frmbtn1, text =fa.icons['plus'], relief='groove', width=3, font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncAddAction(treev) )
        btnRemoveAction = tk.Button ( frmbtn1, text =fa.icons['trash'], relief='groove', width=3,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncAddAction(treev) )
        btnMoveUpAction = tk.Button ( frmbtn1, text =fa.icons['arrow-up'], relief='groove', width=3,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncAddAction(treev) )
        btnMoveDownAction = tk.Button ( frmbtn1, text =fa.icons['arrow-down'], relief='groove', width=3,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command =lambda: self.fncAddAction(treev) )
        btnAddAction.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        btnRemoveAction.grid(row=0,column =1, padx=(10,0),pady=(3,5))
        btnMoveUpAction.grid(row=0,column =2, padx=(10,0),pady=(3,5))
        btnMoveDownAction.grid(row=0,column =3, padx=(10,0),pady=(3,5))

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
        self.treev["columns"] = ("1", "2", "3","4","5","6","7","8")
        # Defining heading
        self.treev['show'] = 'headings'
        # Assigning the width and anchor to the
        # respective columns
        self.treev.column("1", width = 50, anchor ='nw')
        self.treev.column("2", width = 50, anchor ='nw')
        self.treev.column("3", width = 50, anchor ='nw')
        self.treev.column("4", width = 50, anchor ='nw')
        self.treev.column("5", width = 50, anchor ='nw')
        self.treev.column("6", width = 10, anchor ='c')
        self.treev.column("7", width = 10, anchor ='c')
        self.treev.column("8", width = 10, anchor ='c')
        # Assigning the heading names to the
        # respective columns
        self.treev.heading("1", text ="Action Type")
        self.treev.heading("2", text ="Action on")
        self.treev.heading("3", text ="Control")
        self.treev.heading("4", text ="IO Name")
        self.treev.heading("5", text ="Default Value")
        self.treev.heading("6", text ="Move Up")
        self.treev.heading("7", text ="Move Down")
        self.treev.heading("8", text ="Remove")

        cmbAllTemplate.bind("<<ComboboxSelected>>", self.BindExistingTreeview)


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
    AddTemplate(myframe,config)
    root.mainloop()
