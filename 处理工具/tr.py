import json
import codecs
import copy
import os
from tqdm import tqdm

def trans(file):
    with codecs.open(file, "r") as f:
        j = json.load(f)
    
    j_new = copy.copy(j)
    j_new["notes"] = []

    delete_list = []
    id_list = [0]
    counter = 1

    for note in j["notes"]:
        if not "pos" in note.keys():
            note["pos"] = 0
            j_new["notes"].append(note)
            id_list.append(note["$id"])
            note["$id"] = counter
            counter += 1
        elif note["pos"] > 3.499:
            delete_list.append(note["$id"])
        else:
            j_new["notes"].append(note)
            id_list.append(note["$id"])
            note["$id"] = counter
            counter += 1
    
    j_new["links"] = []

    for link in j["links"]:
        link_new = []
        for note in link["notes"]:
            if note["$ref"] in delete_list:
                delete_list.pop(delete_list.index(note["$ref"]))
            else:
                link_new.append(note)
        if link_new:
            for note in link["notes"]:
                note["$ref"] = id_list.index(note["$ref"])
            j_new["links"].append(link)
    
    with codecs.open(file, "w") as f:
        json.dump(j_new, f)


re = [0, 0]
failed_file = "failed.txt"

with open(failed_file, "w") as ff:
    for file_name in tqdm(os.listdir("./")):
        if ".json" in file_name:
            try:
                trans(file_name)
                re[0] += 1
            except:
                ff.writelines(file_name + "\t转换失败\n")
                re[1] += 1
    print("%i个文件转换成功，%i个文件转换失败！" %(re[0], re[1]))
    ff.writelines("%i个文件转换成功，%i个文件转换失败！" %(re[0], re[1]))