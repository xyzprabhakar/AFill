from tkinter import RAISED, ttk
import tkinter as tk
from turtle import color
import fontawesome as fa
import os,json
import GenerateConfig as Gc
import frmImportData as ImpData
import frmAddTemplate as AddTmp
import frmDataReport as DataReport
import frmDashboard as Dash
import frmFillData as FillData
import frmSetting as setting
import _thread


class AutoFill(tk.Frame):
    config=None
    icon =None
    varMenu=None
    frmDashBoard,frmTemplate,frmFillData,frmImportData,frmReport,frmReport,frmSetting,frmChangePassword=None,None,None,None,None,None,None,None    
    
    frmChangePassword=None
    #Left Menu Items
    MenuItems=[{"name":"rdoDashBoard", "text":"Dashboard","icon":"images\icons\cil-moon.png", "ficon":fa.icons['palette']},
                {"name":"rdoTemplate", "text":"Template","icon":"images\icons\cil-moon.png", "ficon":fa.icons['file']},
                {"name":"rdoFillData", "text":"Fill Data","icon":"images\icons\cil-moon.png", "ficon":fa.icons['database']},
                {"name":"rdoImportData", "text":"Import Data","icon":"images\icons\cil-moon.png", "ficon":fa.icons['file-import']},
                {"name":"rdoReport", "text":"Report","icon":"images\icons\cil-moon.png", "ficon":fa.icons['chart-line']},
                {"name":"rdoSetting", "text":"Setting","icon":"images\icons\cil-moon.png", "ficon":fa.icons['wrench']},
                {"name":"rdoChangePassword", "text":"Change Password","icon":"images\icons\cil-moon.png", "ficon":fa.icons['user']}]

    def __init__(self,config,isapp=True, name='AutoFill'):
        tk.Frame.__init__(self)        
        self.config=config
        self.master.geometry("900x600")
        self.master.minsize(900,600)
        self.config.set_theme(None,self) 
        self.master.title("Auto Fill")
        self.master.iconbitmap(r"logoIcon.ico")
        self.pack(expand=tk.Y, fill=tk.BOTH)
        self.master["bd"]=3
        self.master["relief"]=tk.RAISED        
        self.master.unbind("<FocusIn>")             
        
        _thread.start_new_thread(self.intlizeform,())   

        

    def intlizeform(self):
        #self.master.overrideredirect(True)
        self.varMenu= tk.StringVar()
        self.varMenu.set("Dashboard")
        #self.isapp = isapp                        
        #self.varMenu =tk.StringVar()
        self._create_Frame()
        self._create_inner_content()
        #self.master.eval('tk::PlaceWindow . center')
        
    
    def _create_Frame(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.rowconfigure(2, weight=1)

        frmTopFrame = ttk.Frame(self,height=48,style="Topframe.TFrame")
        frmTopFrame.bind("<B1-Motion>",lambda e: self.move_app(e,self.master)) 
        frmTopFrame.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)        
        
        frmBottomFrame = tk.Frame(self)        
        frmBottomFrame.grid(row=1, column=0, sticky=tk.N+tk.W+tk.E+tk.S)

        frmStatusFrame = tk.Frame(self)        
        frmStatusFrame.grid(row=2, column=0, sticky=tk.W+tk.E+tk.S)

        btnClose = tk.Button(frmTopFrame, text = fa.icons['trash'],font= self.config.headerFonts ,command =lambda: self.master.destroy(), bg=self.config.COLOR_TOP_BACKGROUND,fg=self.config.COLOR_MENU_BACKGROUND,relief=tk.FLAT)
        btnClose.pack(side=tk.RIGHT, pady=7,padx=5)
        self.icon = tk.PhotoImage(file="logoIcon32.png")
        self.icon.subsample(1, 2)
        lblHeader1=ttk.Label(frmTopFrame,image=self.icon,style="Toplable.TLabel")        
        lblHeader1.pack(side=tk.LEFT, pady=7,padx=(10,2))
        lblHeader2=ttk.Label(frmTopFrame,text="Auto Fill", style="Toplable.TLabel")
        lblHeader2.pack(side=tk.LEFT, pady=7,padx=2)

        frmBottomFrame.columnconfigure(0, weight=1)
        frmBottomFrame.columnconfigure(1, weight=100)
        frmBottomFrame.rowconfigure(0, weight=1)
        

        self.frmLeftFrame = ttk.Frame(frmBottomFrame,width=200)   
        self.frmLeftFrame.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)
        #frmLeftFrame.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.NW, expand=tk.TRUE)
        
        frmContentFrame = tk.Frame(frmBottomFrame)   
        frmContentFrame.grid(row=0, column=1, sticky=tk.N+tk.W+tk.E+tk.S)
        #frmContentFrame.pack(side=tk.RIGHT, fill=tk.BOTH, anchor=tk.NW, expand=tk.TRUE)

        frmInnerContentFrame = ttk.Frame(frmContentFrame)
        frmInnerContentFrame.pack(side=tk.LEFT,fill=tk.BOTH,anchor=tk.NW ,pady = 20,padx=20,expand=tk.TRUE )
        frmInnerContentFrame.columnconfigure(0, weight=1)
        frmInnerContentFrame.rowconfigure(0, weight=1)
        frmInnerContentFrame.rowconfigure(1, weight=2)
        frmInnerContentFrame.rowconfigure(2, weight=1)
        frmInnerContentFrame.rowconfigure(3, weight=100)

        lblHeader= tk.Label(frmInnerContentFrame,textvariable=self.varMenu,font= self.config.headerFonts,bg=self.config.COLOR_MENU_BACKGROUND, padx=10)
        lblHeader.grid(row=0, column=0, sticky=tk.N+tk.W, pady=(5,0))
        
        separator = tk.Frame(frmInnerContentFrame, bg=self.config.COLOR_TOP_BACKGROUND, height=2, bd=0,pady=10)
        separator.grid(row=1, column=0, sticky=tk.E+tk.W)
        
        self.frmInnerDisplayContentFrame = tk.Frame(frmInnerContentFrame,bg=self.config.COLOR_MENU_BACKGROUND)
        self.frmInnerDisplayContentFrame.grid(row=3, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self._draw_menu(self.frmLeftFrame)
    
    def move_app(self,event,parent):
        parent.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    def _draw_menu(self,parent):        
        for thisdict in self.MenuItems:            
            button = tk.Radiobutton(parent, name= thisdict["name"], text =thisdict["ficon"] +" "+thisdict["text"] , variable = self.varMenu,	value = thisdict["text"],             
             indicator = 0, fg=self.config.COLOR_FOREGROUND, bg=self.config.COLOR_MENU_BACKGROUND, activeforeground="red" ,selectcolor=self.config.COLOR_BACKGROUND
             ,font=self.config.displayFont,
             borderwidth=0,
             anchor=tk.W,
             padx=10,
             command=lambda: self._create_inner_content(),
             relief=tk.RAISED 
            )
            #button.image=photo
            button.pack( fill=tk.X ,ipady = 8,ipadx=8)
            button.bind('<Enter>', self.on_enter_menu)
            button.bind('<Leave>', self.on_leave_menu)
    
    def on_enter_menu(self,event):
        event.widget['background'] = self.config.COLOR_BACKGROUND
        event.widget['foreground'] = self.config.COLOR_MENU_FOREGROUND
    def on_leave_menu(self,event):
        event.widget['background'] = self.config.COLOR_MENU_BACKGROUND
        event.widget['foreground'] = self.config.COLOR_FOREGROUND
    

    def _create_inner_content(self):        
        if(self.frmTemplate!=None):
            self.frmTemplate.pack_forget()        
        if(self.frmDashBoard!=None):
            self.frmDashBoard.pack_forget()
        if(self.frmFillData!=None):
            self.frmFillData.pack_forget()
        if(self.frmImportData!=None):
            self.frmImportData.pack_forget()
        if(self.frmReport!=None):
            self.frmReport.pack_forget()
        if(self.frmSetting!=None):
            self.frmSetting.pack_forget()

        if(self.varMenu.get()=="Dashboard"):            
            if(self.frmDashBoard==None):
                self.frmDashBoard=ttk.Frame(self.frmInnerDisplayContentFrame)
                self.frmDashBoard.pack(fill=tk.BOTH,expand=tk.TRUE)
                Dash.Dashboard(self.frmDashBoard,self.config)
            else:
                self.frmDashBoard.pack(fill=tk.BOTH,expand=tk.TRUE)
        elif(self.varMenu.get()=="Import Data"):
            if(self.frmImportData==None):
                self.frmImportData=ttk.Frame(self.frmInnerDisplayContentFrame)
                self.frmImportData.pack(fill=tk.BOTH,expand=tk.TRUE)
                ImpData.ImportData(self.frmImportData,self.config)
            else:
                self.frmImportData.pack(fill=tk.BOTH,expand=tk.TRUE)
        elif(self.varMenu.get()=="Fill Data"):
            if(self.frmFillData==None):
                self.frmFillData=ttk.Frame(self.frmInnerDisplayContentFrame)
                self.frmFillData.pack(fill=tk.BOTH,expand=tk.TRUE)
                FillData.FillData(self.frmFillData,self.config)
            else:
                self.frmFillData.pack(fill=tk.BOTH,expand=tk.TRUE)
        elif(self.varMenu.get()=="Template"):
            if(self.frmTemplate==None):
                self.frmTemplate=ttk.Frame(self.frmInnerDisplayContentFrame)
                self.frmTemplate.pack(fill=tk.BOTH,expand=tk.TRUE)
                AddTmp.AddTemplate(self.frmTemplate,self.config)
            else:
                self.frmTemplate.pack(fill=tk.BOTH,expand=tk.TRUE)
        elif(self.varMenu.get()=="Report"):
            if(self.frmReport==None):
                self.frmReport=ttk.Frame(self.frmInnerDisplayContentFrame)
                self.frmReport.pack(fill=tk.BOTH,expand=tk.TRUE)
                DataReport.DataReport(self.frmReport,self.config)
            else:
                self.frmReport.pack(fill=tk.BOTH,expand=tk.TRUE)
        elif(self.varMenu.get()=="Setting"):
            if(self.frmSetting==None):
                self.frmSetting=ttk.Frame(self.frmInnerDisplayContentFrame)
                self.frmSetting.pack(fill=tk.BOTH,expand=tk.TRUE)
                setting.Setting(self.frmSetting,self.config)
            else:
                self.frmSetting.pack(fill=tk.BOTH,expand=tk.TRUE)
            
            #self._create_Template(frmInnerDisplayContentFrame)


if __name__ == '__main__':
    # root = tk.Tk()
    # root.wm_title("This is my title")
    # AutoFill(root)
    # root.mainloop()
    config= Gc.GenerateConfig()
    if(config.Name==None):
        config.fnc_CreateDefaultFile()
    AutoFill(config).mainloop()