from tkinter import RAISED, ttk
import tkinter as tk
import fontawesome as fa
import os,json
import GenerateConfig as Gc


class AutoFill1(tk.Frame):
    config=None
    icon =None
    varMenu=None
    #Left Menu Items
    MenuItems=[{"name":"rdoDashBoard", "text":"Dashboard","icon":"images\icons\cil-moon.png", "ficon":fa.icons['palette']},
                {"name":"rdoTemplate", "text":"Template","icon":"images\icons\cil-moon.png", "ficon":fa.icons['file']},
                {"name":"rdoDataTemplate", "text":"Data Template","icon":"images\icons\cil-moon.png", "ficon":fa.icons['database']},
                {"name":"rdoImportData", "text":"Import Data","icon":"images\icons\cil-moon.png", "ficon":fa.icons['file-import']},
                {"name":"rdoReport", "text":"Report","icon":"images\icons\cil-moon.png", "ficon":fa.icons['chart-line']},
                {"name":"rdoSetting", "text":"Setting","icon":"images\icons\cil-moon.png", "ficon":fa.icons['wrench']},
                {"name":"rdoChangePassword", "text":"Change Password","icon":"images\icons\cil-moon.png", "ficon":fa.icons['user']}]

    def __init__(self,config,isapp=True, name='AutoFill'):
        tk.Frame.__init__(self)
        self.master.overrideredirect(True)
        
        self.config=config
        self.config.set_theme(None,self)
        self.master.iconbitmap(r"logoIcon.ico")
        self.master.geometry("900x600")
        self.master.minsize(900,600)
        self.pack(expand=tk.Y, fill=tk.BOTH)
        self.master["bd"]=3
        self.master["relief"]=tk.RAISED
        self.master.title('Auto Fill')        
        self.master.unbind("<FocusIn>")
        

        self.varMenu= tk.StringVar()
        #self.isapp = isapp                        
        #self.varMenu =tk.StringVar()
        self._create_Frame()
    
    def _create_Frame(self):
        frmTopFrame = ttk.Frame(self,height=48,style="Topframe.TFrame")
        frmTopFrame.bind("<B1-Motion>",lambda e: self.move_app(e,self.master)) 
        frmTopFrame.pack(side=tk.TOP, fill=tk.X, anchor=tk.NW)
        btnClose = tk.Button(frmTopFrame, text = fa.icons['trash'],font= self.config.headerFonts ,command =self.master.destroy, bg=self.config.COLOR_TOP_BACKGROUND,fg=self.config.COLOR_MENU_BACKGROUND,relief=tk.FLAT)
        btnClose.pack(side=tk.RIGHT, pady=7,padx=5)
        self.icon = tk.PhotoImage(file="logoIcon32.png")
        self.icon.subsample(1, 2)
        lblHeader1=ttk.Label(frmTopFrame,image=self.icon,style="Toplable.TLabel")        
        lblHeader1.pack(side=tk.LEFT, pady=7,padx=(10,2))
        lblHeader2=ttk.Label(frmTopFrame,text="Auto Fill", style="Toplable.TLabel")
        lblHeader2.pack(side=tk.LEFT, pady=7,padx=2)
        frmLeftFrame = ttk.Frame(self,width=200)   
        frmLeftFrame.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.NW, expand=tk.TRUE)
        self._draw_menu(frmLeftFrame,None)
    
    def move_app(self,event,parent):
        parent.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    def _draw_menu(self,parent,container):        
        for thisdict in self.MenuItems:            
            button = ttk.Radiobutton(parent, name= thisdict["name"], text =thisdict["ficon"] +" "+thisdict["text"] , variable = self.varMenu,	value = thisdict["text"],
             #indicator = 0,
             style="Menu.TRadiobutton", 
             #borderwidth=0,
             #anchor=tk.W,
             #padx=10,
             command=lambda: self._create_inner_content(container)             
            )
            #button.image=photo
            button.pack( fill=tk.X ,ipady = 8,ipadx=8)
            button.bind('<Enter>', self.on_enter_menu)
            button.bind('<Leave>', self.on_leave_menu)
    def on_enter_menu(self,event):
        print ('hello')
    def on_leave_menu(self,event):
        print ('bye')

if __name__ == '__main__':
    # root = tk.Tk()
    # root.wm_title("This is my title")
    # AutoFill(root)
    # root.mainloop()
    config= Gc.GenerateConfig()
    if(config.Name==None):
        config.fnc_CreateDefaultFile();    
    AutoFill1(config).mainloop()