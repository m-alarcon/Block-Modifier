import numpy as np
import math
import random as rnd
import csv



#RECORDAR CAMBIAR EL NUMERO DE ENTRADAS AQUI
num_entradas = 3
num_coeficientes = 6

array_coef = np.zeros(num_coeficientes, 'float')
umbral = 0.001

def calcula_t(array_coef, array_entradas):

	t = float(0)
	if (array_entradas.shape[0] == array_coef.shape[0]):
		for i in range(0, array_entradas.shape[0]):
			t = t + (array_coef[i]*array_entradas[i])

	elif (2*array_entradas.shape[0] == array_coef.shape[0]):
		for i in range(0, array_entradas.shape[0]):
			t = t + (array_coef[i]*array_entradas[i])
			t = t + (array_coef[i+array_entradas.shape[0]]*(array_entradas[i]**2))

	return t

def simulated_annealing(array_coef):

	umbral = 0.001
	error_actual = 10000000000
	rango = float(-10)
	inc = 0

	while (error_actual > umbral):
		error = 0
		varianza = 0
		rango = rango + inc
		if rango >= 10:
			inc = -inc
		elif rango <= -10:
			inc = 0.001

		victima = rnd.randint(0,array_coef.shape[0]-1)
		aux = array_coef[victima]
		array_coef[victima] = array_coef[victima] + (rnd.random()*rango)

		#Por cada linea del fichero de entradas y salidas
		array_entradas = np.zeros(num_entradas, 'float')
		salida = float(0)
		n_ej = 0
		reader = csv.reader(open('MultiplicacionPorUno.csv'))
		for index, row in enumerate(reader):
			for i in range(0, num_entradas):
				array_entradas[i] = row[i]
			for j in range(num_entradas, num_entradas+1):
				salida = row[j]

			t_calculado = calcula_t(array_coef, array_entradas)
			e = abs(float(salida) - float(t_calculado))
			error = error + e
			varianza = varianza + (150*float(salida)-150*float(t_calculado))**2
			n_ej = index

		e_medio = error/n_ej

		sumatorio = 0
		for i in range(0, len(lista_errores)):
			sumatorio = sumatorio + ((lista_errores[i]-error)**2)

		varianza = 1/(n_ej-1)*sumatorio

		if e_medio*varianza < error_actual:
			error_actual = e_medio*varianza
			print (error_actual)
		else:
			array_coef[victima] = aux

		#En cada iteración guardar la matriz de coeficientes

	print (array_coef)



simulated_annealing(array_coef)


array_entradas = np.zeros(num_entradas, 'float')
coef_calculados =np.array([1, 1], 'float')
reader = csv.reader(open('MultiplicacionPorUno.csv'))
for index, row in enumerate(reader):
	for i in range(0, num_entradas):
		array_entradas[i] = row[i]
	print (calcula_t(coef_calculados, array_entradas))