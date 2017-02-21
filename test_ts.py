import numpy as np
import math
import random as rnd
import csv

num_entradas = 23
num_coeficientes = 24

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
	reader = csv.reader(open('entrenamientoSDcochesFiltradoSA.csv'))#entrenamientoFiltrado.csv'))
	for index, row in enumerate(reader):
		for i in range(1, num_entradas+1):
			array_entradas[i-1] = row[i]
		for j in range(num_entradas+1, num_entradas+2):
			salida = float(row[j])
			salida_calculada = calcula_t(array_coef, array_entradas)
			error_cometido = abs(float(salida)-salida_calculada)
			print ("Se esperaba: ", salida, "se ha obtenido: ", salida_calculada, "cometiendo un error de: ", error_cometido)
			if error_cometido > 0.01:
				n_fallos += 1
	print (n_fallos)



array_coef = np.array([0.0205247871985,0.105074815144,0.124383569984,-0.0394530770654,0.0679784649652,-0.02386587747,0.047260609387,-0.153847317235,-0.0584888889214,-0.0494507240843,-0.0571915631902,-0.0145929754464,-0.526052397961,-0.687915759255,-0.751003273424,0.0563007012971,-2.28208156058,1.81058138241,0.140009343107,-0.449020867525,-0.425461053351,0.0497125805752,326.498796078,0.498760068162],
	'float')

extraccion_salidas(array_coef)