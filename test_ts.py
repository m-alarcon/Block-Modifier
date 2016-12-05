import numpy as np
import math
import random as rnd
import csv

num_entradas = 27
num_coeficientes = 55

def calcula_t(array_coef, array_entradas):

	t = float(0)
	if (array_entradas.shape[0]+1 == array_coef.shape[0]):
		for i in range(0, array_entradas.shape[0]-1):
			t = t + (array_coef[i]*array_entradas[i])

	elif ((2*array_entradas.shape[0])+1 == array_coef.shape[0]):
		for i in range(0, array_entradas.shape[0]-1):
			t = t + (array_coef[i]*array_entradas[i])
			t = t + (array_coef[i+array_entradas.shape[0]]*(array_entradas[i]**2))

	t = t + array_coef[array_coef.shape[0]-1]

	return t


def extraccion_salidas(array_coef):

	array_entradas = np.zeros(num_entradas, 'float')
	n_fallos = 0
	reader = csv.reader(open('entrenamientoFiltrado.csv'))#entrenamientoFiltrado.csv'))
	for index, row in enumerate(reader):
		for i in range(1, num_entradas+1):
			array_entradas[i-1] = row[i]
		for j in range(num_entradas+1, num_entradas+2):
			salida = float(row[j])
			salida_calculada = calcula_t(array_coef, array_entradas)
			error_cometido = abs(salida-salida_calculada)
			print ("Se esperaba: ", salida, "se ha obtenido: ", salida_calculada, "cometiendo un error de: ", error_cometido)
			if error_cometido > 0.01:
				n_fallos += 1
	print (n_fallos)



array_coef = np.array([-0.39876827827,0.115497103325,0.559520152414,1.49942196467,-1.11287954474,1.17048921504,-2.0432747666,-0.571854490639,5.95794183831,0.0190734538255,0.657177563442,-1.1266214016,-3.03806872425,-0.155779945193,-0.686880308284,0.911990178763,0.199942948879,1.1828709574,0.00619105544995,0.0490288653883,1.55176603171,1.34362561862,0.114275760608,1.15718159867,0.647734680775,1.06350728872,-443.075762199,0.271492317873,-0.124408675589,-0.398060451526,-1.23638347327,0.895908239036,-0.903604831826,1.68193574104,0.417234994967,-4.5786515958,0.0152289987111,-0.481111774032,0.858895069517,2.25020922363,0.126854119064,0.534625395696,-0.681292690238,0.674866343702,-0.714748058287,3.07375130385,0.795563364734,-5.79973119305,-6.25254404621,1.1218729567,-2.01860439281,-0.311832195513,-1.83574088042,74.3804698993,-0.365192978547],
	'float')

# 0.0248119093417,0.066621042158,-0.0288546753753,0.019824594573,0.0725884122146,
# 						0.0130959472942,0.051863972607,-0.0345304308377,0.539705193266,0.100612117262,
# 						-0.0975769816671,-0.027412103237,-0.579654901967,-0.195285093474,0.0653865679789,
# 						0.0858613264226,0.606377604767,0.572717290238,0.690928314515,0.525284112662,
# 						-0.0681420614741,0.82261338757,0.570942465527,0.693469991001,0.623154477968,
						# 0.293365739048,-0.537166361795], 'float')
extraccion_salidas(array_coef)