import os

import shutil

import time

 

###################################################################

#Coded by ROHAN SANGODKAR.

###################################################################

###################################################################

#Capturing start time.

###################################################################

start = time.time()

 

###################################################################

#Header

###################################################################

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

print("x Welcome to the package creation utility!!! x")

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

###################################################################

#Option select logic.

###################################################################

print("You want to create a package for?")

print("1. Oracle")

print("2. Postgres")

region=input("Option:")

 

region=region.strip()

 

if region!='1' and region!='2':

                print("Invalid selection!")

                exit()

###################################################################

#Accepting the package name.

###################################################################

print('\n')

name=input("Enter the package name:")

 

name=name.strip()

 

if len(name)==0:

                print("Package name cannont be empty!")

                exit()

ban=r'\/:?<",>|'

for l in name:

                if l in ban:

                                print("Invalid package name!")

                                print(ban)

                                print("Above special characters are not allowed.")

                                exit()

###################################################################

#Accepting the package path.

###################################################################

pkg_path = input(r"Please enter the path for final package:")

 

pkg_path=pkg_path.strip()

 

if pkg_path[0]==r"'" or pkg_path[0]==r'"':

                pkg_path=pkg_path[1:]

if pkg_path[-1]==r"'" or pkg_path[-1]==r'"':

                pkg_path=pkg_path[:len(pkg_path)-1]  

 

if pkg_path[-1] != "\\":

                pkg_path += "\\"

 

if not os.path.isdir(pkg_path):

                print("This path is invalid.")

                exit()

 

zip_dest=pkg_path[:]

 

pkg_path+=name

 

if os.path.isdir(pkg_path):

                print("Folder with the same name already exists.")

                exit()

 

###################################################################

#Accepting the Synergy path.

###################################################################

syn_path = input(r"Please enter the Base Synergy path:")

 

syn_path=syn_path.strip()

 

if syn_path[0]==r"'" or syn_path[0]==r'"':

                syn_path=syn_path[1:]

if syn_path[-1]==r"'" or syn_path[-1]==r'"':

                syn_path=syn_path[:len(syn_path)-1]    

 

if syn_path[-1] != "\\":

                syn_path += "\\"

 

if not os.path.isdir(syn_path):

                print("This path is invalid.")

                exit()

 

#mainframe check:

syn_path+='\\acq\\mainframe'

if not os.path.isdir(syn_path):

                print("This path is invalid.")

                exit()

syn_path=syn_path.replace('\\acq\\mainframe','')

 

#unix check:

syn_path+='acq\\unix'

if not os.path.isdir(syn_path):

                print("This path is invalid.")

                exit()

syn_path=syn_path.replace('\\unix','')

 

###################################################################

#Accepting the intskels path.

###################################################################

intskel_path = input(r"Please enter the intskels Synergy path:")

 

intskel_path=intskel_path.strip()

 

if intskel_path[0]==r"'" or intskel_path[0]==r'"':

                syn_path=syn_path[1:]

if intskel_path[-1]==r"'" or intskel_path[-1]==r'"':

                intskel_path=intskel_path[:len(intskel_path)-1] 

 

if intskel_path[-1] != "\\":

                intskel_path += "\\"

 

if not os.path.isdir(intskel_path):

                print("This path is invalid.")

                exit()

 

#internal folder check:

intskel_path=os.path.join(intskel_path,'internal')

 

if not os.path.isdir(intskel_path):

                print("This path is invalid.")

                exit()

###################################################################

#Accepting the PR.

###################################################################

pr=input("Please enter your PR number:")

 

pr=pr.strip()

if len(pr)!=9:

                print("Invalid PR length.")

                exit()

if pr[:2].lower() != "uk":

                print("Invalid PR tag. PR should start with UK.")

                exit()

if not pr[2].isnumeric():

                print("Invalid PR tag.")

                exit()

if pr[3] != "#":

                print("Invalid PR tag.")

                exit()

if not pr[4:].isnumeric():

                print("Invalid PR tag.")

                exit()

###################################################################

#Creating the main directory.

###################################################################

 

os.mkdir(pkg_path)

 

###################################################################

#Synergy path modification as per the user's choice.

###################################################################

if region=='1':

                syn_path+='\\unix\\oracle'

else:

                syn_path+='\\unix\\postgres'

###################################################################

#Creating the subfolders within main directory and copying from

#Synergy.

###################################################################

print("\n")

print("Processing started...")

#cbl

print("copying cbl.")

pkg_path+='\\cbl'

syn_path+='\\source\\cbl'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\cbl','')

syn_path=syn_path.replace('\\source\\cbl','')

print("cbl copied.")

 

#classes

print(".")

print("copying classes.")

pkg_path+='\\classes'

syn_path+='\\executables\\classes'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\classes','')

syn_path=syn_path.replace('\\executables\\classes','')

print("classes copied.")

 

#copybook

print(".")

print("copying copybooks.")

pkg_path+='\\copybook'

syn_path+='\\source\\copybook'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\copybook','')

syn_path=syn_path.replace('\\source\\copybook','')

print("copybooks copied.")

 

#dclgen

print(".")

print("copying declgens.")

pkg_path+='\\dclgen'

syn_path+='\\source\\dclgen'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\dclgen','')

syn_path=syn_path.replace('\\source\\dclgen','')

print("declgens copied.")

 

#ddl

print(".")

print("copying ddls.")

pkg_path+='\\ddl'

syn_path+='\\database\\ddl'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\ddl','')

syn_path=syn_path.replace('\\database\\ddl','')

print("ddls copied.")

 

#ddl_update                      

pkg_path+='\\ddl_update'

os.mkdir(pkg_path)

pkg_path=pkg_path.replace('\\ddl_update','')

 

#ref_data

print(".")

print("copying ref datas.")

pkg_path+='\\ref_data'

syn_path+='\\database\\ref_data'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\ref_data','')

syn_path=syn_path.replace('\\database\\ref_data','')

print("ref datas copied.")

 

#ref_data_update

pkg_path+='\\ref_data_update'

os.mkdir(pkg_path)

pkg_path=pkg_path.replace('\\ref_data_update','')

 

#postgres/oracle parms

if region=='1':

                print(".")

                print("copying Oracle parms")

                pkg_path+='\\oracle_parms'

                syn_path+='\\database\\oracle_parms'

                shutil.copytree(syn_path,pkg_path)

                pkg_path=pkg_path.replace('\\oracle_parms','')

                syn_path=syn_path.replace('\\database\\oracle_parms','')

                print("Oracle parms copied.")

else:

                print(".")

                print("copying Postgres parms")

                pkg_path+='\\postgres_parms'

                syn_path+='\\database\\postgres_parms'

                shutil.copytree(syn_path,pkg_path)

                pkg_path=pkg_path.replace('\\postgres_parms','')

                syn_path=syn_path.replace('\\database\\postgres_parms','')

                print("Postgres parms copied.")

 

###################################################################

#shared components processing.

###################################################################

syn_path=syn_path.replace('\\oracle','')

syn_path=syn_path.replace('\\postgres','')

syn_path+='\\shared'

#batch_scripts

print(".")

print("copying batch scripts.")

pkg_path+='\\batch_scripts'

syn_path+='\\batch_scripts'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\batch_scripts','')

syn_path=syn_path.replace('\\batch_scripts','')

print("batch scripts copied.")

 

#parms

print(".")

print("copying parms.")

pkg_path+='\\parms'

syn_path+='\\parms'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\parms','')

syn_path=syn_path.replace('\\parms','')

print("parms copied.")

 

#c_header

print(".")

print("copying c_header.")

pkg_path+='\\c_header'

syn_path+='\\source\\c_header'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\c_header','')

syn_path=syn_path.replace('\\source\\c_header','')

print("c_header copied.")

 

#c_source

print(".")

print("copying c_source.")

pkg_path+='\\c_source'

syn_path+='\\source\\c_source'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\c_source','')

syn_path=syn_path.replace('\\source\\c_source','')

print("c_source copied.")

 

#linux_shared_objects

print(".")

print("copying linux shared objects.")

pkg_path+='\\linux_shared_objects'

syn_path+='\\executables\\linux_shared_objects'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\linux_shared_objects','')

syn_path=syn_path.replace('\\executables\\linux_shared_objects','')

print("Linux shared objects copied.")

 

syn_path+='\\files'

 

#app_files

print(".")

print("copying app files.")

pkg_path+='\\app_files'

syn_path+='\\app_files'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\app_files','')

syn_path=syn_path.replace('\\app_files','')

print("app files copied.")

 

#cosbatch

print(".")

print("copying cosbatch files.")

pkg_path+='\\cosbatch'

syn_path+='\\cosbatch'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\cosbatch','')

syn_path=syn_path.replace('\\cosbatch','')

print("cosbatch files copied.")

 

#cosort_cards

print(".")

print("copying cosort cards files.")

pkg_path+='\\cosort_cards'

syn_path+='\\cosort_cards'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\cosort_cards','')

syn_path=syn_path.replace('\\cosort_cards','')

print("cosort cards copied.")

 

#ctl

print(".")

print("copying ctl files.")

pkg_path+='\\ctl'

syn_path+='\\ctl'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\ctl','')

syn_path=syn_path.replace('\\ctl','')

print("ctl copied.")

 

#ddf

print(".")

print("copying ddf files.")

pkg_path+='\\ddf'

syn_path+='\\ddf'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\ddf','')

syn_path=syn_path.replace('\\ddf','')

print("ddf copied.")

 

#mtp_sys

print(".")

print("copying mtp_sys files.")

pkg_path+='\\mtp_sys'

syn_path+='\\mtp_sys'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\mtp_sys','')

syn_path=syn_path.replace('\\mtp_sys','')

print("mtp_sys copied.")

 

#statement

print(".")

print("copying statements.")

pkg_path+='\\statement'

syn_path+='\\statement'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\statement','')

syn_path=syn_path.replace('\\statement','')

print("statements copied.")

 

#tools

print(".")

print("copying tools.")

pkg_path+='\\tools'

syn_path+='\\tools'

shutil.copytree(syn_path,pkg_path)

pkg_path=pkg_path.replace('\\tools','')

syn_path=syn_path.replace('\\tools','')

print("tools copied.")

 

###################################################################

#intskels processing.

###################################################################

if region=='1':

                intskel_path=os.path.join(intskel_path,"acquirer_unix")

                intskel_path=os.path.join(intskel_path,"acq_compliance")

else:

                intskel_path=os.path.join(intskel_path,"acquirer_postgres")

                intskel_path=os.path.join(intskel_path,"acq_compliance")

 

#RDATA

print(".")

print("copying rdatas from intskels.")

intskel_path=os.path.join(intskel_path,"rdata")

 

for file in os.listdir(intskel_path):

                src=os.path.join(intskel_path,file)

                dest=os.path.join(pkg_path,"ref_data")

                shutil.copy2(src,dest)

pkg_path=pkg_path.replace('\\ref_data','')

intskel_path=intskel_path.replace('\\rdata','')

print("rdatas from intskels copied.")

 

#ADTA(Based on PR)

print(".")

print("copying adta.")

intskel_path=os.path.join(intskel_path,"adata")

dest=os.path.join(pkg_path,"ref_data_update")

for filename in os.listdir(intskel_path):

                file_path=os.path.join(intskel_path,filename)

                with open(file_path,'r') as file:

                                file_contents = file.read()

                                if pr in file_contents:

                                                shutil.copy2(file_path,dest)

intskel_path=intskel_path.replace('\\adata','')

print("adta copied.")

 

#AGEN(Based on PR)

print(".")

print("copying agen.")

intskel_path=os.path.join(intskel_path,"agen")

dest=os.path.join(pkg_path,"ddl_update")

for filename in os.listdir(intskel_path):

                file_path=os.path.join(intskel_path,filename)

                with open(file_path,'r') as file:

                                file_contents = file.read()

                                if pr in file_contents:

                                                shutil.copy2(file_path,dest)

intskel_path=intskel_path.replace('\\agen','')

print("agen copied.")

###################################################################

#Zipping the folder.

###################################################################

 

print('\n')

print("Zipping the folder...")

print("...")

print("Please do not terminate the session.")

print("This step will run for a while.")

shutil.make_archive(name,'zip',pkg_path)

pkg=name+'.zip'

cwd=os.getcwd()

cwd=os.path.join(cwd,pkg)

zip_dest+=pkg

 

shutil.move(cwd,zip_dest)

 

###################################################################

#Information display.

###################################################################

print('\n')

print("Your package folder structure is created at:")

print(pkg_path)

print('\n')

print("Your zip file is located at:")

print(zip_dest)

###################################################################

#Capturing end time.

###################################################################

end = time.time()

total_time = end - start

m, s = divmod(total_time, 60)

print('\n')

print("Script got completed in",round(m),'minutes and',round(s),'seconds.')

print('\n')

print("            !!!!!!!!!!!THANK YOU!!!!!!!!!!!                 ")

print("************************************************************")

time.sleep(100)
