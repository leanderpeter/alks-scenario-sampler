import xml.etree.ElementTree as ET
from io import BytesIO


def change_scenario(scenario, param_list):

	tree = ET.parse(scenario)

	root = tree.getroot()

	for el in root.iter('ParameterDeclaration'):
		for i in range(len(param_list)):
			if el.attrib['name'] == str(param_list[i][0]):
				el.set('value', str(param_list[i][1]))

	tree.write('n_scenario.xosc', encoding='utf-8', xml_declaration=True)


	return tree