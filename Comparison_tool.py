
import os
from pip._internal import main as pipmain
pipmain(['install', 'pandas', 'openpyx1', 'xIrd'])
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp

script_name = "COMPARISON!!!"
top_border = "\u256D" + "\u2500" * (len(script_name) + 4) + "\u256E"
bottom_border = "\u2570" + "\u2500" * (len(script_name) + 4) + "\u256F"
print (top_border)
print ("\u2502", script_name," ", "\u2502")
print (bottom_border)

limit=0
Found = False

while limit < 3:
    ACI_Res = input ('Please enter ACI resourcing file path:')
    ACT_Res = ACI_Res. strip()
    if ACI_Res[0]=r"'" or ACI_Res[0]==r'"':
        ACI_Res=ACI_Res[1:]
    if ACI_Res[-1]==r"'" or ACI_Res[-1]==r'"':
        ACI_Res=ACI_Res[:len(ACI_Res)-1]
    if not os. path. isfile (ACI_Res):
        limit+=1
        print(" This path for ACI resourcing file is invalid! Please try again")
    else:
        ACI_Res = pd.ExcelFile (ACI_Res)
        ACI_Data = 'ACI resourcing sheet'
        sheet=ACI_Res.sheet_names
        for a in sheet:
            if a.lower().strip() == ACI_Data.lower().strip():
                ACI_Res = pd.read.excel(ACI_Res,sheet_name = a)
                Found = True
                break
        if not Found and limit < 3:
            limit = 0
            print(" Incorrect ACI resourcing TAB name. Please Try again!")
            exit(1)
        else:
            limit = 0
            Found = False
            break
        
#ACI_Res = pd. readexcel (r"C: \Users \rudrani. singhal Documents Workday_auto \ACI Resourcing sheet - 18th Sep 2023.xlsx",sheet_name = 'ACI resourcing sheet')

while limit < 3:
    Syn_all = input('Please enter Synechron file path:')
    Syn_all = Syn_all. strip()
    if Syn_all[0]==r"'" or Syn_all[0]==r'"':
        Syn_all=Syn_all[1:]
    if Syn_all[-1]==r"'" or Syn_all[-1]==r'"':
        Syn_all=Syn_all[:len(Syn_all)-1]
    if not os.path.isfile(Syn_all):
        limit+=1
        print(" This path for Synechron file is invalid! Please try again")
    else:
        Syn_all = pd.ExcelFile(Syn_all)
        Syn_all = pd.read_excel(Syn_all)
        limit = 0
        break

if limit==3:
    print ('Out of attempts. Try again!')
    exit (1)

ACI_Res['EMP ID'].dropna(inplace = True)
x= Syn_all.values.tolist()
Remarks={}
Flag = False
ACI_Res['Project Name'].fillna(0, inplace = True)

for index, row in ACI_Res.iterrows():
    id = row['EMP ID']
    Remarks[id]=[]
    for a in x:
        if id == a[0]:
            Flag = True
            if row['Project Name'] != 0:
                if int (row['Project Name'].split(' ')[0]) != a[15]:
                    Remarks[id].append('Project code discrepancy')
            if row['Role End Date'] != a[21]:
                Remarks[id].append('Allocation End date discrepancy')
            if row['Oracle  status'].lower().strip() != a[24].lower().strip():
                Remarks[id].append('Billability discrepancy')
            break
    if Flag:
        Flag = False
    else:
        Remarks[id].append ('Record not found')

Report = {'Emp ID':[], 'Emp Name':[], 'Location':[], 'Gender':[], 'SOW#': [], 'Project Number': [], 'Project Start Date': [], 'Project End Date': [], 'Allocation End Date': [], 'Billable Status': [], 'Remarks':[]}

for index, rows in ACI_Res.iterrows():
    id = rows['EMP ID']
    if len (Remarks[id]) >0:
        SOW_Start = Timestamp(rows['Role Start Date'])
        SOW_Start = SOW_Start.date()
        SOW_End = Timestamp(rows['Role End Date'])
        SOW_End = SOW_End.date()
        Report['Emp ID'].append(id)
        Report['Emp Name'].append(rows['Resource Name'])
        Report['Location'].append(rows['Base Location'])
        Report['Gender']. append(rows['Gender'])
        Report['SOW#'].append(rows['2023 SOW#'])
        if rows['Project Name']!= 0:
            Report['Project Number'].append(rows['Project Name'].split(' ')[0])
        else:
            Report['Project Number'].append(None)
        Report['Project Start Date']. append(SOW_Start)
        Report['Project End Date']. append(SOW_End)
        Report['Allocation End Date'].append(SOW_End)
        Report['Billable Status'].append(rows['Oracle status'])
        Report['Remarks'].append ('. '.join(Remarks[id]))

Output=pd.DataFrame (Report)

#Output. to_excel(r"C:\Users\rudrani.singhal\Documents \Workday_auto\Out_Report.x1s", index-False)

Output=pd.DataFrame(Report)

while True: # repeat until the try statement succeeds
    try:
        path = input('Please, Enter the path where you want report to be generated:')
        Output.to_excel(path+ '\ComparedOutput. x1sx',sheet_name='Report',index=False)
        print ("Comparison report Generated Successfully!")
        print("Report is generated in : {b}".format(b=path))
        break
        # exit the loop
    except IOError:
            input("Could not open file or incorrect path given ! Please close Report Excel or give the correct.Press Enter to retry.")
            # restart the loop