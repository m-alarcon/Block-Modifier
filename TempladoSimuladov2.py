#TempladoSimuladoVersionNoMonotonaV1

import numpy as np
import math
import random as rnd
import csv


num_entradas = 27
num_coeficientes = 82
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
'''
def func_costo(array_coef):
	error = 0
	varianza = 0
	n_ej = 0
	array_entradas = np.zeros(num_entradas, 'float')
	reader = csv.reader(open('entrenamientoFiltrado.csv'))
	for index, row in enumerate(reader):
		for i in range(1, num_entradas+1):
			array_entradas[i-1] = row[i]
		for j in range(num_entradas+1, num_entradas+2):
			salida = row[j]

		t_calculado = calcula_t(array_coef, array_entradas)
		e = abs(float(salida) - float(t_calculado))
		error = error + e

	return error

def simulatedAnnealing():
	array_coef = np.zeros(num_coeficientes, 'float')
	array_coef_nuevo = np.zeros(num_coeficientes, 'float')
	# for i in range(0, array_coef.shape[0]):
	# 	array_coef[i] = rnd.random() #Estado inicial del sistema, puede ser aleatorio o un estado que se defina

	array_coef = np.array([-0.01360564908,0.571569239327,-0.115013110691,-6.31424124689,-0.483284367932,0.0944584570448,0.951094016055,0.566179830218,-0.962494948062,-0.168058151189,0.036841669159,2.00085797517,0.495945175563,-0.307227873364,-0.134891365577,1.85434420663,2.99211956242,6.70183142749,9.17483857473,-3.09570414774,12.3219703151,-14.6006233554,-2.73058076144,4.21062717719,3.16152873581,-1.99474751096,385.605980362,0.607078601467,-1.75531555557,2.34011342244,5.24803836653,-0.706282523019,-0.218298166703,-1.17767196418,0.693324603761,1.31055064108,0.735694089545,-0.716869012829,-0.0919161650846,0.47170495879,1.00410731851,-0.974486602961,-1.02901910961,-5.50204788339,-27.177867546,-63.4031209595,19.9319446737,-123.374416645,115.021882933,14.0782761414,-18.1067925762,-6.25556271321,36.8184267998,240.609738049,-0.510967974188,1.22562276643,-2.07845078644,-0.51376700699,0.994078551996,0.1186810953,0.390904736283,-0.948451489557,-0.588039125184,-0.604461893606,0.638166022259,-1.31142159669,-0.816451678708,-0.71433950993,1.06026533667,-0.357472846083,5.096957457,34.608294455,120.959344086,-24.8884940425,281.057142476,53.6452418467,-11.561078927,25.7789207933,6.71749750555,-80.4437288589,213.733866037,-0.934198968228], 'float')

	T = 30 #Temperatura inicial del sistema para dar un grado de libertad de cambio
	K = 150 #Cantidad de iteraciones que estamos dispuestos a hacer en cada etapa
	A = 150 #Cantidad de aceptaciones que se permiten hacer en cada etapa
	FRZN = 0.001 #Parametro de congelamiento
	ro = 1.05 #Parámetro de aumento de K
	alpha = 0.8 #Factor de enfriamiento geometrico
	etha = 1.25 #Factor de recalentamiento
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