import numpy as np
import os
import math as mth


def is_valid_file(path):
    arc_type = os.path.splitext(str(path))[-1]
    return os.path.isfile(path) and (arc_type == ".dat" or arc_type == ".txt")

def get_first_valid_line_index(lines):
    for i in range(len(lines)):
        if lines[i][0] != '#':
            return i;
    return Null


def for_all_folders_on_path(path):
    arcs = os.listdir(path)
    print("Found " + str(len(arcs)) + " folder in " + path)
    for archive in arcs:
    	
        print(" Starting: " + archive)
        path_n = os.path.join(path, archive)
        create_average_file(path_n, path)
        print("  Done!")
        print("")

def create_average_file(path, dirname_general):
    dic = {}
    key = "key"
    dir_name = None
    headerText = None
    N = 0

    for archive in os.listdir(path):
        path_n = os.path.join(path, archive)
        if is_valid_file(path_n):
            try:
                with open(path_n, 'r', encoding='utf-8') as file:
                    N = N + 1
                    if(dir_name == None):
                        dir_name = os.path.basename(os.path.dirname(path_n))
                    lines = file.readlines()
                    initial_data_line = get_first_valid_line_index(lines)
                    if headerText == None:
                        headerText = lines[initial_data_line - 1]
                    data_matrix = np.array([line.split() for line in lines[initial_data_line:]], dtype=object).astype(float)
                    data_list = [float(line.split()) for line in lines[initial_data_line:]]
                    #data = [arr for arr in data_matrix]
                    data = data_list
                    if key not in dic:
                        dic[key] = (data, 1)
                    else:
                        dic[key] = ([a + b for a, b in zip(data, dic[key][0])], dic[key][1] + 1)
            except Exception as e:
                print("     The following error occurred during the compression of the file: " + path_n)
                print("      " + str(e))
                return                
    for key in dic.keys():
        data = dic[key][0]
        n = dic[key][1]
        dic[key] = ([a / n for a in data], n)
    dirname_general = dirname_general.split("/")[-1]
    path_n = outputs_path() + "/" + dirname_general + "/" + dir_name + "_avg.dat"
    
    os.makedirs(os.path.dirname(path_n), exist_ok=True)
    with open(path_n, 'w') as file:
        file.write("# N: " + str(N) + "\n")
        file.write(headerText)
        np.savetxt(file, np.column_stack(dic[key][0]))
        file.close()
        
        
def inputs_path():
    return str(os.path.dirname(os.path.abspath(__file__)) + "/inputs")


def outputs_path():
    return str(os.path.dirname(os.path.abspath(__file__)) + "/outputs")


def createDirAtPath(path):
	os.makedirs(path, exist_ok=True)

def createNecessaryPaths():
	createDirAtPath(inputs_path());
	createDirAtPath(outputs_path());
	

p = None
i = 0
createNecessaryPaths()
path = inputs_path()
dirs = []
dirs = os.listdir(path)
d = []
for arc in dirs:
    if arc != "data":
        print(str(i)+": "+arc)
        d.append(arc)
        i += 1
if len(d) > 0:
	print("Which directory you want to analyze?\n")
	while p == None:
		try:
		    numero = int(input("\n"))
		    p = d[numero]
		except (ValueError, IndexError):
		    print("Please, insert a valid number.")
	for_all_folders_on_path("inputs/"+p)
else:
	print("There's no data to analyze...")
	print("	Please, add archives to a directory inside 'data' to analyze all the data archives inside it.")
