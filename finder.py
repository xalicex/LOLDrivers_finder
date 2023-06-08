import json

dico_driver_terminate = {}
mydico = {}

with open('drivers.json', 'r', encoding="utf8") as f:
    json_data = json.load(f)
    

terminate_functions = ["ZwTerminateProcess","NtTerminateProcess"]
open_functions = ["ZwOpenProcess","NtOpenProcess"]

for driver in json_data:
    flag = 0
    try: 
        md5list = []
        namelist = []
        name_and_hash={}

        for elem in driver['KnownVulnerableSamples']:
            if (any(func in elem['ImportedFunctions'] for func in terminate_functions) and any(func2 in elem['ImportedFunctions'] for func2 in open_functions)):
                flag = 1
                
                try:
                    md5list.append(elem["MD5"])
                except:
                    pass
                
                try:
                    namelist.append(elem["Filename"])
                except:
                    try:
                        namelist.append(elem["FileName"])
                    except:
                        namelist.append("no_name")       
                    
                
        if(flag):
            dico_driver_terminate[driver['Id']] = driver
            if(md5list):
                name_and_hash["md5"]=md5list
            if(namelist):
                name_and_hash["names"]=namelist
            
            mydico[driver['Id']] = name_and_hash
    except:
        continue


#print(mydico["22aa985b-5fdb-4e38-9382-a496220c27ec"])
for elem in mydico:
    print("\nID : "+elem)
    print("names : "+str(mydico[elem]["names"]))
    print("md5 : "+str(mydico[elem]["md5"]))

unique_name = []
for elem in mydico:
    for name in mydico[elem]["names"]:
        if name.lower() not in unique_name:
            print(name.lower())
            unique_name.append(name.lower())
