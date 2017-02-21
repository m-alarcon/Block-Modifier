#TempladoSimuladoVersionNoMonotonaV1

import numpy as np
import math
import random as rnd
import csv


num_entradas = 23
num_coeficientes = 24
monotona = False

#Función costo. Va a ser el error entre la salida de mi busqueda de desplazamientos
#y el valor cometido

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

'''
def func_costo(array_coef):
	#Calcula el error absoluto y la varianza y da su multiplicacion a la salida
	#Esto va a ser lo que queremos minimizar con el algoritmo de templado simulado

	error = 0
	varianza = 0
	n_ej = 0
	array_entradas = np.zeros(num_entradas, 'float')
	lista_errores = []
	reader = csv.reader(open('entrenamientoFiltrado.csv'))
	for index, row in enumerate(reader):
		for i in range(1, num_entradas+1):
			array_entradas[i-1] = row[i]
		for j in range(num_entradas+1, num_entradas+2):
			salida = row[j]

		t_calculado = calcula_t(array_coef, array_entradas)
		e = abs(float(salida) - float(t_calculado))
		lista_errores.append(e)
		error = error + e
		n_ej = index+1

	e_medio = error/n_ej

	sumatorio = 0
	for i in range(0, len(lista_errores)):
		sumatorio = sumatorio + ((lista_errores[i]-error)**2)

	varianza = 1/(n_ej-1)*sumatorio

	return (e_medio*varianza)

def func_costo(array_coef):
	error = 0
	varianza = 0
	n_ej = 0
	array_entradas = np.zeros(num_entradas, 'float')
	reader = csv.reader(open('EntrenamientoRNAMismoPeso1.csv'))
	for index, row in enumerate(reader):
		for i in range(1, num_entradas+1):
			array_entradas[i-1] = row[i]
		for j in range(num_entradas+1, num_entradas+2):
			salida = row[j]

		t_calculado = calcula_t(array_coef, array_entradas)
		e = abs(float(salida) - float(t_calculado))
		error = error + e
		n_ej = index+1

	return error
'''
#Funcion de costo que intenta maximizar el número de aciertos
def func_costo(array_coef):
	error = 0
	varianza = 0
	n_ej = 0
	aciertos = 0
	array_entradas = np.zeros(num_entradas, 'float')
	reader = csv.reader(open('EntrenamientoRNAMismoPeso1.csv'))
	for index, row in enumerate(reader):
		for i in range(1, num_entradas+1):
			array_entradas[i-1] = row[i]
		for j in range(num_entradas+1, num_entradas+2):
			salida = row[j]

		t_calculado = calcula_t(array_coef, array_entradas)
		e = abs(float(salida) - float(t_calculado))
		if e < 0.01:
			aciertos += 1
		else:
			aciertos = aciertos
		error = error + e
		n_ej = index+1

	return (n_ej-aciertos)*error


def simulatedAnnealing():
	array_coef = np.zeros(num_coeficientes, 'float')
	array_coef_nuevo = np.zeros(num_coeficientes, 'float')
	for i in range(0, array_coef.shape[0]):
		array_coef[i] = rnd.random() #Estado inicial del sistema, puede ser aleatorio o un estado que se defina

	#array_coef = np.array([0.00111060438329,0.00384068699641,-0.000469502874433,0.000496208238149,0.000829797676848,-0.00238013364339,0.000309188641157,0.00273464610212,-0.535004171928,-0.350778150284,-0.438044810176,-0.434194690297,-0.441428398425,-0.431908578959,-0.381530034457,-0.37366872591,-0.425372407785,-0.476923621971,-1515.83221218,0.428789812739], 'float')

	T = 30 #Temperatura inicial del sistema para dar un grado de libertad de cambio
	K = 150 #Cantidad de iteraciones que estamos dispuestos a hacer en cada etapa
	A = 150 #Cantidad de aceptaciones que se permiten hacer en cada etapa
	FRZN = 0.001 #Parametro de congelamiento
	ro = 1.005 #Parámetro de aumento de K
	alpha = 0.9 #Factor de enfriamiento geometrico
	etha = 1.05 #Factor de recalentamiento
	k = 0
	a = 0
	while (A/K > FRZN): #Se puede poner de condición de congelamiento que el error de todas las pruebas sea menor que un numero
		while (k < K and a < A):
			victima = rnd.randint(0,array_coef.shape[0]-1)
			array_coef_nuevo = array_coef.copy() #generar j en N(i) (Solucion distinta de i)
			array_coef_nuevo[victima] = array_coef_nuevo[victima] + (rnd.uniform(-1,1)*T)

			if (float(func_costo(array_coef_nuevo)) - float(func_costo(array_coef)) < 0):
				array_coef = array_coef_nuevo.copy()
				a = a + 1
			else:
				r = rnd.random()
				if (r < float(math.exp((func_costo(array_coef) - func_costo(array_coef_nuevo))/T))):
					array_coef = array_coef_nuevo.copy()
					a = a + 1
			k = k + 1
			
		if (monotona == False):
			if (a == A):
				T = alpha * T
			elif (k == K):
				T = etha * T
		else:
			T = alpha * T

		K = ro * K
		k = 0
		a = 0
		print (array_coef, func_costo(array_coef))
		if (monotona == False):	
			with open("resultadoNoMonotona.csv", 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
				writer.writerow(array_coef)
		if (monotona == True):	
			with open("resultadoMonotona.csv", 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
				writer.writerow(array_coef)


simulatedAnnealing()