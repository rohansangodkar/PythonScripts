import time

import datetime

import os

 

if not os.path.exists(r"G:\Users\Scripts\team_list\ACQ.txt"):

                print(r"G drive is not connected!! Cannot access G:\Users\Scripts\team_list\ACQ.txt")

                exit(1)

               

with open (r"G:\Users\Scripts\team_list\ACQ.txt","r") as name:

                names = name.readlines()

               

 

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

        if not pr[5:].isnumeric():

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

                                line_splt=line.split(" ")

                                if count == 1:

                                        comp = line_splt[1]

                                                       

                                else:

                                        for l in line_splt:

                                                if "*" not in l and "version" not in l.lower() and ":" not in l and "-" not in l :

                                                        if comp == l:

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

        pre1 = "01I"+pr[5:]

        pre2 = "01M"+pr[5:]

        pr_tag = [pre1,pre2]

        count = 0

        err = []

        for d in data:

            count+=1

            if pr_tag[0] in d:

                if d[72:80] != pr_tag[0]:

                    err.append(count)

            elif pr_tag[1] in d:

                if d[72:80] != pr_tag[1]:

                    err.append(count)

        return err

   

def cobol_section_check(data):

        section = []

        exits = []

        for d in data:

                if "SECTION." in d:

                        d = d.strip()

                        splt = d.split(" ")

                        if splt[0][0] != "*" and splt[0].lower() != "file":

                                if splt[0] in section:

                                        return splt[0]

                                section.append(splt[0])
 

        return "noerror"

 

def print_final_result(data):

        i=0

        print("-----------------------------------------------------------------------")

        print("Component    |  Review comment")

        print("-----------------------------------------------------------------------")

        while i < len(data):

                print("{ele} | {reason}".format(ele=data[i],reason=data[i+1]))

                i+=2

        print("-----------------------------------------------------------------------")

        print("Total review comments : {c}".format(c=len(data)//2))

 

 

if __name__ == '__main__':

 

        report=[]

       

        PR = input("Please enter your PR# : ")

        if not pr_format_checker(PR):

                print("Invalid PR!!!")

                exit(1)

        path = input("Please enter the folder path where you have placed all the components to be  reviewed : ")

        if not path_checker(path):

                print("Invalid path!!!")

                exit(1)

               

        error_log = {1:"Company copyright tag is not proper.",2:"PR# not present in the code logs.",3:"Incorrect version number in the logs.",

                     4:"Date in the modlog doesn't match with the checkout date.",5:"Latest code log does not belong to the ACQ developer.",

                     6:"Tabs are present in the code",7:"Some data is present after the 81st column",8:"Tags are misaligned or some junk value present in the column 72 till 80",

                     9:"tag is repeated in the COBOL code."}

       

        for file in os.listdir(path):

                element_path = os.path.join(path,file)

                with open (element_path,"r") as f_content:

                        content_array = f_content.readlines()

                        content_line = " ".join(content_array)

                       

                        if "(c)" in content_array[1]:

                                line = 1

                        else:

                                line = 2

                        if not year_tag_checker(content_array[line],content_array):

                                report.append(file)

                                report.append(error_log[1])

 

                        if not pr_checker(content_line,PR):

                                report.append(file)

                                report.append(error_log[2])

 

                        if not version_checker(content_array):

                                report.append(file)

                                report.append(error_log[3])

 

                        if not log_date_checker(content_array):

                                report.append(file)

                                report.append(error_log[4])

 

                        if not name_check(content_array):

                                report.append(file)

                                report.append(error_log[5])

 

                        tab_err = tab_check(content_array)

                        if len(tab_err) > 0:

                                msg_tab=""

                                report.append(file)

                                msg_tab+=error_log[6]

                                msg_tab+=" in the following line nos:"

                                msg_tab+= ",".join(tab_err)

                                report.append(msg_tab)

                               

                        len_err = length_check(content_array)

                        if len(len_err) > 0:

                                len_msg=""

                                report.append(file)

                                len_msg+=error_log[7]

                                len_msg+=" for the following line nos:"

                                len_msg+= ",".join(len_err)

                                report.append(len_msg)

 

                        if ".cbl" in file.lower():

                            tag_err = tag_check(content_array,PR)

                            if len(tag_err) > 0:

                                tag_msg=""

                                report.append(file)

                                tag_msg+=error_log[8]

                                tag_msg+=" for the following line nos:"

                                tag_msg+=",".join(tag_err)

                                report.append(tag_msg)

                                

                            ret_cob = cobol_section_check(content_array)

                            if ret_cob != "noerror":

                                msg_cob=""

                                report.append(file)

                                msg_cob+=ret_cob

                                msg_cob+=error_log[9]

                                report.append(msg_cob)

 

                               

        print_final_result(report)

       

        

        
