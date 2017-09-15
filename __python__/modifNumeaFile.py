from __future__ import print_function
import xml.etree.ElementTree as ET
import sys


# if dbg_ = True 
#   script 'modifNumeaFile" can be launched without argument (debugging mode).
# It requires put "input1.nma" file in the same directory.

dbg_ = False


if dbg_ :
    argv = ["modifNumeaFile","NMA_FILE","input1.nma",\
            "Solver","gen_solver_ddsolv",\
            "blablafile","false",\
            "dumpfile","false",\
            "FETI","1",\
            "eps_iter","1e-5",\
            "dumpfileCSRmatrix","false",\
            "LocalSolver","0",\
            "MortarLocalization","master"]
    sys.argv = argv


def setPar(argv,param):
    try:
        i = argv.index(param)
    except ValueError:
        i = -1
    if i < 0 or i == len(argv): 
        print("parameter %s does not exist" % (param))
        print("\n or  %s does not have specified a value" % (param))
        outList = []
    else:
        outList = [ param, argv[i+1] ]
        argv.pop(i)
        argv.pop(i)

    return outList 

NMA_FILE = None 

ddsolv_setting = {}

if len(sys.argv)>0:

    # first entry is name of this script
    sys.argv.pop(0)	
    print("dddsolv_input_param = ",sys.argv)

    outList = setPar(sys.argv,"NMA_FILE") 
    if len(outList)==2:
        str0 = outList[0]+"=str('"+outList[1]+"')"
        exec(str0); print(str0) 

    ddsolv_input_param = sys.argv 
    print("dddsolv_input_param = ",ddsolv_input_param)
    if (len(ddsolv_input_param) % 2) is not 0:
        print( "number of input 'ddsolv' must be even")

    for i in range( int(0.5 * len(ddsolv_input_param)) ):
        if ddsolv_input_param[2 * i + 1] is not "":
            ddsolv_setting[ddsolv_input_param[2 * i]] = ddsolv_input_param[2 * i + 1]


if  NMA_FILE is not None:
    tree = ET.parse(NMA_FILE)
    root = tree.getroot()
    
 
print("\n\n--\n")
all_root = root.getiterator()     
for ii in all_root: 
     
    if ddsolv_setting.get(ii.tag) != None:
        
        
        if ii.tag == "Solver":        
            ii.attrib["name"] = ddsolv_setting.get(ii.tag)
            continue
        
        ii.text = ddsolv_setting.get(ii.tag)
        

if dbg_:
    NMA_FILE = "_"+NMA_FILE
 
tree.write(NMA_FILE)
