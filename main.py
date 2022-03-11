# import tkinter module
#from tkinter import  * 
#from tkinter.ttk import *
from cgitb import grey
from pickle import TRUE
from tkinter import ttk
import tkinter as tk
import fontawesome as fa
import os

class AutoFill(tk.Frame):
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
        self.master.title('Auto Fill')
        self.isapp = isapp
        self.varMenu =tk.StringVar()
        self._create_widgets()
        

    def _create_widgets(self):
        self._create_Master()

    def _create_Master(self):
        frmTopFrame = tk.Frame(self,height=48,width=768,bg=self.COLOR_TOP_BACKGROUND)
        frmMainFrame = tk.Frame(self,height=450,width=768,bg="grey")
        frmLeftFrame = tk.Frame(frmMainFrame,height=450,width=200,bg=self.COLOR_MENU_BACKGROUND)
        frmContentFrame = tk.Frame(frmMainFrame,height=450,width=514,bg=self.COLOR_BACKGROUND)
        #statusbar = tk.Label(self, text="Status", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        
        

        frmTopFrame.pack(side=tk.TOP, fill=tk.X)        
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

    def _create_inner_content(self,parent):
        headerFonts = ("Verdana", 15, "bold")
        if ("frmInnerContentFrame" in parent.children.keys()) :
            parent.children["frmInnerContentFrame"].pack_forget()
        frmInnerContentFrame = tk.Frame(parent,name="frmInnerContentFrame",height=400 ,width=490,bg=self.COLOR_MENU_BACKGROUND)
        frmInnerContentFrame.pack(fill=tk.BOTH ,pady = 20,padx=20,expand=True)
        frmInnerContentFrame.columnconfigure(0, weight=1)
        frmInnerContentFrame.rowconfigure(0, weight=1)
        frmInnerContentFrame.rowconfigure(1, weight=1)
        frmInnerContentFrame.rowconfigure(2, weight=100)

        lblHeader= tk.Label(frmInnerContentFrame,text=self.varMenu.get(),font= headerFonts,bg=self.COLOR_MENU_BACKGROUND, padx=10)
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
        displayFont = ( "Verdana", 10)        
        frmHeader = tk.Frame(parent,height=100 ,width=460,bg=self.COLOR_MENU_BACKGROUND)
        frmBody = tk.Frame(parent,height=300 ,width=460,bg=self.COLOR_MENU_BACKGROUND)
        lblTemplateName = tk.Label(frmHeader,text = "Template Name",font=displayFont, bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 10, anchor=tk.NW)
        lblTemplateUrl = tk.Label(frmHeader,text = "Url" ,font=displayFont,bg=self.COLOR_MENU_BACKGROUND).place(x = 40,y = 50, anchor=tk.NW)
        txtTemplateName = tk.Entry(frmHeader,name="txtTemplateName",bg=self.COLOR_BACKGROUND, width = 30,font=displayFont).place(x = 200,y = 10, anchor=tk.NW)	
        txtUrl =tk.Entry(frmHeader,name="txtUrl", width = 30,bg=self.COLOR_BACKGROUND,font=displayFont).place(x = 200,y = 50, anchor=tk.NW)
        treev = ttk.Treeview(frmBody, selectmode ='browse')
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








# creating main tkinter window/toplevel
#master = tk.Tk()
#master.geometry("768x480")
#master.config(bg="grey")


# b4_button = tk.Button(frmTopFrame, text ="Geeks4", fg ="green")
# b4_button.pack( side = tk.LEFT)
  
# b5_button = tk.Button(frmTopFrame, text ="Geeks5", fg ="green")
# b5_button.pack( side = tk.LEFT)


if __name__ == '__main__':
    AutoFill().mainloop()

