from curses import keyname
from typing import Counter
import fontawesome as fa
from multiprocessing.sharedctypes import Value
from tkinter import TOP, Widget,  font
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
from tkinter import ttk,messagebox
import GenerateConfig as Gc
import json

# import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from choosen import Chosen
from datetime import datetime
from dateutil.relativedelta import relativedelta

class FillData(ttk.Frame):
    config=None
    frm_Applicant1Canvas,ContainerFrame,IsShrink=None ,None ,False
    varCurrentTemplateName,varCurrentDataFileName,varCurrentTab  = None,None,None
    varAllTemlateName,varAllTemlate,varAllJsonData,varAllJsonFileName,varAllWrapperData=[],[],[],[],[]
    frmLeftPanel,frmRightPanel,ddlTemplateName,ddlFileName=None,None,None,None
    varCurrentData,varCurrentTemplateData=None,None
    driver=None
    FindIndex=-1


    def __init__(self,Container,config):  
        self.config=config   
        self.ContainerFrame=Container
        self.displayFont = ( "Verdana", 10)       
        self.varCurrentTemplateName,self.varCurrentDataFileName,self.varCurrentTab = tk.StringVar(), tk.StringVar() , tk.StringVar()
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

        if os.path.isfile(os.path.join(self.config.FilePath, self.config.WrapperFileName)) is False:
                with io.open(os.path.join(self.config.FilePath, self.config.WrapperFileName), 'w') as fp:
                    print('Empty File Created')
        else:
            with io.open(os.path.join(self.config.FilePath, self.config.WrapperFileName)) as fp:                    
                tempData= json.load(fp)
                if(self.checkKey(tempData,"allData")):
                    self.varAllWrapperData = tempData["allData"]
           
    
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
        self.clear_frame(self.frmInnerContentFrame1)
        if(self.varCurrentDataFileName.get()==""):
            messagebox.showerror("Required", "Please select filename")
            return
        if(self.varCurrentTemplateName.get()==""):
            messagebox.showerror("Required", "Please select template")
            return
        if(len(self.varAllTemlate)==0):
            messagebox.showerror("Required", "could not find any template")
            return
        FoundTemplateName=False
        for templ in  self.varAllTemlate:            
            if templ["templateName"]==self.varCurrentTemplateName.get():
                FoundTemplateName=True
                self.varCurrentTemplateData=templ
        if(not FoundTemplateName):
            messagebox.showerror("Required", "Invalid template name")
            return
        
        self.frm_Applicant1Canvas = tk.Canvas(self.frmInnerContentFrame1, bg=  self.config.COLOR_MENU_BACKGROUND,highlightthickness=0, relief='ridge')
        scrollbar_y = ttk.Scrollbar(self.frmInnerContentFrame1, orient=tk.VERTICAL, command=self.frm_Applicant1Canvas.yview)        
        scrollbar_y.pack(side=tk.RIGHT, fill="y")        
        scrollbar_x = ttk.Scrollbar(self.frmInnerContentFrame1, orient=tk.HORIZONTAL, command=self.frm_Applicant1Canvas.xview)        
        scrollbar_x.pack(side=tk.BOTTOM, fill="x")        
        self.frm_Applicant1Canvas.pack(expand=tk.TRUE, fill="both")
        self.frm_Applicant1 = ttk.Frame(self.frm_Applicant1Canvas,border=1)            
        

        if not os.path.exists(self.config.FilePath):
            os.makedirs(self.config.FilePath)
        if os.path.isfile(os.path.join(self.config.FilePath, self.varCurrentDataFileName.get()+".json")) is False:
            with io.open(os.path.join(self.config.FilePath, self.varCurrentDataFileName.get()+".json"), 'w') as fp:
                print('Empty File Created')
        else:
            with io.open(os.path.join(self.config.FilePath, self.varCurrentDataFileName.get()+".json")) as fp:
                self.varCurrentData=None
                self.varCurrentData = json.load(fp)                   
                self.txtData.delete('1.0', tk.END)    
                self.txtData.insert(tk.END,self.varCurrentData)
        if (self.checkKey(self.varCurrentTemplateData,"sections")):
            for sectCounter, sect in enumerate(self.varCurrentTemplateData["sections"]) :     
                if (self.checkKey(sect,"sectionType")):                    
                    if (self.checkKey(sect,"sectionCategory")):
                        sectioncounter =sect["sectionCategory"]
                        for ApplicantId,ApplicantData in enumerate(self.varCurrentData) :
                            if(sectCounter==0):
                                ttk.Label(self.frm_Applicant1,text="Applicant "+str(ApplicantId +1)).grid(row=sectCounter,column=ApplicantId,padx=(2,2))
                            if (self.checkKey(ApplicantData,sectioncounter)):                                                                    
                                tempFrame=ttk.Frame(self.frm_Applicant1)
                                tempFrame.grid(row=sectCounter+1,column=ApplicantId,padx=(2,2))
                                gridcounter=0
                                if(sect["sectionType"]=="Multiple"):
                                    datacounter=len(ApplicantData[sectioncounter])                                         
                                    for i in range(0,datacounter):
                                        ttk.Button (tempFrame, text =sect["sectionName"]+ " "+str(i+1) , command =lambda sectionName=sect["sectionName"],aplId=ApplicantId,i=i : self.fill_data(sectionName,i,aplId)).grid(row=gridcounter+i,column=ApplicantId,pady=(8,3),padx=(2,2))
                                else:                    
                                    ttk.Button(tempFrame, text =sect["sectionName"] ,  command =lambda sectionName=sect["sectionName"],aplId=ApplicantId: self.fill_data(sectionName,0,aplId)).grid(row=gridcounter,column=ApplicantId,pady=(8,3),padx=(2,2))
                                gridcounter=gridcounter+1
        self.frm_Applicant1Canvas.create_window((0, 0), window=self.frm_Applicant1, anchor='nw')
        self.frm_Applicant1Canvas.configure(yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set)
        
        self.frm_Applicant1Canvas.bind("<Configure>",  lambda e: self.frm_Applicant1Canvas.configure(scrollregion=self.frm_Applicant1Canvas.bbox("all")))
        self.frm_Applicant1Canvas.bind_all("<MouseWheel>",   lambda e: self.OnMouseWheel1(e))
        
        #print(self.varCurrentData)
        # self.children["txtApplicantData"].delete('1.0', tk.END)
        # self.children["txtApplicantData"].insert('1.0', str(self.varCurrentData) )

    def Get_Action(self,section,actionId):
        for action in section["actions"]:
            if(actionId==None ):
                if(self.checkKey(action,"startupType")):
                    if(action["startupType"]=="Start"):
                        return action
            elif(actionId==""):
                return None
            else:
                if(self.checkKey(action,"actionId")):
                    if(str(action["actionId"]) ==str(actionId)):
                        return action
        return None

    def Get_Element(self,actionOn,ControlName,GetOnlyId,counter,ApplicantId):        
        ControlName=ControlName.replace("{applicantid}",str(ApplicantId+1))           
        ControlName=ControlName.replace("{counter}",str(counter))

        if(GetOnlyId=="GetOnlyId"):
            return ControlName

        if(actionOn=="ByName"):
            return self.driver.find_element(By.NAME,ControlName)
        elif(actionOn=="ById") :
            return self.driver.find_element(By.ID ,ControlName)
        elif(actionOn=="ByXpath") :
            return self.driver.find_element(By.XPATH ,ControlName)
    
    def Get_WrapperValue(self,HaveWrapper,SectionCategory,IOName,IOValue):
        if(HaveWrapper):
            for data in self.varAllWrapperData:
                ioName_=str( data["ioName"]).lower().replace(' ','_')
                if(data["template"]==self.varCurrentTemplateName.get() and data["sectionCategory"]==SectionCategory and ioName_==str(IOName).lower() and str(data["ioValue"]).lower() == str(IOValue).lower() ):
                    return data["wrapperValue"]
        return IOValue

    def GetApplicantFullName(self,ApplicantId):
        try:
            tempData=self.varCurrentData[ApplicantId-1]
            FirstName,LastName="",""
            if(self.checkKey(tempData,"PersonalDetails")):                
                if(self.checkKey(tempData["PersonalDetails"],"First_Name")):
                    FirstName=tempData["PersonalDetails"]["First_Name"]
                if(self.checkKey(tempData["PersonalDetails"],"Last_Name")):
                    LastName=tempData["PersonalDetails"]["Last_Name"]
            return FirstName+" "+LastName
        except:
            return " "

    def GetYearMonth(self,inputvalue,procType):
        tempinputvalue=''
        try:
            if(procType==1):
                return inputvalue[-4:]
            elif(procType==2):
                return inputvalue[3:5]
            elif(procType==3):
                EndDt=datetime.today()
                StartDt=datetime.strptime(inputvalue, '%d/%m/%Y')
                return int( (EndDt-StartDt).days//365.4)            
            elif(procType==4):
                EndDt=datetime.today()
                StartDt=datetime.strptime(inputvalue, '%d/%m/%Y')
                return int(((EndDt-StartDt).days - (self.GetYearMonth(inputvalue,3)*365.4))//30.41667)
            elif(procType==5):
                if(str(inputvalue).lower().find('y')):
                    return int( str(inputvalue).lower().replace(' ','').split('y')[0])
                else:
                    return '0'
            elif(procType==6):
                if(str(inputvalue).lower().find('y')):
                    tempinputvalue= str(inputvalue).lower().replace(' ','').split('y')[1]
                if(str(tempinputvalue).lower().find('m')):                
                    return int( str(tempinputvalue).lower().replace(' ','').split('m')[0])
                return '0'
        except Exception as ex:
                print("Error", ex)
            


    def Get_ActionValue(self,jsonKeyName,counter,ApplicantId):
        if(jsonKeyName.strip().lower()=="fncgetapplicantname(1)"):
            return self.GetApplicantFullName(1)
        elif(jsonKeyName.strip().lower()=="fncgetapplicantname(2)"):
            return self.GetApplicantFullName(2)
        elif(jsonKeyName.strip().lower()=="fncgetapplicantname(3)"):
            return self.GetApplicantFullName(3)
        elif(jsonKeyName.strip().lower()=="fncgetapplicantname(4)"):
            return self.GetApplicantFullName(4)
        elif(jsonKeyName.strip().lower()=="fncgetapplicantname(@)"):
            return self.GetApplicantFullName(ApplicantId+1)

        keynames=jsonKeyName.split(":")
        sectionkeyname,datakeyname='',''
        if(len(keynames)>0):
            sectionkeyname=keynames[0]
        if(len(keynames)>1):
            datakeyname=keynames[1]                
        if(ApplicantId==None):
            ApplicantId=0
        tempData=self.varCurrentData[ApplicantId]

        HaveWrapper,HaveGetYearFunction,HaveGetMonthFunction,HaveGetYearTermFunction,HaveGetMonthTermFunction,HaveYearDiff,HaveMonthDiff=False,False,False,False,False,False,False
        if(sectionkeyname.find('fncWrapper ')!=-1):
            HaveWrapper=True
            sectionkeyname=sectionkeyname.replace('fncWrapper ','')
        if(sectionkeyname.find('fncGetYear ')!=-1):
            HaveGetYearFunction=True
            sectionkeyname=sectionkeyname.replace('fncGetYear ','')        
        if(sectionkeyname.find('fncGetMonth ')!=-1):
            HaveGetMonthFunction=True
            sectionkeyname=sectionkeyname.replace('fncGetMonth ','')
        if(sectionkeyname.find('fncGetYearTerm ')!=-1):
            HaveGetYearTermFunction=True
            sectionkeyname=sectionkeyname.replace('fncGetYearTerm ','')        
        if(sectionkeyname.find('fncGetMonthTerm ')!=-1):
            HaveGetMonthTermFunction=True
            sectionkeyname=sectionkeyname.replace('fncGetMonthTerm ','')
        if(sectionkeyname.find('fncCalculateYearDiff ')!=-1):
            HaveYearDiff=True
            sectionkeyname=sectionkeyname.replace('fncCalculateYearDiff ','')        
        if(sectionkeyname.find('fncCalcualteMonthDiff ')!=-1):
            HaveMonthDiff=True
            sectionkeyname=sectionkeyname.replace('fncCalcualteMonthDiff ','')

        if(sectionkeyname.find('[]')!=-1):
            sectionkeyname=sectionkeyname.replace('[]','')
            if(self.checkKey(tempData,sectionkeyname)):
                if(len(tempData[sectionkeyname])>counter ):
                    if(self.checkKey(tempData[sectionkeyname][counter],datakeyname)):
                        if(HaveWrapper):
                            return self.Get_WrapperValue(HaveWrapper,sectionkeyname,datakeyname, tempData[sectionkeyname][counter][datakeyname])
                        elif(HaveGetYearFunction):
                            return self.GetYearMonth(tempData[sectionkeyname][counter][datakeyname],1)
                        elif(HaveGetMonthFunction):
                            return self.GetYearMonth(tempData[sectionkeyname][counter][datakeyname],2)
                        elif(HaveYearDiff):
                            return self.GetYearMonth(tempData[sectionkeyname][counter][datakeyname],3)
                        elif(HaveMonthDiff):
                           return self.GetYearMonth(tempData[sectionkeyname][counter][datakeyname],4)
                        elif(HaveGetYearTermFunction):
                            return self.GetYearMonth(tempData[sectionkeyname][counter][datakeyname],5)
                        elif(HaveGetMonthTermFunction):
                            return self.GetYearMonth(tempData[sectionkeyname][counter][datakeyname],6)
                        else:
                           return tempData[sectionkeyname][counter][datakeyname]
        elif(sectionkeyname.find('[@]')!=-1):
            sectionkeyname=sectionkeyname.replace('[@]','')
            if(self.checkKey(tempData,sectionkeyname)):
                if(len(tempData[sectionkeyname])>self.FindIndex and self.FindIndex!=-1):
                    if(self.checkKey(tempData[sectionkeyname][self.FindIndex],datakeyname)):                       
                        if(HaveWrapper):
                            return self.Get_WrapperValue(HaveWrapper,sectionkeyname,datakeyname,tempData[sectionkeyname][self.FindIndex][datakeyname])
                        elif(HaveGetYearFunction):
                            return self.GetYearMonth(tempData[sectionkeyname][self.FindIndex][datakeyname],1)
                        elif(HaveGetMonthFunction):
                           return self.GetYearMonth(tempData[sectionkeyname][self.FindIndex][datakeyname],2)
                        elif(HaveYearDiff):
                           return self.GetYearMonth(tempData[sectionkeyname][self.FindIndex][datakeyname],3)
                        elif(HaveMonthDiff):
                           return self.GetYearMonth(tempData[sectionkeyname][self.FindIndex][datakeyname],4)
                        elif(HaveGetYearTermFunction):
                            return self.GetYearMonth(tempData[sectionkeyname][self.FindIndex][datakeyname],5)
                        elif(HaveGetMonthTermFunction):
                           return self.GetYearMonth(tempData[sectionkeyname][self.FindIndex][datakeyname],6)
                        else:
                           return tempData[sectionkeyname][self.FindIndex][datakeyname]
        else:
            if(self.checkKey(tempData,sectionkeyname)):
                if(tempData[sectionkeyname],datakeyname):           
                    if(HaveWrapper):
                        return self.Get_WrapperValue(HaveWrapper,sectionkeyname,datakeyname,tempData[sectionkeyname][datakeyname])
                    elif(HaveGetYearFunction):
                        return self.GetYearMonth(tempData[sectionkeyname][datakeyname],1)
                    elif(HaveGetMonthFunction):
                        return self.GetYearMonth(tempData[sectionkeyname][datakeyname],2)
                    elif(HaveYearDiff):
                        return self.GetYearMonth(tempData[sectionkeyname][datakeyname],3)
                    elif(HaveMonthDiff):
                        return self.GetYearMonth(tempData[sectionkeyname][datakeyname],4)
                    else:
                        return tempData[sectionkeyname][datakeyname]
        return ""

    def fncFindIndex(self,jsonKeyName,checkValue,conditionType,ApplicantId):
        keynames=jsonKeyName.split(":")
        sectionkeyname,datakeyname='',''
        if(len(keynames)>0):
            sectionkeyname=keynames[0]
        if(len(keynames)>1):
            datakeyname=keynames[1]                
        if(ApplicantId==None):
            ApplicantId=0
        tempData=self.varCurrentData[ApplicantId]
        HaveWrapper=False;        
        if(sectionkeyname.find('fncWrapper ')!=-1):
            HaveWrapper=True
            sectionkeyname=sectionkeyname.replace('fncWrapper ','')


        if(sectionkeyname.find('[]')!=-1):
            sectionkeyname=sectionkeyname.replace('[]','')
            if(self.checkKey(tempData,sectionkeyname)):
                for index,data in enumerate(tempData[sectionkeyname]):
                    if(self.checkKey( data,datakeyname)):
                        if(conditionType=="eq"):
                            if(str(self.Get_WrapperValue(HaveWrapper,sectionkeyname,datakeyname,data[datakeyname])).strip().lower()  == str(checkValue).strip().lower() ):
                                self.FindIndex=index
                                return index
                        
        return -1

    def InitlinzeDriver(self):
        if(self.driver != None):
            self.driver.quit()
        if(self.config.DriverName=="Chrome"):
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get(self.varCurrentTemplateData["url"])
        if(self.config.DriverName=="FireFox"):
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
            self.driver.get(self.varCurrentTemplateData["url"])
        if(self.config.DriverName=="IE"):
            self.driver = webdriver.Ie(IEDriverManager().install())
            self.driver.get(self.varCurrentTemplateData["url"])
        if(self.config.DriverName=="Edge"):
            self.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
            self.driver.get(self.varCurrentTemplateData["url"])

    def fill_data(self,sectionName,buttoncounter,applicantId=0):
        print(sectionName,buttoncounter,applicantId)
        if(self.driver is None):            
            self.InitlinzeDriver()
            

        element,controlId,IoName,controlValue,actiontype,finalValue,actionOn,CurrentActionId,CurrentAction=None,None,None,None,None,None,None,None,None
        for section in self.varCurrentTemplateData["sections"]:                     
            if(section["sectionName"]!=sectionName):
                continue
            else :
                ActionCounter=0
                CurrentActionId,PreviousActionId=None,-1
                CurrentAction=self.Get_Action(section,CurrentActionId)
                while (CurrentAction !=None and ActionCounter<500 and CurrentActionId != PreviousActionId ):

                    ActionCounter=ActionCounter+1
                    PreviousActionId=CurrentActionId
                    try:
                        if(CurrentAction["actionType"]=="Fill Input"):
                            CurrentActionId=CurrentAction["nextActionId"]
                            element=self.Get_Element(CurrentAction["selectorType"],CurrentAction["control"],"",buttoncounter,applicantId)
                            if(element != None):
                                finalValue=""
                                if(CurrentAction["inputType"]=="IOValue"):
                                    finalValue=self.Get_ActionValue(CurrentAction["ioValue"],buttoncounter,applicantId)
                                else:
                                    finalValue=CurrentAction["manualValue"]
                            element.clear()
                            element.send_keys(finalValue)                            
                        elif(CurrentAction["actionType"]=="Select Option" or CurrentAction["actionType"]=="Select Text" ):
                            CurrentActionId=CurrentAction["nextActionId"]
                            element=self.Get_Element(CurrentAction["selectorType"],CurrentAction["control"],"",buttoncounter,applicantId)
                            if(element != None):
                                finalValue=""
                                if(CurrentAction["inputType"]=="IOValue"):
                                    finalValue=self.Get_ActionValue(CurrentAction["ioValue"],buttoncounter,applicantId)
                                else:
                                    finalValue=CurrentAction["manualValue"]
                                select = Select(element)
                                if(CurrentAction["actionType"]=="Select Option"):
                                    select.select_by_value(finalValue)
                                else:
                                    select.select_by_visible_text(finalValue)       
                        elif(CurrentAction["actionType"]=="Single Choosen Text" or CurrentAction["actionType"]=="Multiple Choosen Text"):
                            CurrentActionId=CurrentAction["nextActionId"]
                            finalValue=""
                            if(CurrentAction["inputType"]=="IOValue"):
                                finalValue=self.Get_ActionValue(CurrentAction["ioValue"],buttoncounter,applicantId)
                            else:
                                finalValue=CurrentAction["manualValue"]                                
                            if(CurrentAction["actionType"]=="Single Choosen Text"):                                
                                self.select_from_chosen( self.Get_Element(CurrentAction["selectorType"],CurrentAction["control"],"GetOnlyId",buttoncounter,applicantId), finalValue)
                            else:
                                fullFinalValue=[]
                                fullFinalValue.append(finalValue)
                                self.select_from_multi_chosen(self.Get_Element(CurrentAction["selectorType"],CurrentAction["control"],"GetOnlyId",buttoncounter,applicantId),fullFinalValue)
                        elif(CurrentAction["actionType"]=="Button Click"):
                            CurrentActionId=CurrentAction["nextActionId"]
                            element=self.Get_Element(CurrentAction["selectorType"],CurrentAction["control"],section["sectionType"],buttoncounter,applicantId)
                            if(element != None):                            
                                element.click()
                                # element.send_keys(finalValue)
                                # action=ActionChains(self.driver)
                                # action.move_to_element(element)
                                # action.click(on_element = element)                            
                                # action.perform()                            
                        elif(CurrentAction["actionType"]=="Wait"):
                            finalValue=CurrentAction["manualValue"]
                            self.driver.implicitly_wait(finalValue)
                            CurrentActionId=CurrentAction["nextActionId"]
                        elif(CurrentAction["actionType"]=="Check Checkbox"):
                            CurrentActionId=CurrentAction["nextActionId"]
                            element=self.Get_Element(CurrentAction["selectorType"],CurrentAction["control"],"",buttoncounter,applicantId)
                            if(element != None):
                                isSelected = element.is_selected()
                                if(isSelected==False):
                                    action=ActionChains(self.driver)
                                    action.move_to_element(element)
                                    action.click(on_element = element)                            
                                    action.perform()
                        elif(CurrentAction["actionType"]=="Condition"):
                            leftfinalValue,rightfinalValue="",""                            
                            if(CurrentAction["leftInputType"]=="IOValue"):
                                leftfinalValue=self.Get_ActionValue(CurrentAction["leftIOValue"],buttoncounter,applicantId)
                            else:
                                leftfinalValue=CurrentAction["leftManualValue"]                        
                            if(CurrentAction["rightInputType"]=="IOValue"):
                                rightfinalValue=self.Get_ActionValue(CurrentAction["rightIOValue"],buttoncounter,applicantId)
                            else:
                                rightfinalValue=CurrentAction["rightManualValue"]
                            if(CurrentAction["conditionType"]=="eq"):
                                if(str(leftfinalValue)==str(rightfinalValue)):
                                    CurrentActionId=CurrentAction["trueActionId"]
                                else:
                                    CurrentActionId=CurrentAction["falseActionId"]
                            elif(CurrentAction["conditionType"]=="nq"):
                                if(str(leftfinalValue)!=str(rightfinalValue)):
                                    CurrentActionId=CurrentAction["trueActionId"]
                                else:
                                    CurrentActionId=CurrentAction["falseActionId"]
                        elif(CurrentAction["actionType"]=="Find Index"):
                            self.FindIndex=-1                            
                            if(CurrentAction["leftInputType"]=="IOValue"):
                                self.FindIndex==self.fncFindIndex(CurrentAction["leftIOValue"],CurrentAction["rightManualValue"],CurrentAction["conditionType"],applicantId)
                            else:
                                self.FindIndex==self.fncFindIndex(CurrentAction["rightIOValue"],CurrentAction["leftManualValue"],CurrentAction["conditionType"],applicantId)
                            if(self.FindIndex!=-1):
                                CurrentActionId=CurrentAction["trueActionId"]
                            else:
                                CurrentActionId=CurrentAction["falseActionId"] 
                    except Exception as ex:
                        print("Error", ex)
                        
                    
                    CurrentAction=self.Get_Action(section,CurrentActionId)
    def change_tab(self):
         try:
            if(self.driver != None):
                self.driver.switch_to.window(self.driver.window_handles[int(self.varCurrentTab.get())-1]) 
         except:
            print('Invalid Tab')           

    def Open_Browser(self):
        if(self.varCurrentTemplateName.get()==""):
            messagebox.showerror("Required", "Please select template")
            return
        FoundTemplateName=False
        for templ in  self.varAllTemlate:            
            if templ["templateName"]==self.varCurrentTemplateName.get():
                FoundTemplateName=True
                self.varCurrentTemplateData=templ
        if(not FoundTemplateName):
            messagebox.showerror("Required", "Invalid template name")
            return
        
        self.InitlinzeDriver()
        

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

        
    
    def OnMouseWheel1(self, event):        
            self.frm_Applicant1Canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()


    def checkKey(self,dict, key):      
        if key in dict.keys():
            return True
        else:
            return False

    def shrinkForm(self):   
        parent = Widget.winfo_toplevel(self.ContainerFrame)
        if(not self.IsShrink):            
            parent.geometry("400x800")  
            parent.minsize(400,800)
            self.btnShrinkData["image"]=self.config.ico_up
        else:
            parent.geometry("900x600")
            parent.minsize(900,600)
            self.btnShrinkData["image"]=self.config.ico_down
        self.IsShrink= not self.IsShrink
            

    def fncCreateItems(self):
        self.varCurrentTab.set("1")
        frmHeader,frmBody  = ttk.Frame(self.ContainerFrame) ,ttk.Frame(self.ContainerFrame)        
        self.ContainerFrame.grid_columnconfigure(0, weight=100)
        self.ContainerFrame.grid_rowconfigure(0, weight=1)
        self.ContainerFrame.grid_rowconfigure(1, weight=100)

        frmHeader.grid(row=0,column = 0, sticky=tk.N+tk.S+tk.W+tk.E)
        frmBody.grid(row=1,column = 0,  sticky=tk.N+tk.S+tk.W+tk.E)

        frmHeader.columnconfigure(0, weight=100)                
        frmHeader.rowconfigure(0, weight=1)        
        frmbtn1 = ttk.Frame(frmHeader)        
        frmbtn1.grid(row=0,column = 1, columnspan=3, sticky=tk.N+tk.W+tk.E)
        btnReffreshData = ttk.Button ( frmbtn1,name="btnReffreshData",image=self.config.ico_sync, text =fa.icons['sync'],   command = lambda :self.LoadAllJsonData() )
        btnReffreshData.grid(row=0,column = 0, padx=(10,0),pady=(3,5))
        self.btnShrinkData = ttk.Button ( frmbtn1,name="btnShrink",image=self.config.ico_down,    command = lambda :self.shrinkForm() )
        self.btnShrinkData.grid(row=0,column = 1, padx=(10,0),pady=(3,5))
        
        
        frmBody.columnconfigure(0, weight=1)
        frmBody.columnconfigure(1, weight=100)  
        frmBody.rowconfigure(0, weight=100)  
        self.frmLeftPanel,self.frmRightPanel= ttk.Frame(frmBody,width=350),ttk.Frame(frmBody)
        
        self.frmLeftPanel.grid(row=0,column=0,sticky=tk.N+tk.S+tk.W+tk.E,padx=(10,10))
        self.frmRightPanel.grid(row=0,column=1,sticky=tk.N+tk.S+tk.W+tk.E,padx=(10,10))
        self.frmRightPanel.grid_forget()
        self.frmRightPanel.columnconfigure(0, weight=100)  
        self.frmRightPanel.rowconfigure(0, weight=100)  
        self.txtData= tk.Text(self.frmRightPanel, name="txtData")
        self.txtData.grid(row=0,column = 0,columnspan=3 ,padx=(0, 10), pady=(5, 2), sticky=tk.N+tk.S+tk.W+tk.E)

        
        self.frmLeftPanel.columnconfigure(0, weight=1)
        self.frmLeftPanel.columnconfigure(1, weight=100)
        self.frmLeftPanel.rowconfigure(0, weight=1)
        self.frmLeftPanel.rowconfigure(1, weight=1)
        self.frmLeftPanel.rowconfigure(2, weight=1)
        self.frmLeftPanel.rowconfigure(3, weight=1)
        self.frmLeftPanel.rowconfigure(4, weight=1)
        self.frmLeftPanel.rowconfigure(5, weight=1)        
        self.frmLeftPanel.rowconfigure(6, weight=100)

        ttk.Label(self.frmLeftPanel,text="Template").grid(row=0,column=0,sticky=tk.N+tk.S+tk.W,pady=(10,3),padx=(10,10))
        self.ddlTemplateName=ttk.Combobox(self.frmLeftPanel,textvariable = self.varCurrentTemplateName,values=self.varAllTemlateName,width=24)
        self.ddlTemplateName.grid(row=0,column=1,sticky=tk.N+tk.S+tk.W,pady=(10,3))
        ttk.Label(self.frmLeftPanel,text="File Name").grid(row=1,column=0,sticky=tk.N+tk.S+tk.W,pady=(10,3),padx=(10,10))
        self.ddlFileName=ttk.Combobox(self.frmLeftPanel,textvariable = self.varCurrentDataFileName,values=self.varAllJsonFileName,width=24)
        self.ddlFileName.grid(row=1,column=1,sticky=tk.N+tk.S+tk.W,pady=(10,3))        
        ttk.Label(self.frmLeftPanel,text="Current Tab").grid(row=2,column=0,sticky=tk.N+tk.S+tk.W,pady=(10,3),padx=(10,10))
        ttk.Entry(self.frmLeftPanel,textvariable = self.varCurrentTab,width=26).grid(row=2,column=1,sticky=tk.N+tk.S+tk.W,pady=(10,3))
        

        self.frmInnerContentFrame1 = ttk.Frame(self.frmLeftPanel)
        self.frmInnerContentFrame1.grid(row=6, column=0,columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)  
        frmbtn2 = ttk.Frame(self.frmLeftPanel)        
        frmbtn2.grid(row=3,column = 0,columnspan=2,pady=(10,3),padx=(10,10))
        ttk.Button (frmbtn2, text ="Open Browser", width=12, command =lambda: self.Open_Browser()).grid(row=0,column = 0,padx=(2,2) )
        ttk.Button ( frmbtn2, text ="Load Data", width=9, command =lambda: self.load_data()).grid(row=0,column = 1 ,padx=(2,2))
        ttk.Button ( frmbtn2, text ="Change Tab", width=9, command =lambda: self.change_tab()).grid(row=0,column = 2 ,padx=(2,2))

        #ttk.Frame(self.frmLeftPanel, height=10).grid(row=4, column=0,columnspan=2, sticky=tk.E+tk.W)
        # ttk.Frame(self.frmLeftPanel, style="Separator.TFrame", height=1).grid(row=5, column=0,columnspan=2, sticky=tk.E+tk.W)
        # ttk.Frame(self.frmLeftPanel, height=10).grid(row=6, column=0,columnspan=2, sticky=tk.E+tk.W)
              
        
    def select_from_chosen(self,  id, value):                      
        try:
            ch=Chosen(self.driver, id)
            if(value==""):
                ch.select_by_visible_text("Please select",False)   
            else:
                ch.select_by_visible_text(value,True)                   
        except:
            ch=Chosen(self.driver, id)
            ch.select_by_visible_text("Please select",False)   
        
        


    def select_from_multi_chosen(self, id, values):
        chosen = self.driver.find_element(By.ID,id + '_chzn')

        results = chosen.find_element(By.CSS_SELECTOR,".chzn-results li")
        for value in values:
            found = False
            for result in results:
                if str(result.text).lower()  == str(value).lower():
                    found = True
                    break
            if found:
                chosen.find_element(By.CSS_SELECTOR, "input").click()
                result.click()



if __name__ == '__main__':
    config= Gc.GenerateConfig()     
    
    root = tk.Tk()
    sizex = 600
    sizey = 400
    posx  = 100
    posy  = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    config.set_theme(None,root)
    config.set_icons()
    myframe=tk.Frame(root,relief=tk.GROOVE,width=600,height=700,bd=1)
    myframe.pack( fill="both" ,expand=tk.TRUE ,anchor=tk.N+tk.W)   
    FillData(myframe,config)
    #root.eval('tk::PlaceWindow . center')
    root.mainloop()

        

