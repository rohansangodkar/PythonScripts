import time
import datetime
import os

####################################################################################################
#CodeStandardChecker-ACQ: Version 1 : 27/06/2023 : Developed by : ROHAN SANGODKAR
#                                        
#                         Version 2 : 03/08/2023 : Hardcoded team members to remove dependency
#                                                  on G drive.
#                                                  Report will contain all the elements which have
#                                                  no comments as well.
#                         Version 3 : 25/10/2023 : Further Code Enhancement
####################################################################################################

#if not os.path.exists(r"G:\Users\Scripts\team_list\ACQ.txt"):
#                print(r"G drive is not connected!! Cannot access G:\Users\Scripts\team_list\ACQ.txt")
#                exit(1)
#             
#with open (r"G:\Users\Scripts\team_list\ACQ.txt","r") as name:
#                names = [line.strip() for line in name.readlines() if line.strip()]

names = ["Rohan","Vidya","Swarna","Latha","Bhagya","Nandhini","Rutuparna","Pavan","Deb","Avik","Srimathruka","Jyothi","Preeti"]
                
def synergy_version_checker(data):
    return "%version" in data

def synergy_date_checker(data):
    return "%date_created" in data
        
def year_tag_checker(file,data):
    count = 0
    dde = ""
    calendar={"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        
    for l in data:
            if "%" in l:
                    count+=1
                    if count == 2:
                            l=l.strip()
                            l_splt = [x for x in l.split(" ") if x!= '']
                            if l_splt[1] in days:
                                year=l_splt[-2]
                            else:
                                year=l_splt[3]
                            return year in file

def path_checker(p):
        return os.path.isdir(p)

def pr_format_checker(pr):
        pr=pr.strip()
        if len(pr) < 7 or len(pr) > 9:
                return False
        if pr[:2].lower() != "uk":
                return False
        if not pr[2].isnumeric():
                return False
        if "#" not in pr:
                return False
        if not pr[4:].isnumeric():
                return False
        return True

def pr_checker(file,pr):
        return pr.lower() in file.lower()

def version_checker(content):
        count = 0
        while count < 3:
                for line in content:
                        line=line.strip()
                        if "version" in line.lower():
                                count+=1
                                line_splt=[x for x in line.split(" ") if x!= '']
                                if count == 1:
                                        comp = line_splt[1].strip()
                                                        
                                else:
                                        for l in line_splt:
                                                if "*" not in l and "version" not in l.lower() and ":" not in l and "-" not in l :
                                                        if comp == l.strip():
                                                                    return True
                                                        else:
                                                                return False

def log_date_checker(listdata):
        count = 0
        dde = ""
        calendar={"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
        days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        
        for l in listdata:
                if "%" in l:
                        count+=1
                        if count == 2:
                                l=l.strip()
                                l_splt = [x for x in l.split(" ") if x!= '']
                                if l_splt[1] in days:
                                        if len(l_splt[3]) == 1:
                                                dde+="0"
                                                dde+=l_splt[3]
                                        else:
                                                dde = l_splt[3]
                                        date1 = "{dd}/{mm}/{yyyy}".format(dd=dde,mm=calendar[l_splt[2]],yyyy=l_splt[-2])
                                else:
                                        date1 = "{dd}/{mm}/{yyyy}".format(dd=l_splt[1],mm=calendar[l_splt[2][:3]],yyyy=l_splt[3])
        count = 0
        for l in listdata:
                if "created" in l.lower():
                        count+=1
                        if count == 2:
                                l=l.strip()
                                l_splt = [x for x in l.split(" ") if x!= '']
                                t=0
                                while t == 0:
                                        for e in l_splt:
                                                if "/" in e:
                                                        date2 = e[:10]
                                                        t=1

        return date1 == date2

def name_check(data):
        for l in data:
                if "author" in l.lower():
                        for n in names:
                                n = n.strip()
                                if n.lower() in l.lower():
                                        return True
                        return False

def tab_check(data):
        tab_err =[]
        for d in data:
                if "\t" in d:
                        if str(data.index(d)+1) not in tab_err:
                                tab_err.append(str(data.index(d)+1))
        return tab_err

def length_check(data):
        len_err = []
        for d in data:
                if len(d) > 81:
                        if str(data.index(d)+1) not in len_err:
                                len_err.append(str(data.index(d)+1))
        return len_err

def tag_check(data,pr):
        pre1 = "01I"+pr[4:]
        pre2 = "01M"+pr[4:]
        pr_tag = [pre1,pre2]
        count = 0
        err = []
        for d in data:
            count+=1
            if pr_tag[0] in d:
                if d[72:80] != pr_tag[0]:
                    err.append(str(count))
            elif pr_tag[1] in d:
                if d[72:80] != pr_tag[1]:
                    err.append(str(count))
        return err
    
def cobol_section_check(data):
        section = []
        exits = []
        for d in data:
                if "SECTION." in d:
                        d = d.strip()
                        splt = [x for x in d.split(" ") if x!= '']
                        if splt[0][0] != "*" and splt[0].lower() != "file":
                                if splt[0] in section:
                                        return splt[0]
                                section.append(splt[0])

        return "noerror"

def tag_present(data,pr):
    pre1 = "01I"+pr[4:]
    pre2 = "01M"+pr[4:]
    return pre1 in data or pre2 in data

def PType(data):
        CICS_id = False
        DB2_id = False
        for d in data:
              d=d.strip()
              if d[0] != '*':
                     if 'EXEC CICS' in d:
                            CICS_id = True
                     if 'EXEC SQL' in d:
                            DB2_id = True
        return CICS_id, DB2_id

def Pgm_Name(content_array_index):
        for line in content_array_index :
                if 'PROGRAM-ID.' in line:
                       line=line.strip()
                       if line[0] != '*':
                                d=line.split('.')[1]
                                pname_line = (str(int(line[-8:])+1))
                                return d,pname_line
        return False

def PNAME_check(content_array_index,PNAME,PLINE):
    PNLINE = []   
    for line in content_array_index:
        if line[6] != '*' :
            if PNAME in line and str(PLINE) not in line and 'PROGRAM-ID.' not in line:
                PNLINE.append(str(int(line[-8:])+1))
    
    return PNLINE
 
def WS_checks(content_array_index,pre1,pre2):
        LEVEL,WS,PIC,VALUE,ALIGN,TO,ALTER,NXT,CNT,GTE,CRT = [],[],[],[],[],[],[],[],[],[],[]

        WS_Found = False
        for line in content_array_index:
                if line[6] != "*":
                        if 'WORKING-STORAGE SECTION.' in line:
                               WS_Found = True
                        if "WS-END" in line or "LINKAGE SECTION" in line or "PROCEDURE DIVISION" in line:
                                WS_Found = False
                                break
                        elif "WS-" in line and WS_Found and (pre1 in line or pre2 in line): #add PR tag for latest only check
                                if "01" in line[:40]:
                                        ALIGN.append('01')
                                        ALIGN.append(str(int(line[-8:])+1))
                                        if line.index("01") != 7:
                                                LEVEL.append(str(int(line[-8:])+1))
                                        if line.index("WS-") != 11:
                                                WS.append(str(int(line[-8:])+1))
                                elif "03" in line[:40]:
                                        ALIGN.append('03')
                                        ALIGN.append(str(int(line[-8:])+1)) 
                                        if line.index("03") != 11:
                                                LEVEL.append(str(int(line[-8:])+1))
                                        if line.index("WS-") != 15:
                                                WS.append(str(int(line[-8:])+1))
                                elif "05" in line[:40]:
                                        ALIGN.append('05')
                                        ALIGN.append(str(int(line[-8:])+1))                                               
                                        if line.index("05") != 15:
                                                LEVEL.append(str(int(line[-8:])+1))
                                        if line.index("WS-") != 19:
                                                WS.append(str(int(line[-8:])+1))
                                elif "07" in line[:40]:
                                        ALIGN.append('07')
                                        ALIGN.append(str(int(line[-8:])+1))                                            
                                        if line.index("07") != 19:
                                                LEVEL.append(str(int(line[-8:])+1))
                                        if line.index("WS-") != 23:
                                                WS.append(str(int(line[-8:])+1))
                                elif "09" in line[:40]:
                                        ALIGN.append('09')
                                        ALIGN.append(str(int(line[-8:])+1))                                               
                                        if line.index("09") != 23:
                                                LEVEL.append(str(int(line[-8:])+1))
                                        if line.index("WS-") != 27:
                                                WS.append(str(int(line[-8:])+1))
                        if "PIC" in line and (pre1 in line or pre2 in line):  #add PR tag for latest only check 
                                if line.index("PIC") != 39:
                                        PIC.append(str(int(line[-8:])+1))
                        if "VALUE" in line and (pre1 in line or pre2 in line):  #add PR tag for latest only check
                                if line.index("VALUE") != 39:
                                        VALUE.append(str(int(line[-8:])+1))
                        if " TO " in line and (pre1 in line or pre2 in line): #add PR tag for latest only check
                               if line.index(" TO ") != 38:
                                      TO.append(str(int(line[-8:])+1))
                        if "ALTER " in line and (pre1 in line or pre2 in line): #add PR tag for latest only check
                                ALTER.append(str(int(line[-8:])+1))
                        if "NEXT-SENTENCE" in line and (pre1 in line or pre2 in line): #add PR tag for latest only check
                                NXT.append(str(int(line[-8:])+1))
                        if "CONTINUE" in line and (pre1 in line or pre2 in line): #add PR tag for latest only check
                                CNT.append(str(int(line[-8:])+1))
                        if "GO TO" in line and (pre1 in line or pre2 in line): #add PR tag for latest only check
                               if "EXIT" not in line:
                                        GTE.append(str(int(line[-8:])+1))                        

                checker=[]
                exist = False
                CRT = []
                i = 0
                while i < len(ALIGN):
                        if ALIGN[0] != '01':
                                CRT.append(ALIGN[1])
                                break
                        elif ALIGN[i] == '88' or ALIGN[i] == '66' or ALIGN[i] == '77':
                               i+=2                               
                        elif ALIGN[i] == '01':
                                exist=False
                                CRT = []
                                checker=['01']
                                i+=2
                        elif ALIGN[i] not in checker:
                                if ALIGN[i] == ALIGN[i-2] or int(ALIGN[i]) == (int(ALIGN[i-2])+ 2):
                                        checker.append(ALIGN[i])
                                        CRT = []
                                        exist = False
                                        i+=2
                                else:     
                                        CRT.append(ALIGN[i+1])                                            
                                        break                                                                                                                                   
                        elif ALIGN[i] in checker and not exist :  
                                CRT = []
                                exist = True
                                i+=2                                                                                                                                    
                        elif exist:
                                if ALIGN[i] == ALIGN[i-2] or int(ALIGN[i]) == (int(ALIGN[i-2])+ 2) or ALIGN[i] == '01':
                                        CRT = []
                                        i+=2
                                else:
                                       CRT.append(ALIGN[i+1])
                                       break

        return LEVEL,WS,PIC,VALUE,TO,ALTER,NXT,CNT,GTE,CRT                    

def CICS_checker(content_array_index,pre1,pre2):
        found = False
        call,gobck = [],[]
        for line in content_array_index:
            if line[6] !="*" and (pre1 in line or pre2 in line):
                if "EXEC CICS" in line:
                    found = True
                if found:
                       if "CICS LINK" in line:
                              call.append(str(int(line[-8:])+1))
                if "END-EXEC" in line or "GOBACK" in line:
                    if found and "GOBACK" in line:
                           gobck.append(str(int(line[-8:])+1))
                    found = False

        return call,gobck  

def SQL_checker(content_array_index,pre1,pre2):
        found = False
        call,gobck = [],[]
        for line in content_array_index:
            if line[6] !="*" and (pre1 in line or pre2 in line):
                if "EXEC CICS" in line or "EXEC SQl" in line:
                    found = True
                if found:
                       if "CICS LINK" in line:
                              call.append(str(int(line[-8:])+1))
                if "END-EXEC" in line or "GOBACK" in line:
                    if found and "GOBACK" in line:
                           gobck.append(str(int(line[-8:])+1))
                    found = False
                if found:
                       if "CICS LINK" in line:
                              call.append(str(int(line[-8:])+1))
        
        return call,gobck       

def COM_check(content_array_index):
       if "(c)" in content_array_index[1]:
              return True
       return False

def VER_check(content_array_index):
       if "*%VERSION:".lower() in content_array_index[3].lower():
              return True
       return False    

def DT_check(content_array_index):
       if '*%DATE_CREATED:'.lower() in content_array_index[4].lower():
              return True
       return False

def DESC_check(content_array_index,pre1,pre2):
    D = False
    DLine = []
    for i in range(len(content_array_index)):
        if 'SECTION.' in content_array_index[i] and (pre1 in content_array_index[i] or pre2 in content_array_index[i]):
            j = 0
            while j <3:
                if content_array_index[i+1][6] != '*':
                    D = True
                    DLine.append(str(int(content_array_index[i+1][-8:])+1))
                    break
                else:
                    j+=1
                    i+=1
                    D = False
    
    return D,DLine
                      
def CALL_check(content_array_index,pre1,pre2):
    C_check = []
    WSVAR = []
    WSVAR_line = []
    for line in content_array_index:
        if line[6] != "*"  and (pre1 in line or pre2 in line):
            if 'CALL ' in line:
                Line = line.strip().split(' ')[1]
                if 'WS-' not in Line:
                       C_check.append(str(int(line[-8:])+1))
                else:
                    if Line not in WSVAR:
                        WSVAR.append(Line)
                        WSVAR_line.append(str(int(line[-8:])+1))
    
    return C_check, WSVAR, WSVAR_line

def WS_var_check(content_array_index,WSVAR,WSVAR_line):
    ws = []
    for i in range(len(content_array_index)):
        if 'WORKING-STORAGE' in content_array_index[i]:
                i+=1
                while i < len(content_array_index):
                        if ("WS-END" in content_array_index[i] or "LINKAGE SECTION" in content_array_index[i] or "PROCEDURE DIVISION" in content_array_index[i]):
                                break
                        else:
                                ws.append(content_array_index[i])
                        i+=1
        i+=1

    for var in WSVAR:
        for sourcews in ws:
            if var in sourcews:
                del WSVAR_line[WSVAR.index(var)]
                WSVAR.remove(var)
                break

    return WSVAR,WSVAR_line            

def THRU_check(content_array_index,pre1,pre2):
    Thru = []
    for line in content_array_index:
        if line[6] != '*'  and (pre1 in line or pre2 in line):
            if 'THRU' in line:
                   Thru.append(str(int(line[-8:])+1))
    
    return Thru                                              
        
def print_final_result(data,count):
        i=0
        print("-----------------------------------------------------------------------")
        print("Component    |  Review comment")
        print("-----------------------------------------------------------------------")
        while i < len(data):
                print("{ele} | {reason}".format(ele=data[i],reason=data[i+1]))
                i+=2
        print("-----------------------------------------------------------------------")
        print("Total review comments : {c}".format(c=count))

if __name__ == '__main__':

        report=[]
        
        PR = input("Please enter your PR# : ")
        if not pr_format_checker(PR):
                print("Invalid PR!!!")
                exit(1)
        path = input("Please enter the folder path where you have placed all the components to be reviewed : ")
        if not path_checker(path):
                print("Invalid path!!!")
                exit(1)
                
        error_log = {1:"COM copyright tag is not proper.",2:"PR# not present in the code logs.",3:"Incorrect version number in the logs.",
                     4:"Date in the modlog doesn't match with the checkout date.",5:"Latest code log does not belong to the ACQ developer.",
                     6:"Tabs are present in the code",7:"Some data is present after the 81st column",8:"Tags are misaligned",
                     9:"Tag is repeated in the COBOL code.",10:"Synergy version is absent in the Synergy tag. Cannot perform version check.",
                     11:"Synergy date is not present in the Synergy tag. Cannot perform date check and COM copyright tag check.",
                     12:"No PR tag is present in the code. Please verify the component.",13:"VALUE literal is not at 40th column",
                     14:"PIC literal is not at 40th column ",15:"WS levels are not at the standard columns",16:"WS varibale is not starting at the standard column",
                     17:"WS Levels discrepancy found at Line Number ",18:"'TO' is not starting at the standard column ",19:"AVOID USE OF ALTER ",
                     20:"AVOID USE OF NEXT SENTENCE ",21:"AVOID USE OF CONTINUE ",22:"AVOID USE OF GO TO BUT GO TO EXIT ACCEPTABLE ",
                     23:"Corresponding End-Compute not found ",24:"USE CALL statement instead of CICS LINK ",25:"USE RETURN instead of GOBACK ",
                     26:"'* (c) YYYY(Current year)  COM Worldwide, Inc' is not found in second line ",27:"'*%version:' is not found in fourth line ", 28:"'*%date_created:' is not found in fifth line ",
                     29:"Add description for Section ",30:"Never allow a program to call itself ",31:"Avoid using static call ",
                     32:"CALL parameters must be passed as level 01 data items ",33:"Avoid use of 'THRU' "}

        pre1 = '01I' + PR[4:]
        pre2 = '01M' + PR[4:]

        for file in os.listdir(path):
                element_path = os.path.join(path,file)
                with open (element_path,"r") as f_content:
                        content_array = f_content.readlines()
                        content_line = " ".join(content_array)
                        
                        content_array_index = []
                        for count,value in enumerate(content_array):
                                index = str(count).zfill(8)
                                content_array_index.append(value + ' ' + index)
                                
                        if synergy_date_checker(content_line):
                            if "(c)" in content_array[1]:
                                    line = 1
                            else:
                                line = 2
                            if not year_tag_checker(content_array[line],content_array):
                                    report.append(file)
                                    report.append(error_log[1])

                            if not log_date_checker(content_array):
                                    report.append(file)
                                    report.append(error_log[4])
                        else:
                            report.append(file)
                            report.append(error_log[11])
                            
                        if not pr_checker(content_line,PR):
                                report.append(file)
                                report.append(error_log[2])
    
                        if synergy_version_checker(content_line):
                            if not version_checker(content_array):
                                    report.append(file)
                                    report.append(error_log[3])
                        else:
                            report.append(file)
                            report.append(error_log[10])

                        if not name_check(content_array):
                                report.append(file)
                                report.append(error_log[5])

                        tab_err = tab_check(content_array)
                        if len(tab_err) > 0:
                                msg_tab=""
                                report.append(file)
                                msg_tab+=error_log[6]
                                msg_tab+=" in the following line nos: "
                                msg_tab+= ",".join(tab_err)
                                report.append(msg_tab)
                                
                        len_err = length_check(content_array)
                        if len(len_err) > 0:
                                len_msg=""
                                report.append(file)
                                len_msg+=error_log[7]
                                len_msg+=" for the following line nos: "
                                len_msg+= ",".join(len_err)
                                report.append(len_msg)

                        if ".cbl" in file.lower() or ".cpy" in file.lower() or ".cob" in file.lower() or ".sbc" in file.lower():
                          
                            if not tag_present(content_line,PR):
                                report.append(file)
                                report.append(error_log[12])
                                
                            tag_err = tag_check(content_array,PR)
                            if len(tag_err) > 0:
                                tag_msg=""
                                report.append(file)
                                tag_msg+=error_log[8]
                                tag_msg+=" for the following line nos: "
                                tag_msg+=",".join(tag_err)
                                report.append(tag_msg)
                                
                        if ".cbl" in file.lower() or ".cob" in file.lower():       
                            ret_cob = cobol_section_check(content_array)
                            if ret_cob != "noerror":
                                msg_cob=""
                                report.append(file)
                                msg_cob+=ret_cob
                                msg_cob+=error_log[9]
                                report.append(msg_cob)
                        
                        if ".cbl" in file.lower() or ".cob" in file.lower():
                                CICS_id, DB2_id = PType(content_array_index)
                                PNAME, PNLINE = Pgm_Name(content_array_index)
                                Pname_line = PNAME_check(content_array_index,PNAME,PNLINE)
                                LEVEL,WS,PIC,VALUE,TO, ALTER,NXT,CNT,GTE,CRT = WS_checks(content_array_index,pre1,pre2)
                                DES,DESC_line = DESC_check(content_array_index,pre1,pre2)
                                C_check,WSVAR,WSVAR_line = CALL_check(content_array_index,pre1,pre2)
                                WS_var,WSVAR_line  = WS_var_check(content_array_index,WSVAR,WSVAR_line)
                                Thru = THRU_check(content_array_index,pre1,pre2)
                                CICS_DB2 = False
                                Batch_only = False
                                CICS_notDB2 = False
                                Batch_DB2 = False
                                CALL, GOBCK = [], []

                                if CICS_id and DB2_id :
                                        CICS_DB2 = True
                                elif not CICS_id and not DB2_id:
                                        Batch_only = True
                                elif CICS_id and not DB2_id :
                                        CICS_notDB2 = True
                                elif not CICS_id and DB2_id:
                                       Batch_DB2 = True

                                if CICS_DB2:
                                       CALL,GOBCK = SQL_checker(content_array_index,pre1,pre2)
                                elif CICS_notDB2:
                                       CALL,GOBCK = CICS_checker(content_array_index,pre1,pre2)
                                
                                if not COM_check(content_array_index):
                                    report.append(file)
                                    report.append(error_log[26])

                                if not VER_check(content_array_index):
                                    report.append(file)
                                    report.append(error_log[27])                                    

                                if not DT_check(content_array_index):
                                    report.append(file)
                                    report.append(error_log[28])

                                if DES:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[29]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(DESC_line)
                                    report.append(len_msg)

                                if Pname_line:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[30]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(Pname_line)
                                    report.append(len_msg)

                                if C_check:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[31]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(C_check)
                                    report.append(len_msg)

                                if WS_var:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[32]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(WSVAR_line)
                                    report.append(len_msg)                                   

                                if Thru:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[33]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(Thru)
                                    report.append(len_msg) 

                                if PIC:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[14]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(PIC)
                                    report.append(len_msg)

                                if VALUE:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[13]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(VALUE)
                                    report.append(len_msg)

                                if WS:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[16]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(WS)
                                    report.append(len_msg)

                                if LEVEL:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[15]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(LEVEL)
                                    report.append(len_msg)

                                if CRT:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[17]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(CRT)
                                    report.append(len_msg)

                                if TO:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[18]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(TO)
                                    report.append(len_msg)                                    

                                if ALTER:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[19]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(ALTER)
                                    report.append(len_msg)   

                                if NXT:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[20]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(NXT)
                                    report.append(len_msg)

                                if CNT:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[21]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(CNT)
                                    report.append(len_msg)        

                                if GTE:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[22]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(GTE)
                                    report.append(len_msg)     

                                if CALL:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[24]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(CALL)
                                    report.append(len_msg) 

                                if GOBCK:
                                    len_msg=""
                                    report.append(file)
                                    len_msg+=error_log[25]
                                    len_msg+=" for the following line nos: "
                                    len_msg+= ",".join(GOBCK)
                                    report.append(len_msg) 

                        if file not in report:
                            report.append(file)
                            report.append("No review comments.")
        
        
        t_count = report.count("No review comments.") * 2
        count_review = len(report) - t_count
        c = count_review//2
        print_final_result(report,c)
        
        
        
