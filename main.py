# import tkinter module
#from tkinter import  * 
#from tkinter.ttk import *
from cgitb import grey
from pickle import TRUE
from tkinter import RAISED, ttk
import tkinter as tk
import fontawesome as fa
import os
import json
import GenerateConfig as Gc

class AutoFill(tk.Frame):
    RootPath=""
    TemplatePath=""
    DataFilePath=""

    #Theme Color
    COLOR_TOP_BACKGROUND="#44a2d2"
    COLOR_TOP_FOREGROUND="#44a2d2"
    COLOR_BACKGROUND="#f2f5f7"
    COLOR_FOREGROUND="#343a40"
    COLOR_MENU_BACKGROUND="#ffffff"    
    COLOR_MENU_FOREGROUND="#44a2d2"
    COLOR_MENU_PRESSED="#44a2d2"
    COLOR_MENU_HOVER="#44a2d2"

    COLOR_BUTTON_HOVER_BACKGROUND="#283234"
    COLOR_BUTTON_PRESSED_BACKGROUND="#bd55f9"
    COLOR_BUTTON_PRESSED_FOREGROUND="#f5f5f5"
    
    
    headerFonts = ("Verdana", 15, "bold")
    displayFont = ( "Verdana", 10)
    ##Declare All Control 
    # frmTopFrame = tk.Frame(self)
    # frmMainFrame= tk.Frame(self)
    # frmLeftFrame=tk.Frame(frmMainFrame)
    # frmContentFrame=tk.Frame(frmMainFrame)
    # frmInnerContentFrame=tk.Frame(frmContentFrame)
    # frmDashboardFrame=tk.Frame(frmInnerContentFrame)
    # frmTemplateFrame=tk.Frame(frmInnerContentFrame)
    # frmDataTemplateFrame=tk.Frame(frmInnerContentFrame)
    # frmImportDataFrame=tk.Frame(frmInnerContentFrame)
    # frmReportFrame=tk.Frame(frmInnerContentFrame)
    # frmSettingFrame=tk.Frame(frmInnerContentFrame)
    # frmChangePassword=tk.Frame(frmInnerContentFrame)

    #Left Menu Items
    MenuItems=[{"name":"rdoDashBoard", "text":"Dashboard","icon":"images\icons\cil-moon.png", "ficon":fa.icons['palette']},
                {"name":"rdoTemplate", "text":"Template","icon":"images\icons\cil-moon.png", "ficon":fa.icons['file']},
                {"name":"rdoDataTemplate", "text":"Data Template","icon":"images\icons\cil-moon.png", "ficon":fa.icons['database']},
                {"name":"rdoImportData", "text":"Import Data","icon":"images\icons\cil-moon.png", "ficon":fa.icons['file-import']},
                {"name":"rdoReport", "text":"Report","icon":"images\icons\cil-moon.png", "ficon":fa.icons['chart-line']},
                {"name":"rdoSetting", "text":"Setting","icon":"images\icons\cil-moon.png", "ficon":fa.icons['wrench']},
                {"name":"rdoChangePassword", "text":"Change Password","icon":"images\icons\cil-moon.png", "ficon":fa.icons['user']}]


    def __init__(self, isapp=True, name='AutoFill'):
        tk.Frame.__init__(self)
        self.pack(expand=tk.Y, fill=tk.BOTH)
        self.master["bd"]=1
        self.master["relief"]=tk.RAISED
        self.master.title('Auto Fill')
        self.master.unbind("<FocusIn>")
        self.isapp = isapp                        
        self.varMenu =tk.StringVar()
        self._create_widgets()

        


    def _create_widgets(self):
        self._create_Master()


    

    def _create_Master(self):
        frmTopFrame = tk.Frame(self,height=48,width=768,bg=self.COLOR_TOP_BACKGROUND)
        frmTopFrame.bind("<B1-Motion>",lambda e: self.move_app(e,self.master))        
        btnClose = tk.Button(frmTopFrame, text = fa.icons['trash'],font= self.headerFonts,command =self.master.destroy,bg=self.COLOR_TOP_BACKGROUND,fg=self.COLOR_MENU_BACKGROUND,relief=tk.FLAT)
        btnClose.pack(side=tk.RIGHT, pady=7,padx=5)        
        btnClose.bind('<Enter>', self.on_enter_button)
        btnClose.bind('<Leave>', self.on_leave_button)

        frmMainFrame = tk.Frame(self,height=450,width=768)
        frmLeftFrame = tk.Frame(frmMainFrame,height=450,width=200,bg=self.COLOR_MENU_BACKGROUND)
        frmContentFrame = tk.Frame(frmMainFrame,height=450,width=514,bg=self.COLOR_BACKGROUND)
        lblHeader= tk.Label(frmTopFrame,text="Auto Fill",font= self.headerFonts,bg=self.COLOR_TOP_BACKGROUND,fg=self.COLOR_MENU_BACKGROUND)
        lblHeader.pack(side=tk.LEFT, pady=7,padx=5)

        frmTopFrame.pack(side=tk.TOP, fill=tk.X, anchor=tk.NW)        
        #statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        frmMainFrame.pack(expand=True,fill=tk.BOTH)
        frmLeftFrame.pack(side=tk.LEFT, fill=tk.BOTH)
        frmContentFrame.pack( expand=True,fill=tk.BOTH)

        self._draw_menu(frmLeftFrame,frmContentFrame)

    def _draw_menu(self,parent,container):
        #global varMenu
        #varMenu =tk.StringVar(parent,"Dashboard")
        for thisdict in self.MenuItems:
            #photo = tk.PhotoImage(file = os.path.join(script_dir, thisdict["icon"]) )  
            # Resizing image to fit on button
            #photoimage = photo.subsample(10, 10)
            button = tk.Radiobutton(parent, name= thisdict["name"], text =thisdict["ficon"] +" "+thisdict["text"] , variable = self.varMenu,	value = thisdict["text"],
             indicator = 0, fg=self.COLOR_FOREGROUND, bg=self.COLOR_MENU_BACKGROUND,selectcolor=self.COLOR_BACKGROUND,
             borderwidth=0,anchor=tk.W,padx=10,
             command=lambda: self._create_inner_content(container)
             #image = photo,compound = tk.LEFT
            )
            #button.image=photo
            button.pack( fill=tk.X ,ipady = 8,ipadx=8)
            button.bind('<Enter>', self.on_enter_menu)
            button.bind('<Leave>', self.on_leave_menu)
        
    def on_enter_menu(self,e):
        e.widget['background'] = self.COLOR_BACKGROUND
        e.widget['foreground'] = self.COLOR_MENU_FOREGROUND

    def on_leave_menu(self,e):
        e.widget['background'] = self.COLOR_MENU_BACKGROUND
        e.widget['foreground'] = self.COLOR_FOREGROUND     

    def on_enter_button(self,e):
        e.widget['background'] = self.COLOR_BACKGROUND
        e.widget['foreground'] = self.COLOR_MENU_FOREGROUND

    def on_leave_button(self,e):
        e.widget['background'] = self.COLOR_TOP_BACKGROUND
        e.widget['foreground'] = self.COLOR_MENU_BACKGROUND 
    
    def move_app(self,event,parent):
        parent.geometry('+{0}+{1}'.format(event.x_root, event.y_root))
    
    

    def _create_inner_content(self,parent):
        
        if ("frmInnerContentFrame" in parent.children.keys()) :
            parent.children["frmInnerContentFrame"].pack_forget()
        frmInnerContentFrame = tk.Frame(parent,name="frmInnerContentFrame",height=400 ,width=490,bg=self.COLOR_MENU_BACKGROUND)
        frmInnerContentFrame.pack(fill=tk.BOTH ,pady = 20,padx=20,expand=True)
        frmInnerContentFrame.columnconfigure(0, weight=1)
        frmInnerContentFrame.rowconfigure(0, weight=1)
        frmInnerContentFrame.rowconfigure(1, weight=1)
        frmInnerContentFrame.rowconfigure(2, weight=100)

        lblHeader= tk.Label(frmInnerContentFrame,text=self.varMenu.get(),font= self.headerFonts,bg=self.COLOR_MENU_BACKGROUND, padx=10)
        lblHeader.grid(row=0, column=0, sticky=tk.N+tk.W)
        #lblHeader.pack(side=tk.TOP,  anchor=tk.NW,padx=8,pady=8)
        separator = tk.Frame(frmInnerContentFrame, bg=self.COLOR_TOP_BACKGROUND, height=1, bd=0)
        separator.grid(row=1, column=0, sticky=tk.E+tk.W)
        #separator.pack( side=tk.TOP,fill=tk.X,expand=True,padx=8,anchor=tk.NW )        
        frmInnerDisplayContentFrame = tk.Frame(frmInnerContentFrame,height=400 ,width=490,bg=self.COLOR_MENU_BACKGROUND,padx=10)        
        frmInnerDisplayContentFrame.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        #frmInnerDisplayContentFrame.pack(side=tk.TOP, fill=tk.BOTH,expand=True,padx=8,pady=8,anchor=tk.N )
        if(self.varMenu.get()=="Dashboard"):
            self._create_Template(frmInnerDisplayContentFrame)

    def _create_Template(self,parent):
                
        frmHeader = tk.Frame(parent,height=100 ,width=480,bg=self.COLOR_MENU_BACKGROUND)
        frmBody = tk.Frame(parent,height=300 ,width=480,bg=self.COLOR_MENU_BACKGROUND)
        lblTemplateName = tk.Label(frmHeader,text = "Template Name",font=self.displayFont, bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 10, anchor=tk.NW)
        lblTemplateUrl = tk.Label(frmHeader,text = "Url" ,font=self.displayFont,bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 50, anchor=tk.NW)
        txtTemplateName = tk.Entry(frmHeader,name="txtTemplateName",bg=self.COLOR_BACKGROUND, width = 25,font=self.displayFont).place(x = 170,y = 10, anchor=tk.NW)	
        txtUrl =tk.Entry(frmHeader,name="txtUrl", width = 25,bg=self.COLOR_BACKGROUND,font=self.displayFont).place(x = 170,y = 50, anchor=tk.NW)
        treev = ttk.Treeview(frmBody, selectmode ='browse')
        btnAction = tk.Button ( frmHeader, text ="Add Action",width=10, relief='flat', font=self.displayFont,fg=self.COLOR_MENU_BACKGROUND,bg=self.COLOR_TOP_BACKGROUND,  command =lambda: self.fncAddAction(treev) )
        btnSave = tk.Button ( frmHeader, text ="Save", width=10,relief='flat', font=self.displayFont,fg=self.COLOR_MENU_BACKGROUND,bg=self.COLOR_TOP_BACKGROUND, command =lambda: self.fncAddAction(treev))
        btnAction.bind('<Enter>', self.on_enter_button)
        btnAction.bind('<Leave>', self.on_leave_button)
        btnSave.bind('<Enter>', self.on_enter_button)
        btnSave.bind('<Leave>', self.on_leave_button)
        btnAction.place(x = 390,y = 8, anchor=tk.NW)
        btnSave.place(x = 390,y = 43, anchor=tk.NW)

        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)        
        parent.rowconfigure(1, weight=100)
        frmHeader.grid(row=0, column=0, sticky=tk.N+tk.W)
        frmBody.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(frmBody,orient ="vertical",command = treev.yview)

        # Calling pack method w.r.to vertical
        # scrollbar
        verscrlbar.pack(side ='right', fill ='y')
        treev.pack(fill=tk.BOTH,expand=True)

        # Configuring treeview
        treev.configure(xscrollcommand = verscrlbar.set)

        # Defining number of columns
        treev["columns"] = ("1", "2", "3")

        # Defining heading
        treev['show'] = 'headings'

        # Assigning the width and anchor to the
        # respective columns
        treev.column("1", width = 90, anchor ='c')
        treev.column("2", width = 90, anchor ='se')
        treev.column("3", width = 90, anchor ='se')

        # Assigning the heading names to the
        # respective columns
        treev.heading("1", text ="Name")
        treev.heading("2", text ="Sex")
        treev.heading("3", text ="Age")

        # Inserting the items and their features to the
        # columns built
        treev.insert("", 'end', text ="L1",values =("Nidhi", "F", "25"))
        treev.insert("", 'end', text ="L2",values =("Nisha", "F", "23"))
        treev.insert("", 'end', text ="L3",values =("Preeti", "F", "27"))
        treev.insert("", 'end', text ="L4",values =("Rahul", "M", "20"))
        treev.insert("", 'end', text ="L5",values =("Sonu", "F", "18"))
        treev.insert("", 'end', text ="L6",values =("Rohit", "M", "19"))
        treev.insert("", 'end', text ="L7",values =("Geeta", "F", "25"))
        treev.insert("", 'end', text ="L8",values =("Ankit", "M", "22"))
        treev.insert("", 'end', text ="L10",values =("Mukul", "F", "25"))
        treev.insert("", 'end', text ="L11",values =("Mohit", "M", "16"))
        treev.insert("", 'end', text ="L12",values =("Vivek", "M", "22"))
        treev.insert("", 'end', text ="L13",values =("Suman", "F", "30"))
        treev.insert("", 'end', text ="L1",values =("Nidhi", "F", "25"))
        treev.insert("", 'end', text ="L2",values =("Nisha", "F", "23"))
        treev.insert("", 'end', text ="L3",values =("Preeti", "F", "27"))
        treev.insert("", 'end', text ="L4",values =("Rahul", "M", "20"))
        treev.insert("", 'end', text ="L5",values =("Sonu", "F", "18"))
        treev.insert("", 'end', text ="L6",values =("Rohit", "M", "19"))
        treev.insert("", 'end', text ="L7",values =("Geeta", "F", "25"))
        treev.insert("", 'end', text ="L8",values =("Ankit", "M", "22"))
        treev.insert("", 'end', text ="L10",values =("Mukul", "F", "25"))
        treev.insert("", 'end', text ="L11",values =("Mohit", "M", "16"))
        treev.insert("", 'end', text ="L12",values =("Vivek", "M", "22"))
        treev.insert("", 'end', text ="L13",values =("Suman", "F", "30"))
        treev.insert("", 'end', text ="L1",values =("Nidhi", "F", "25"))
        treev.insert("", 'end', text ="L2",values =("Nisha", "F", "23"))
        treev.insert("", 'end', text ="L3",values =("Preeti", "F", "27"))
        treev.insert("", 'end', text ="L4",values =("Rahul", "M", "20"))
        treev.insert("", 'end', text ="L5",values =("Sonu", "F", "18"))
        treev.insert("", 'end', text ="L6",values =("Rohit", "M", "19"))
        treev.insert("", 'end', text ="L7",values =("Geeta", "F", "25"))
        treev.insert("", 'end', text ="L8",values =("Ankit", "M", "22"))
        treev.insert("", 'end', text ="L10",values =("Mukul", "F", "25"))
        treev.insert("", 'end', text ="L11",values =("Mohit", "M", "16"))
        treev.insert("", 'end', text ="L12",values =("Vivek", "M", "22"))
        treev.insert("", 'end', text ="L13",values =("Suman", "F", "30"))
        treev.insert("", 'end', text ="L1",values =("Nidhi", "F", "25"))
        treev.insert("", 'end', text ="L2",values =("Nisha", "F", "23"))
        treev.insert("", 'end', text ="L3",values =("Preeti", "F", "27"))
        treev.insert("", 'end', text ="L4",values =("Rahul", "M", "20"))
        treev.insert("", 'end', text ="L5",values =("Sonu", "F", "18"))
        treev.insert("", 'end', text ="L6",values =("Rohit", "M", "19"))
        treev.insert("", 'end', text ="L7",values =("Geeta", "F", "25"))
        treev.insert("", 'end', text ="L8",values =("Ankit", "M", "22"))
        treev.insert("", 'end', text ="L10",values =("Mukul", "F", "25"))
        treev.insert("", 'end', text ="L11",values =("Mohit", "M", "16"))
        treev.insert("", 'end', text ="L12",values =("Vivek", "M", "22"))
        treev.insert("", 'end', text ="L13",values =("Suman", "F", "30"))
    

    def fncAddAction(self,treeView):
        frmAddAction = tk.Toplevel(relief=tk.RAISED,bd=1,bg=self.COLOR_BACKGROUND)
        frmAddAction.title("Add Action")
        frmAddAction.geometry("480x400")
        frmAddAction.overrideredirect(1)

        frmTopFrame1 = tk.Frame(frmAddAction,height=48,width=480,bg=self.COLOR_TOP_BACKGROUND)
        frmTopFrame1.pack( side=tk.TOP,fill=tk.X,expand=True,anchor=tk.NW )
        frmTopFrame1.bind("<B1-Motion>",lambda e: self.move_app(e,frmAddAction))

        lblHeader= tk.Label(frmTopFrame1,text="Add Action",font= self.headerFonts,bg=self.COLOR_TOP_BACKGROUND,fg=self.COLOR_MENU_BACKGROUND)
        lblHeader.pack(side=tk.LEFT, pady=7,padx=5)
        btnClose = tk.Button(frmTopFrame1, text = fa.icons['trash'],font= self.headerFonts,command =frmAddAction.destroy,bg=self.COLOR_TOP_BACKGROUND,fg=self.COLOR_MENU_BACKGROUND,relief=tk.FLAT)
        btnClose.pack(side=tk.RIGHT, pady=7,padx=5)        
        btnClose.bind('<Enter>', self.on_enter_button)
        btnClose.bind('<Leave>', self.on_leave_button)
        frmBody = tk.Frame(frmAddAction,height=300 ,width=480,bg=self.COLOR_MENU_BACKGROUND,padx=20,pady=20)
        frmBody.pack( side=tk.TOP,fill=tk.BOTH,expand=True,anchor=tk.NW,ipadx=20,ipady=20 )

        varActionType = tk.StringVar()
        varActionOn = tk.StringVar(frmAddAction,"ById")
        
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'selectbackground': self.COLOR_MENU_FOREGROUND,'fieldbackground': self.COLOR_BACKGROUND,'background': self.COLOR_BACKGROUND}}})
        combostyle.theme_use('combostyle') 
        cmbActionType = ttk.Combobox(frmBody, width = 25, textvariable = varActionType)
        # Adding combobox drop down list
        cmbActionType['values'] = ('Fill Input', 'Fill TextArea','Select Option','Click Button','Click Submit' )
        rdoById = tk.Radiobutton(frmBody, text="ById", variable=varActionOn, value="ById",bg=self.COLOR_MENU_BACKGROUND,font=self.displayFont)
        rdoByName = tk.Radiobutton(frmBody, text="ByName", variable=varActionOn, value="ByName",bg=self.COLOR_MENU_BACKGROUND,font=self.displayFont)
        txtControlId = tk.Entry(frmBody,bg=self.COLOR_BACKGROUND, width = 25,font=self.displayFont)
        txtControlName =tk.Entry(frmBody, width = 25,bg=self.COLOR_BACKGROUND,font=self.displayFont)
        txtFieldId =tk.Entry(frmBody, width = 25,bg=self.COLOR_BACKGROUND,font=self.displayFont)

        lbl1 = tk.Label(frmBody,text = "Action Type",font=self.displayFont, bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 10, anchor=tk.NW)
        lbl2 = tk.Label(frmBody,text = "Action On" ,font=self.displayFont,bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 50, anchor=tk.NW)
        lbl3 = tk.Label(frmBody,text = "Control Id" ,font=self.displayFont,bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 90, anchor=tk.NW)
        lbl4 = tk.Label(frmBody,text = "Control Name" ,font=self.displayFont,bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 130, anchor=tk.NW)
        lbl5 = tk.Label(frmBody,text = "IO Name" ,font=self.displayFont,bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 170, anchor=tk.NW)
        cmbActionType.place(x = 170,y = 10, anchor=tk.NW)	
        rdoById.place(x = 170,y = 50, anchor=tk.NW)	
        rdoByName.place(x = 210,y = 50, anchor=tk.NW)	
        txtControlId.place(x = 170,y = 90, anchor=tk.NW)	
        txtControlName.place(x = 170,y = 130, anchor=tk.NW)	
        txtFieldId.place(x = 170,y = 170, anchor=tk.NW)	


        btnAction = tk.Button ( frmBody, text ="Save",width=10, relief='flat', font=self.displayFont,fg=self.COLOR_MENU_BACKGROUND,bg=self.COLOR_TOP_BACKGROUND,  command =lambda: self.fncAddAction(treeView) )
        btnSave = tk.Button ( frmBody, text ="Reset", width=10,relief='flat', font=self.displayFont,fg=self.COLOR_MENU_BACKGROUND,bg=self.COLOR_TOP_BACKGROUND, command =lambda: self.fncAddAction(treeView))
        btnAction.bind('<Enter>', self.on_enter_button)
        btnAction.bind('<Leave>', self.on_leave_button)
        btnSave.bind('<Enter>', self.on_enter_button)
        btnSave.bind('<Leave>', self.on_leave_button)
        btnAction.place(x = 170,y = 210, anchor=tk.NW)
        btnSave.place(x = 230,y = 210, anchor=tk.NW)


        frmAddAction.mainloop()
    
    






# creating main tkinter window/toplevel
#master = tk.Tk()
#master.geometry("768x480")
#master.config(bg="grey")


# b4_button = tk.Button(frmTopFrame, text ="Geeks4", fg ="green")
# b4_button.pack( side = tk.LEFT)
  
# b5_button = tk.Button(frmTopFrame, text ="Geeks5", fg ="green")
# b5_button.pack( side = tk.LEFT)


if __name__ == '__main__':
    # root = tk.Tk()
    # root.wm_title("This is my title")
    # AutoFill(root)
    # root.mainloop()
    config= Gc.GenerateConfig()
    if(config.Name==None):
        config.fnc_CreateDefaultFile();
    AutoFill().mainloop()


