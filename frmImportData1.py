#import PyPDF2 as pdf
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage

import ctypes
from email.headerregistry import Address
import os
from cv2 import merge
from numpy import pad
import tabula
#from tabula import read_pdf
#from tabulate import tabulate
import pandas as pd
import io
import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import RAISED, ttk
import GenerateConfig as Gc
import json

import tkinter as tk


class ImportData:
    config = None
    varApplicant1 = None
    varApplicant2 = None
    varTemplateType = None
    varApplicantType = None
    varStarttingPoint = 0
    varAllJsonData = []
    varId = None
    canvas = None
    frame = None
    ContainerCanvas = None
    ContainerFrame = None
    Parent_Height = 500
    Parent_Width = 600
    tables = None

    def __init__(self, Container, config):
        self.config = config
        self.varTemplateType = tk.StringVar()
        self.varApplicantType = tk.StringVar()
        self.varApplicant1 = tk.StringVar()
        self.varApplicant2 = tk.StringVar()
        self.varId = tk.StringVar()

        #self.ContainerCanvas = tk.Canvas(Container, bg=self.config.COLOR_MENU_BACKGROUND,highlightthickness=0, relief='ridge')
        self.ContainerCanvas = tk.Canvas(Container, bg=self.config.COLOR_MENU_BACKGROUND,highlightthickness=0, relief='ridge',width=Container["width"], height=Container["height"])
        self.ContainerFrame = ttk.Frame(self.ContainerCanvas,width=Container["width"], height=Container["height"])
        self.scrollbar_y = ttk.Scrollbar(Container, orient=tk.VERTICAL, command=self.ContainerCanvas.yview)
        scrollbar_x = ttk.Scrollbar(Container, orient=tk.HORIZONTAL, command=self.ContainerCanvas.xview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill="y")
        scrollbar_x.pack(side=tk.BOTTOM, fill="x")
        self.ContainerCanvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.ContainerCanvas.pack(expand=tk.TRUE, fill="both", pady=(5,3))
        self.ContainerCanvas.create_window((0, 0), window=self.ContainerFrame, anchor='n')
        self.ContainerFrame.bind("<Configure>", self.fnc_resizeScroll)
        self.ContainerCanvas.bind_all("<MouseWheel>", self.OnMouseWheel)
        self.fncCreateItems()
        
    def OnMouseWheel(self, event):
        self.ContainerCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def fnc_resizeScroll(self, event):
        self.ContainerCanvas.configure(scrollregion=self.ContainerCanvas.bbox(
            "all"), width=self.Parent_Width, height=self.Parent_Height)

    def fnc_Read_PersonalDetails(self, ParentContainer, Applicantid):
        
        frmTopFrame = ttk.Notebook(ParentContainer,name="tab_Section_"+str(Applicantid),height=500)        
        frmTopFrame.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)
        if(self.varTemplateType.get() == "IO Template"):            
            
            frmDetailFrame = ttk.Frame(frmTopFrame)            
            
            frmPersonalDetailsFrame = ttk.LabelFrame(frmDetailFrame, text="Personal Details", style="Details.TLabelframe")
            frmPersonalDetailsFrame.grid(row=0, column=0, sticky=tk.N+tk.W, pady=(10, 10), padx=(10, 10))
            self.fnc_Read_PersonalDetails_IO_Template(frmPersonalDetailsFrame, Applicantid)
            
            frmAddressFrame = ttk.Notebook(frmDetailFrame,name="tab_Section_Address_"+str(Applicantid))
            # Add Current Address
            frmCurrentAddressFrame = ttk.Frame(frmAddressFrame)            
            self.fnc_Read_CurrentAddress_IO_Template(frmCurrentAddressFrame, Applicantid)
            frmAddressFrame.add(frmCurrentAddressFrame, text ='Current Address')            

            # Add Previous Address
            frmPreviousAddressFrame = ttk.Frame(frmAddressFrame)
            self.fnc_Read_PreviousAddress_IO_Template(frmPreviousAddressFrame, Applicantid)
            frmAddressFrame.add(frmPreviousAddressFrame, text ='Previous Address')
            # Contact Details
            frmContactDetailFrame = ttk.LabelFrame(frmDetailFrame, text="Contact Details", style="Details.TLabelframe")            
            self.fnc_Read_ContactDetails_IO_Template(frmContactDetailFrame, Applicantid)
            frmContactDetailFrame.grid(row=1, column=0, sticky=tk.N+tk.W, pady=(10, 10), padx=(10, 10))

            
            # ProfessionalContacts
            frmProfessionalContactsFrame = ttk.Frame(frmAddressFrame)
            self.fnc_Read_ProfessionalContact_IO_Template(frmProfessionalContactsFrame, Applicantid)
            frmAddressFrame.add(frmProfessionalContactsFrame, text ='Professional Contacts')
            # Bank Details
            frmBankDetailFrame = ttk.Frame(frmAddressFrame)
            self.fnc_Read_BankAccountDetails_IO_Template(frmBankDetailFrame, Applicantid)
            frmAddressFrame.add(frmBankDetailFrame, text ='Bank Details')

            frmAddressFrame.grid(row=2, column=0, sticky=tk.N+tk.W+tk.E)
            frmTopFrame.add(frmDetailFrame, text ='Details')

            

            
            # Family And Dependants
            frmFamilyAndDependantsrame = ttk.LabelFrame(frmTopFrame, text="Family And Dependants", style="Details.TLabelframe")
            self.fnc_Read_FamilyAndDependants_IO_Template(frmFamilyAndDependantsrame, Applicantid)
            frmTopFrame.add(frmFamilyAndDependantsrame, text ='Family')
            # ID Verfication
            frmIDVerificationFrame = ttk.Frame(frmTopFrame)
            self.fnc_Read_IDVerification_IO_Template(frmIDVerificationFrame, Applicantid)
            frmTopFrame.add(frmIDVerificationFrame, text ='ID Verification')

            # Current Employement Details
            frmCurrentEmployementDetailsFrame = ttk.LabelFrame(frmTopFrame,text="Current Employement Details",style="Details.TLabelframe")
            self.fnc_Read_CurrentEmployementDetails_IO_Template(frmCurrentEmployementDetailsFrame, Applicantid)           
            frmTopFrame.add(frmCurrentEmployementDetailsFrame, text ='Employement')


            frmAssetsLiabilitiesFrame=ttk.Notebook(frmTopFrame)            
            
            # Assets Details            
            frmAssetsFrame = ttk.Frame(frmAssetsLiabilitiesFrame)            
            self.fnc_Read_Assets_IO_Template(frmAssetsFrame, Applicantid)            
            frmAssetsLiabilitiesFrame.add(frmAssetsFrame, text ='Assets')

            # Liabilities
            frmLiabilitiesFrame = ttk.Frame(frmAssetsLiabilitiesFrame)            
            self.fnc_Read_Liabilities_IO_Template(frmLiabilitiesFrame, Applicantid)
            frmAssetsLiabilitiesFrame.add(frmLiabilitiesFrame, text ='Liabilities')
            # Expenditure
            frmExpenditureFrame = ttk.Frame(frmAssetsLiabilitiesFrame)            
            self.fnc_Read_Expenditure_IO_Template(frmExpenditureFrame, Applicantid)
            frmAssetsLiabilitiesFrame.add(frmExpenditureFrame, text ='Expenditure')
            frmTopFrame.add(frmAssetsLiabilitiesFrame, text ='Assets/Liabilities')

            frmMortgageFrame = ttk.Notebook(frmTopFrame)
            # ExistingMortgage
            frmExistingMortgageFrame = ttk.Frame(frmMortgageFrame)
            self.fnc_Read_ExistingMortgageDetails_IO_Template(frmExistingMortgageFrame, Applicantid)
            frmMortgageFrame.add(frmExistingMortgageFrame, text ='Existing Mortgage')
            #Mortage Requirement
            frmMortgageRequirementsFrame = ttk.Frame(frmMortgageFrame)            
            self.fnc_Read_MortgageRequirements_IO_Template(frmMortgageRequirementsFrame, Applicantid)
            frmMortgageFrame.add(frmMortgageRequirementsFrame, text ='Mortgage Requirements')
            frmTopFrame.add(frmMortgageFrame, text ='Mortgage')

            
                
    def fnc_GenrateControl(self, ParentContainer, DetailTable, FindingColumnIndex, FromPosition, IO_Name, IO_Template_Name, Suffix):
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
        if (not("[M]" in IO_Name)):
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
        entrybox.insert(0, FindingValue)
        entrybox.grid(row=self.gridrowindex, column=(
            self.gridcolumnindex + 1), sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))

    def fnc_GenrateControl_Vertical(self, ParentContainer, DetailTable, FindingColumnIndex, FindingRowIndex, IO_Name, IO_Template_Name, Suffix):
        if(self.IsEvenColumn):
            self.IsEvenColumn = False
            self.gridcolumnindex = 2
        else:
            self.IsEvenColumn = True
            self.gridcolumnindex = 0
            self.gridrowindex = self.gridrowindex+1
        FindingValue = ""
        if (not("[M]" in IO_Name) and FindingRowIndex > 0):
            for i, j in DetailTable.iterrows():
                if(i < FindingRowIndex):
                    continue
                try:
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
        entrybox.insert(0, FindingValue)
        entrybox.grid(row=self.gridrowindex, column=(
            self.gridcolumnindex + 1), sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))

    def fnc_GenrateControl_Vertical_asset(self, ParentContainer, FindingValue, IO_Name, Suffix):
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
        entrybox.insert(0, FindingValue)
        entrybox.grid(row=self.gridrowindex, column=(
            self.gridcolumnindex + 1), sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))


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
            if(DetailTable.columns[0] == "rofessional Contacts"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Company Name"):
                    return True
        elif(tableName == "Bank Account Details"):
            if(DetailTable.columns[0] == "ank Account Details"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Bank Name" and row[0] =="Account Holder(s)"):
                    return True
        elif(tableName == "Family And Dependants"):
            if(DetailTable.columns[0] == "amily And Dependants"):
                return True
            if(DetailTable.columns[0] == "Full Name" and DetailTable.columns[1] == "Date of Birth" and DetailTable.columns[2] == "Age"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Full Name" and row[1] == "Date of Birth" and row[2] == "Age"):
                    return True
        elif(tableName == "ID Verification"):
            if(DetailTable.columns[0] == "D Verification"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Original Driving Licence Seen" or row[0] == "Driving Licence Ref"):
                    return True
        elif(tableName == "Electronic ID Verification"):
            if(DetailTable.columns[0] == "lectronic ID Verification"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "ID Check Completed Date" or row[0] == "ID Check Expiry Date"):
                    return True
        elif(tableName == "Current Employment Details"):
            if(DetailTable.columns[0] == "urrent Employment Details"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Highest rate of income tax paid (%)" or row[0] == "Employment Status" or row[0] == "Most Recent Annual Accounts Net Profit"):
                    return True
        elif(tableName == "Assets"):
            if(DetailTable.columns[0] == "ssets" or DetailTable.columns[0] == "Do you have any assets?" ):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Do you have any assets?" ):
                    return True
        elif(tableName == "Assets1"):
            if(DetailTable.columns[0] == "Owner" or DetailTable.columns[1] == "Category" ):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Owner" or row[1] == "Category"):
                    return True
        elif(tableName == "Liabilities"):
            if(DetailTable.columns[0] == "iabilities" or DetailTable.columns[0] == "Do you have any liabilities?" ):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Do you have any liabilities?"):
                    return True
        elif(tableName == "Liabilities1"):            
            for i, row in DetailTable.iterrows():
                if(row[0] == "Owner" or row[0] == "Client does not wish to disclose"):
                    return True
        elif(tableName == "Income"):            
            if(DetailTable.columns[0] == "ncome" or DetailTable.columns[0] == "Do you have any liabilities?" ):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Total Gross Annual Earnings or Net Relevant Earnings"):
                    return True
        elif(tableName == "Expenditure"):
            if(DetailTable.columns[0] == "xpenditure" or DetailTable.columns[0] == "Do you wish to carry out a detailed expenditure analysis? If 'no' then please" ):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Do you wish to carry out a detailed expenditure analysis? If 'no' then please" ):
                    return True
        elif(tableName == "Expenditure1"):
            if(DetailTable.columns[0] == "Category" or DetailTable.columns[1] == "Owner" ):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Category" or row[1] == "Owner"):
                    return True
        elif(tableName == "Expenditure Details"):
            if(DetailTable.columns[0] == "xpenditure Details"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Calculated Total Monthly Household Expenditure" ):
                    return True
        elif(tableName == "Current Monthly Cash Flow"):
            if(DetailTable.columns[0] == "urrent Monthly Cash Flow"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Total Net Monthly Income" ):
                    return True
        elif(tableName == "Existing Mortgage Details"):            
            if(DetailTable.columns[0] == "xisting Mortgage Details" or DetailTable.columns[0] == "Do you have an existing mortgage?" ):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Do you have an existing mortgage?"):
                    return True
        elif(tableName == "Existing Mortgage Details1"):
            if(DetailTable.columns[0] == "Owner"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Owner"):
                    return True
        elif(tableName == "Mortgage Requirements"):            
            if(DetailTable.columns[0] == "ortgage Requirements"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Unique Identifier"):                    
                    return True
        elif(tableName == "Property Details"):            
            if(DetailTable.columns[0] == "roperty Details"):
                return True    
        elif(tableName == "Mortgage Preferences & Attitude to Risk"):            
            if(DetailTable.columns[0] == "ortgage Preferences & Attitude to Risk"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Do you want the certainty of the mortgage being repaid at the end of the term?"):
                    return True        
        elif(tableName == "Which of the following are important to you?"):            
            if(DetailTable.columns[0] == "hich of the following are important to you?"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "The maximum early redemption period I would accept is"):
                    return True        
        elif(tableName == "Final Salary Pension Schemes"):            
            if(DetailTable.columns[0] == "inal Salary Pension Schemes" or DetailTable.columns[0]=="Do you have any existing final salary schemes?"):
                return True
            for i, row in DetailTable.iterrows():
                if(row[0] == "Do you have any existing final salary schemes?"):
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
            for ioindex, x in enumerate(self.config.IO_Name_PersonalDetail):
                self.fnc_GenrateControl(ParentContainer, PersonalDetailTable, Applicantid, 0, x,
                                        self.config.IO_Template_PersonalDetail[ioindex], "txt_PersonalDetails_"+str(Applicantid))

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
                    if(row[ColumnIndex] == Adressee):
                        FoundApplicant = True
                    else:
                        if(ColumnIndex+1 <= columnLength-1):
                            return self.fnc_Read_Address_GetRowColumnIndex(DetailTable, PreviousRowIndex, ColumnIndex, Adressee, IsCurrentAddress)
                        else:
                            return self.fnc_Read_Address_GetRowColumnIndex(DetailTable, PreviousRowIndex+10, 0, Adressee, IsCurrentAddress)
                if(FoundApplicant):
                    if(row[0] == "Address Status" and ((IsCurrentAddress and row[ColumnIndex] == "Current Address") or (row[ColumnIndex] == "Previous Address"))):
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
                    if(row[ColumnIndex] == Adressee or row[ColumnIndex] == Adressee+".1" or row[ColumnIndex] == Adressee+".2" or row[ColumnIndex] == Adressee+".3" or (ApplicantId == 1 and row[ColumnIndex] == "Joint")):
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
        IsFound = False
        RowIndex = PreviousRowIndex
        ColumnIndex = PreviousColumnIndex
        CurrentIndex = {"row": RowIndex,
                        "column": ColumnIndex, "IsFound": IsFound}
        for i, row in DetailTable.iterrows():
            try:
                if(i < PreviousRowIndex):
                    continue
                if((row[ColumnIndex] == Adressee or row[ColumnIndex] == "Joint") and row[KeyColumn] == KeyData):
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

    def fnc_Read_CurrentAddress_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem = False, False
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

    def fnc_Read_PreviousAddress_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem = False, False
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
                    for ioindex, x in enumerate(self.config.IO_Name_PreviousAddress):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_PreviousAddress[ioindex], "txt_PreviousAddress_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1

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
        foundTable, foundItem = False, False
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
                    for ioindex, x in enumerate(self.config.IO_Name_ProfessionalContacts):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_ProfessionalContacts[ioindex], "txt_ProfessionalContacts_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                    PreviousColumnIndex+1
                PreviousAddressCounter += 1

    def fnc_Read_BankAccountDetails_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem = False, False
        self.RecursionDepthCount, self.CurrentDepthCount = 15, 0
        for tableindex, table in enumerate(self.tables):
            if(tableindex<self.SkipTable):
                continue
            if(table.columns[0] == "ank Account Details"):
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
                    for ioindex, x in enumerate(self.config.IO_Name_BankAccountDetails):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_BankAccountDetails[
                                                ioindex], "txt_BankAccountDetails_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
    
    def fnc_Read_FamilyAndDependants_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        DetailTable = None
        foundTable, foundItem = False, False
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
                        membercounter=membercounter+1
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 0,i, "Full Name",
                                                 "Full Name", "txt_FamilyAndDependants_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 1,i, "Date of Birth",
                                                 "Date of Birth", "txt_FamilyAndDependants_"+str(Applicantid)+"_"+str(membercounter))                        
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 2,i, "Age",
                                                 "Age", "txt_FamilyAndDependants_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 3,i, "Relationship",
                                                 "Relationship", "txt_FamilyAndDependants_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 4,i, "Related To",
                                                 "Related To", "txt_FamilyAndDependants_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 5,i, "Financially Dependant",
                                                 "Financially Dependant", "txt_FamilyAndDependants_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical(ParentContainer, DetailTable, 7,i, "Dependant Living with Client",
                                                 "Dependant Living with Client", "txt_FamilyAndDependants_"+str(Applicantid)+"_"+str(membercounter))
                        self.gridrowindex = self.gridrowindex+1
                        ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                        self.gridrowindex = self.gridrowindex+1
                        self.IsEvenColumn = False
                except Exception as ex:
                    print("Error", ex) 
            
    def fnc_Read_IDVerification_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem = False, False
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
                    for ioindex, x in enumerate(self.config.IO_Name_IDVerification):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_IDVerification[ioindex], "txt_IDVerification_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1
    
    def fnc_Read_CurrentEmployementDetails_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem = False, False
        
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
                    for ioindex, x in enumerate(self.config.IO_Name_CurrentEmploymentDetails):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x,
                                                self.config.IO_Template_CurrentEmploymentDetails[ioindex], "txt_CurrentEmploymentDetails_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    #ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1

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
        foundTable, foundItem,foundAssetTable = False, False,False
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
        if(foundTable):
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
                        membercounter=membercounter+1
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][0],  DetailTable.iloc[i+1][0] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][0] if(combinedRows>2)else "",DetailTable.iloc[i+3][0] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Owner", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][1],  DetailTable.iloc[i+1][1] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][1] if(combinedRows>2)else "",DetailTable.iloc[i+3][1] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Category", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][2],  DetailTable.iloc[i+1][2] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][2] if(combinedRows>2)else "",DetailTable.iloc[i+3][2] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Related To Address", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 1[M]", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 2[M]", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 3[M]", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Address Line 4[M]", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "City[M]", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Country[M]", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,"", "Postcode[M]", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))

                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][7],  DetailTable.iloc[i+1][7] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][7] if(combinedRows>2)else "",DetailTable.iloc[i+3][7] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Original Value", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][8],  DetailTable.iloc[i+1][8] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][8] if(combinedRows>2)else "",DetailTable.iloc[i+3][8] if(combinedRows>3)else "") 
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Purchased On", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][9],  DetailTable.iloc[i+1][9] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][9] if(combinedRows>2)else "",DetailTable.iloc[i+3][9] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Value", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= self.fnc_combinedRows(combinedRows,DetailTable.iloc[i][10],  DetailTable.iloc[i+1][10] if(combinedRows>1)else "" ,DetailTable.iloc[i+2][10] if(combinedRows>2)else "",DetailTable.iloc[i+3][10] if(combinedRows>3)else "")                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Valuation Date", "txt_Assets_"+str(Applicantid)+"_"+str(membercounter))
                        
                        self.gridrowindex = self.gridrowindex+1
                        ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                        self.gridrowindex = self.gridrowindex+1
                        self.IsEvenColumn = False
                    except Exception as ex:
                        print("Error", ex) 
                    i=i+combinedRows


    def fnc_Read_Liabilities_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem,Liabilities = False, False,False        
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
                    for ioindex, x in enumerate(self.config.IO_Name_Liabilities):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_Liabilities[
                                                ioindex], "txt_Liabilities_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1

    def fnc_Read_Expenditure_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        DetailTable = None
        foundTable, foundItem,Expenditure,membercounter = False, False,False,0
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
        if(foundTable):
            Addressee = self.varApplicant1.get() if (
                Applicantid == 1) else self.varApplicant2.get() if (Applicantid == 2) else ""
            for ioindex, x in enumerate(self.config.IO_Name_Expenditure):
                foundItem = False
                PreviousRowIndex = 0
                if (not("[M]" in x)):
                    tempData = self.fnc_Read_Vertical_GetRowColumnIndex(
                        DetailTable, 0, 1, Addressee, self.config.IO_Template_Expenditure[ioindex], 0)
                    foundItem = tempData["IsFound"]
                    if(foundItem):
                        membercounter=membercounter+1
                        PreviousRowIndex = tempData["row"]                        
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,x, "Category", "txt_Category_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= DetailTable.iloc[PreviousRowIndex][1]
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Owner", "txt_Category_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= DetailTable.iloc[PreviousRowIndex][2]
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Description", "txt_Category_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= DetailTable.iloc[PreviousRowIndex][3]
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Net Amount", "txt_Category_"+str(Applicantid)+"_"+str(membercounter))
                        rowValue= DetailTable.iloc[PreviousRowIndex][4]
                        self.fnc_GenrateControl_Vertical_asset(ParentContainer,rowValue, "Frequency", "txt_Category_"+str(Applicantid)+"_"+str(membercounter))
                        self.gridrowindex = self.gridrowindex+1
                        ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                        self.gridrowindex = self.gridrowindex+1
                        self.IsEvenColumn = False

    def fnc_Read_ExistingMortgageDetails_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem,ExistingMortgageDetails= False, False,False        
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
                    for ioindex, x in enumerate(self.config.IO_Name_ExistingMortgage):
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_ExistingMortgage[
                                                ioindex], "txt_ExistingMortgage_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1

    def fnc_Read_MortgageRequirements_IO_Template(self, ParentContainer, Applicantid):
        self.gridrowindex, self.gridcolumnindex = -1, 0
        columnIndex, rowIndex = 0, 0
        DetailTable = None
        foundTable, foundItem= False, False
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
                    for ioindex, x in enumerate(self.config.IO_Name_MortgageRequirements):                        
                        self.fnc_GenrateControl(ParentContainer, DetailTable, columnIndex, rowIndex, x, self.config.IO_Template_MortgageRequirements[
                                                ioindex], "txt_MortgageRequirements_" + str(PreviousAddressCounter+1)+"_" + str(Applicantid))

                    self.gridrowindex = self.gridrowindex+1
                    ttk.Frame(ParentContainer, style="NormalSeparator.TFrame", height=1).grid(
                        row=self.gridrowindex, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(5, 5))
                PreviousAddressCounter += 1

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


    def hide_unhide_applicant(self):
        yaxis = self.varStarttingPoint
        if(self.varApplicantType.get() == "Single"):
            for x in self.config.IO_Name:
                self.ContainerFrame.children["txtCoApplicant" +
                                             x.strip().replace(' ', '_')].place_forget()
        else:
            for x in self.config.IO_Name:
                self.ContainerFrame.children["txtCoApplicant" + x.strip().replace(
                    ' ', '_')].place(x=400, y=(10+yaxis), anchor=tk.NW)
                yaxis = yaxis+40

    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def open_file(self):
        open_file = askopenfilename(initialdir="d:", title="Open Template", filetypes=[
                                    ('Pdf Files', '*.pdf')])
        if open_file:
            self.tables = tabula.read_pdf(open_file, pages="all")
            self.CurrentAddressFound = False
            frm_Applicant1 = None
            frm_Applicant2 = None
            if "frm_Applicant1" in self.ContainerFrame.children.keys():
                frm_Applicant1 = self.ContainerFrame.children["frm_Applicant1"]
                self.clear_frame(frm_Applicant1)
            else:
                frm_Applicant1 = ttk.Frame(self.ContainerFrame)
            if "frm_Applicant2" in self.ContainerFrame.children.keys():
                frm_Applicant2 = self.ContainerFrame.children["frm_Applicant2"]
                self.clear_frame(frm_Applicant2)
            else:
                frm_Applicant2 = ttk.Frame(self.ContainerFrame)

            frm_Applicant1.columnconfigure(0, weight=1)
            frm_Applicant1.rowconfigure(0, weight=1)
            frm_Applicant1.rowconfigure(1, weight=1)
            frm_Applicant1.rowconfigure(2, weight=100)
            frm_Applicant1.grid_forget()
            frm_Applicant2.columnconfigure(0, weight=1)
            frm_Applicant2.rowconfigure(0, weight=1)
            frm_Applicant2.rowconfigure(1, weight=1)
            frm_Applicant2.rowconfigure(2, weight=100)
            frm_Applicant2.grid_forget()
            
            ttk.Label(frm_Applicant1, text="Applicant 1", textvariable=self.varApplicant1, style="H1.TLabel").grid(
                row=0, column=0, sticky=tk.N+tk.W, pady=(5, 3), padx=(10, 10))
            ttk.Frame(frm_Applicant1, style="Separator.TFrame", height=1).grid(
                row=1, column=0, sticky=tk.E+tk.W, pady=(5, 5))
            frmInnerContentFrame1 = ttk.Frame(frm_Applicant1)
            frmInnerContentFrame1.grid(
                row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S, pady=(10, 10), padx=(10, 10))

            ttk.Label(frm_Applicant2, text="Applicant 2", textvariable=self.varApplicant2, style="H1.TLabel").grid(
                row=0, column=0, sticky=tk.N+tk.W, pady=(5, 3), padx=(10, 10))
            ttk.Frame(frm_Applicant2, style="Separator.TFrame", height=1).grid(
                row=1, column=0, sticky=tk.E+tk.W, pady=(5, 5))
            frmInnerContentFrame2 = ttk.Frame(frm_Applicant2)
            frmInnerContentFrame2.grid(
                row=2, column=0, sticky=tk.E+tk.W+tk.N+tk.S, pady=(10, 10), padx=(10, 10))

            frm_Applicant1.grid(row=4, column=0, columnspan=3,
                                sticky=tk.E+tk.W+tk.N+tk.S)
            self.SkipTable=0
            self.fnc_Read_PersonalDetails(frmInnerContentFrame1, 1)

            if(self.varApplicantType.get() == "Co Applicant"):
                self.SkipTable=0
                frm_Applicant2.grid(
                    row=5, column=0, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)
                self.fnc_Read_PersonalDetails(frmInnerContentFrame2, 2)

    def fncCreateItems(self):
        self.ContainerFrame.columnconfigure(0, weight=1)
        self.ContainerFrame.columnconfigure(1, weight=1)
        self.ContainerFrame.columnconfigure(2, weight=100)
        self.ContainerFrame.rowconfigure(0, weight=1)
        self.ContainerFrame.rowconfigure(1, weight=1)
        self.ContainerFrame.rowconfigure(2, weight=1)
        self.varApplicantType.set("Co Applicant")
        self.varTemplateType.set("IO Template")
        ttk.Label(self.ContainerFrame, text="File Name").grid(
            row=0, column=0, sticky=tk.N+tk.S+tk.E, pady=(5, 2), padx=(10, 10))
        ttk.Entry(self.ContainerFrame, name="txt__Id", textvariable=self.varId, width=25).grid(
            row=0, column=1, sticky=tk.N+tk.S+tk.W, pady=(5, 2), padx=(10, 10))
        ttk.Label(self.ContainerFrame, text="Template Type").grid(
            row=1, column=0, sticky=tk.N+tk.S+tk.E, pady=(5, 2), padx=(10, 10))
        cmbTemplateType = ttk.Combobox(
            self.ContainerFrame, width=23, textvariable=self.varTemplateType)
        # Adding combobox drop down list
        cmbTemplateType['values'] = ('IO Template', 'Fact Find')
        cmbTemplateType.grid(row=1, column=1, sticky=tk.N +
                             tk.S+tk.W, pady=(5, 2), padx=(10, 10))
        ttk.Label(self.ContainerFrame, text="Applicant Type").grid(
            row=2, column=0, sticky=tk.N+tk.S+tk.E, pady=(5, 2), padx=(10, 10))

        cmbApplicantType = ttk.Combobox(
            self.ContainerFrame, width=23, textvariable=self.varApplicantType)
        cmbApplicantType['values'] = ('Single', 'Co Applicant')
        cmbApplicantType.grid(row=2, column=1, sticky=tk.N +
                              tk.S+tk.W, pady=(5, 2), padx=(10, 10))
        cmbApplicantType.bind("<<ComboboxSelected>>",
                              lambda: self.hide_unhide_applicant())

        btnFrame = ttk.Frame(self.ContainerFrame)
        btnFrame.grid(row=0, rowspan=3, column=2, sticky=tk.N+tk.S+tk.W)

        # yaxis=3
        # self.varStarttingPoint=yaxis
        # for x in self.config.IO_Name:
        #     ttk.Label(self.ContainerFrame,  text = x.strip()).grid(row=yaxis,column =0, sticky=tk.N+tk.S+tk.E)
        #     ttk.Entry(self.ContainerFrame,name="txtApplicant"+ x.strip().replace(' ', '_'), width = 25).grid(row=yaxis,column = 1, sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))
        #     ttk.Entry(self.ContainerFrame,name="txtCoApplicant"+ x.strip().replace(' ', '_'), width = 25).grid(row=yaxis,column = 2, sticky=tk.N+tk.S+tk.W, padx=(10, 10), pady=(5, 2))
        #     yaxis=yaxis+1

        btnImport = ttk.Button(btnFrame, text="Import",
                               width=10,  command=lambda: self.open_file())
        btnLoad = ttk.Button(btnFrame, text="Load", width=10,
                             command=lambda: self.open_file())
        btnSave = ttk.Button(btnFrame, text="Save", width=10,
                             command=lambda: self.save_data())
        btnReset = ttk.Button(btnFrame, text="Reset",
                              width=10, command=lambda: self.reset_data())
        # btnImport.bind('<Enter>', self.config.on_enter_button)
        # btnImport.bind('<Leave>', self.config.on_leave_button)
        # btnSave.bind('<Enter>', self.config.on_enter_button)
        # btnSave.bind('<Leave>', self.config.on_leave_button)
        # btnReset.bind('<Enter>', self.config.on_enter_button)
        # btnReset.bind('<Leave>', self.config.on_leave_button)
        btnImport.grid(row=0, column=0, sticky=tk.N +
                       tk.S+tk.W, padx=(5, 5), pady=(5, 5))
        btnLoad.grid(row=0, column=1, sticky=tk.N +
                     tk.S+tk.W, padx=(5, 5), pady=(5, 5))
        btnSave.grid(row=1, column=0, sticky=tk.N +
                     tk.S+tk.W, padx=(5, 5), pady=(5, 5))
        btnReset.grid(row=1, column=1, sticky=tk.N +
                      tk.S+tk.W, padx=(5, 5), pady=(5, 5))


# if __name__ == '__main__':
#     config = Gc.GenerateConfig()

#     #ctypes.windll.shcore.SetProcessDpiAwareness(1)
#     root = tk.Tk()
#     sizex = 700
#     sizey = 500
#     posx = 100
#     posy = 100
#     root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
#     myframe = tk.Frame(root, relief=tk.GROOVE, width=500, height=600, bd=1)
#     myframe.pack(fill="both", expand=tk.TRUE, anchor=tk.N+tk.W)
#     config.set_theme(None, myframe)
#     ImportData(myframe, config)
#     root.mainloop()
