from pyDOE2 import *
import time
import matplotlib.pyplot as plt
from xosc_reader import change_scenario
import os
import sys
import json
import argparse

''' OpenScenario variables to change. Thank god theyre normalized 
example ALKS Scenario 4.1_2 Swerving lead vehicle.
Params:
	Ego_InitSpeed_Ve0
	S_value = 16.6667

	LeadVehicle_InitDistance_dx0
	S_value = 33.3333

	Swerve_Offset_Left
	S_value = 1.0

	Swerve_Offset_Right
	S_value = -1.0

	Swerve_MaxLateralAcc
	S_value = 0.3 

for the future we could also change nominal labels like 
dynamicShape = sinusoidal/linear

This time we have 5 factors we can vary.
2 of these factors need to be normalized
'''

parser = argparse.ArgumentParser()
parser.add_argument('--scenario', help='path of the scenario',
                    default='/home/l/doe/ALKS_Scenario_4.1_2_SwervingLeadVehicle_TEMPLATE.xosc', type=str)
parser.add_argument('--samples', help='amount of scenarios to be created', type=int,
                    default=30)
parser.add_argument('--criterion', help='a string that tells lhs how to sample the points', type=str,
                    default='corr')
args = parser.parse_args()


print('#######################################')
print('##Welcome to Latin Hypercube sampling##')
print('#######################################')


with open('parameters_config.json') as json_file:
    data = json.load(json_file)
    param_list = list(data.keys())


def doe(scenario, n, samples, criterion, factor):

	# number of factors
	# eg speed and steering ankle
	# n = 3

	# int that designates the number of sample points for each factor
	# samples = 10

	# critertion to randomize
	# criterion = 'corr'
	save_path = 'new_scenarios'
	counter = 0

	# create the lhs matrix
	lhs_matrix = lhs(n=n, samples=samples, criterion=criterion)

	# initialize empty list to hold the parameters
	lhs_params = []

	# iterate through the lhs matrix and create list with tuples containing parameter name and value
	for i in range(len(lhs_matrix)):
		entry = []
		for x in range(len(lhs_matrix[i])):
			# print(lhs_matrix[i][x])
			entry.append((param_list[x], round(lhs_matrix[i][x]*data.get(param_list[x]), 4)))
		lhs_params.append(entry)

	'''iterate through the list and create scenarios 
	according to vectors'''
	for scenario_params in lhs_params:
		counter += 1
		scenario_name = 'LHS_scenario_' + str(counter) + '.xosc'
		complete_name = os.path.join(save_path, scenario_name)
		n_scenario = open(complete_name, "w")
		n_scenario = change_scenario(scenario, scenario_params)
		n_scenario.write(complete_name, encoding='utf-8', xml_declaration=True)

	plt.scatter(lhs_matrix[:,0], lhs_matrix[:,1])
	plt.title("Latin Hypercube")
	plt.xlabel("x-range")
	plt.ylabel("y-range")
	plt.grid()
	plt.show()

	


doe(scenario=args.scenario, n=len(data.keys()), samples=args.samples, criterion=args.criterion, factor=3)