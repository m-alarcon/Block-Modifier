import numpy as np
import math
import random as rnd
import csv

num_entradas = 27
num_coeficientes = 82

def calcula_t(array_coef, array_entradas):

	t = float(0)
	if (array_entradas.shape[0]+1 == array_coef.shape[0]):
		for i in range(0, array_entradas.shape[0]-1):
			t = t + (array_coef[i]*array_entradas[i])

	elif ((2*array_entradas.shape[0])+1 == array_coef.shape[0]):
		for i in range(0, array_entradas.shape[0]-1):
			t = t + (array_coef[i]*array_entradas[i])
			t = t + (array_coef[i+array_entradas.shape[0]]*(array_entradas[i]**2))

	elif ((3*array_entradas.shape[0])+1 == array_coef.shape[0]):
		for i in range(0, array_entradas.shape[0]-1):
			t = t + (array_coef[i]*array_entradas[i])
			t = t + (array_coef[i+array_entradas.shape[0]]*(array_entradas[i]**2))
			t = t + (array_coef[i+2*array_entradas.shape[0]]*(array_entradas[i]**3))

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



array_coef = np.array([-0.01360564908,0.571569239327,-0.115013110691,-6.31424124689,-0.483284367932,0.0944584570448,0.951094016055,0.566179830218,-0.962494948062,-0.168058151189,0.036841669159,2.00085797517,0.495945175563,-0.307227873364,-0.134891365577,1.85434420663,2.99211956242,6.70183142749,9.17483857473,-3.09570414774,12.3219703151,-14.6006233554,-2.73058076144,4.21062717719,3.16152873581,-1.99474751096,385.605980362,0.607078601467,-1.75531555557,2.34011342244,5.24803836653,-0.706282523019,-0.218298166703,-1.17767196418,0.693324603761,1.31055064108,0.735694089545,-0.716869012829,-0.0919161650846,0.47170495879,1.00410731851,-0.974486602961,-1.02901910961,-5.50204788339,-27.177867546,-63.4031209595,19.9319446737,-123.374416645,115.021882933,14.0782761414,-18.1067925762,-6.25556271321,36.8184267998,240.609738049,-0.510967974188,1.22562276643,-2.07845078644,-0.51376700699,0.994078551996,0.1186810953,0.390904736283,-0.948451489557,-0.588039125184,-0.604461893606,0.638166022259,-1.31142159669,-0.816451678708,-0.71433950993,1.06026533667,-0.357472846083,5.096957457,34.608294455,120.959344086,-24.8884940425,281.057142476,53.6452418467,-11.561078927,25.7789207933,6.71749750555,-80.4437288589,213.733866037,-0.934198968228],
	'float')

extraccion_salidas(array_coef)