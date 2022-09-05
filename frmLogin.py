import fontawesome as fa
from multiprocessing.sharedctypes import Value
from tkinter import TOP, font
from io import StringIO
import os
from cryptography.fernet import Fernet
import tabula 
#from tabula import read_pdf
#from tabulate import tabulate  SakshemIT@1234
import GenerateConfig as Gc
import io
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import ttk,messagebox

import json
import main as AFill
import hashlib



class Login(ttk.Frame):
    config=None    
    logoicon=None
    varName,varContactNo,varEmail=None,None,None
    varExistingUserName,varExistingPassword,varUserName,varPassword=None,None,None,None
    def __init__(self,Container,config):  
        self.config=config   
        self.ContainerFrame=Container
        self.displayFont = ( "Verdana", 10)       
        self.varName,self.varContactNo,self.varEmail = tk.StringVar(), tk.StringVar(), tk.StringVar()        
        self.varExistingUserName,self.varExistingPassword,self.varUserName,self.varPassword= tk.StringVar(), tk.StringVar(), tk.StringVar() , tk.StringVar()                
        self.LoadData()
        self.fncCreateItems()    
        self.txtLogin.focus_set()    

    def LoadData(self):        
        self.varName.set(self.config.Name)
        self.varContactNo.set(self.config.ContactNo)
        self.varEmail.set(self.config.Email)
        self.varExistingUserName.set(self.config.UserName)
        self.varExistingPassword.set(self.config.Password)        
        self.logoicon = tk.PhotoImage(file="logoIcon64.png")
        #self.logoicon.subsample(10, 10)         

    def Login_click(self):        
        a_string = self.varPassword.get() 
        hashed_string = hashlib.sha256(a_string.encode('utf-8')).hexdigest()        
        #print(self.varExistingPassword.get()) 
        if(self.varExistingPassword.get()==hashed_string
        and self.varUserName.get()==self.varExistingUserName.get()):
            root.destroy()
            AFill.AutoFill(self.config).mainloop()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")


    def fncCreateItems(self):
        frmBody  = ttk.Frame(self.ContainerFrame)        
        frmBody.grid(row=0,column = 0,  sticky=tk.N+tk.S+tk.W+tk.E)
        frmBody.columnconfigure(0, weight=50) 
        frmBody.columnconfigure(1, weight=50) 
        frmBody.rowconfigure(0, weight=100) 
        frmLeftFrame  = ttk.Frame(frmBody,style="Separator.TFrame",height=400,width=300)
        frmLeftFrame.grid(row=0,column = 0,  sticky=tk.N+tk.S+tk.W+tk.E)
        frmRightFrame  = ttk.Frame(frmBody,height=400,width=300)
        frmRightFrame.grid(row=0,column = 1,  sticky=tk.N+tk.S+tk.W+tk.E)

        frmLeftFrame1 = ttk.Frame(frmLeftFrame,style="Separator.TFrame")
        frmLeftFrame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)       
        lblHeader1=ttk.Label(frmLeftFrame1,image=self.logoicon,style="Toplable.TLabel")                
        lblHeader1.pack(side=tk.TOP, pady=7,padx=2)
        lblHeader2=ttk.Label(frmLeftFrame1,text="Auto Fill", style="Toplable.TLabel")
        lblHeader2.pack(side=tk.BOTTOM, pady=7,padx=2)
        frmRightFrame1  = ttk.Frame(frmRightFrame)
        frmRightFrame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        frmRightFrame1.columnconfigure(0, weight=100) 
        frmRightFrame1.rowconfigure(0, weight=1)        
        frmRightFrame1.rowconfigure(1, weight=1)        
        frmRightFrame1.rowconfigure(2, weight=1)        
        frmRightFrame1.rowconfigure(3, weight=1)        
        frmRightFrame1.rowconfigure(4, weight=1)                        
        ttk.Label(frmRightFrame1,text="User Name",style="Login.TLabel").grid(row=0,column=0,sticky=tk.W+tk.N+tk.S, padx=(10,10),pady=(8,3))
        self.txtLogin=ttk.Entry(frmRightFrame1,textvariable=self.varUserName,width=24,font=("Verdana",11) )
        self.txtLogin.grid(row=1,column=0,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Label(frmRightFrame1,text="Password",style="Login.TLabel").grid(row=2,column=0,sticky=tk.W+tk.N+tk.S, padx=(10,10),pady=(8,3))
        ttk.Entry(frmRightFrame1,textvariable=self.varPassword,show='*',width=24, font=("Verdana",11)).grid(row=3,column=0,sticky=tk.E+tk.N+tk.S, padx=(10,10),pady=(8,3))
        frmbtn2 = ttk.Frame(frmRightFrame1)        
        frmbtn2.grid(row=4,column = 0,pady=(15,3),padx=(10,10) )
        ttk.Button (frmbtn2, text ="Login", width=10, command =lambda: self.Login_click()).grid(row=0,column = 0,padx=(5,5) )        
        if(self.varUserName==""):
            ttk.Button ( frmbtn2, text ="Register", width=10, command =lambda: self.Register_click()).grid(row=0,column = 1 ,padx=(5,5))
        


# if __name__ == '__main__':
#     config= Gc.GenerateConfig()         
#     root = tk.Tk()    
#     sizex = 600
#     sizey = 400
#     posx  = 100
#     posy  = 100
#     root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
#     config.set_theme(None,root)
#     myframe=ttk.Frame(root,relief=tk.GROOVE,width=500,height=600)
#     myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
#     Login(myframe,config)
#     root.title("Login")
#     root.iconbitmap(r"logoIcon.ico")
#     root.eval('tk::PlaceWindow . center')
#     root.mainloop()
config= Gc.GenerateConfig()         
root = tk.Tk()    
sizex = 600
sizey = 400
posx  = 1
posy  = 1
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
config.set_theme(None,root)
myframe=ttk.Frame(root,relief=tk.GROOVE,width=500,height=600)
myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
Login(myframe,config)
root.title("Login")
root.iconbitmap(r"logoIcon.ico")
root.eval('tk::PlaceWindow . center')
root.mainloop()

        

