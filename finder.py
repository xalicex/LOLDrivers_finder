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

            set_imported_functions = set(elem['ImportedFunctions'])
            set_open = set(open_functions)
            set_terminate = set(terminate_functions)

            if((len(set_imported_functions.intersection(set_open)) > 0) and (len(set_imported_functions.intersection(set_terminate)) > 0)):

                flag = 1
                
                for key, data in elem.items():
                    if("md5" in key.lower()):
                        md5list.append(elem[key])
                    if("filename" in key.lower()):
                        namelist.append(elem[key])
                    
        if(flag):
            dico_driver_terminate[driver['Id']] = driver
            if(md5list):
                name_and_hash["md5"]=md5list
            if(namelist):
                name_and_hash["names"]=namelist
            
            mydico[driver['Id']] = name_and_hash
    except:
        continue



for elem in mydico:
    print("\nID : "+elem)
    print("names : "+str(mydico[elem]["names"]))
    print("md5 : "+str(mydico[elem]["md5"]))

#print(mydico["22aa985b-5fdb-4e38-9382-a496220c27ec"])

"""
unique_name = []
for elem in mydico:
    for name in mydico[elem]["names"]:
        if name.lower() not in unique_name:
            unique_name.append(name.lower())
            print(name)
"""
