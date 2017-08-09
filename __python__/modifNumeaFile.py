from __future__ import print_function
import xml.etree.ElementTree as ET
import sys


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
ddsolv_or_pardiso = None

ddsolv_setting = {}

if len(sys.argv)>0:

	sys.argv.pop(0)	
	print("dddsolv_input_param = ",sys.argv)

	outList = setPar(sys.argv,"NMA_FILE") 
	if len(outList)==2:
		str0 = outList[0]+"=str('"+outList[1]+"')"
		exec(str0); print(str0)

	outList = setPar(sys.argv,"ddsolv_or_pardiso") 
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

	

	

#ddsolv_or_pardiso = 'pardiso'
#path_to_my_xml = "circle_ddsolv.nma" 



#ddsolv_setting = {'dumpfile': 'true','blablafile':'true','FETI' : '2',\
#    			'Tolerance' : '1e-3','eps_iter' : '1e-4',\
#    			'force_unsymmetric' : '1','LocalSolver' : '2'}

#######################################################################################
if  NMA_FILE is not None:
	tree = ET.parse(NMA_FILE)
	root = tree.getroot()

	# name of used solver
	SIMULATION_Solver_name = root.findall('./SIMULATION/Solver')[-1].attrib['name']
	# change "NonLinearSolver" (assumption only one NonLinearSolver is present)
	# <NonLinearSolver linear="ddsolv" name="nls_ddsolv" type="FULL_NEWTON">  
	SOL_COL__NonLinSol = root.findall('./SOLVER_COLLECTION/NonLinearSolver') # [0].attrib['name']
	for i in range(len(SOL_COL__NonLinSol)):
		if (SOL_COL__NonLinSol[i].attrib.get('name') is not None and \
				SOL_COL__NonLinSol[i].attrib['name'] == SIMULATION_Solver_name):
			used_SOL_COL__NonLinSol = SOL_COL__NonLinSol[i]
			break 
	if used_SOL_COL__NonLinSol.attrib.get('linear') is not None:
		used_SOL_COL__NonLinSol.attrib['linear'] = ddsolv_or_pardiso
		print("solver setup:\t%s" % (ddsolv_or_pardiso))
	#NonLinearSolver.set('linear','pardiso')


	# change DDSolv parameters
	LinearSolver = root.findall("./SOLVER_COLLECTION/LinearSolver")
	for i in range(len(LinearSolver)):
		if (LinearSolver[i].attrib.get('name') is not None and \
			LinearSolver[i].attrib['name'] == 'ddsolv'):
			i_LinearSolver = LinearSolver[i]
			for j in ddsolv_setting.iteritems():
				for k in range(len(i_LinearSolver)):
					if i_LinearSolver[k].tag == j[0]:
						print('---')
						print(i_LinearSolver[k].tag)
						print(i_LinearSolver[k].text)
						print(j[1])
						i_LinearSolver[k].text = j[1]
						break	

	tree.write(NMA_FILE)
