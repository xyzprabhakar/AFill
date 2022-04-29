import fontawesome as fa
from multiprocessing.sharedctypes import Value
from tkinter import font
#import PyPDF2 as pdf
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
from io import StringIO
import os

import tabula 
#from tabula import read_pdf
#from tabulate import tabulate

import io
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import ttk
import GenerateConfig as Gc
import json

# import webdriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



class FillData(ttk.Frame):
    config=None
    ContainerFrame=None  
    varCurrentTemplate,varCurrentDataFileName  = None,None
    varAllTemlateName,varAllTemlate,varAllJsonData,varAllJsonFileName=[],[],[],[]       
    frmLeftPanel,frmRightPanel,ddlTemplateName,ddlFileName=None,None,None,None
    varCurrentData=None
    driver=None


    def __init__(self,Container,config):  
        self.config=config   
        self.ContainerFrame=Container
        self.displayFont = ( "Verdana", 10)       
        self.varCurrentTemplate,self.varCurrentDataFileName = tk.StringVar(), tk.StringVar()        
        self.LoadAllJsonData()
        self.fncCreateItems()        
    
    def LoadAllJsonData(self):
        if not os.path.exists(self.config.FilePath):
            os.makedirs(self.config.FilePath)
        if os.path.isfile(os.path.join(self.config.FilePath, self.config.DataFileName)) is False:
            with io.open(os.path.join(self.config.FilePath, self.config.DataFileName), 'w') as fp:
                print('Empty File Created')
        else:
            with io.open(os.path.join(self.config.FilePath, self.config.DataFileName)) as fp:
                self.varAllJsonData = json.load(fp)
                self.varAllJsonFileName.clear()
                for x in self.varAllJsonData:
                    self.varAllJsonFileName.append(x["FileName"])
                
        if os.path.isfile(os.path.join(self.config.FilePath, self.config.TemplateFileName)) is False:
            with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName), 'w') as fp:
                print('Empty File Created')
        else:
            with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName)) as fp:
                self.varAllTemlate = json.load(fp)
                self.varAllTemlateName.clear()
                for x in self.varAllTemlate:
                    self.varAllTemlateName.append(x["templateName"])
        self.AppendDataToDropDown()        
    
    def AppendDataToDropDown(self):
        if(self.ddlFileName != None):
            for x in self.varAllJsonFileName:
                if x not in self.ddlFileName['values']:
                    self.ddlFileName['values'] = (*self.ddlFileName['values'], x)
        if(self.ddlTemplateName != None):
            for x in self.varAllTemlateName:
                if x not in self.ddlTemplateName['values']:
                    self.ddlTemplateName['values'] = (*self.ddlTemplateName['values'], x)
    
    def load_data(self):
        self.varCurrentData=self.varAllJsonData[0]
        self.varCurrentTemplate=self.varAllTemlate[0]
        #print(self.varCurrentData)
        self.children["txtApplicantData"].delete('1.0', tk.END)
        self.children["txtApplicantData"].insert('1.0', str(self.varCurrentData) )

    
    def fill_data(self):
        timeout=30
        if(self.driver is None):
            self.driver = webdriver.Firefox()
            self.driver.get(self.varCurrentTemplate["url"])
        
        element=None        
        controlId=None
        IoName=None
        controlValue=None
        actiontype=None
        finalValue=None
        actionOn=None
        # get google.co.in
        for action in self.varCurrentTemplate["actions"]:            
            element=None
            actiontype=action["action_type"]
            IoName=action["io_name"]
            controlValue=action["control_value"]
            
            controlId=action["control"]
            actionOn=action["action_on"]            
            if(len(IoName)>0):
                finalValue=self.varCurrentData["applicantData"][action["io_name"].strip().replace(' ', '_')]
            if(controlValue != None and len(str(controlValue))>0):
                finalValue=str(controlValue)

            if( actiontype=="Wait"):
                timeout=int(controlValue)
                self.driver.implicitly_wait(timeout) 
            if(actiontype=="Fill Input" or actiontype=="Select Option" ):
                if(actionOn=="ByName"):
                    element=self.driver.find_element(By.NAME,controlId)
                elif(actionOn=="ById") :
                    element=self.driver.find_element(By.ID ,controlId)
                elif(actionOn=="ByXpath") :
                    element=self.driver.find_element(By.XPATH ,controlId)
                if(element != None):
                    if(actiontype=="Fill Input"):
                        element.send_keys(finalValue)
                    elif(actiontype=="Select Option"):
                        select = Select(element)
                        select.select_by_value(finalValue)

            if(actiontype=="Check Checkbox"):
                if(actionOn=="ByName"):
                    if(len(finalValue)>0 ):
                        element=self.driver.find_element(By.XPATH,f"//input[@name='{controlId}'][@value='{finalValue}']")
                    else:
                        element=self.driver.find_element(By.XPATH,f"//input[@name='{controlId}']")
                elif(actionOn=="ById") :
                    if(len(finalValue)>0 ):
                        element=self.driver.find_element(By.XPATH,f"//input[@id='{controlId}'][@value='{finalValue}']")
                    else:
                        element=self.driver.find_element(By.XPATH,f"//input[@id='{controlId}']")
                elif(actionOn=="ByXpath") :
                    if(len(finalValue)>0 ):
                        element=self.driver.find_element(By.XPATH,controlId)
                    else:
                        element=self.driver.find_element(By.XPATH,controlId)
                if(element != None):
                    #self.driver.execute_script("arguments[0].scrollIntoView();",element )
                    #self.driver.execute_script("arguments[0].click();",element )
                    
                    action=ActionChains(self.driver)
                    action.move_to_element(element)
                    action.click(on_element = element)
                    #element.click()
                    action.perform()
            
            if(actiontype=="Button Click" or actiontype=="Hover"):
                if(actionOn=="ByName"):
                    element=self.driver.find_element(By.NAME,controlId)
                elif(actionOn=="ById") :
                    element=self.driver.find_element(By.ID ,controlId)
                elif(actionOn=="ByXpath") :
                    element=self.driver.find_element(By.XPATH,controlId)

                if(element != None):
                    action=ActionChains(self.driver)
                    action.move_to_element(element)
                    if(actiontype=="Button Click"):
                        action.click(on_element = element)
                    #element.click()
                    action.perform()
        try:
            print (1)
        except:
            print ('error occured')
        #finally:

            #self.driver.quit()

    def Open_Browser(self):
        if(self.driver is None):
            self.driver = webdriver.Firefox()
            self.driver.get(self.varCurrentTemplate["url"])
        
        

    def reset_data(self):
        for x in self.config.IO_Name:
            self.children["txtApplicant"+ x.strip().replace(' ', '_')].delete(0,"end")
            if(self.varApplicantType.get()=="Co Applicant"):                
                self.children["txtCoApplicant"+ x.strip().replace(' ', '_')].delete(0,"end")
        try:
            self.varId.set(int(self.varId.get()) +1)
        except:
            print('Id is not a number')
                

    def hide_unhide_applicant(self,event):
        yaxis= self.varStarttingPoint
        if(self.varApplicantType.get()=="Single"):
            for x in self.config.IO_Name:
               self.children["txtCoApplicant"+ x.strip().replace(' ', '_')].place_forget() 
        else:
            for x in self.config.IO_Name:
               self.children["txtCoApplicant"+ x.strip().replace(' ', '_')].place(x = 400,y = (10+yaxis), anchor=tk.NW)
               yaxis=yaxis+40

        
    


    def fncCreateItems(self):
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
        
        frmbtn1 = ttk.Frame(self.frmHeader,name="frmTreeviewhandler2")        
        frmbtn1.grid(row=3,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnReffreshData = tk.Button ( frmbtn1,name="btnReffreshData", text =fa.icons['sync'], relief='groove', width=3,font=self.displayFont,bg=self.config.COLOR_MENU_BACKGROUND,fg=self.config.COLOR_TOP_BACKGROUND,  command = lambda :self.LoadAllJsonData() )                
        btnReffreshData.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        
        frmBody.columnconfigure(0, weight=1)
        frmBody.columnconfigure(1, weight=100)  
        frmBody.rowconfigure(0, weight=100)  
        self.frmLeftPanel,self.frmRightPanel= ttk.Frame(frmBody,width=300),ttk.Frame(frmBody)
        self.frmLeftPanel.grid(row=0,column=0,sticky=tk.N+tk.S+tk.W+tk.E)
        self.frmRightPanel.grid(row=0,column=0,sticky=tk.N+tk.S+tk.W+tk.E)
        self.frmLeftPanel.columnconfigure(0, weight=1)
        self.frmLeftPanel.columnconfigure(1, weight=100)
        self.frmLeftPanel.rowconfigure(0, weight=1)
        self.frmLeftPanel.rowconfigure(1, weight=1)
        self.frmLeftPanel.rowconfigure(2, weight=1)
        self.frmLeftPanel.rowconfigure(3, weight=1)
        self.frmLeftPanel.rowconfigure(4, weight=1)
        self.frmLeftPanel.rowconfigure(5, weight=1)        
        self.frmLeftPanel.rowconfigure(6, weight=100)        
        ttk.Label(self.frmLeftPanel,text="Template").grid(row=0,column=0,sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(self.frmLeftPanel,textvariable = self.varCurrentTemplate,values=self.varAllTemlateName).grid(row=0,column=1,sticky=tk.N+tk.S+tk.W)
        ttk.Label(self.frmLeftPanel,text="File Name").grid(row=1,column=0,sticky=tk.N+tk.S+tk.E)
        ttk.Combobox(self.frmLeftPanel,textvariable = self.varCurrentTemplate,values=self.varAllTemlateName).grid(row=1,column=1,sticky=tk.N+tk.S+tk.W)
        ttk.Button ( self.frmLeftPanel, text ="Open Browser", width=20, command =lambda: self.Open_Browser()).grid(row=2,column = 0 , sticky=tk.N+tk.W)
        ttk.Button ( self.frmLeftPanel, text ="Load Data", width=20, command =lambda: self.load_data()).grid(row=2,column = 1 , sticky=tk.N+tk.W)
        ttk.Frame(self.frmLeftPanel, height=10).grid(row=3, column=0,columnspan=2, sticky=tk.E+tk.W)
        ttk.Frame(self.frmLeftPanel, style="Separator.TFrame", height=1).grid(row=4, column=0,columnspan=2, sticky=tk.E+tk.W)
        ttk.Frame(self.frmLeftPanel, height=10).grid(row=5, column=0,columnspan=2, sticky=tk.E+tk.W)
        frmInnerContentFrame1 = ttk.Frame(self.frmLeftPanel)
        frmInnerContentFrame1.grid(row=6, column=0,columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)        
        # scrollbar_y = ttk.Scrollbar(frmInnerContentFrame1, orient=tk.VERTICAL, command=self.frm_Applicant1Canvas.yview)
        #     scrollbar_x_Applicant1 = ttk.Scrollbar(self.frm_Applicant1Parent, orient=tk.HORIZONTAL, command=self.frm_Applicant1Canvas.xview)
        #     scrollbar_y_Applicant1.pack(side=tk.RIGHT, fill="y")
        #     scrollbar_x_Applicant1.pack(side=tk.BOTTOM, fill="x")
        #     self.frm_Applicant1Canvas.pack(expand=tk.TRUE, fill="both",pady=(5,3), padx=(10,10))



        # self.varApplicantType.set("")
        # self.varTemplateType.set("")
        
        # yaxis=0
        # tk.Label(self,text = "Id",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10), anchor=tk.NW)
        # tk.Entry(self,bg=self.config.COLOR_BACKGROUND,name="txt__Id",textvariable = self.varId ,width = 25,font=self.config.displayFont).place(x = 170,y = (10), anchor=tk.NW)	
        # yaxis=40
        # tk.Label(self,text = "Template",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
        # combostyle = ttk.Style()
        # combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'fieldbackground': self.config.COLOR_BACKGROUND,'background': self.config.COLOR_BACKGROUND}}})
        
        # combostyle.theme_use('combostyle') 
        # cmbTemplateType = ttk.Combobox(self, width = 23, textvariable =self.varTemplateType,font=self.config.displayFont)
        # # Adding combobox drop down list
        # cmbTemplateType['values'] = self.varAllTemlateName
        # cmbTemplateType.place(x = 170,y = (10+yaxis), anchor=tk.NW)	

        # yaxis=yaxis+40
        # tk.Label(self,text = "Data",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
        # tk.Text(self,name="txtApplicantData",bg=self.config.COLOR_BACKGROUND, width = 25, height=5,font=self.config.displayFont).place(x = 170,y = (10+yaxis), anchor=tk.NW)
        
        # btnLoadData = tk.Button ( self, text ="Get Data",width=10, relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND,  command =self.load_data )
        # btnOpenTemplate = tk.Button ( self, text ="Open Template", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command = self.Open_Template)
        # btnFillData = tk.Button ( self, text ="Fill", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command = self.fill_data)
        
        # btnLoadData.bind('<Enter>', self.config.on_enter_button)
        # btnLoadData.bind('<Leave>', self.config.on_leave_button)
        # btnFillData.bind('<Enter>', self.config.on_enter_button)
        # btnFillData.bind('<Leave>', self.config.on_leave_button)
        # btnOpenTemplate.bind('<Enter>', self.config.on_enter_button)
        # btnOpenTemplate.bind('<Leave>', self.config.on_leave_button)
        
        # btnLoadData.place(x = 400,y = 10, anchor=tk.NW)
        # btnOpenTemplate.place(x = 400,y = 50, anchor=tk.NW)
        # btnFillData.place(x = 400,y = 90, anchor=tk.NW)
        


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
    FillData(myframe,config)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

        

