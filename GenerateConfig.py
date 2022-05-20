import wget
import configparser,os
#from msilib.schema import Directory
from ttkthemes import ThemedStyle


class GenerateConfig:
    # CREATE OBJECT
    config_file = configparser.ConfigParser(interpolation=None)
    ConfigFileName="configurations.ini"
    Name=None
    Email=None
    ContactNo=None
    IO_Name=[]
    IO_Template=[]
    COLOR_TOP_BACKGROUND="#44a2d2"
    COLOR_BACKGROUND="#f2f5f7"
    COLOR_FOREGROUND="#343a40"
    COLOR_MENU_BACKGROUND="#ffffff"
    COLOR_MENU_FOREGROUND="#44a2d2"    
    displayFont=( "Verdana", 10)
    ChromeDriver="chromedriver.exe"
    themeName=None
    customStyle=None
    headerFonts =None 
    SecretKey ='fpxNyunUji5SJod5sK1dCwmovsukz1qLC1sJYOsVTzo='
    ActionTypes=("Wait","Check Checkbox","Click Button","Click Link","Click Submit","Fill Input","Select Text","Select Option","Condition","Find Index")
    ActionStartTypes=("Start","End","Middle")
    SelectorType=("ByName","ById","BySelector")
    InputType=("IOValue","ManualValue")
    ConditionType=("eq","nq","gt","ge","lt","le")
    SectionNames=("Personal Details","Current Address","Previous Address","Contact Details","Professional Contacts","Bank Account Details","Family And Dependants","ID Verification","Current Employment Details","Assets","Liabilities","Existing Mortgage","Mortgage Requirements","Expenditure")
    SectionType=("Multiple","Single")
    SectionCategory=("PersonalDetails","CurrentAddress","PreviousAddress","ContactDetails","ProfessionalContacts","BankAccount","FamilyAndDependants","IDVerification","CurrentEmployementDetails","Assets","Liabilities","Expenditure","ExistingMortgage","MortgageRequirements")
    SectionCategoryType=("Single","Single","Multiple","Single","Multiple","Multiple","Multiple","Single","Single","Multiple","Multiple","Multiple","Multiple","Multiple")
    

    def set_theme(self,event,frameData):
        self.customStyle= ThemedStyle(frameData)
        if(self.themeName=="arc"):
            self.customStyle.theme_use('arc')
            self.customStyle.configure('TButton', foreground = '#343a40', background = '#44a2d2', font=("Verdana",10))
            self.customStyle.configure('TreeViewAction.TButton', foreground = '#44a2d2', background = '#ffffff',font=("Verdana",10))
            self.customStyle.configure('TCombobox', background = '#f2f5f7',font=("Verdana",10))
            self.customStyle.configure('TFrame', background = '#ffffff')
            self.customStyle.configure('TLabelframe', background = '#44a2d2')
            self.customStyle.configure('Details.TLabelframe', background = '#ffffff',activebackground= '#ffffff')
            self.customStyle.configure('Separator.TFrame', background = '#44a2d2')
            self.customStyle.configure('NormalSeparator.TFrame', background = '#343a40')
            self.customStyle.configure('Topframe.TFrame', background = '#44a2d2')
            self.customStyle.configure('DashboardContent.TFrame', background = '#f2f5f7')
            self.customStyle.configure('Dashboard1.TFrame', background = '#ffe763')
            self.customStyle.configure('Dashboard2.TFrame', background = '#e3b2ac')
            self.customStyle.configure('Dashboard3.TFrame', background = '#b9e3ac')
            self.customStyle.configure('Dashboard4.TFrame', background = '#acdce3')
            self.customStyle.configure('TEntry', background = '#f2f5f7',font=("Verdana",10))
            self.customStyle.configure('Toplable.TLabel', background = '#44a2d2',font=("Verdana",15,'bold'),foreground="#ffffff")
            self.customStyle.configure('Dashboard1.TLabel',background = '#ffe763', font=("Verdana",12,'bold'))
            self.customStyle.configure('Dashboard2.TLabel',background = '#e3b2ac', font=("Verdana",12,'bold'))
            self.customStyle.configure('Dashboard3.TLabel',background = '#b9e3ac', font=("Verdana",12,'bold'))
            self.customStyle.configure('Dashboard4.TLabel',background = '#acdce3', font=("Verdana",12,'bold'))

            self.customStyle.configure('Login.TLabel',background = '#ffffff', font=("Verdana",11))
            

            self.customStyle.configure('H1.TLabel', background = '#ffffff',font=("Verdana",12,'bold'))
            self.customStyle.configure('Menu.TRadiobutton',indicator=0, background = '#ffffff',font=("Verdana",10,'bold'),foreground="#343a40",selectcolor="#f2f5f7")
        else :
            self.customStyle.theme_use('default')
        #print (self.customStyle.theme_use())



    def on_enter_menu(self,e):
        e.widget['background'] = self.COLOR_BACKGROUND
        e.widget['foreground'] = self.COLOR_TOP_BACKGROUND

    def on_leave_menu(self,e):
        e.widget['background'] = self.COLOR_TOP_BACKGROUND
        e.widget['foreground'] = self.COLOR_FOREGROUND     

    def on_enter_button(self,e):
        e.widget['background'] = self.COLOR_BACKGROUND
        e.widget['foreground'] = self.COLOR_TOP_BACKGROUND

    def on_leave_button(self,e):
        e.widget['background'] = self.COLOR_TOP_BACKGROUND
        e.widget['foreground'] = self.COLOR_FOREGROUND 

    def __init__(self):   
        self.headerFonts= ("Verdana", 15, "bold")             
        self.LoadAllData()
        if(self.FilePath ==None or self.FilePath==""):
            self.FilePath=os.getcwd()+"/data"
        
        
    
    def LoadAllData(self):
        if not os.path.exists(self.ConfigFileName):
            self.fnc_CreateDefaultFile()
        self.config_file.read(self.ConfigFileName)
        
        self.Name = self.config_file['AFill_Register']['Name']
        self.Email = self.config_file['AFill_Register']['Email']
        self.ContactNo =self.config_file['AFill_Register']['ContactNo']
        self.FilePath = self.config_file['AFill_FileSetting']['FilePath']
        self.TemplateFileName = self.config_file['AFill_FileSetting']['TemplateFileName']
        self.DataFileName = self.config_file['AFill_FileSetting']['DataFileName']
        self.ChromeDriver = self.config_file['AFill_FileSetting']['ChromeDriver']
        self.UserName = self.config_file['AFill_Users']['UserName']
        self.Password = self.config_file['AFill_Users']['Password']
        self.IO_Name=self.config_file['InputTemplate']['IO_Name'].split(",")
        self.IO_Template=self.config_file['InputTemplate']['IO_Template'].split(",")
        self.IO_Name_PersonalDetails=self.config_file['InputTemplate']['IO_Name_PersonalDetails'].split(",")
        self.IO_Template_PersonalDetails=self.config_file['InputTemplate']['IO_Template_PersonalDetails'].split(",")
        self.IO_Name_CurrentAddress=self.config_file['InputTemplate']['IO_Name_CurrentAddress'].split(",")
        self.IO_Template_CurrentAddress=self.config_file['InputTemplate']['IO_Template_CurrentAddress'].split(",")
        self.IO_Name_PreviousAddress=self.config_file['InputTemplate']['IO_Name_PreviousAddress'].split(",")
        self.IO_Template_PreviousAddress=self.config_file['InputTemplate']['IO_Template_PreviousAddress'].split(",")
        self.IO_Name_ContactDetails=self.config_file['InputTemplate']['IO_Name_ContactDetails'].split(",")
        self.IO_Template_ContactDetails=self.config_file['InputTemplate']['IO_Template_ContactDetails'].split(",")        
        self.IO_Name_ProfessionalContacts=self.config_file['InputTemplate']['IO_Name_ProfessionalContacts'].split(",")
        self.IO_Template_ProfessionalContacts=self.config_file['InputTemplate']['IO_Template_ProfessionalContacts'].split(",")
        self.IO_Name_BankAccountDetails=self.config_file['InputTemplate']['IO_Name_BankAccountDetails'].split(",")
        self.IO_Template_BankAccountDetails=self.config_file['InputTemplate']['IO_Template_BankAccountDetails'].split(",")
        self.IO_Name_FamilyAndDependants=self.config_file['InputTemplate']['IO_Name_FamilyAndDependants'].split(",")
        self.IO_Template_FamilyAndDependants=self.config_file['InputTemplate']['IO_Template_FamilyAndDependants'].split(",")
        self.IO_Name_IDVerification=self.config_file['InputTemplate']['IO_Name_IDVerification'].split(",")
        self.IO_Template_IDVerification=self.config_file['InputTemplate']['IO_Template_IDVerification'].split(",")
        self.IO_Name_CurrentEmploymentDetails=self.config_file['InputTemplate']['IO_Name_CurrentEmploymentDetails'].split(",")
        self.IO_Template_CurrentEmploymentDetails=self.config_file['InputTemplate']['IO_Template_CurrentEmploymentDetails'].split(",")
        self.IO_Name_Assets=self.config_file['InputTemplate']['IO_Name_Assets'].split(",")
        self.IO_Name_Liabilities=self.config_file['InputTemplate']['IO_Name_Liabilities'].split(",")
        self.IO_Template_Liabilities=self.config_file['InputTemplate']['IO_Template_Liabilities'].split(",")
        self.IO_Name_ExistingMortgage=self.config_file['InputTemplate']['IO_Name_ExistingMortgage'].split(",")
        self.IO_Template_ExistingMortgage=self.config_file['InputTemplate']['IO_Template_ExistingMortgage'].split(",")
        self.IO_Name_MortgageRequirements=self.config_file['InputTemplate']['IO_Name_MortgageRequirements'].split(",")
        self.IO_Template_MortgageRequirements=self.config_file['InputTemplate']['IO_Template_MortgageRequirements'].split(",")
        self.IO_Name_Expenditure=self.config_file['InputTemplate']['IO_Name_Expenditure'].split(",")
        self.IO_Template_Expenditure=self.config_file['InputTemplate']['IO_Template_Expenditure'].split(",")
        self.IO_Name_Expenditure1=self.config_file['InputTemplate']['IO_Name_Expenditure1'].split(",")
        self.IO_Template_Expenditure1=self.config_file['InputTemplate']['IO_Template_Expenditure1'].split(",")
        self.IO_Name_Whichofthefollowingareimportant=self.config_file['InputTemplate']['IO_Name_Whichofthefollowingareimportant'].split(",")
        self.IO_Template_Whichofthefollowingareimportant=self.config_file['InputTemplate']['IO_Template_Whichofthefollowingareimportant'].split(",")


        self.themeName= self.config_file['Themes']['Theme_Name']

        

    def fnc_CreateDefaultFile(self):    
        
        # ADD SECTION
        self.config_file.add_section("AFill_FileSetting")
        # ADD SETTINGS TO SECTION
        self.config_file.set("AFill_FileSetting", "FilePath", os.getcwd()+"/data")
        self.config_file.set("AFill_FileSetting", "TemplateFileName", "template.json")
        self.config_file.set("AFill_FileSetting", "DataFileName", "data.json")
        self.config_file.set("AFill_FileSetting", "ChromeDriver", "chromedriver.exe")         

        self.config_file.add_section("AFill_Users")
        # ADD SETTINGS TO SECTION        
        self.config_file.set("AFill_Users", "UserName", "admin")
        self.config_file.set("AFill_Users", "Password", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")

        self.config_file.add_section("AFill_Register")
        # ADD SETTINGS TO SECTION        
        self.config_file.set("AFill_Register", "Name", "Prabhakar Kumar Singh")
        self.config_file.set("AFill_Register", "Email", "")
        self.config_file.set("AFill_Register", "ContactNo", "")

        self.config_file.add_section("InputTemplate")
        self.config_file.set("InputTemplate", "IO_Name", "Title,First Name,Middle Name,Last Name,Salutation,Date of Birth,Gender,Marital Status,"+
        "Country of Birth,Nationality,National Insurance No.,Country Of Residence,Country of Birth,"+
        "CurrentAddress[G],PreviousAddress[A],Mobile,E Mail, Home Telephone[M],Work Telephone[M],ProfessionalContact[A],BankAccount[A],"+                
        "FamilyAndDependants[A],IDVerification[G],CurrentEmployment[G],Asset[A],Liabilities[A],Expenditure[A],Source of Deposit[M][D]," +
        "ExistingMortgage[A],MortgageRequirements[A]"
        )
        self.config_file.set("InputTemplate", "IO_Name_PersonalDetails","Title,First Name,Middle Name,Last Name,Salutation,Date of Birth,Gender,Marital Status,Country of Birth,Nationality,National Insurance No.,Country Of Residence")
        self.config_file.set("InputTemplate", "IO_Template_PersonalDetails","Title,First Name,Middle Name,Last Name,Salutation,Date of Birth,Gender,Marital Status,Country of Birth,Nationality,National Insurance No.,Country Of Residence")
        self.config_file.set("InputTemplate", "IO_Name_CurrentAddress","Address Line 1,Address Line 2,Address Line 3,Address Line 4,City,Country,Postcode,Residency Status,Date From")
        self.config_file.set("InputTemplate", "IO_Template_CurrentAddress","Address Line 1,Address Line 2,Address Line 3,Address Line 4,City / Town,Country,Postcode,Residency Status,Date From")
        self.config_file.set("InputTemplate", "IO_Name_PreviousAddress","Address Line 1,Address Line 2,Address Line 3,Address Line 4,City,Country,Postcode,Residency Status,Date From,Date To")
        self.config_file.set("InputTemplate", "IO_Template_PreviousAddress","Address Line 1,Address Line 2,Address Line 3,Address Line 4,City / Town,Country,Postcode,Residency Status,Date From,Date To")
        self.config_file.set("InputTemplate", "IO_Name_ContactDetails","Mobile,Email,Home Telephone[M],Work Telephone[M]")
        self.config_file.set("InputTemplate", "IO_Template_ContactDetails","Mobile,E-Mail,-,-")
        self.config_file.set("InputTemplate", "IO_Name_ProfessionalContacts","Contact Type,Contact Name,Address Line 1,Address Line 2,Address Line 3,Address Line 4,City,Postcode,Telephone Number,Mobile Number,Email Address")
        self.config_file.set("InputTemplate", "IO_Template_ProfessionalContacts","Contact Type,Contact Name,Address Line 1,Address Line 2,Address Line 3,Address Line 4,City Town,Postcode,Telephone Number,Mobile Number,Email Address")
        self.config_file.set("InputTemplate", "IO_Name_BankAccountDetails","Owner,Bank Name,Account Holder(s),Account Number,Sort Code")
        self.config_file.set("InputTemplate", "IO_Template_BankAccountDetails","Owner,Bank Name,Account Holder(s),Account Number,Sort Code")
        self.config_file.set("InputTemplate", "IO_Name_FamilyAndDependants","Full Name,Date of Birth,Age,Relationship,Related To,Financially Dependant,Dependant Living with Client")
        self.config_file.set("InputTemplate", "IO_Template_FamilyAndDependants","Full Name,Date of Birth,Age,Relationship,Related To,Financially Dependant,Dependant Living with Client")
        self.config_file.set("InputTemplate", "IO_Name_IDVerification","Original Driving Licence Seen,Driving Licence Ref,Driving Licence Expiry Date,Original Passport Seen,Country of Origin,Passport ref,Passport Expiry Date,Mother Maiden Name,Electricity Bill Ref,Bank Statement Seen,Mortgage Statement Seen,Council Tax Bill Seen,Utilities Bill Seen")
        self.config_file.set("InputTemplate", "IO_Template_IDVerification","Original Driving Licence Seen,Driving Licence Ref,Driving Licence Expiry Date,Original Passport Seen,Country of Origin,Passport ref,Passport Expiry Date,Mother's Maiden Name,Electricity Bill Ref,Bank Statement Seen,Mortgage Statement Seen,Council Tax Bill Seen,Utilities Bill Seen")
        self.config_file.set("InputTemplate", "IO_Name_CurrentEmploymentDetails","Highest rate of income tax paid,Owner,Employment Status,Occupation,Shareholding percentage[M],Contractor[M],Inside IR35[M],Employer,Business Type,Address Line 1,Address Line 2,Address Line 3,Address Line 4,City,Country,Post Code,Intended Retirement Age,Start Date,"+
        "Most Recent Annual Accounts Net Profit,Most Recent Annual Accounts Net Dividend,Most Recent Annual Accounts Salary,Most Recent Annual Accounts Year End,"+
        "Year 2 Annual Accounts Net Profit,Year 2 Annual Accounts Net Dividend,Year 2 Annual Accounts Salary,Year 2 Year End,"+
        "Year 3 Annual Accounts Net Profit,Year 3 Annual Accounts Net Dividend,Year 3 Annual Accounts Salary,Year 3 Year End,"+
        "Gross Basic Annual Income,Net Basic Monthly Income,Net Basic Monthly Income,Do you receive Overtime Income,Gross Guaranteed Annual Overtime,"+
        "Net Guaranteed Monthly Overtime,Gross Regular Annual Overtime,Net Regular Monthly Overtime,Do you receive Bonus Income,Gross Guaranteed Annual Bonus,Net Guaranteed Annual Bonus,Gross Regular Annual Bonus,Net Regular Annual Bonus,"+
        "Other Gross Income,Total Gross Annual Earnings,In Probation"
        )
        self.config_file.set("InputTemplate", "IO_Template_CurrentEmploymentDetails","Highest rate of income tax paid (%),Owner,Employment Status,Occupation,Shareholding percentage[M],Contractor[M],Inside IR35[M],Employer,Business Type,Address Line 1,Address Line 2,Address Line 3,Address Line 4,City,Country,Post Code,Intended Retirement Age,Start Date,"+
        "Most Recent Annual Accounts Net Profit,Most Recent Annual Accounts Net Dividend,Most Recent Annual Accounts Salary,Most Recent Annual Accounts Year End,"+
        "Year 2 Annual Accounts Net Profit,Year 2 Annual Accounts Net Dividend,Year 2 Annual Accounts Salary,Year 2 Year End,"+
        "Year 3 Annual Accounts Net Profit,Year 3 Annual Accounts Net Dividend,Year 3 Annual Accounts Salary,Year 3 Year End,"+
        "Gross Basic Annual Income,Net Basic Monthly Income,Net Basic Monthly Income,Do you receive Overtime Income?,Gross Guaranteed Annual Overtime,"+
        "Net Guaranteed Monthly Overtime,Gross Regular Annual Overtime,Net Regular Monthly Overtime,Do you receive Bonus Income?,Gross Guaranteed Annual Bonus,Net Guaranteed Annual Bonus,Gross Regular Annual Bonus,Net Regular Annual Bonus,"+
        "Other Gross Income,Total Gross Annual Earnings,In Probation,"
        )

        self.config_file.set("InputTemplate", "IO_Name_Liabilities","Owner,Liability Account Number,Liability Category,Original Loan Amount,Repayment or Interest Only,Rate Type,Amount Outstanding,Credit Limit,Interest Rate,"+
        "Payment Amount Monthly,Lender,Loan Term years,Start Date[M],End Date,Early Redemption Charge,Whether liability is to be repaid,How will liability be repaid")
        self.config_file.set("InputTemplate", "IO_Template_Liabilities","Owner,Liability Account Number,Liability Category,Original Loan Amount,Repayment or Interest Only?,Rate Type,Amount Outstanding,Credit Limit,Interest Rate (%),"+
        "Payment Amount (Monthly),Lender,Loan Term (years),Start Date[M],End Date,Early Redemption Charge,Whether liability is to be repaid?,How will liability be repaid")

        self.config_file.set("InputTemplate", "IO_Name_ExistingMortgage","Owner,Lender,Policy Number,Address Line 1,Rate Type,Mortage Type,Are you a First Time Buyer,"+
        "Property Type,Repayment Method,Capital Repayment Amount,Interest Only Amount,Interest Only Repayment Vehicle,"
        "Original Loan Amount,Interest Rate,Base Rate,Feature Expires,Original Mortgage Term,Start Date,End Date,Remaining Term,"+
        "Current Balance,Account Number,Is the loan subject to Redemption Penalty,Redemption End Date,Consent to Let,Linked to Asset,Asset Value")
        self.config_file.set("InputTemplate", "IO_Template_ExistingMortgage","Owner,Lender,Policy Number,Address Line 1,Rate Type,Mortage Type,Are you a First Time Buyer,"+
        "Property Type,Repayment Method,Capital Repayment Amount,Interest Only Amount,Interest Only Repayment Vehicle,"
        "Original Loan Amount,Interest Rate %,Base Rate,Feature Expires,Original Mortgage Term,Start Date,End Date,Remaining Term,"+
        "Current Balance,Account Number,Is the loan subject to Redemption Penalty?,Redemption End Date,Consent to Let?,Linked to Asset,Asset Value")

        self.config_file.set("InputTemplate", "IO_Name_MortgageRequirements","Source of Deposit[M],Owner,RequirementType[M][D],Mortage Type,Property,Number of Bedrooms,Number of living rooms,Number of kitchen,Number of Toilets,Number of bathrooms,Parking space,Garage,Is area gt 2 acres,"+
        "Repayment Method,Tenure Type[M][D],Region[M],Year Built[M],Property Type[M][D],Property Description[M],Floor[M],Total floors in the block[M],Lift[M],Lease Years Remaining[M],Is above commercial[M],Ground rent[M],Service charge[M],EWS1 Form available[M],Capital Repayment Amount,Interest Only Amount,Price/Valuation,Deposit/Equity,Loan,LTV,Term,Source Of Deposit")
        self.config_file.set("InputTemplate", "IO_Template_MortgageRequirements","[Builder Gift][Customer’s Bank][Equity][Gifted Deposit][Immediate Family Gift][Inheritance][Loan],[Proceeds of house sale][Sale Of Other Property][Vendor Gifted],Owner,[Purchase][Re-mortgage][Product Transfer][Additional Borrow],Mortage Type,Property,Number of Bedrooms,Number of living rooms,Number of kitchen,Number of Toilets,Number of bathrooms,[on-site parking][off-street parking],[Yes][No],[Yes][No],"+
        "Repayment Method,[Freehold][Leasehold],Region[M],Year Built[M],[House][Bungalow][Flat][Maisonette],Property Description[M],Floor,Total floors in the block,Lift,Lease Years Remaining,Is above commercial,Ground rent,Service charge,EWS1 Form available,Capital Repayment Amount,Interest Only Amount,Price/Valuation,Deposit/Equity,Loan,LTV(%),Term,Source Of Deposit")

        self.config_file.set("InputTemplate", "IO_Name_Assets","Owner,Category,Related to Address,Original Value,Purchased On,Value,Valuation Date,"+
        "Address Line 1[M],Address Line 2[M],Address Line 3[M],Address Line 4[M],City[M],Country[M],Postcode[M]")
        
        self.config_file.set("InputTemplate", "IO_Name_Expenditure","Category,Owner,Description,Net Amount,Frequency")
        self.config_file.set("InputTemplate", "IO_Template_Expenditure","Category,Owner,Description,Net Amount,Frequency")
        self.config_file.set("InputTemplate", "IO_Name_Expenditure1","Council Tax,Gas,Electricity,Water,Telephone Mobile,Food Personal Care,Car Travelling Expenses,Housekeeping,Building Insurance,Combined Utilities,Maintenance Alimony,Clothing,Basic Recreation,School Fee Childcare,Life General Assurance,Other")
        self.config_file.set("InputTemplate", "IO_Template_Expenditure1","Council Tax,Gas,Electricity,Water,Telephone/Mobile,Food & Personal Care,Car/Travelling Expenses,Housekeeping,Building Insurance,Combined Utilities,Maintenance/Alimony,Clothing,TV/Satellite/Internet/Basic,School Fee/Childcare,Life/General Assurance,Other (Non-Essential)")
        
        self.config_file.set("InputTemplate", "IO_Name_D_Expenditure_Category","Council Tax,Gas,Electricity,Water,Telephone/Mobile,Food & Personal Care,Car/Travelling Expenses,Housekeeping,Building Insurance,"
        "Combined Utilities,Maintenance/Alimony,Clothing,TV/Satellite/Internet/Basic Recreation,School Fee/Childcare,Life/General Assurance Premium,Other (Non-Essential)")
        self.config_file.set("InputTemplate", "IO_Name_D_SourceofDeposit","Builder Gift,Customer’s Bank Account-UK/Savings,Equity,Gifted Deposit,Immediate Family Gift,Inheritance,Loan,Proceeds of house sale,Sale Of Other Property,Vendor Gifted")
        self.config_file.set("InputTemplate", "IO_Name_D_MortgageRequirements_RequirementType","Builder Gift,Customer’s Bank Account-UK/Savings,Equity,Gifted Deposit,Immediate Family Gift,Inheritance,Loan,Proceeds of house sale,Sale Of Other Property,Vendor Gifted")

        self.config_file.set("InputTemplate", "IO_Template", "Title,First Name,Middle Name,Last Name,Salutation,Date of Birth,Gender,"+
        "Country of Birth,Nationality,National Insurance No.,Country Of Residence,Country of Birth,Address Line 1,Address Line 2,City,Country,Postcode,Address Type,Address Status,Date From,Date To,Telephone,Mobile,E-Mail")

        self.config_file.set("InputTemplate", "IO_Name_Whichofthefollowingareimportant","The maximum early redemption period I would accept is,Ability to add fees to the loan")
        self.config_file.set("InputTemplate", "IO_Template_Whichofthefollowingareimportant","The maximum early redemption period I would accept is,Ability to add fees to the loan")

        self.config_file.add_section("Themes")
        self.config_file.set("Themes", "Theme_Name", "arc")
        # SAVE CONFIG FILE
        with open(self.ConfigFileName, 'w') as configfileObj:
            self.config_file.write(configfileObj)
            configfileObj.flush()
            configfileObj.close()
        
        filepath=os.getcwd()
        dirpath=filepath+"/data"
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        url="http://wms.galway.in/afill/template.json"
        wget.download(url, out=dirpath)
        url="http://wms.galway.in/afill/data.json"
        wget.download(url, out=dirpath)
        url="http://wms.galway.in/afill/PankajAggarwal.json"
        wget.download(url, out=dirpath)
        url="http://wms.galway.in/afill/logo.png"
        wget.download(url, out=filepath)
        url="http://wms.galway.in/afill/logoicon.png"
        wget.download(url, out=filepath)
        url="http://wms.galway.in/afill/logoIcon.ico"
        wget.download(url, out=filepath)
        url="http://wms.galway.in/afill/logoIcon32.png"
        wget.download(url, out=filepath)
        url="http://wms.galway.in/afill/logoIcon64.png"
        wget.download(url, out=filepath)
        self.LoadAllData()
        print("Config file 'configurations.ini' created")

    def fnc_RegisterUser(self,Name,Email,ContactNo):
        self.config_file.read("configurations.ini")
        # UPDATE A FIELD VALUE
        self.config_file["AFill_Register"]["Name"]=Name
        self.config_file["AFill_Register"]["Email"]=Email
        self.config_file["AFill_Register"]["ContactNo"]=ContactNo        
        # ADD A NEW FIELD UNDER A SECTION
        #self.config_file["AFill_Register"].update({"Format":"(message)"})

        # Create Directory
        with open(self.ConfigFileName,"w") as file_object:
            self.config_file.write(file_object)
        self.LoadAllData()

