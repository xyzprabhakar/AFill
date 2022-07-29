
from ast import Return
import ctypes
from email.headerregistry import Address
import os
import tabula
from tabula.io import read_pdf
import pandas as pd
import io
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import RAISED, ttk,messagebox

import GenerateConfig as Gc
import json
from datetime import datetime
import time



class ImportData:
    varError=None;
    config = None
    varApplicant1,varApplicant2 = None,None     
    varTemplateType,varApplicantType,varFileName = None,None  ,None   
    varStarttingPoint = 0
    varAllJsonData = []     
    ContainerCanvas,ContainerFrame,ApplicantTab,frm_Applicant1,frm_Applicant1Canvas,frm_Applicant1Parent,frm_Applicant2,frm_Applicant2Canvas,frm_Applicant2Parent = None,None,None,None,None ,None,None ,None,None   
    Parent_Height = 500
    Parent_Width = 600
    tables = None


    def __init__(self, Container, config):
        self.varError= tk.StringVar()
        self.config = config
        self.varTemplateType = tk.StringVar()
        self.varApplicantType = tk.StringVar()
        self.varApplicant1 = tk.StringVar()
        self.varApplicant2 = tk.StringVar()
        self.varFileName = tk.StringVar()

        self.ContainerFrame=ttk.Frame(Container)
        self.ContainerFrame.pack(expand=tk.TRUE, fill="both",pady=(5,3))       
        self.fncCreateItems()
        
    def OnMouseWheel1(self, event,canvas_):
        canvas_=self.ApplicantTab.index(self.ApplicantTab.select())
        if(canvas_==0):
            self.frm_Applicant1Canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif(canvas_==1):            
            self.frm_Applicant2Canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        

    # def fnc_resizeScroll(self, e,canvas):
    #     canvas.configure(scrollregion=canvas.bbox("all"))
    def fnc_resizeScroll(self,event):
        self.ContainerCanvas.configure(scrollregion=self.ContainerCanvas.bbox("all"))


    def fncReplaceName(self,value):
        if(not(  str(value).find(self.varApplicant1.get(),0) ==-1 and str(value).find(self.varApplicant2.get(),0) ==-1)):
            for i in range(1 ,30):
                if(value==self.varApplicant1.get()+"."+str(i)):
                    return self.varApplicant1.get()
                if(value==self.varApplicant2.get()+"."+str(i)):
                    return self.varApplicant2.get()
                if(value=="Joint."+str(i)):
                    return "Joint"
        return value


    def fnc_Read_PersonalDetails(self, ParentContainer, Applicantid):
        
        
        
        frmTopFrame = ttk.Notebook(ParentContainer,name="tab_Section_"+str(Applicantid))
        frmTopFrame.pack(fill="both",anchor="nw")        

        if(self.varTemplateType.get() == "IO Template"): 
            
            self.varError_.insert(tk.END,"\nAdding Personal Details")
            self.ContainerFrame.update()
            frmDetailFrame = ttk.Frame(frmTopFrame ,name="frmDetailFrame_"+str(Applicantid)) 
            frmPersonalDetailsFrame = ttk.LabelFrame(frmDetailFrame,name="frmPersonalDetailsFrame_"+str(Applicantid), text="Personal Details", style="Details.TLabelframe")
            frmPersonalDetailsFrame.grid(row=0, column=0, sticky=tk.N+tk.W, pady=(10, 10), padx=(10, 10))
            self.fnc_Read_PersonalDetails_IO_Template(frmPersonalDetailsFrame, Applicantid)            

            
            frmAddressFrame = ttk.Notebook(frmDetailFrame,name="tab_Section_Address_"+str(Applicantid))
            # Add Current Address
            self.varError_.insert(tk.END,"\nAdding Current Address")
            self.ContainerFrame.update()
            
            frmCurrentAddressFrame = ttk.Frame(frmAddressFrame, name="frmCurrentAddressFrame_"+str(Applicantid))    
            self.fnc_Read_CurrentAddress_IO_Template(frmCurrentAddressFrame, Applicantid)
            frmAddressFrame.add(frmCurrentAddressFrame, text ='Current Address')            

            # Add Previous Address
            self.varError_.insert(tk.END,"\nAdding Previous Address")
            self.ContainerFrame.update()            
            frmPreviousAddressFrame = ttk.Frame(frmAddressFrame,name="frmPreviousAddressFrame_"+str(Applicantid))
            self.fnc_Read_PreviousAddress_IO_Template(frmPreviousAddressFrame, Applicantid)
            frmAddressFrame.add(frmPreviousAddressFrame, text ='Previous Address')
            # Contact Details
            self.varError_.insert(tk.END,"\nAdding Contact Details")
            self.ContainerFrame.update()            
            frmContactDetailFrame = ttk.LabelFrame(frmDetailFrame,name="frmContactDetailFrame_"+str(Applicantid) ,text="Contact Details", style="Details.TLabelframe")            
            self.fnc_Read_ContactDetails_IO_Template(frmContactDetailFrame, Applicantid)
            frmContactDetailFrame.grid(row=1, column=0, sticky=tk.N+tk.W, pady=(10, 10), padx=(10, 10))

            
            # ProfessionalContacts
            self.varError_.insert(tk.END,"\nAdding Professional Contacts")
            self.ContainerFrame.update()
            frmProfessionalContactsFrame = ttk.Frame(frmAddressFrame,name="frmProfessionalContactsFrame_"+str(Applicantid))
            self.fnc_Read_ProfessionalContact_IO_Template(frmProfessionalContactsFrame, Applicantid)
            frmAddressFrame.add(frmProfessionalContactsFrame, text ='Professional Contacts')
            # Bank Details
            self.varError_.insert(tk.END,"\nAdding Bank Details")
            self.ContainerFrame.update()
            frmBankDetailFrame = ttk.Frame(frmAddressFrame,name="frmBankDetailFrame_"+str(Applicantid))
            self.fnc_Read_BankAccountDetails_IO_Template(frmBankDetailFrame, Applicantid)
            frmAddressFrame.add(frmBankDetailFrame, text ='Bank Details')

            frmAddressFrame.grid(row=2, column=0, sticky=tk.N+tk.W+tk.E)
            frmTopFrame.add(frmDetailFrame, text ='Details')

            

            
            # Family And Dependants
            self.varError_.insert(tk.END,"\nAdding Family And Dependants")
            self.ContainerFrame.update()
            frmFamilyAndDependantsrame = ttk.LabelFrame(frmTopFrame,name="frmFamilyAndDependantsrame_"+str(Applicantid), text="Family And Dependants", style="Details.TLabelframe")
            self.fnc_Read_FamilyAndDependants_IO_Template(frmFamilyAndDependantsrame, Applicantid)
            frmTopFrame.add(frmFamilyAndDependantsrame, text ='Family')
            # ID Verfication
            self.varError_.insert(tk.END,"\nAdding ID Verfication")
            self.ContainerFrame.update()
            frmIDVerificationFrame = ttk.Frame(frmTopFrame,name="frmIDVerificationFrame_"+str(Applicantid))
            self.fnc_Read_IDVerification_IO_Template(frmIDVerificationFrame, Applicantid)
            frmTopFrame.add(frmIDVerificationFrame, text ='ID Verification')

            # Current Employment Details
            self.varError_.insert(tk.END,"\nAdding Current Employment Details")
            self.ContainerFrame.update()
            frmCurrentEmploymentDetailsFrame = ttk.LabelFrame(frmTopFrame,name="frmCurrentEmploymentDetailsFrame_"+str(Applicantid),text="Current Employment Details",style="Details.TLabelframe")
            self.fnc_Read_CurrentEmploymentDetails_IO_Template(frmCurrentEmploymentDetailsFrame, Applicantid)           
            frmTopFrame.add(frmCurrentEmploymentDetailsFrame, text ='Employment')


            frmAssetsLiabilitiesFrame=ttk.Notebook(frmTopFrame,name="frmAssetsLiabilitiesFrame_"+str(Applicantid))            
            self.varError_.insert(tk.END,"\nAdding Assets")
            self.ContainerFrame.update()
            # Assets Details            
            frmAssetsFrame = ttk.Frame(frmAssetsLiabilitiesFrame,name="frmAssetsFrame_"+str(Applicantid))
            self.fnc_Read_Assets_IO_Template(frmAssetsFrame, Applicantid)            
            frmAssetsLiabilitiesFrame.add(frmAssetsFrame, text ='Assets')

            
            # Liabilities
            self.varError_.insert(tk.END,"\nAdding Liabilities")
            self.ContainerFrame.update()
            frmLiabilitiesFrame = ttk.Frame(frmAssetsLiabilitiesFrame,name="frmLiabilitiesFrame_"+str(Applicantid))
            self.fnc_Read_Liabilities_IO_Template(frmLiabilitiesFrame, Applicantid)
            frmAssetsLiabilitiesFrame.add(frmLiabilitiesFrame, text ='Liabilities')
            # Expenditure
            self.varError_.insert(tk.END,"\nAdding Expenditure")
            self.ContainerFrame.update()
            frmExpenditureFrame = ttk.Frame(frmAssetsLiabilitiesFrame,name="frmExpenditureFrame_"+str(Applicantid))
            self.fnc_Read_Expenditure_IO_Template(frmExpenditureFrame, Applicantid)
            frmAssetsLiabilitiesFrame.add(frmExpenditureFrame, text ='Expenditure')
            frmTopFrame.add(frmAssetsLiabilitiesFrame, text ='Assets/Liabilities')

            frmMortgageFrame = ttk.Notebook(frmTopFrame,name="frmMortgageFrame_"+str(Applicantid))
            self.ContainerFrame.update()
            # ExistingMortgage
            self.varError_.insert(tk.END,"\nAdding Existing Mortgage")
            frmExistingMortgageFrame = ttk.Frame(frmMortgageFrame,name="frmExistingMortgageFrame_"+str(Applicantid))
            self.fnc_Read_ExistingMortgageDetails_IO_Template(frmExistingMortgageFrame, Applicantid)
            frmMortgageFrame.add(frmExistingMortgageFrame, text ='Existing Mortgage')
            #Mortage Requirement
            self.varError_.insert(tk.END,"\nAdding Mortage Requirement")
            self.ContainerFrame.update()
            frmMortgageRequirementsFrame = ttk.Frame(frmMortgageFrame,name="frmMortgageRequirementsFrame_"+str(Applicantid))
            self.fnc_Read_MortgageRequirements_IO_Template(frmMortgageRequirementsFrame, Applicantid)
            frmMortgageFrame.add(frmMortgageRequirementsFrame, text ='Mortgage Requirements')
            frmTopFrame.add(frmMortgageFrame, text ='Mortgage')

            
                
    def fnc_GenrateControl(self, ParentContainer, DetailTable, FindingColumnIndex, FromPosition, IO_Name, IO_Template_Name, Suffix,HaveDtValue=True):
        try:
            if(IO_Name=="Repayment Method"):
                pass
            if(self.IsEvenColumn):
                self.IsEvenColumn = False
                self.gridcolumnindex = 2
            else:
                self.IsEvenColumn = True
                self.gridcolumnindex = 0
                self.gridrowindex = self.gridrowindex+1
            FindingValue = ""
            if ((not("[M]" in IO_Name)) and HaveDtValue):
                for i, j in DetailTable.iterrows():
                    if(i < FromPosition):
                        continue
                    try:
                        if(j[0] == IO_Template_Name):
                            FindingValue = j[FindingColumnIndex]
                            if(str(FindingValue) == "nan"):
                                FindingValue = ""
                            break

                    except Exception as ex:
                        print("Error", ex)
            ttk.Label(ParentContainer, text=IO_Name.replace('[M]', '').replace('[D]', '')).grid(
                row=self.gridrowindex, column=self.gridcolumnindex, sticky=tk.N+tk.S+tk.E, padx=(10, 10), pady=(5, 2))
            txtboxname = Suffix+IO_Name.strip().replace(' ',
                                                        '_').replace('[M]', '').replace('[D]', '')
            entrybox = ttk.Entry(ParentContainer, name=txtboxname)
            entrybox.insert(0, self.fncReplaceName(FindingValue) )
            entrybox.grid(row=self.gridrowindex, column=(
                self.gridcolumnindex + 1), sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))
        except Exception as ex:
                print("Error", ex)

    def fnc_GenrateControl_Vertical(self, ParentContainer, DetailTable, FindingColumnIndex, FindingRowIndex, IO_Name, IO_Template_Name, Suffix,CastToInt=False,HaveDtValue=True):
        try:
            if(self.IsEvenColumn):
                self.IsEvenColumn = False
                self.gridcolumnindex = 2
            else:
                self.IsEvenColumn = True
                self.gridcolumnindex = 0
                self.gridrowindex = self.gridrowindex+1
            FindingValue = ""
            if ((not("[M]" in IO_Name) and FindingRowIndex > 0) and HaveDtValue):
                for i, j in DetailTable.iterrows():
                    if(i < FindingRowIndex):
                        continue
                    try:
                        if(CastToInt):
                            FindingValue = int(j[FindingColumnIndex]) 
                        else:
                            FindingValue = j[FindingColumnIndex] 
                        if(str(FindingValue) == "nan"):
                            FindingValue = ""
                        break
                    except Exception as ex:
                        print("Error", ex)
            ttk.Label(ParentContainer, text=IO_Name.replace('[M]', '').replace('[D]', '')).grid(
                row=self.gridrowindex, column=self.gridcolumnindex, sticky=tk.N+tk.S+tk.E, padx=(10, 10), pady=(5, 2))
            txtboxname = Suffix+IO_Name.strip().replace(' ',
                                                        '_').replace('[M]', '').replace('[D]', '')
            entrybox = ttk.Entry(ParentContainer, name=txtboxname)
            entrybox.insert(0,self.fncReplaceName(FindingValue) )
            entrybox.grid(row=self.gridrowindex, column=(
                self.gridcolumnindex + 1), sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))
        except Exception as ex:
                print("Error", ex)

    def fnc_GenrateControl_Vertical_asset(self, ParentContainer, FindingValue, IO_Name, Suffix,HaveDtValue=True):
        try:
            if(self.IsEvenColumn):
                self.IsEvenColumn = False
                self.gridcolumnindex = 2
            else:
                self.IsEvenColumn = True
                self.gridcolumnindex = 0
                self.gridrowindex = self.gridrowindex+1          
            ttk.Label(ParentContainer, text=IO_Name.replace('[M]', '').replace('[D]', '')).grid(
                row=self.gridrowindex, column=self.gridcolumnindex, sticky=tk.N+tk.S+tk.E, padx=(10, 10), pady=(5, 2))
            txtboxname = Suffix+IO_Name.strip().replace(' ',
                                                        '_').replace('[M]', '').replace('[D]', '')
            entrybox = ttk.Entry(ParentContainer, name=txtboxname)
            entrybox.insert(0,self.fncReplaceName( FindingValue))
            entrybox.grid(row=self.gridrowindex, column=(
                self.gridcolumnindex + 1), sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))
        except Exception as ex:
                print("Error", ex)


    def fun_mergetables(self, table, IsPrentTable, IncludeHeader=False):
        currentColumnLength = len(table.columns)
        if(IsPrentTable):
            self.tableData = []
            self.tableDataColumnLength = len(table.columns)
            self.tableDataColumnName = []
            for colindex in range(self.tableDataColumnLength):
                self.tableDataColumnName.append("columns"+str(colindex))
        if(IncludeHeader):
            subrow1 = []
            for colindex in range(self.tableDataColumnLength):
                if(colindex >= currentColumnLength):
                    subrow1.append("")
                else:
                    subrow1.append(table.columns[colindex])
            self.tableData.append(subrow1)

        for i, j in table.iterrows():
            subrow2 = []
            for colindex in range(self.tableDataColumnLength):
                if(colindex >= currentColumnLength):
                    subrow2.append("")
                else:
                    try:
                        subrow2.append(j[colindex])
                    except:
                        subrow2.append("")
            self.tableData.append(subrow2)

    def fnc_IsTable_Found(self, DetailTable, tableName):
        if(tableName == "Professional Contacts"):
            if( str(DetailTable.columns[0]).find("rofessional Contacts")>=0 ):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Company Name")>=0 ):
                    return True
        elif(  tableName==("Bank Account Details") ):
            if( str(DetailTable.columns[0]).find("ank Account Details")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Bank Name")>=0  or str(row[0]).find("Account Holder(s)")>=0):
                    return True
        elif( tableName ==("Family And Dependants")):
            if( str(DetailTable.columns[0]).find("amily And Dependants")>=0):
                return True
            if(str(DetailTable.columns[0]).find("Full Name")>=0 and str(DetailTable.columns[1]).find("Date of Birth")>=0 and str(DetailTable.columns[2]).find("Age")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Full Name")>=0 and str(row[1]).find("Date of Birth")>=0 and str(row[2]).find("Age")>=0 ):
                    return True
        elif(tableName==("ID Verification")):
            if(str(DetailTable.columns[0]).find("D Verification")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Original Driving Licence Seen")>=0 or str(row[0]).find("Driving Licence Ref")>=0):
                    return True
        elif(str(tableName)==("Electronic ID Verification")):
            if(str(DetailTable.columns[0]).find("lectronic ID Verification")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("ID Check Completed Date")>=0 or str(row[0]).find("ID Check Expiry Date")>=0):
                    return True
        elif(str(tableName)==("Current Employment Details")):
            if(str(DetailTable.columns[0]).find("urrent Employment Details")>=0 ):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Highest rate of income tax paid")>=0 or str(row[0]).find("Employment Status")>=0 or str(row[0]).find("Most Recent Annual Accounts Net Profit")>=0):
                    return True
        elif(tableName == "Assets"):
            if(str(DetailTable.columns[0]).find("ssets")>=0 or str(DetailTable.columns[0]).find("Do you have any assets")>=0 ):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Do you have any assets")>=0 ):
                    return True
        elif(str(tableName)==("Assets1")):
            if(str(DetailTable.columns[0]).find("Owner")>=0 or str(DetailTable.columns[1]).find("Category" )>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Owner")>=0 or str(row[1]).find("Category")>=0):
                    return True
        elif(str(tableName)==("Liabilities")):
            if(str(DetailTable.columns[0]).find("iabilities")>=0 or str(DetailTable.columns[0]).find("Do you have any liabilities")>=0  ):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Do you have any liabilities")>=0):
                    return True
        elif(str(tableName)==("Liabilities1")):            
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Owner")>=0 or str(row[0]).find("Liability Account Number")>=0):
                    return True
        elif(tableName == "Income"):            
            if(DetailTable.columns[0].find("ncome")>=0 or DetailTable.columns[0].find("Do you have any liabilities")>=0 ):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Total Gross Annual Earnings")>=0):
                    return True
        elif(str(tableName)==("Expenditure")):
            if(str(DetailTable.columns[0]).find("xpenditure")>=0 or str(DetailTable.columns[0]).find("Do you wish to carry out a detailed" )>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Do you wish to carry out a detailed")>=0 ):
                    return True
        elif(tableName == "Expenditure1"):
            if(str(DetailTable.columns[0]).find("Category")>=0 or str(DetailTable.columns[1]).find("Owner")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Category")>=0 or str(row[1]).find("Owner")>=0):
                    return True
        elif(tableName == "Expenditure Details"):
            if(str(DetailTable.columns[0]).find("xpenditure Details")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Calculated Total Monthly Household Expenditure")>=0 ):
                    return True
        elif(str(tableName)==("Current Monthly Cash Flow")):
            if(DetailTable.columns.find("urrent Monthly Cash Flow")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0].find("Total Net Monthly Income")>=0  ):
                    return True
        elif(str(tableName)==("Existing Mortgage Details")):            
            if(str(DetailTable.columns[0]).find("xisting Mortgage Detai")>=0  or str(DetailTable.columns[0]).find("Do you have an existing mortgage?")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Do you have an existing mortgage?")>=0):
                    return True
        elif(str(tableName)==("Existing Mortgage Details1")):
            if(str(DetailTable.columns[0]).find("Owner")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Owner")>=0  ):
                    return True
        elif(str(tableName)==("Mortgage Requirements")):            
            if(str(DetailTable.columns[0]).find("ortgage Requirements")>=0 or str(DetailTable.columns[0]).find("Mortgage Requirements")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).lower().find("unique identifier")>=0) :                    
                    return True
        elif(str(tableName)==("Property Details")):            
            if(str(DetailTable.columns[0]).find("roperty Details")>=0):
                return True    
        elif(str(tableName).find("Mortgage Preferences & Attitude to Risk")>=0):            
            if(str(DetailTable.columns[0]).find("ortgage Preferences & Attitude to Risk")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Do you want the certainty of the")>=0):
                    return True        
        elif(str(tableName)==("Which of the following are important to you")):            
            if(str(DetailTable.columns[0]).find("hich of the following are important to you")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("The maximum early redemption period I would accept is")>=0):
                    return True        
        elif(str(tableName)==("Final Salary Pension Schemes")):            
            if(str(DetailTable.columns[0]).find("inal Salary Pension Schemes")>=0 or str(DetailTable.columns[0]).find("Do you have any existing final salary schemes")>=0):
                return True
            for i, row in DetailTable.iterrows():
                if(str(row[0]).find("Do you have any existing final salary schemes")>=0):
                    return True        
        return False

    def fnc_Read_PersonalDetails_IO_Template(self, ParentContainer, Applicantid):
        self.IsEvenColumn = False
        self.gridrowindex = -1
        self.gridcolumnindex = 0
        PersonalDetailTable = None
        foundTable = False
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(table.columns[0] == "ersonal Details"):
                PersonalDetailTable = table
                foundTable = True
                self.SkipTable=tableindex
                break
        if(foundTable):
            addressee = ""
            try:
                for i, j in PersonalDetailTable.iterrows():
                    if(j[0] == "First Name"):
                        addressee = j[1] if(Applicantid == 1) else j[2]
                    elif(j[0] == "Last Name"):
                        addressee = addressee+" " + \
                            (j[1] if(Applicantid == 1) else j[2])
                        break
            except:
                print('Some Error')
            if(Applicantid == 1):
                self.varApplicant1.set(addressee)
            elif(Applicantid == 2):
                self.varApplicant2.set(addressee)
            for ioindex, x in enumerate(self.config.IO_Name_PersonalDetails):
                self.fnc_GenrateControl(ParentContainer, PersonalDetailTable, Applicantid, 0, x,
                                        self.config.IO_Template_PersonalDetails[ioindex], "txt_PersonalDetails_"+str(Applicantid))

    def fnc_Read_Address_GetRowColumnIndex(self, DetailTable, PreviousRowIndex, PreviousColumnIndex, Adressee, IsCurrentAddress):
        FoundApplicant = False
        IsFound = False
        columnLength = len(DetailTable.columns)
        if(PreviousColumnIndex >= columnLength-1):
            PreviousColumnIndex = 0
            PreviousRowIndex = PreviousRowIndex+10

        RowIndex = PreviousRowIndex
        ColumnIndex = PreviousColumnIndex+1

        CurrentIndex = {"row": RowIndex,
                        "column": ColumnIndex, "IsFound": IsFound}
        self.CurrentDepthCount += 1
        if(self.RecursionDepthCount < self.CurrentDepthCount):
            return CurrentIndex
        for i, row in DetailTable.iterrows():
            try:
                if(i < PreviousRowIndex):
                    continue
                if(row[0] == "Addressee" and (not FoundApplicant)):
                    RowIndex = i
                    if(str(row[ColumnIndex]).replace(' ','').lower() == str(Adressee).replace(' ','').lower() ):
                        FoundApplicant = True
                    else:
                        if(ColumnIndex+1 <= columnLength-1):
                            return self.fnc_Read_Address_GetRowColumnIndex(DetailTable, PreviousRowIndex, ColumnIndex, Adressee, IsCurrentAddress)
                        else:
                            return self.fnc_Read_Address_GetRowColumnIndex(DetailTable, PreviousRowIndex+10, 0, Adressee, IsCurrentAddress)
                if(FoundApplicant):
                    if(str(row[0]).lower().replace(' ','')  == "addressstatus" and ((IsCurrentAddress and str(row[ColumnIndex]).replace(' ','').lower()  == "currentaddress") or (str(row[ColumnIndex]).replace(' ','').lower()  == "previousaddress"))):
                        IsFound = True
                        break
                    if(row[0] == "Addressee" and i > RowIndex):
                        break
            except Exception as ex:
                print("Error", ex)
        if(IsFound):
            CurrentIndex["row"] = RowIndex
            CurrentIndex["column"] = ColumnIndex
            CurrentIndex["IsFound"] = True
        else:
            if(self.RecursionDepthCount > self.CurrentDepthCount):
                if(ColumnIndex+1 <= columnLength-1):
                    return self.fnc_Read_Address_GetRowColumnIndex(DetailTable, PreviousRowIndex, ColumnIndex, Adressee, IsCurrentAddress)
                else:
                    return self.fnc_Read_Address_GetRowColumnIndex(DetailTable, PreviousRowIndex+10, 0, Adressee, IsCurrentAddress)
        return CurrentIndex

    def fnc_Read_Bank_GetRowColumnIndex(self, DetailTable, PreviousRowIndex, PreviousColumnIndex, Adressee, ApplicantId):
        FoundApplicant = False
        IsFound = False
        columnLength = len(DetailTable.columns)
        if(PreviousColumnIndex >= columnLength-1):
            PreviousColumnIndex = 0
            PreviousRowIndex = PreviousRowIndex+10

        RowIndex = PreviousRowIndex
        ColumnIndex = PreviousColumnIndex+1

        CurrentIndex = {"row": RowIndex,
                        "column": ColumnIndex, "IsFound": IsFound}
        self.CurrentDepthCount += 1
        if(self.RecursionDepthCount < self.CurrentDepthCount):
            return CurrentIndex
        for i, row in DetailTable.iterrows():
            try:
                if(i < PreviousRowIndex):
                    continue
                if(row[0] == "Owner"):
                    RowIndex = i
                    if(str(row[ColumnIndex]).lower().replace(' ','')  == str(Adressee).lower().replace(' ','')  or str(row[ColumnIndex]).lower().replace(' ','') == str(Adressee+".1").lower().replace(' ','') or str(row[ColumnIndex]).lower().replace(' ','') == str(Adressee+".2").lower().replace(' ','') or str(row[ColumnIndex]).lower().replace(' ','') == str(Adressee+".3").lower().replace(' ','') or (ApplicantId == 1 and row[ColumnIndex] == "Joint")):
                        IsFound = True
                        break
                    else:
                        if(ColumnIndex+1 <= columnLength-1):
                            return self.fnc_Read_Bank_GetRowColumnIndex(DetailTable, PreviousRowIndex, ColumnIndex, Adressee, ApplicantId)
                        else:
                            return self.fnc_Read_Bank_GetRowColumnIndex(DetailTable, PreviousRowIndex+10, 0, Adressee, ApplicantId)
            except Exception as ex:
                print("Error", ex)
        if(IsFound):
            CurrentIndex["row"] = RowIndex
            CurrentIndex["column"] = ColumnIndex
            CurrentIndex["IsFound"] = True
        else:
            if(self.RecursionDepthCount > self.CurrentDepthCount):
                if(ColumnIndex+1 <= columnLength-1):
                    return self.fnc_Read_Bank_GetRowColumnIndex(DetailTable, PreviousRowIndex, ColumnIndex, Adressee, ApplicantId)
                else:
                    return self.fnc_Read_Bank_GetRowColumnIndex(DetailTable, PreviousRowIndex+10, 0, Adressee, ApplicantId)
        return CurrentIndex

    def fnc_Read_Vertical_GetRowColumnIndex(self, DetailTable, PreviousRowIndex, PreviousColumnIndex, Adressee, KeyData, KeyColumn):
        try:
            IsFound = False
            RowIndex = PreviousRowIndex
            ColumnIndex = PreviousColumnIndex
            CurrentIndex = {"row": RowIndex,
                            "column": ColumnIndex, "IsFound": IsFound}
            for i, row in DetailTable.iterrows():
                try:
                    if(i < PreviousRowIndex):
                        continue
                    if(( str(row[ColumnIndex]).lower().replace(' ','') == str(Adressee).lower().replace(' ','') or row[ColumnIndex] == "Joint") and row[KeyColumn] == KeyData):
                        RowIndex = i
                        IsFound = True
                        break
                except Exception as ex:
                    print("Error", ex)
            if(IsFound):
                CurrentIndex["row"] = RowIndex
                CurrentIndex["column"] = ColumnIndex
                CurrentIndex["IsFound"] = True
            return CurrentIndex
        except Exception as ex:
                print("Error", ex)

    def fnc_Read_CurrentAddress_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem,foundAnyItem = False, False,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(table.columns[0] == "ontact Address"):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.tables[tableindex+1].columns[0] == "ontact Details")):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not (self.tables[tableindex+2].columns[0] == "ontact Details")):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break

        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 1:
                self.IsEvenColumn = False
                foundItem = False
                tempData = self.fnc_Read_Address_GetRowColumnIndex(
                    DetailTable, PreviousRowIndex, PreviousColumnIndex, Addressee, True)
                foundItem = tempData["IsFound"]
                if(foundItem):
                    foundAnyItem=True
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex

                    for ioindex, x in enumerate(self.config.IO_Name_CurrentAddress):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_CurrentAddress[ioindex], "txt_CurrentAddress_"+str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    #ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            for ioindex, x in enumerate(self.config.IO_Name_CurrentAddress):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_CurrentAddress[ioindex], "txt_CurrentAddress_"+str(Applicantid),False)


    def fnc_Read_PreviousAddress_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem,foundAnyItem = False, False,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0

        if(self.CurrentAddressFound):
            DetailTable = pd.DataFrame(
                self.tableData, columns=self.tableDataColumnName)
            foundTable = True
        else:
            for tableindex, table in enumerate(self.tables):
                if(tableindex<self.SkipTable):
                    continue
                if(table.columns[0] == "ontact Address"):
                    self.SkipTable=tableindex
                    self.fun_mergetables(table, True,True)
                    # check Next Table is on Next Page
                    if (not (self.tables[tableindex+1].columns[0] == "ontact Details")):
                        self.fun_mergetables(self.tables[tableindex+1], False,False)
                        # check Next Table is on Next to Next Page
                        if (not (self.tables[tableindex+2].columns[0] == "ontact Details")):
                            self.fun_mergetables(
                                self.tables[tableindex+2], False,False)
                    DetailTable = pd.DataFrame(
                        self.tableData, columns=self.tableDataColumnName)
                    foundTable = True
                    self.CurrentAddressFound = True
                    break
        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 4:
                self.IsEvenColumn = False
                foundItem = False
                tempData = self.fnc_Read_Address_GetRowColumnIndex(
                    DetailTable, PreviousRowIndex, PreviousColumnIndex, Addressee, False)
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    foundAnyItem=True
                    for ioindex, x in enumerate(self.config.IO_Name_PreviousAddress):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_PreviousAddress[ioindex], "txt_PreviousAddress_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            PreviousAddressCounter=0
            for ioindex, x in enumerate(self.config.IO_Name_PreviousAddress):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_PreviousAddress[ioindex], "txt_PreviousAddress_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid),False)


    def fnc_Read_ContactDetails_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        DetailTable = None
        foundTable, foundItem = False, False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(table.columns[0] == "ontact Details"):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.tables[tableindex+1].columns[0] == "rofessional Contacts")):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not (self.tables[tableindex+2].columns[0] == "rofessional Contacts")):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break
        if(foundTable):
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            for ioindex, x in enumerate(self.config.IO_Name_ContactDetails):
                foundItem = False
                PreviousRowIndex = 0
                if (not("[M]" in x)):
                    tempData = self.fnc_Read_Vertical_GetRowColumnIndex(
                        DetailTable, 0, 0, Addressee, self.config.IO_Template_ContactDetails[ioindex], 1)
                    foundItem = tempData["IsFound"]
                    if(foundItem):
                        PreviousRowIndex = tempData["row"]
                self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 2, PreviousRowIndex, x,
                                                 self.config.IO_Template_ContactDetails[ioindex], "txt_ContactDetails_"+str(Applicantid))

    def fnc_Read_ProfessionalContact_IO_Template(self, ParentContainer, Applicantid):
        if(Applicantid!=1):
            return
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex, columnLength = 0, 0,0
        DetailTable = None
        foundTable, foundItem ,foundAnyItem = False, False,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(self.fnc_IsTable_Found(table, "Professional Contacts")):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Bank Account Details"))):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not (self.fnc_IsTable_Found(self.tables[tableindex+2], "Bank Account Details"))):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                DetailTable = pd.DataFrame(self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                columnLength=len(DetailTable.columns)
                break
        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 4 and columnLength>PreviousColumnIndex+1:
                self.IsEvenColumn = False
                foundItem = False
                tempData = {"IsFound":True,"column":PreviousColumnIndex+1,"row":0} 
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    foundAnyItem=True
                    for ioindex, x in enumerate(self.config.IO_Name_ProfessionalContacts):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_ProfessionalContacts[ioindex], "txt_ProfessionalContacts_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                    PreviousColumnIndex+1
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            PreviousAddressCounter=0
            for ioindex, x in enumerate(self.config.IO_Name_ProfessionalContacts):                
                self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_ProfessionalContacts[ioindex], "txt_ProfessionalContacts_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid),False)

    def fnc_Read_BankAccountDetails_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem ,foundAnyItem = False, False,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if( self.fnc_IsTable_Found(table, "Bank Account Details")):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Family And Dependants") or self.fnc_IsTable_Found(self.tables[tableindex+1], "ID Verification"))):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not (self.fnc_IsTable_Found(self.tables[tableindex+2], "Family And Dependants") or self.fnc_IsTable_Found(self.tables[tableindex+2], "ID Verification"))):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break
        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 6:
                self.IsEvenColumn = False
                foundItem = False
                tempData = self.fnc_Read_Bank_GetRowColumnIndex(
                    DetailTable, PreviousRowIndex, PreviousColumnIndex, Addressee, Applicantid)
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    foundAnyItem = True
                    for ioindex, x in enumerate(self.config.IO_Name_BankAccountDetails):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_BankAccountDetails[
                                                ioindex], "txt_BankAccountDetails_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            PreviousAddressCounter=0
            for ioindex, x in enumerate(self.config.IO_Name_BankAccountDetails):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_BankAccountDetails[
                                                ioindex], "txt_BankAccountDetails_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid),False)

    
    def fnc_Read_FamilyAndDependants_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        DetailTable = None
        foundTable, foundAnyItem = False, False
        membercounter=0
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(self.fnc_IsTable_Found(table, "Family And Dependants")):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.tables[tableindex+1].columns[0] == "ID Verification")):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not (self.tables[tableindex+2].columns[0] == "ID Verification")):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break
        if(foundTable):
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            for i, row in DetailTable.iterrows():
                try:
                    
                    if(row[4] == Addressee or  (row[4] == "Joint" and Applicantid== 1)):
                        foundAnyItem=True
                        membercounter=membercounter+1
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 0,i, "Full Name",
                                                 "Full Name", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 1,i, "Date of Birth",
                                                 "Date of Birth", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid))                        
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 2,i, "Age",
                                                 "Age", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid),True)
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 3,i, "Relationship",
                                                 "Relationship", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 4,i, "Related To",
                                                 "Related To", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 5,i, "Financially Dependant",
                                                 "Financially Dependant", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 7,i, "Dependant Living with Client",
                                                 "Dependant Living with Client", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid))
                        self.gridrowindex = self.gridrowindex+1
                        ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                        self.gridrowindex = self.gridrowindex+1
                        self.IsEvenColumn = False
                except Exception as ex:
                    print("Error", ex) 
        if ((not foundAnyItem) and Applicantid == 1):
            membercounter=1
            i=0
            self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 0,i, "Full Name",
                                                 "Full Name", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid),False,False)
            self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 1,i, "Date of Birth",
                                        "Date of Birth", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid),False,False)                        
            self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 2,i, "Age",
                                        "Age", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid),False,False)
            self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 3,i, "Relationship",
                                        "Relationship", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid),False,False)
            self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 4,i, "Related To",
                                        "Related To", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid),False,False)
            self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 5,i, "Financially Dependant",
                                        "Financially Dependant", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid),False,False)
            self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 7,i, "Dependant Living with Client",
                                        "Dependant Living with Client", "txt_FamilyAndDependants_"+str(membercounter)+"_"+str(Applicantid),False,False)

            
    def fnc_Read_IDVerification_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem ,foundAnyItem = False, False,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(self.fnc_IsTable_Found(table, "ID Verification")):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Electronic ID Verification"))):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not (self.fnc_IsTable_Found(self.tables[tableindex+2], "Electronic ID Verification"))):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break
        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 1:
                self.IsEvenColumn = False
                foundItem = False
                tempData = {"column": 1, "row": 0, "IsFound": True} if(
                    Applicantid == 1) else {"column": 2, "row": 0, "IsFound": True}
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    foundAnyItem=True
                    for ioindex, x in enumerate(self.config.IO_Name_IDVerification):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_IDVerification[ioindex], "txt_IDVerification_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            PreviousAddressCounter=0
            for ioindex, x in enumerate(self.config.IO_Name_IDVerification):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_IDVerification[ioindex], "txt_IDVerification_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid),False)
    
    def fnc_Read_CurrentEmploymentDetails_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem ,foundAnyItem = False, False,False
        
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(self.fnc_IsTable_Found(table, "Current Employment Details")):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Assets") or self.fnc_IsTable_Found(self.tables[tableindex+1], "Liabilities"))):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not ( self.fnc_IsTable_Found(self.tables[tableindex+2], "Assets") or self.fnc_IsTable_Found(self.tables[tableindex+2], "Liabilities"))):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                        if (not ( self.fnc_IsTable_Found(self.tables[tableindex+3], "Assets") or self.fnc_IsTable_Found(self.tables[tableindex+3], "Liabilities"))):
                            self.fun_mergetables(self.tables[tableindex+3], False)
                            if (not ( self.fnc_IsTable_Found(self.tables[tableindex+4], "Assets") or self.fnc_IsTable_Found(self.tables[tableindex+4], "Liabilities"))):
                                self.fun_mergetables(self.tables[tableindex+4], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break
        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 1:
                self.IsEvenColumn = False
                foundItem = False
                tempData = {"column": 1, "row": 0, "IsFound": True} if(
                    Applicantid == 1) else {"column": 2, "row": 0, "IsFound": True}
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    foundAnyItem=True
                    for ioindex, x in enumerate(self.config.IO_Name_CurrentEmploymentDetails):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_CurrentEmploymentDetails[ioindex], "txt_CurrentEmploymentDetails_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    #ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            PreviousAddressCounter=0
            for ioindex, x in enumerate(self.config.IO_Name_CurrentEmploymentDetails):                
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_CurrentEmploymentDetails[ioindex], "txt_CurrentEmploymentDetails_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid),False)

    def fnc_combinedRows(self,combinedRows,r1,r2,r3,r4):
        if(r1==None):
            r1=""
        if(r2==None):
            r2=""
        if(r3==None):
            r3=""
        if(r4==None):
            r4=""
        if(str(r1) =="nan"):
            r1=""
        if(str(r2) =="nan"):
            r2=""
        if(str(r3) =="nan"):
            r3=""
        if(str(r4) =="nan"):
            r4=""
        if(combinedRows==1):            
                return str(r1) 
        elif(combinedRows==2):            
            return (r1+" "+r2).strip()
        elif(combinedRows==3):          
            return (r1+" "+r2+" "+r3).strip()
        elif(combinedRows==4):          
            return (r1+" "+r2+" "+r3+" "+r4).strip()
    
    def fnc_howManyRowCombined(self,DetailTable,CurrentRow,Addressee,ApplicantId):        
        row1vale,row2vale,row3vale,row4vale="","","",""
        row1vale=DetailTable.iloc[CurrentRow][0]
        if(str(row1vale)=="nan" or str(row1vale)==""):
            return 0
        if( len(DetailTable.index)> CurrentRow+1):
            row2vale=DetailTable.iloc[CurrentRow+1][0]
            if( len(DetailTable.index)> CurrentRow+2):
                row3vale=DetailTable.iloc[CurrentRow+2][0]
                if( len(DetailTable.index)> CurrentRow+3):
                    row3vale=DetailTable.iloc[CurrentRow+3][0]
        if(str(row2vale)=="nan"):
            row2vale=""
        if(str(row3vale)=="nan"):
            row3vale=""
        if(str(row4vale)=="nan"):
            row4vale=""        
        if ( (len(DetailTable.index)> CurrentRow+3) and
            ((row1vale+" "+row2vale+" "+row3vale+" "+row4vale).strip()==Addressee or 
            ((row1vale+" "+row2vale+" "+row3vale+" "+row4vale).strip()=="Joint"  and ApplicantId==1))):
            return 4
        elif ( (len(DetailTable.index)> CurrentRow+2) and
            ((row1vale+" "+row2vale+" "+row3vale).strip()==Addressee or 
            ((row1vale+" "+row2vale+" "+row3vale).strip()=="Joint"  and ApplicantId==1))):
            return 3
        elif ((len(DetailTable.index)> CurrentRow+1) and 
            ((row1vale+" "+row2vale).strip()==Addressee or
             ((row1vale+" "+row2vale).strip()=="Joint") and  ApplicantId==1)):
            return 2
        elif((row1vale).strip()==Addressee or ((row1vale).strip()=="Joint" and ApplicantId==1)):
            return 1
        else :
            return 0
        
    def fnc_Read_Assets_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        DetailTable = None
        foundTable, foundItem,foundAssetTable,foundAnyItem = False, False,False,False
        membercounter=0
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(self.fnc_IsTable_Found(table, "Assets")):
                foundAssetTable=True
                continue
            if(foundAssetTable and self.fnc_IsTable_Found(table, "Assets1")):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.tables[tableindex+1].columns[0] == "Liabilities")):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not (self.tables[tableindex+2].columns[0] == "Liabilities")):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break
        if (foundTable):
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            combinedRows=0            
            i=0
            while (i< len(DetailTable.index)):   
                combinedRows=0         
                
                combinedRows= self.fnc_howManyRowCombined(DetailTable,i,Addressee,Applicantid)
                if(combinedRows==0):
                    i=i+1
                    continue
                if (combinedRows>0):                    
                    try:
                        foundAnyItem=True
                        membercounter=membercounter+1
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][0],  DetailTable.iloc[i+1][0] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][0] if(combinedRows>2)else "",DetailTable.iloc[i+3][0] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Owner", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][1],  DetailTable.iloc[i+1][1] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][1] if(combinedRows>2)else "",DetailTable.iloc[i+3][1] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Category", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][2],  DetailTable.iloc[i+1][2] if(membercounter>1)else "" ,DetailTable.iloc[i+2][2] if(combinedRows>2)else "",DetailTable.iloc[i+3][2] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Related To Address", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 1[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 2[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 3[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 4[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "City[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Country[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Postcode[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))

                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][7],  DetailTable.iloc[i+1][7] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][7] if(combinedRows>2)else "",DetailTable.iloc[i+3][7] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Original Value", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][8],  DetailTable.iloc[i+1][8] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][8] if(combinedRows>2)else "",DetailTable.iloc[i+3][8] if(combinedRows>3)else "") 
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Purchased On", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][9],  DetailTable.iloc[i+1][9] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][9] if(combinedRows>2)else "",DetailTable.iloc[i+3][9] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Value", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][10],  DetailTable.iloc[i+1][10] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][10] if(combinedRows>2)else "",DetailTable.iloc[i+3][10] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Valuation Date", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid))
                        
                        self.gridrowindex = self.gridrowindex+1
                        ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                        self.gridrowindex = self.gridrowindex+1
                        self.IsEvenColumn = False
                    except Exception as ex:
                        print("Error", ex) 
                    i=i+combinedRows
        if ((not foundAnyItem) and Applicantid == 1):
            membercounter=1
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Owner", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)            
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Category", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)            
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Related To Address", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 1[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 2[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 3[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 4[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "City[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Country[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Postcode[M]", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Original Value", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Purchased On", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Value", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Valuation Date", "txt_Assets_"+str(membercounter)+"_"+str(Applicantid),False)
                        

    def fnc_Read_Liabilities_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem,Liabilities,foundAnyItem = False, False,False,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(self.fnc_IsTable_Found(table, "Liabilities")):
                Liabilities=True                
                continue
            if(Liabilities):                
                if(self.fnc_IsTable_Found(table, "Liabilities1")):
                    self.SkipTable=tableindex
                    self.fun_mergetables(table, True,True)
                    # check Next Table is on Next Page
                    if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Credit History") or self.fnc_IsTable_Found(self.tables[tableindex+1], "Income"))):
                        self.fun_mergetables(self.tables[tableindex+1], False,False)
                        # check Next Table is on Next to Next Page
                        if (not ( self.fnc_IsTable_Found(self.tables[tableindex+2], "Credit History") or self.fnc_IsTable_Found(self.tables[tableindex+2], "Income"))):
                            self.fun_mergetables(self.tables[tableindex+2], False,False)
                            if (not ( self.fnc_IsTable_Found(self.tables[tableindex+3], "Credit History") or self.fnc_IsTable_Found(self.tables[tableindex+3], "Income"))):
                                self.fun_mergetables(self.tables[tableindex+3], False,False)                
                
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break
        if (foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 15:
                self.IsEvenColumn = False
                foundItem = False
                tempData = self.fnc_Read_Bank_GetRowColumnIndex(
                    DetailTable, PreviousRowIndex, PreviousColumnIndex, Addressee, Applicantid)
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    foundAnyItem=True
                    for ioindex, x in enumerate(self.config.IO_Name_Liabilities):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_Liabilities[
                                                ioindex], "txt_Liabilities_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            for ioindex, x in enumerate(self.config.IO_Name_Liabilities):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_Liabilities[
                                                ioindex], "txt_Liabilities_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid),False)


    def fnc_Read_Expenditure_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        DetailTable = None
        foundTable, foundItem,Expenditure,membercounter,foundAnyItem = False, False,False,0,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue            
            if(self.fnc_IsTable_Found(table, "Expenditure")):
                Expenditure=True                
                continue
            if(Expenditure):                
                if(self.fnc_IsTable_Found(table, "Expenditure1")):
                    self.SkipTable=tableindex
                    self.fun_mergetables(table, True,True)
                    # check Next Table is on Next Page
                    if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Expenditure Details") or self.fnc_IsTable_Found(self.tables[tableindex+1], "Current Monthly Cash Flow"))):
                        self.fun_mergetables(self.tables[tableindex+1], False,False)
                        # check Next Table is on Next to Next Page
                        if (not ( self.fnc_IsTable_Found(self.tables[tableindex+2], "Expenditure Details") or self.fnc_IsTable_Found(self.tables[tableindex+2], "Current Monthly Cash Flow"))):
                            self.fun_mergetables(self.tables[tableindex+2], False,False)
                            if (not ( self.fnc_IsTable_Found(self.tables[tableindex+3], "Expenditure Details") or self.fnc_IsTable_Found(self.tables[tableindex+3], "Current Monthly Cash Flow"))):
                                self.fun_mergetables(self.tables[tableindex+3], False,False)                
                
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True
                break
        if (foundTable):
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            for ioindex, x in enumerate(self.config.IO_Name_Expenditure1):
                foundItem = False
                PreviousRowIndex = 0
                if (not("[M]" in x)):
                    tempData = self.fnc_Read_Vertical_GetRowColumnIndex(
                        DetailTable, 0, 1, Addressee, self.config.IO_Template_Expenditure1[ioindex], 0)
                    foundItem = tempData["IsFound"]
                    if(foundItem):
                        foundAnyItem=True
                        membercounter=membercounter+1
                        PreviousRowIndex = tempData["row"]                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,x, "Category", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= DetailTable.iloc[PreviousRowIndex][1]
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Owner", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= DetailTable.iloc[PreviousRowIndex][2]
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Description", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= DetailTable.iloc[PreviousRowIndex][3]
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Net Amount", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid))
                        rowValue= DetailTable.iloc[PreviousRowIndex][4]
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Frequency", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid))
                        self.gridrowindex = self.gridrowindex+1
                        ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                        self.gridrowindex = self.gridrowindex+1
                        self.IsEvenColumn = False
        if ((not foundAnyItem) and Applicantid == 1):
            membercounter=1                        
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Category", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid),False)            
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Owner", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Description", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Net Amount", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid),False)
            self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Frequency", "txt_Expenditure_"+str(membercounter)+"_"+str(Applicantid),False)


    def fnc_Read_ExistingMortgageDetails_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem,ExistingMortgageDetails,foundAnyItem = False, False,False ,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(self.fnc_IsTable_Found(table, "Existing Mortgage Details")):
                ExistingMortgageDetails=True                
                continue
            if(ExistingMortgageDetails):                
                if(self.fnc_IsTable_Found(table, "Existing Mortgage Details1")):
                    self.SkipTable=tableindex
                    self.fun_mergetables(table, True,True)
                    # check Next Table is on Next Page
                    if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Mortgage Requirements") or self.fnc_IsTable_Found(self.tables[tableindex+1], "Property Details"))):
                        self.fun_mergetables(self.tables[tableindex+1], False,False)
                        # check Next Table is on Next to Next Page
                        if (not ( self.fnc_IsTable_Found(self.tables[tableindex+2], "Mortgage Requirements") or self.fnc_IsTable_Found(self.tables[tableindex+2], "Property Details") )):
                            self.fun_mergetables(self.tables[tableindex+2], False,False)
                            if (not ( self.fnc_IsTable_Found(self.tables[tableindex+3], "Mortgage Requirements") or self.fnc_IsTable_Found(self.tables[tableindex+3], "Property Details"))):
                                self.fun_mergetables(self.tables[tableindex+3], False,False)
                                if (not ( self.fnc_IsTable_Found(self.tables[tableindex+4], "Mortgage Requirements") or self.fnc_IsTable_Found(self.tables[tableindex+4], "Property Details"))):
                                    self.fun_mergetables(self.tables[tableindex+4], False,False)                
                                    if (not ( self.fnc_IsTable_Found(self.tables[tableindex+5], "Mortgage Requirements") or self.fnc_IsTable_Found(self.tables[tableindex+5], "Property Details"))):
                                        self.fun_mergetables(self.tables[tableindex+5], False,False)                
                
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True                
                break
        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 15:
                self.IsEvenColumn = False
                foundItem = False
                tempData = self.fnc_Read_Bank_GetRowColumnIndex(
                    DetailTable, PreviousRowIndex, PreviousColumnIndex, Addressee, Applicantid)
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    foundAnyItem=True
                    for ioindex, x in enumerate(self.config.IO_Name_ExistingMortgage):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_ExistingMortgage[
                                                ioindex], "txt_ExistingMortgage_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            for ioindex, x in enumerate(self.config.IO_Name_ExistingMortgage):
                    self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_ExistingMortgage[
                                                ioindex], "txt_ExistingMortgage_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid),False)

    def fnc_Read_MortgageRequirements_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem, foundAnyItem= False, False,False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue            
            if(self.fnc_IsTable_Found(table, "Mortgage Requirements")):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Mortgage Preferences & Attitude to Risk") or self.fnc_IsTable_Found(self.tables[tableindex+1], "Which of the following are important to you?"))):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not ( self.fnc_IsTable_Found(self.tables[tableindex+2], "Mortgage Preferences & Attitude to Risk") or self.fnc_IsTable_Found(self.tables[tableindex+2], "Which of the following are important to you?") )):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                        if (not ( self.fnc_IsTable_Found(self.tables[tableindex+3], "Mortgage Preferences & Attitude to Risk") or self.fnc_IsTable_Found(self.tables[tableindex+3], "Which of the following are important to you?"))):
                            self.fun_mergetables(self.tables[tableindex+3], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True                
                break
        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 15:
                self.IsEvenColumn = False
                foundItem = False
                tempData = self.fnc_Read_Bank_GetRowColumnIndex(
                    DetailTable, PreviousRowIndex, PreviousColumnIndex, Addressee, Applicantid)
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    foundAnyItem=True
                    for ioindex, x in enumerate(self.config.IO_Name_MortgageRequirements):                        
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_MortgageRequirements[
                                                ioindex], "txt_MortgageRequirements_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
        if ((not foundAnyItem) and Applicantid == 1):
            PreviousAddressCounter=0
            for ioindex, x in enumerate(self.config.IO_Name_MortgageRequirements):                        
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_MortgageRequirements[
                                                ioindex], "txt_MortgageRequirements_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid),False)
        

    def fnc_Read_whichofthefollowingareimportant_IO_Template(self, ParentContainer, Applicantid):
        if(Applicantid!=1):
            return
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem= False, False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue            
            if(self.fnc_IsTable_Found(table, "Which of the following are important to you?")):
                self.SkipTable=tableindex
                self.fun_mergetables(table, True,True)
                # check Next Table is on Next Page
                if (not (self.fnc_IsTable_Found(self.tables[tableindex+1], "Final Salary Pension Schemes"))):
                    self.fun_mergetables(self.tables[tableindex+1], False,False)
                    # check Next Table is on Next to Next Page
                    if (not ( self.fnc_IsTable_Found(self.tables[tableindex+2], "Final Salary Pension Schemes"))):
                        self.fun_mergetables(self.tables[tableindex+2], False,False)
                        if (not ( self.fnc_IsTable_Found(self.tables[tableindex+3], "Final Salary Pension Schemes"))):
                            self.fun_mergetables(self.tables[tableindex+3], False,False)
                DetailTable = pd.DataFrame(
                    self.tableData, columns=self.tableDataColumnName)
                foundTable = True
                self.CurrentAddressFound = True                
                break
        if(foundTable):
            PreviousAddressCounter = 0
            PreviousColumnIndex = 0
            PreviousRowIndex = 0
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            while PreviousAddressCounter < 15:
                self.IsEvenColumn = False
                foundItem = False
                tempData ={"IsFound":True,"row":0,"column":1}
                foundItem = tempData["IsFound"]
                if(foundItem):
                    PreviousColumnIndex = tempData["column"]
                    PreviousRowIndex = tempData["row"]
                    rowIndex = PreviousRowIndex
                    columnIndex = PreviousColumnIndex
                    for ioindex, x in enumerate(self.config.IO_Name_MortgageRequirements):                        
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_MortgageRequirements[
                                                ioindex], "txt_Whichofthefollowingareimportant_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))
                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1

    def hide_unhide_applicant(self,event):       
        if(self.frm_Applicant1Parent!= None):
                self.ApplicantTab.forget(self.frm_Applicant1Parent)      
                self.clear_frame(self.frm_Applicant1Parent)
                self.frm_Applicant1Parent=None
        if(self.frm_Applicant2Parent!= None):
                self.ApplicantTab.forget(self.frm_Applicant2Parent)      
                self.clear_frame(self.frm_Applicant2Parent)
                self.frm_Applicant2Parent=None
                        
    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    

    def open_file(self):
        try:
            self.varError_.delete("1.0","end")
            open_file = askopenfilename(initialdir="d:", title="Open Template", filetypes=[
                                        ('Pdf Files', '*.pdf')])
            if open_file:         
                self.ContainerFrame.update()
                self.varError_.insert(tk.END,"Loading Data..")
                self.tables = tabula.read_pdf(open_file, pages="all")
                print(self.tables)
                self.ContainerFrame.update()
                self.varError_.insert(tk.END,"\nPdf read Successfully")
                #self.varError_.insert(tk.END,self.tables)
                time.sleep(10)
                self.ContainerFrame.update()
                self.varError_.insert(tk.END,"\nGenrating Canvas")
                self.CurrentAddressFound = False
                self.hide_unhide_applicant(None)                
                self.frm_Applicant1Parent=ttk.Frame(self.ApplicantTab)
                self.frm_Applicant2Parent=ttk.Frame(self.ApplicantTab)
                self.frm_Applicant1Canvas = tk.Canvas(self.frm_Applicant1Parent, bg=self.config.COLOR_MENU_BACKGROUND,highlightthickness=0, relief='ridge')
                self.frm_Applicant1 = ttk.Frame(self.frm_Applicant1Canvas)            
                self.frm_Applicant1.columnconfigure(0, weight=1)
                self.frm_Applicant1.rowconfigure(0, weight=1)
                self.frm_Applicant1.rowconfigure(1, weight=1)
                self.frm_Applicant1.rowconfigure(2, weight=1)
                self.frm_Applicant1.rowconfigure(3, weight=1)
                self.frm_Applicant1.rowconfigure(4, weight=1)
                self.frm_Applicant1.rowconfigure(5, weight=100)                                
                ttk.Frame(self.frm_Applicant1, height=10).grid(row=0, column=0, sticky=tk.E+tk.W)
                ttk.Label(self.frm_Applicant1, text="Applicant 1", textvariable=self.varApplicant1, style="H1.TLabel").grid(row=1, column=0, sticky=tk.N+tk.W)
                ttk.Frame(self.frm_Applicant1, height=10).grid(row=2, column=0, sticky=tk.E+tk.W)
                ttk.Frame(self.frm_Applicant1, style="Separator.TFrame", height=1).grid(row=3, column=0, sticky=tk.E+tk.W)
                ttk.Frame(self.frm_Applicant1, height=10).grid(row=4, column=0, sticky=tk.E+tk.W)
                frmInnerContentFrame1 = ttk.Frame(self.frm_Applicant1,name="frmInnerContentFrame1")
                frmInnerContentFrame1.grid(row=5, column=0, sticky=tk.E+tk.W+tk.N+tk.S)            
                self.SkipTable=0
                self.ContainerFrame.update()
                self.varError_.insert(tk.END,"\nGenrating Control (Applicant 1)")                
                self.fnc_Read_PersonalDetails(frmInnerContentFrame1, 1)
                self.frm_Applicant1Canvas.create_window((0, 0), window=self.frm_Applicant1, anchor='nw')
                self.ApplicantTab.add(self.frm_Applicant1Parent, text ='Applicant 1')
                scrollbar_y_Applicant1 = ttk.Scrollbar(self.frm_Applicant1Parent, orient=tk.VERTICAL, command=self.frm_Applicant1Canvas.yview)
                scrollbar_x_Applicant1 = ttk.Scrollbar(self.frm_Applicant1Parent, orient=tk.HORIZONTAL, command=self.frm_Applicant1Canvas.xview)
                scrollbar_y_Applicant1.pack(side=tk.RIGHT, fill="y")
                scrollbar_x_Applicant1.pack(side=tk.BOTTOM, fill="x")
                self.frm_Applicant1Canvas.pack(expand=tk.TRUE, fill="both",pady=(5,3), padx=(10,10))
                self.frm_Applicant1Canvas.configure(yscrollcommand=scrollbar_y_Applicant1.set,xscrollcommand=scrollbar_x_Applicant1.set)
                self.frm_Applicant1Canvas.bind("<Configure>",  lambda e: self.frm_Applicant1Canvas.configure(scrollregion=self.frm_Applicant1Canvas.bbox("all")))
                self.frm_Applicant1Canvas.bind_all("<MouseWheel>",   lambda e: self.OnMouseWheel1(e,1) )        
                if(self.varApplicantType.get() == "Co Applicant"):
                    self.ContainerFrame.update()
                    self.varError_.insert(tk.END,"\nGenrating Canvas (Applicant 2)")
                    self.frm_Applicant2Canvas = tk.Canvas(self.frm_Applicant2Parent, bg=self.config.COLOR_MENU_BACKGROUND,highlightthickness=0, relief='ridge')
                    self.frm_Applicant2 = ttk.Frame(self.frm_Applicant2Canvas)
                    scrollbar_y_Applicant2 = ttk.Scrollbar(self.frm_Applicant2Parent, orient=tk.VERTICAL, command=self.frm_Applicant2Canvas.yview)
                    scrollbar_x_Applicant2 = ttk.Scrollbar(self.frm_Applicant2Parent, orient=tk.HORIZONTAL, command=self.frm_Applicant2Canvas.xview)
                    scrollbar_y_Applicant2.pack(side=tk.RIGHT, fill="y")
                    scrollbar_x_Applicant2.pack(side=tk.BOTTOM, fill="x")
                    self.frm_Applicant2Canvas.pack(expand=tk.TRUE, fill="both",pady=(5,3), padx=(10,10))
                    self.frm_Applicant2.columnconfigure(0, weight=1)
                    self.frm_Applicant2.rowconfigure(0, weight=1)
                    self.frm_Applicant2.rowconfigure(1, weight=1)
                    self.frm_Applicant2.rowconfigure(2, weight=1)
                    self.frm_Applicant2.rowconfigure(3, weight=1)
                    self.frm_Applicant2.rowconfigure(4, weight=1)
                    self.frm_Applicant2.rowconfigure(5, weight=100)                                
                    ttk.Frame(self.frm_Applicant2, height=10).grid(row=0, column=0, sticky=tk.E+tk.W)
                    ttk.Label(self.frm_Applicant2, text="Applicant 2", textvariable=self.varApplicant2, style="H1.TLabel").grid(row=1, column=0, sticky=tk.N+tk.W)
                    ttk.Frame(self.frm_Applicant2, height=10).grid(row=2, column=0, sticky=tk.E+tk.W)
                    ttk.Frame(self.frm_Applicant2, style="Separator.TFrame", height=1).grid(row=3, column=0, sticky=tk.E+tk.W)
                    ttk.Frame(self.frm_Applicant2, height=10).grid(row=4, column=0, sticky=tk.E+tk.W)
                    frmInnerContentFrame2 = ttk.Frame(self.frm_Applicant2,name="frmInnerContentFrame2" )
                    frmInnerContentFrame2.grid(row=5, column=0, sticky=tk.E+tk.W+tk.N+tk.S)            
                    self.SkipTable=0
                    self.ContainerFrame.update()
                    self.varError_.insert(tk.END,"\nGenrating Control (Applicant 2)")
                    self.fnc_Read_PersonalDetails(frmInnerContentFrame2, 2)
                    self.ApplicantTab.add(self.frm_Applicant2Parent, text ='Applicant 2')
                    self.frm_Applicant2Canvas.configure(yscrollcommand=scrollbar_y_Applicant2.set,xscrollcommand=scrollbar_x_Applicant2.set)
                    self.frm_Applicant2Canvas.bind("<Configure>",  lambda e: self.frm_Applicant2Canvas.configure(scrollregion=self.frm_Applicant2Canvas.bbox("all")))
                    self.frm_Applicant2Canvas.bind_all("<MouseWheel>",   lambda e: self.OnMouseWheel1(e,2) )
                    self.frm_Applicant2Canvas.create_window((0, 0), window=self.frm_Applicant2, anchor='nw')
                    self.ContainerFrame.update()
                self.varError_.insert(tk.END,"\nDone")
            #self.ApplicantTab.update_idletasks()
        except Exception as ex:
            print(ex)
            self.varError_.insert(tk.END,ex)

    def save_data(self):
        if not os.path.exists(self.config.FilePath):
            os.makedirs(self.config.FilePath)
        if(self.varFileName.get()==""):
            messagebox.showerror("Required", "Please add FileName")
            return
        if os.path.isfile(os.path.join(self.config.FilePath, self.varFileName.get()+".json")):
            messagebox.showerror("Already Exists", "FileName already Exists")
            return

        with io.open(os.path.join(self.config.FilePath, self.config.DataFileName)) as fp:
            self.varAllDataFile = json.load(fp)
            if(self.varAllDataFile==None):                
                self.varAllDataFile=[]

        varAllDataFileDetails ={}   
        varAllDataFileDetails.update({"FileName":self.varFileName.get(),"ApplicantType":self.varApplicantType.get(), "TemplateType":self.varTemplateType.get(),"CreationDt": datetime.now().strftime("%d-%b-%Y %H:%M:%S"),"ModifyDt": datetime.now().strftime("%d-%b-%Y %H:%M:%S")}) 
        self.varAllDataFile.append(varAllDataFileDetails)
        

        TotalApplicant=1
        if(self.varApplicantType.get()=="Co Applicant"):
            TotalApplicant=2
        AllData=[]
        for ApplicantId in range(1,TotalApplicant+1):            
            ApplicantData={}            
            ApplicantData.update({"ApplicantId":ApplicantId})                
            ApplicantData.update({"PersonalDetails":self.fnc_Save_PersonalDetails(ApplicantId)})
            ApplicantData.update({"ContactDetails":self.fnc_Save_ContactDetails(ApplicantId)})
            ApplicantData.update({"CurrentAddress":self.fnc_Save_CurrentAddress(ApplicantId)})
            ApplicantData.update({"PreviousAddress":self.fnc_Save_PreviousAddress(ApplicantId)})
            ApplicantData.update({"ProfessionalContacts":self.fnc_Save_ProfessionalContacts(ApplicantId)})
            ApplicantData.update({"BankAccount":self.fnc_Save_BankAccount(ApplicantId)})
            ApplicantData.update({"FamilyAndDependants":self.fnc_Save_FamilyAndDependants(ApplicantId)})
            ApplicantData.update({"IDVerification":self.fnc_Save_IDVerification(ApplicantId)})
            ApplicantData.update({"CurrentEmploymentDetails":self.fnc_Save_CurrentEmploymentDetails(ApplicantId)})
            ApplicantData.update({"Assets":self.fnc_Save_Assets(ApplicantId)})
            ApplicantData.update({"Liabilities":self.fnc_Save_Liabilities(ApplicantId)})
            ApplicantData.update({"Expenditure":self.fnc_Save_Expenditure(ApplicantId)})
            ApplicantData.update({"ExistingMortgage":self.fnc_Save_ExistingMortgage(ApplicantId)})
            ApplicantData.update({"MortgageRequirements":self.fnc_Save_MortgageRequirements(ApplicantId)})
            AllData.append(ApplicantData)

        with open(os.path.join(self.config.FilePath, self.varFileName.get()+".json"), 'w', encoding='utf-8') as f:
            json.dump(AllData, f, ensure_ascii=False, indent=4,separators=(',',': '))
            with open(os.path.join(self.config.FilePath, self.config.DataFileName), 'w', encoding='utf-8') as f1:
                json.dump(self.varAllDataFile, f1, ensure_ascii=False, indent=4,separators=(',',': '))                
                tk.messagebox.showinfo("showinfo", "Save Successfully")
        
            
    def checkKey(self,dict, key):      
        if key in dict.keys():
            return True
        else:
            return False

    def fnc_Save_PersonalDetails(self,ApplicantId):
        PersonalDetails={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmDetailFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children,"frmPersonalDetailsFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["frmPersonalDetailsFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            for  x in self.config.IO_Name_PersonalDetails: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_PersonalDetails_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                PersonalDetails.update({HeaderName:controlVal})                        
        return PersonalDetails

    def fnc_Save_ContactDetails(self,ApplicantId):
        ContactDetails={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmDetailFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children,"frmContactDetailFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["frmContactDetailFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            for  x in self.config.IO_Name_ContactDetails: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_ContactDetails_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                ContactDetails.update({HeaderName:controlVal})                
        
        return ContactDetails

    def fnc_Save_CurrentAddress(self,ApplicantId):
        CurrentAddress={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmDetailFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children,"tab_Section_Address_"+str(ApplicantId))):
                        if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["tab_Section_Address_"+str(ApplicantId)].children,"frmCurrentAddressFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["tab_Section_Address_"+str(ApplicantId)].children["frmCurrentAddressFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            for  x in self.config.IO_Name_CurrentAddress: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_CurrentAddress_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                CurrentAddress.update({HeaderName:controlVal})                
        return CurrentAddress

    def fnc_Save_PreviousAddress(self,ApplicantId):
        PreviousAdd=[]
        for M in range(1,5):
            tempData=self.fnc_Save_PreviousAddressDetail(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    PreviousAdd.append(tempData)        
        return PreviousAdd

    def fnc_Save_PreviousAddressDetail(self,ApplicantId,MemberId):
        CurrentAddress={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmDetailFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children,"tab_Section_Address_"+str(ApplicantId))):
                        if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["tab_Section_Address_"+str(ApplicantId)].children,"frmPreviousAddressFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["tab_Section_Address_"+str(ApplicantId)].children["frmPreviousAddressFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_PreviousAddress_"+str(MemberId)+"_"+str(ApplicantId)+"Address Line 1".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            for  x in self.config.IO_Name_PreviousAddress: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_PreviousAddress_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                CurrentAddress.update({HeaderName:controlVal})                
        return CurrentAddress

    def fnc_Save_ProfessionalContacts(self,ApplicantId):
        ProfessionalContacts=[]
        for M in range(1,10):
            tempData=self.fnc_Save_ProfessionalContactsDetail(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    ProfessionalContacts.append(tempData)              
        return ProfessionalContacts

    def fnc_Save_ProfessionalContactsDetail(self,ApplicantId,MemberId):
        ProfessionalContacts={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmDetailFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children,"tab_Section_Address_"+str(ApplicantId))):
                        if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["tab_Section_Address_"+str(ApplicantId)].children,"frmProfessionalContactsFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["tab_Section_Address_"+str(ApplicantId)].children["frmProfessionalContactsFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_ProfessionalContacts_"+str(MemberId)+"_"+str(ApplicantId)+"Address Line 1".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            for  x in self.config.IO_Name_ProfessionalContacts: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_ProfessionalContacts_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                ProfessionalContacts.update({HeaderName:controlVal})                
        return ProfessionalContacts

    def fnc_Save_BankAccount(self,ApplicantId):
        BankAccount=[]
        for M in range(1,15):
            tempData=self.fnc_Save_BankAccountDetails(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    BankAccount.append(tempData)                
        return BankAccount

    def fnc_Save_BankAccountDetails(self,ApplicantId,MemberId):
        BankAccount={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmDetailFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children,"tab_Section_Address_"+str(ApplicantId))):
                        if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["tab_Section_Address_"+str(ApplicantId)].children,"frmBankDetailFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmDetailFrame_"+str(ApplicantId)].children["tab_Section_Address_"+str(ApplicantId)].children["frmBankDetailFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_BankAccountDetails_"+str(MemberId)+"_"+str(ApplicantId)+"Owner".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            for  x in self.config.IO_Name_BankAccountDetails: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_BankAccountDetails_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                BankAccount.update({HeaderName:controlVal})                
        return BankAccount

    def fnc_Save_FamilyAndDependants(self,ApplicantId):
        BankAccount=[]
        for M in range(1,15):
            tempData=self.fnc_Save_FamilyAndDependantsDetails(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    BankAccount.append(tempData)        
        
        return BankAccount

    def fnc_Save_FamilyAndDependantsDetails(self,ApplicantId,MemberId):
        BankAccount={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmFamilyAndDependantsrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmFamilyAndDependantsrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_FamilyAndDependants_"+str(MemberId)+"_"+str(ApplicantId)+"Date of Birth".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            for  x in self.config.IO_Name_FamilyAndDependants: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_FamilyAndDependants_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                BankAccount.update({HeaderName:controlVal})                
        return BankAccount

    def fnc_Save_IDVerification(self,ApplicantId):
        IDVerification={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmIDVerificationFrame_"+str(ApplicantId))):                    
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmIDVerificationFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            for  x in self.config.IO_Name_IDVerification: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_IDVerification_1_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                IDVerification.update({HeaderName:controlVal})                
        return IDVerification

    def fnc_Save_CurrentEmploymentDetails(self,ApplicantId):
        CurrentEmploymentDetails={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmCurrentEmploymentDetailsFrame_"+str(ApplicantId))):                    
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmCurrentEmploymentDetailsFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            for  x in self.config.IO_Name_CurrentEmploymentDetails: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_CurrentEmploymentDetails_1_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                CurrentEmploymentDetails.update({HeaderName:controlVal})                
        return CurrentEmploymentDetails

    def fnc_Save_Assets(self,ApplicantId):
        Assets=[]
        for M in range(1,25):
            tempData=self.fnc_Save_AssetDetails(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    Assets.append(tempData)                
        return Assets

    def fnc_Save_AssetDetails(self,ApplicantId,MemberId):
        AssetDetails={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmAssetsLiabilitiesFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmAssetsLiabilitiesFrame_"+str(ApplicantId)].children,"frmAssetsFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmAssetsLiabilitiesFrame_"+str(ApplicantId)].children["frmAssetsFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_Assets_"+str(MemberId)+"_"+str(ApplicantId)+"Category".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            for  x in self.config.IO_Name_Assets: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_Assets_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                AssetDetails.update({HeaderName:controlVal})                
        return AssetDetails

    def fnc_Save_Liabilities(self,ApplicantId):
        Liabilities=[]
        for M in range(1,25):
            tempData=self.fnc_Save_LiabilitieDetails(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    Liabilities.append(tempData)                
        return Liabilities

    def fnc_Save_LiabilitieDetails(self,ApplicantId,MemberId):
        LiabilitieDetails={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmAssetsLiabilitiesFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmAssetsLiabilitiesFrame_"+str(ApplicantId)].children,"frmLiabilitiesFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmAssetsLiabilitiesFrame_"+str(ApplicantId)].children["frmLiabilitiesFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_Liabilities_"+str(MemberId)+"_"+str(ApplicantId)+"Owner".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            for  x in self.config.IO_Name_Liabilities: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_Liabilities_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                LiabilitieDetails.update({HeaderName:controlVal})                
        return LiabilitieDetails

    def fnc_Save_Expenditure(self,ApplicantId):
        Expenditure=[]
        for M in range(1,25):
            tempData=self.fnc_Save_ExpenditureDetails(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    Expenditure.append(tempData)                
        return Expenditure

    def fnc_Save_ExpenditureDetails(self,ApplicantId,MemberId):
        ExpenditureDetails={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmAssetsLiabilitiesFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmAssetsLiabilitiesFrame_"+str(ApplicantId)].children,"frmExpenditureFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmAssetsLiabilitiesFrame_"+str(ApplicantId)].children["frmExpenditureFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_Expenditure_"+str(MemberId)+"_"+str(ApplicantId)+"Owner".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            elif(ApplicantId>1 and frmInnerContentFrame.children[controlName].get()=="Joint"):
                                return None
                            for  x in self.config.IO_Name_Expenditure: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_Expenditure_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                ExpenditureDetails.update({HeaderName:controlVal})                
        return ExpenditureDetails

    def fnc_Save_ExistingMortgage(self,ApplicantId):
        ExistingMortgage=[]
        for M in range(1,25):
            tempData=self.fnc_Save_ExistingMortgageDetails(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    ExistingMortgage.append(tempData)                
        return ExistingMortgage

    def fnc_Save_ExistingMortgageDetails(self,ApplicantId,MemberId):
        ExpenditureDetails={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmMortgageFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmMortgageFrame_"+str(ApplicantId)].children,"frmExistingMortgageFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmMortgageFrame_"+str(ApplicantId)].children["frmExistingMortgageFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_ExistingMortgage_"+str(MemberId)+"_"+str(ApplicantId)+"Owner".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            for  x in self.config.IO_Name_ExistingMortgage: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_ExistingMortgage_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                ExpenditureDetails.update({HeaderName:controlVal})                
        return ExpenditureDetails

    def fnc_Save_MortgageRequirements(self,ApplicantId):
        ExistingMortgage=[]
        for M in range(1,25):
            tempData=self.fnc_Save_MortgageRequirementDetails(ApplicantId,M)
            if(tempData != None):
                if(bool(tempData)):
                    ExistingMortgage.append(tempData)                
        return ExistingMortgage

    def fnc_Save_MortgageRequirementDetails(self,ApplicantId,MemberId):
        ExpenditureDetails={}
        TabFrame,frmInnerContentFrame=None,None
        if(ApplicantId==1):
            TabFrame=self.frm_Applicant1
        elif(ApplicantId==2):
            TabFrame=self.frm_Applicant2
        if(self.checkKey(TabFrame.children,"frmInnerContentFrame"+str(ApplicantId))):
            if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children,"tab_Section_"+str(ApplicantId))):
                if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children,"frmMortgageFrame_"+str(ApplicantId))):
                    if(self.checkKey(TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmMortgageFrame_"+str(ApplicantId)].children,"frmMortgageRequirementsFrame_"+str(ApplicantId))):
                            frmInnerContentFrame=TabFrame.children["frmInnerContentFrame"+str(ApplicantId)].children["tab_Section_"+str(ApplicantId)].children["frmMortgageFrame_"+str(ApplicantId)].children["frmMortgageRequirementsFrame_"+str(ApplicantId)]
                            controlName,controlVal,HeaderName='','',''
                            controlName= "txt_MortgageRequirements_"+str(MemberId)+"_"+str(ApplicantId)+"Owner".strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                            
                            if not (self.checkKey(frmInnerContentFrame.children,controlName)):
                                return None
                            for  x in self.config.IO_Name_MortgageRequirements: 
                                controlName,controlVal,HeaderName='','',''
                                controlName= "txt_MortgageRequirements_"+str(MemberId)+"_"+str(ApplicantId)+x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                HeaderName=x.strip().replace(' ','_').replace('[M]', '').replace('[D]', '')
                                if (self.checkKey(frmInnerContentFrame.children,controlName)):
                                    controlVal=frmInnerContentFrame.children[controlName].get()
                                ExpenditureDetails.update({HeaderName:controlVal})                
        return ExpenditureDetails


    def fncCreateItems(self):
        self.ContainerFrame.columnconfigure(0, weight=1)
        self.ContainerFrame.columnconfigure(1, weight=1)
        self.ContainerFrame.columnconfigure(2, weight=100)
        self.ContainerFrame.rowconfigure(0, weight=1)
        self.ContainerFrame.rowconfigure(1, weight=1)
        self.ContainerFrame.rowconfigure(2, weight=1)
        self.ContainerFrame.rowconfigure(3, weight=1)
        self.ContainerFrame.rowconfigure(4, weight=100)
        self.ContainerFrame.rowconfigure(5, weight=1)
        self.varApplicantType.set("Co Applicant")
        self.varTemplateType.set("IO Template")
        
        ttk.Label(self.ContainerFrame, text="File Name").grid(row=0, column=0, sticky=tk.N+tk.S+tk.E, pady=(5, 2), padx=(10, 10))
        ttk.Entry(self.ContainerFrame, name="txtFileName", textvariable=self.varFileName, width=25).grid(row=0, column=1, sticky=tk.N+tk.S+tk.W, pady=(5, 2), padx=(10, 10))
        ttk.Label(self.ContainerFrame, text="Template Type").grid(row=1, column=0, sticky=tk.N+tk.S+tk.E, pady=(5, 2), padx=(10, 10))
        cmbTemplateType = ttk.Combobox(self.ContainerFrame, width=23, textvariable=self.varTemplateType)
        # Adding combobox drop down list
        cmbTemplateType['values'] = ('IO Template', 'Fact Find')
        cmbTemplateType.grid(row=1, column=1, sticky=tk.N+tk.S+tk.W, pady=(5, 2), padx=(10, 10))
        ttk.Label(self.ContainerFrame, text="Applicant Type").grid(row=2, column=0, sticky=tk.N+tk.S+tk.E, pady=(5, 2), padx=(10, 10))

        cmbApplicantType = ttk.Combobox(self.ContainerFrame, width=23, textvariable=self.varApplicantType)
        cmbApplicantType['values'] = ('Single', 'Co Applicant')
        cmbApplicantType.grid(row=2, column=1, sticky=tk.N+tk.S+tk.W, pady=(5, 2), padx=(10, 10))
        cmbApplicantType.bind("<<ComboboxSelected>>",lambda e: self.hide_unhide_applicant(e))

        btnFrame = ttk.Frame(self.ContainerFrame)
        btnFrame.grid(row=0, rowspan=3, column=2, sticky=tk.N+tk.S+tk.W)

        btnImport = ttk.Button(btnFrame, text="Import",width=10,  command=lambda: self.open_file())
        #btnLoad = ttk.Button(btnFrame, text="Load", width=10,command=lambda: self.open_file())
        btnSave = ttk.Button(btnFrame, text="Save", width=10,command=lambda: self.save_data())
        btnReset = ttk.Button(btnFrame, text="Reset",width=10, command=lambda: self.reset_data())
        
        btnImport.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W, padx=(5, 5), pady=(5, 5))
        #btnLoad.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W, padx=(5, 5), pady=(5, 5))
        btnSave.grid(row=1, column=0, sticky=tk.N+tk.S+tk.W, padx=(5, 5), pady=(5, 5))
        btnReset.grid(row=1, column=1, sticky=tk.N+tk.S+tk.W, padx=(5, 5), pady=(5, 5))
        ttk.Frame(self.ContainerFrame,height=5).grid(row=3,column=0,columnspan=3,sticky=tk.W+tk.E)
        self.ApplicantTab= ttk.Notebook(self.ContainerFrame, height=600)
        self.ApplicantTab.grid(row=4,column=0,columnspan=3,sticky=tk.N+tk.S+tk.W+tk.E)
        
        self.varError_=tk.Text(self.ContainerFrame,width=100, height=4)
        self.varError_.grid(row=5, column=0,columnspan=3 ,sticky=tk.N+tk.S+tk.W+tk.E, pady=(5, 2), padx=(10, 10))


if __name__ == '__main__':
    config = Gc.GenerateConfig()

    #ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    sizex = 700
    sizey = 500
    posx = 100
    posy = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    myframe = tk.Frame(root, relief=tk.GROOVE, width=500, height=600, bd=1)
    myframe.pack(fill="both", expand=tk.TRUE, anchor=tk.N+tk.W)
    config.set_theme(None, myframe)
    ImportData(myframe, config)
    root.mainloop()
