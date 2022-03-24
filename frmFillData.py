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
from tkinter import RAISED, ttk
import GenerateConfig as Gc
import json

# import webdriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



class FillData(ttk.Frame):
    config=None
    varTemplateType = None
    varApplicantType = None
    varStarttingPoint=0
    varAllTemlateName=[]
    varAllTemlate=[]
    varAllJsonData=[]
    varCurrentData=None
    varCurrentTemplate=None
    varId=None
    driver=None

    def __init__(self,config):
        tk.Frame.__init__(self)        
        self.config=config
        self["background"]=self.config.COLOR_MENU_BACKGROUND
        self["height"]=300
        self["width"]=560
        self.varTemplateType = tk.StringVar()
        self.varApplicantType = tk.StringVar()
        self.varId=tk.StringVar()
        self.pack(expand=True, fill=tk.BOTH)        
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
                if(len(self.varAllJsonData)>0):
                    last_element = self.varAllJsonData[-1]
                    try:
                        self.varId.set(int(last_element["id"])+1) 
                    except:
                        print('lat Id is not a number')
        if os.path.isfile(os.path.join(self.config.FilePath, self.config.TemplateFileName)) is False:
            with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName), 'w') as fp:
                print('Empty File Created')
        else:
            with io.open(os.path.join(self.config.FilePath, self.config.TemplateFileName)) as fp:
                self.varAllTemlate = json.load(fp)
                for x in self.varAllTemlate:
                    self.varAllTemlateName.append(x["templateName"])
                
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
            
            controlId=action["control_id"]
            actionOn=action["action_on"]            
            if(len(IoName)>0):
                finalValue=self.varCurrentData["applicantData"][action["io_name"].strip().replace(' ', '_')]
            if(len(controlValue)>0):
                finalValue=controlValue

            if(actiontype=="Wait"):
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

    def Open_Template(self):
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
        self.varApplicantType.set("")
        self.varTemplateType.set("")
        
        yaxis=0
        tk.Label(self,text = "Id",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10), anchor=tk.NW)
        tk.Entry(self,bg=self.config.COLOR_BACKGROUND,name="txt__Id",textvariable = self.varId ,width = 25,font=self.config.displayFont).place(x = 170,y = (10), anchor=tk.NW)	
        yaxis=40
        tk.Label(self,text = "Template",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'fieldbackground': self.config.COLOR_BACKGROUND,'background': self.config.COLOR_BACKGROUND}}})
        
        combostyle.theme_use('combostyle') 
        cmbTemplateType = ttk.Combobox(self, width = 23, textvariable =self.varTemplateType,font=self.config.displayFont)
        # Adding combobox drop down list
        cmbTemplateType['values'] = self.varAllTemlateName
        cmbTemplateType.place(x = 170,y = (10+yaxis), anchor=tk.NW)	

        yaxis=yaxis+40
        tk.Label(self,text = "Data",font=self.config.displayFont, bg=self.config.COLOR_MENU_BACKGROUND).place(x = 40,y = (10+yaxis), anchor=tk.NW)
        tk.Text(self,name="txtApplicantData",bg=self.config.COLOR_BACKGROUND, width = 25, height=5,font=self.config.displayFont).place(x = 170,y = (10+yaxis), anchor=tk.NW)
        
        btnLoadData = tk.Button ( self, text ="Get Data",width=10, relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND,  command =self.load_data )
        btnOpenTemplate = tk.Button ( self, text ="Open Template", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command = self.Open_Template)
        btnFillData = tk.Button ( self, text ="Fill", width=10,relief='flat', font=self.config.displayFont,fg=self.config.COLOR_MENU_BACKGROUND,bg=self.config.COLOR_TOP_BACKGROUND, command = self.fill_data)
        
        btnLoadData.bind('<Enter>', self.config.on_enter_button)
        btnLoadData.bind('<Leave>', self.config.on_leave_button)
        btnFillData.bind('<Enter>', self.config.on_enter_button)
        btnFillData.bind('<Leave>', self.config.on_leave_button)
        btnOpenTemplate.bind('<Enter>', self.config.on_enter_button)
        btnOpenTemplate.bind('<Leave>', self.config.on_leave_button)
        
        btnLoadData.place(x = 400,y = 10, anchor=tk.NW)
        btnOpenTemplate.place(x = 400,y = 50, anchor=tk.NW)
        btnFillData.place(x = 400,y = 90, anchor=tk.NW)
        

if __name__ == '__main__':
    config= Gc.GenerateConfig()
    FillData(config).mainloop()
        

