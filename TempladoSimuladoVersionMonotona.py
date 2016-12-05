#TempladoSimuladoVersionMonotonaV1
import numpy as np
import math
import random as rnd
import csv


num_entradas = 27
num_coeficientes = 27

#Función costo. Va a ser el error entre la salida de mi busqueda de desplazamientos
#y el valor cometido

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

def simulatedAnnealing():

	array_coef = np.zeros(num_coeficientes, 'float')
	array_coef_nuevo = np.zeros(num_coeficientes, 'float')
	for i in range(0, array_coef.shape[0]):
		array_coef[i] = rnd.random() #Estado inicial del sistema, puede ser aleatorio o un estado que se defina
	T = 10 #Temperatura inicial del sistema para dar un grado de libertad de cambio
	K = 150 #Cantidad de iteraciones que estamos dispuestos a hacer en cada etapa
	A = 150 #Cantidad de aceptaciones que se permiten hacer en cada etapa
	FRZN = 0.01 #Parametro de congelamiento
	ro = 1.05 #Parámetro de aumento de K
	alpha = 0.99 #Factor de enfriamiento geometrico
	k = 0
	a = 0

	while (A/K > FRZN):
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
		T = alpha * T
		K = ro * K
		k = 0
		a = 0
		print (array_coef, func_costo(array_coef))
	with open("resultado.csv", 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(array_coef)


simulatedAnnealing()