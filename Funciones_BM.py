from PIL import Image, ImageDraw
import numpy as np
import math
import Funciones_div_im as div
import csv
import json

DEPURAR = 0

#Funcion que hace zoom a un bloque
def zoom_positivo(ampliacion, array_imagen):

	array_ampliacion = np.zeros((array_imagen.shape[0]*ampliacion, array_imagen.shape[1]*ampliacion), "uint8")
	array_resultado = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")

	for x in range(0, array_imagen.shape[0]):
		for y in range(0, array_imagen.shape[1]):
			for i in range(0, ampliacion):
				for j in range(0, ampliacion):
					array_ampliacion[x*ampliacion+i][y*ampliacion+j] = array_imagen[x][y]

	sobrante_x = int((array_ampliacion.shape[0]-array_imagen.shape[0])/2)
	sobrante_y = int((array_ampliacion.shape[1]-array_imagen.shape[1])/2)

	for x in range(0, array_imagen.shape[0]):
		for y in range(0, array_imagen.shape[1]):
			array_resultado[x][y] = array_ampliacion[x+sobrante_x][y+sobrante_y]

	return array_resultado

def zoom_negativo(ampliacion, array_imagen):

	i = 0
	x = 0
	j = 0
	y = 0
	array_ampliacion = np.zeros((math.ceil(array_imagen.shape[0]/ampliacion), math.ceil(array_imagen.shape[1]/ampliacion)), "uint8")
	array_resultado = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")

	while i < array_imagen.shape[0]:
		while j < array_imagen.shape[1]:
			array_ampliacion[x][y] = array_imagen[i][j]
			j += ampliacion
			y += 1
		i += ampliacion
		x += 1
		j = 0
		y = 0

	#Rellenar los bordes con el mismo valor que los bordes de la imagen
	sobrante_x = int((array_imagen.shape[0]-array_ampliacion.shape[0])/2)
	sobrante_y = int((array_imagen.shape[1]-array_ampliacion.shape[1])/2)

	#Rellenar el array resultado con el array tras la disminucion
	for x in range(0, array_ampliacion.shape[0]):
		for y in range(0, array_ampliacion.shape[1]):
			array_resultado[x+sobrante_x][y+sobrante_y] = array_ampliacion[x][y]

	#Rellenar los bordes laterales
	for x in range(0, sobrante_x):
		for y in range(sobrante_y, sobrante_y+array_ampliacion.shape[1]):
			array_resultado[x][y] = array_ampliacion[0][y-sobrante_y]
			array_resultado[x+sobrante_x+array_ampliacion.shape[0]][y] = array_ampliacion[array_ampliacion.shape[0]-1][y-sobrante_y]

	#Rellenar el borde superior e inferior
	for x in range(0, array_imagen.shape[0]):
		for y in range(0, sobrante_y):
			array_resultado[x][y] = array_resultado[x][sobrante_y]
			array_resultado[x][y+sobrante_y+array_ampliacion.shape[1]] = array_resultado[x][sobrante_y+array_ampliacion.shape[1]-1]

	return array_resultado

#Función que devuelve el array de pixeles desplazados hacia la derecha px pixeles
#La zona izquierda se rellena de la primera columna de la imagen original
def despl_derecha(px, array_imagen):

	array_resultado = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")

	for x in range(0, array_imagen.shape[1]-px):
		for y in range(0, array_imagen.shape[0]):
			array_resultado[y][x+px] = array_imagen[y][x]

	for x in range(0, px):
	 	for y in range(0, array_imagen.shape[0]):
	 		array_resultado[y][x] = array_imagen[y][0]

	return array_resultado

def despl_izquierda(px, array_imagen):

	array_resultado = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")

	for x in range(px, array_imagen.shape[1]):
		for y in range(0, array_imagen.shape[0]):
			array_resultado[y][x-px] = array_imagen[y][x]

	for x in range(array_imagen.shape[1]-px, array_imagen.shape[1]):
	 	for y in range(0, array_imagen.shape[0]):
	 		array_resultado[y][x] = array_imagen[y][array_imagen.shape[1]-1]

	return array_resultado

def despl_arriba(px, array_imagen):

	array_resultado = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")

	for x in range(0, array_imagen.shape[1]):
		for y in range(px, array_imagen.shape[0]):
			array_resultado[y-px][x] = array_imagen[y][x]

	for x in range(0, array_imagen.shape[1]):
	 	for y in range(array_imagen.shape[0]-px, array_imagen.shape[0]):
	 		array_resultado[y][x] = array_imagen[array_imagen.shape[0]-1][x]

	return array_resultado

def despl_abajo(px, array_imagen):

	array_resultado = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")

	for x in range(0, array_imagen.shape[1]):
		for y in range(0, array_imagen.shape[0]-px):
			array_resultado[y+px][x] = array_imagen[y][x]

	for x in range(0, array_imagen.shape[1]):
	 	for y in range(0, px):
	 		array_resultado[y][x] = array_imagen[0][x]

	return array_resultado

def brillo_positivo(porcentaje, array_imagen):

	array_aux = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")
	for x in range(0, array_imagen.shape[0]):
		for y in range(0, array_imagen.shape[1]):
			array_aux[x][y] = array_imagen[x][y]

	aumento = math.floor((porcentaje*255)/100)
	for x in range(0, array_imagen.shape[0]):
		for y in range(0, array_imagen.shape[1]):
			if array_aux[x][y] + aumento > 255:
				array_aux[x][y] = 255
			else:
				array_aux[x][y] += aumento

	return array_aux

def brillo_negativo(porcentaje, array_imagen):

	array_aux = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")
	for x in range(0, array_imagen.shape[0]):
		for y in range(0, array_imagen.shape[1]):
			array_aux[x][y] = array_imagen[x][y]

	disminucion = math.floor((porcentaje*255)/100)
	for x in range(0, array_imagen.shape[0]):
		for y in range(0, array_imagen.shape[1]):
			if (disminucion <= array_aux[x][y]):
				array_aux[x][y] -= disminucion
			else:
				array_aux[x][y] = 0

	return array_aux

def desplazamiento_v2(tx_px, ty_px, array_imagen):

	array_resultado = np.zeros((array_imagen.shape[0], array_imagen.shape[1]), "uint8")
	array_traslacion = np.array([[1, 0, tx_px], [0, 1, ty_px], [0, 0, 1]])
	#array_traslacion_inv = np.inv(array_traslacion)

	if tx_px >= 0 and ty_px >= 0: #Desplazamiento diagonal abajo derecha

		#Trozo de la imagen inicial que se va a pintar
		for x in range(0, array_imagen.shape[1]-tx_px):
			for y in range(0, array_imagen.shape[0]-ty_px):
				pixel_final = np.zeros((1, 1, 1), 'uint32')
				pixel_inicial = np.array([x, y, 1])
				pixel_final = np.inner(pixel_inicial, array_traslacion)
				array_resultado[pixel_final[1]][pixel_final[0]] = array_imagen[y][x]

		#Copiar la primera columna en el hueco de la izquierda
		for x in range(0, tx_px):
		 	for y in range(ty_px, array_imagen.shape[0]):
		 		array_resultado[y][x] = array_imagen[y][0]

		#Copiar la primera fila en el hueco que queda arriba
		for x in range(0, array_imagen.shape[1]):
		 	for y in range(0, ty_px):
		 		array_resultado[y][x] = array_resultado[ty_px][x]

	elif tx_px < 0 and ty_px >= 0: #Desplazamiento diagonal abajo izquierda

		#Trozo de la imagen inicial que se va a pintar
		for x in range(abs(tx_px), array_imagen.shape[1]):
			for y in range(0, array_imagen.shape[0]-ty_px):
				pixel_final = np.zeros((1, 1, 1), 'uint32')
				pixel_inicial = np.array([x, y, 1])
				pixel_final = np.inner(pixel_inicial, array_traslacion)
				array_resultado[pixel_final[1]][pixel_final[0]] = array_imagen[y][x]

		#Copiar la ultima columna en el hueco de la derecha
		for x in range(array_imagen.shape[1] + tx_px, array_imagen.shape[1]):
		 	for y in range(ty_px, array_imagen.shape[0]):
		 		array_resultado[y][x] = array_imagen[y-ty_px][array_imagen.shape[1]-1]

		#Copiar la primera fila en el hueco que queda arriba
		for x in range(0, array_imagen.shape[1]):
		 	for y in range(0, ty_px):
		 		array_resultado[y][x] = array_resultado[ty_px][x]	

	elif tx_px < 0 and ty_px < 0: #Desplazamiento diagonal arriba izquierda

		#Trozo de la imagen inicial que se va a pintar
		for x in range(abs(tx_px), array_imagen.shape[1]):
			for y in range(abs(ty_px), array_imagen.shape[0]):
				pixel_final = np.zeros((1, 1, 1), 'uint32')
				pixel_inicial = np.array([x, y, 1])
				pixel_final = np.inner(pixel_inicial, array_traslacion)
				array_resultado[pixel_final[1]][pixel_final[0]] = array_imagen[y][x]

		#Copiar la ultima columna en el hueco de la derecha
		for x in range(array_imagen.shape[1]+tx_px, array_imagen.shape[1]):
			for y in range(0, array_imagen.shape[0]+ty_px):
				array_resultado[y][x] = array_imagen[y-ty_px][array_imagen.shape[1]-1]

		#Copiar la ultima fila en el hueco que queda abajo
		for x in range(0, array_imagen.shape[1]):
			for y in range(array_imagen.shape[0]+ty_px, array_imagen.shape[0]):
				array_resultado[y][x] = array_resultado[array_imagen.shape[0]+ty_px-1][x]	

	elif tx_px >= 0 and ty_px < 0: #Desplazamiento diagonal arriba derecha

		#Trozo de la imagen inicial que se va a pintar
		for x in range(0, array_imagen.shape[1]-tx_px):
			for y in range(abs(ty_px), array_imagen.shape[0]):
				pixel_final = np.zeros((1, 1, 1), 'uint32')
				pixel_inicial = np.array([x, y, 1])
				pixel_final = np.inner(pixel_inicial, array_traslacion)
				array_resultado[pixel_final[1]][pixel_final[0]] = array_imagen[y][x]

		#Copiar la primera columna en el hueco de la izquierda
		for x in range(0, tx_px):
		 	for y in range(0, array_imagen.shape[0]+ty_px):
		 		array_resultado[y][x] = array_imagen[y][0]

		#Copiar la ultima fila en el hueco que queda abajo
		for x in range(0, array_imagen.shape[1]):
			for y in range(array_imagen.shape[0]+ty_px, array_imagen.shape[0]):
				array_resultado[y][x] = array_resultado[array_imagen.shape[0]+ty_px-1][x]

	return array_resultado


#def rotacion():



#Esta función nos devuelve un valor de parecido entre las dos imagenes que se le pasan.
#Hay que pasarle el array de bytes de las imagenes a comprobar que deben ser del mismo tamaño.
def comparacion_imagenes(array_imagen_original, array_imagen_transformada):

	diferencia = float(0)
	diferencia_total = float(0)
	porcentaje_diferente = float(0)
	if array_imagen_original.shape[0] == array_imagen_transformada.shape[0] and array_imagen_original.shape[1] == array_imagen_transformada.shape[1]:
		for x in range(0, array_imagen_original.shape[0]):
			for y in range(0, array_imagen_original.shape[1]):
				diferencia = abs(float(array_imagen_original[x][y]) - float(array_imagen_transformada[x][y]))
				diferencia_total += diferencia
		porcentaje_diferente = (diferencia_total*100)/(255*array_imagen_original.shape[0]*array_imagen_original.shape[1])
	else:
		print("El tamaño de las imagenes no coincide")

	return porcentaje_diferente



def experimento_brillo_negativo(a1, a2, bloq):

	#BRILLO NEGATIVO con saltos de 1
	minimo = 100
	valor = 0
	for i in range(0,100):
		array_resultado = brillo_negativo(i, a1)
		diferencia = comparacion_imagenes(array_resultado, a2)
		if diferencia < minimo:
			minimo = diferencia
			valor = i

	if DEPURAR:
		print ("Bloque", bloq, "cambio: brillo negativo")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", valor)

	resultado_final = brillo_negativo(valor, a1)

	return resultado_final, minimo, valor


def experimento_brillo_positivo(a1, a2, bloq):

	#BRILLO POSITIVO con saltos de 1
	minimo = 100
	valor = 0
	for i in range(0,100):
		array_resultado = brillo_positivo(i, a1)
		diferencia = comparacion_imagenes(array_resultado, a2)
		if diferencia < minimo:
			minimo = diferencia
			valor = i

	if DEPURAR:
		print ("Bloque", bloq, "cambio: brillo positivo")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", valor)

	resultado_final = brillo_positivo(valor, a1)

	return resultado_final, minimo, valor

def experimento_despl_derecha(a1, a2, bloq, ancho_bloq):
	
	#DESPLAZAMIENTO DERECHA con saltos de 1 px
	minimo = 100
	valor = 0
	for i in range(0, math.floor(ancho_bloq/2)):#No voy a tener en cuenta movimientos mayores que la mitad del bloque (como los vectores que hice)
		array_resultado = despl_derecha(i, a1)
		diferencia = comparacion_imagenes(array_resultado, a2)
		if diferencia < minimo:
			minimo = diferencia
			valor = i

	if DEPURAR:
		print ("Bloque", bloq, "cambio: desplazamiento derecha")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", valor)

	resultado_final = despl_derecha(valor, a1)

	return resultado_final, minimo, valor

def experimento_despl_izquierda(a1, a2, bloq, ancho_bloq):

	#DESPLAZAMIENTO IZQUIERDA con saltos de 1 px
	minimo = 100
	valor = 0
	for i in range(0, math.floor(ancho_bloq/2)):#No voy a tener en cuenta movimientos mayores que la mitad del bloque (como los vectores que hice)
		array_resultado = despl_izquierda(i, a1)
		diferencia = comparacion_imagenes(array_resultado, a2)
		if diferencia < minimo:
			minimo = diferencia
			valor = i

	if DEPURAR:
		print ("Bloque", bloq, "cambio: desplazamiento izquierda")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", valor)

	resultado_final = despl_izquierda(valor, a1)

	return resultado_final, minimo, valor

def experimento_despl_arriba(a1, a2, bloq, ancho_bloq):

	#DESPLAZAMIENTO ARRIBA con saltos de 1 px
	minimo = 100
	valor = 0
	for i in range(0, math.floor(ancho_bloq/2)):#No voy a tener en cuenta movimientos mayores que la mitad del bloque (como los vectores que hice)
		array_resultado = despl_arriba(i, a1)
		diferencia = comparacion_imagenes(array_resultado, a2)
		if diferencia < minimo:
			minimo = diferencia
			valor = i

	if DEPURAR:
		print ("Bloque", bloq, "cambio: desplazamiento arriba")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", valor)

	resultado_final = despl_arriba(valor, a1)

	return resultado_final, minimo, valor

def experimento_despl_abajo(a1, a2, bloq, ancho_bloq):

	#DESPLAZAMIENTO ABAJO con saltos de 1 px
	minimo = 100
	valor = 0
	for i in range(0, math.floor(ancho_bloq/2)):#No voy a tener en cuenta movimientos mayores que la mitad del bloque (como los vectores que hice)
		array_resultado = despl_abajo(i, a1)
		diferencia = comparacion_imagenes(array_resultado, a2)
		if diferencia < minimo:
			minimo = diferencia
			valor = i

	if DEPURAR:
		print ("Bloque", bloq, "cambio: desplazamiento abajo")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", valor)

	resultado_final = despl_abajo(valor, a1)

	return resultado_final, minimo, valor

def experimento_zoom_positivo(a1, a2, bloq):

	#ZOOM POSITIVO con saltos de 1x (hasta 3x?)
	minimo = 100
	valor = 0
	for i in range(1, 3):
		array_resultado = zoom_positivo(i, a1)
		diferencia = comparacion_imagenes(array_resultado, a2)
		if diferencia < minimo:
			minimo = diferencia
			valor = i

	if DEPURAR:
		print ("Bloque", bloq, "cambio: zoom positivo")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", valor)

	resultado_final = zoom_positivo(valor, a1)

	return resultado_final, minimo, valor

def experimento_zoom_negativo(a1, a2, bloq):

	#ZOOM NEGATIVO con saltos de 1x (hasta 3x?)
	minimo = 100
	valor = 0
	for i in range(1, 3):
		array_resultado = zoom_negativo(i, a1)
		diferencia = comparacion_imagenes(array_resultado, a2)
		if diferencia < minimo:
			minimo = diferencia
			valor = i

	if DEPURAR:
		print ("Bloque", bloq, "cambio: zoom negativo")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", valor)

	resultado_final = zoom_negativo(valor, a1)

	return resultado_final, minimo, valor

def experimento_despl_v2(a1, a2, bloq, ancho_bloq):

	#DESPLAZAMIENTO EN TODOS LOS SENTIDOS con saltos de 1 px desde -ancho_bloq/2
	minimo = 100
	valor_x = 0
	valor_y = 0
	for i in range(-math.floor(ancho_bloq/2), math.floor(ancho_bloq/2)):#No voy a tener en cuenta movimientos mayores que la mitad del bloque (como los vectores que hice)
		for j in range(-math.floor(ancho_bloq/2), math.floor(ancho_bloq/2)):
			array_resultado = desplazamiento_v2(i, j, a1)
			diferencia = comparacion_imagenes(array_resultado, a2)
			if diferencia < minimo:
				minimo = diferencia
				valor_x = i
				valor_y = j

	if DEPURAR:
		print ("Bloque", bloq, "cambio: desplazamiento")
		print ("La minima diferencia es de: ", "%.2f" % (minimo, ), "con un valor de entrada de: ", "%.1f" % (valor_x/ancho_bloq, ), "en el eje X y ", "%.1f" % (valor_y/ancho_bloq, ), "en el eje Y")

	resultado_final = desplazamiento_v2(valor_x, valor_y, a1)

	return resultado_final, minimo, valor_x/ancho_bloq, valor_y/ancho_bloq

#Extraccion de los deltas
#deltas anteriores divididos entre el numero de pixeles por bloque
#El numero de fotograma tiene que empezar por el 2
def deltas(num_fotograma, bloque):

	im = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD"+str(num_fotograma)+".bmp")
	im = im.convert('L')
	im2 = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD"+str(num_fotograma-1)+".bmp")
	im2 = im2.convert('L')

	#Calculo el numero de bloques que tienen las imagenes
	(ancho, largo) = im.size
	ancho_bloq = int(ancho/32)
	num_filas = int(largo/ancho_bloq)
	num_bloques = 32*num_filas
	pixeles = ancho_bloq*ancho_bloq

	bloque_im = div.sel_bloque(bloque,im)
	bloque_im2 = div.sel_bloque(bloque,im2)
	a1 = np.array(bloque_im, 'int16')
	a2 = np.array(bloque_im2, 'int16')

	#El delta va a ser la resta de los valores de los píxeles en el bloque. Un delta por píxel.
	deltas = np.zeros((im.size[0], im.size[1]), 'int16')
	deltas = np.subtract(a2,a1)

	delta0 = 0
	delta1 = 0
	delta2 = 0
	delta3 = 0
	delta4 = 0
	delta5 = 0
	delta_1 = 0
	delta_2 = 0
	delta_3 = 0
	delta_4 = 0
	delta_5 = 0

	for x in range(0, ancho_bloq):
		for y in range(0, ancho_bloq):

			if deltas[x][y] == 0:
				delta0 = delta0+1
			elif deltas[x][y] > 0 and deltas[x][y] <= 3:
				delta1 = delta1+1
			elif deltas[x][y] < 0 and deltas[x][y] >= -3:
				delta_1 = delta_1+1
			elif deltas[x][y] > 3 and deltas[x][y] <= 9:
				delta2 = delta2+1
			elif deltas[x][y] < -3 and deltas[x][y] >= -9:
				delta_2 = delta_2+1
			elif deltas[x][y] > 9 and deltas[x][y] <= 75:
				delta3 = delta3+1
			elif deltas[x][y] < -9 and deltas[x][y] >= -75:
				delta_3 = delta_3+1
			elif deltas[x][y] > 75 and deltas[x][y] <= 150:
				delta4 = delta4+1
			elif deltas[x][y] < -75 and deltas[x][y] >= -150:
				delta_4 = delta_4+1
			elif deltas[x][y] > 150 and deltas[x][y] <= 255:
				delta5 = delta5+1
			elif deltas[x][y] < -150 and deltas[x][y] >= -255:
				delta_5 = delta_5+1

	delta0 = float(delta0/pixeles)
	delta1 = float(delta1/pixeles)
	delta2 = float(delta2/pixeles)
	delta3 = float(delta3/pixeles)
	delta4 = float(delta4/pixeles)
	delta5 = float(delta5/pixeles)
	delta_1 = float(delta_1/pixeles)
	delta_2 = float(delta_2/pixeles)
	delta_3 = float(delta_3/pixeles)
	delta_4 = float(delta_4/pixeles)
	delta_5 = float(delta_5/pixeles)

	return (delta0, delta1, delta2, delta3, delta4, delta5, delta_1, delta_2, delta_3, delta_4, delta_5)

#Extraccion de las metricas
def metricas(fotograma, bloque):

	with open("D:/Manuel/Downloads/Beca/Block modifier/MetricasSD/metricasframeSD"+str(fotograma)+".txt") as archivo_json:
		metricas = json.load(archivo_json)

	filas = int(len(metricas)/33)
	m_metricas = np.zeros((33,filas,2), 'float')

	for i in range(0, int(filas)):
		for j in range(0, 33):
			m_metricas[j][i][0] = metricas[33*i+j]["prx"]
			m_metricas[j][i][1] = metricas[33*i+j]["pry"]

	n_fila = math.ceil(bloque/32)
	n_col = (bloque - ((n_fila-1)*32))

	prx1 = m_metricas[n_col-1][n_fila-1][0]
	prx2 = m_metricas[n_col-1][n_fila][0]
	prx3 = m_metricas[n_col][n_fila-1][0]
	prx4 = m_metricas[n_col][n_fila][0]
	pry1 = m_metricas[n_col-1][n_fila-1][1]
	pry2 = m_metricas[n_col-1][n_fila][1]
	pry3 = m_metricas[n_col][n_fila-1][1]
	pry4 = m_metricas[n_col][n_fila][1]

	return (prx1, prx2, prx3, prx4, pry1, pry2, pry3, pry4)

# #Caracterizacion del delta
# #Se va a caracterizar tanto la dispersión como los valores del delta de los bloques de dos fotogramas consecutivos
# #para agruparlos.
# for i in range (1, 328):

# 	im = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD_sillon/frameSD"+str(i)+".bmp")
# 	im = im.convert('L')
# 	im2 = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD_sillon/frameSD"+str(i+1)+".bmp")
# 	im2 = im2.convert('L')

# 	with open("./Deltas_sillon/deltas"+str(i)+".csv", 'w', newline='') as csvfile:

# 		#Calculo el numero de bloques que tienen las imagenes
# 		(ancho, largo) = im.size
# 		ancho_bloq = int(ancho/32)
# 		num_filas = int(largo/ancho_bloq)
# 		num_bloques = 32*num_filas

# 		for bloq in range(1, num_bloques):

# 			bloque_im = div.sel_bloque(bloq,im)
# 			bloque_im2 = div.sel_bloque(bloq,im2)
# 			a1 = np.array(bloque_im, 'int16')
# 			a2 = np.array(bloque_im2, 'int16')

# 			#El delta va a ser la resta de los valores de los píxeles en el bloque. Un delta por píxel.
# 			deltas = np.zeros((im.size[0], im.size[1]), 'int16')
# 			deltas = np.subtract(a2,a1)

# 			writer = csv.writer(csvfile, delimiter=',',
# 			                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
# 			writer.writerow(["Bloque", bloq, "Deltas", deltas[0][0], deltas[0][1], deltas[0][2], deltas[0][3], deltas[0][4], deltas[0][5], deltas[0][6], deltas[0][7], deltas[0][8], deltas[0][9], deltas[0][10],
# 													   deltas[1][0], deltas[1][1], deltas[1][2], deltas[1][3], deltas[1][4], deltas[1][5], deltas[1][6], deltas[1][7], deltas[1][8], deltas[1][9], deltas[1][10],
# 													   deltas[2][0], deltas[2][1], deltas[2][2], deltas[2][3], deltas[2][4], deltas[2][5], deltas[2][6], deltas[2][7], deltas[2][8], deltas[2][9], deltas[2][10],
# 													   deltas[3][0], deltas[3][1], deltas[3][2], deltas[3][3], deltas[3][4], deltas[3][5], deltas[3][6], deltas[3][7], deltas[3][8], deltas[3][9], deltas[3][10],
# 													   deltas[4][0], deltas[4][1], deltas[4][2], deltas[4][3], deltas[4][4], deltas[4][5], deltas[4][6], deltas[4][7], deltas[4][8], deltas[4][9], deltas[4][10],
# 													   deltas[5][0], deltas[5][1], deltas[5][2], deltas[5][3], deltas[5][4], deltas[5][5], deltas[5][6], deltas[5][7], deltas[5][8], deltas[5][9], deltas[5][10],
# 													   deltas[6][0], deltas[6][1], deltas[6][2], deltas[6][3], deltas[6][4], deltas[6][5], deltas[6][6], deltas[6][7], deltas[6][8], deltas[6][9], deltas[6][10],
# 													   deltas[7][0], deltas[7][1], deltas[7][2], deltas[7][3], deltas[7][4], deltas[7][5], deltas[7][6], deltas[7][7], deltas[7][8], deltas[7][9], deltas[7][10],
# 													   deltas[8][0], deltas[8][1], deltas[8][2], deltas[8][3], deltas[8][4], deltas[8][5], deltas[8][6], deltas[8][7], deltas[8][8], deltas[8][9], deltas[8][10],
# 													   deltas[9][0], deltas[9][1], deltas[9][2], deltas[9][3], deltas[9][4], deltas[9][5], deltas[9][6], deltas[9][7], deltas[9][8], deltas[9][9], deltas[9][10],
# 													   deltas[10][0], deltas[10][1], deltas[10][2], deltas[10][3], deltas[10][4], deltas[10][5], deltas[10][6], deltas[10][7], deltas[10][8], deltas[10][9], deltas[10][10],])




#Se cargan las imagenes que se van a comparar por bloques.
# im = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD1.bmp")
# im = im.convert('L')
# im2 = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD2.bmp")
# im2 = im2.convert('L')


# with open('salidas.csv', 'w', newline='') as csvfile:

# 	#Calculo el numero de bloques que tienen las imagenes
# 	(ancho, largo) = im.size
# 	ancho_bloq = int(ancho/32)
# 	num_filas = int(largo/ancho_bloq)
# 	num_bloques = 32*num_filas

# 	#Se coge el mismo bloque de las dos imagenes
# 	for bloq in range(1, num_bloques):

# 		bloque_im = div.sel_bloque(bloq,im)
# 		bloque_im2 = div.sel_bloque(bloq,im2)
# 		a1 = np.array(bloque_im, 'int16')
# 		a2 = np.array(bloque_im2, 'int16')

# 	# 	experimento_brillo_negativo(a1, a2, bloq, csvfile)
# 	# 	# experimento_brillo_positivo(a1, a2, bloq)
# 	# 	# experimento_despl_derecha(a1, a2, bloq, ancho_bloq)
# 	# 	# experimento_despl_izquierda(a1, a2, bloq, ancho_bloq)
# 	# 	# experimento_despl_arriba(a1, a2, bloq, ancho_bloq)
# 	# 	# experimento_despl_abajo(a1, a2, bloq, ancho_bloq)
# 	# 	# experimento_zoom_positivo(a1, a2, bloq)
# 	# 	# experimento_zoom_negativo(a1, a2, bloq)
# 		(resultado, minimo, valorx, valory) = experimento_despl_v2(a1, a2, bloq, ancho_bloq)

# 		writer = csv.writer(csvfile, delimiter=',',
# 		                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
# 		writer.writerow(["Bloque", bloq, "Desplazamiento x - y", valorx, valory])

# 	#Aqui solo voy a hacer un bloque para ver los cambios que se producen realizando varios experimentos uno tras otro
# 	bloque_im = div.sel_bloque(518,im)
# 	bloque_im2 = div.sel_bloque(518,im2)
# 	a1 = np.array(bloque_im)
# 	a2 = np.array(bloque_im2)
# 	# resultado = experimento_brillo_negativo(a1, a2, 516, csvfile)
# 	# experimento_brillo_positivo(a1, a2, bloq)
	
# 	# experimento_despl_derecha(resultado, a2, 516, ancho_bloq)
# 	# resultado2 = experimento_despl_izquierda(resultado, a2, 516, ancho_bloq)
# 	# experimento_despl_arriba(a1, a2, bloq, ancho_bloq)
# 	# experimento_despl_abajo(a1, a2, bloq, ancho_bloq)
# 	# experimento_zoom_positivo(resultado2, a2, 516)
# 	# experimento_zoom_negativo(resultado2, a2, 516)

# 	dif = comparacion_imagenes(a1,a2)
# 	print ("La diferencia inicial es de: " + "%.2f" % (dif, ))

# 	# resultado = experimento_despl_izquierda(a1, a2, 516, ancho_bloq)
# 	# resultado2 = experimento_brillo_positivo(resultado, a2, 516)#, csvfile)
# 	# experimento_zoom_negativo(resultado2, a2, 516)

# 	#Aqui cojo el minimo de un bloque de todas las transformaciones

# 	array_minimos = np.zeros(8, "float")
# 	(resultado, array_minimos[0], valor) = experimento_brillo_positivo(a1, a2, 518)
# 	(resultado1, array_minimos[1], valor1) = experimento_brillo_negativo(a1, a2, 518, csvfile)
# 	(resultado2, array_minimos[2], valor2) = experimento_despl_derecha(a1, a2, 518, ancho_bloq)
# 	(resultado3, array_minimos[3], valor3) = experimento_despl_izquierda(a1, a2, 518, ancho_bloq)
# 	(resultado4, array_minimos[4], valor4) = experimento_despl_arriba(a1, a2, 518, ancho_bloq)
# 	(resultado5, array_minimos[5], valor5) = experimento_despl_abajo(a1, a2, 518, ancho_bloq)
# 	(resultado6, array_minimos[6], valor6) = experimento_zoom_negativo(a1, a2, 518)
# 	(resultado7, array_minimos[7], valor7) = experimento_zoom_positivo(a1, a2, 518)

# 	valor_minimo = float(150)
# 	funcion_minimo = 10
# 	for i in range (0, 7):
# 		if array_minimos[i] < valor_minimo:
# 			valor_minimo = array_minimos[i]
# 			funcion_minimo = i

# 	funcion = "ninguna"
# 	if funcion_minimo == 0:
# 		funcion = "Brillo positivo"
# 	elif funcion_minimo == 1:
# 		funcion = "Brillo negativo"
# 	elif funcion_minimo == 2:
# 		funcion = "Desplazamiento derecha"
# 	elif funcion_minimo == 3:
# 		funcion = "Desplazamiento izquierda"
# 	elif funcion_minimo == 4:
# 		funcion = "Desplazamiento arriba"
# 	elif funcion_minimo == 5:
# 		funcion = "Desplazamiento abajo"
# 	elif funcion_minimo == 6:
# 		funcion = "Zoom negativo"
# 	elif funcion_minimo == 7:
# 		funcion = "Zoom positivo"


# 	print (valor_minimo, funcion)

# 	(resultado_minimo1, minimo, valor) = experimento_despl_abajo(a1, a2, 100, ancho_bloq)
# 	(array_resultado_final, minimo, valor) = experimento_despl_izquierda(resultado_minimo1, a2, 100, ancho_bloq)

# 	# img = Image.fromarray(a1, 'L')
# 	# img.show()
# 	# img1 = Image.fromarray(array_resultado_final, 'L')
# 	# img1.show()
# 	# img2 = Image.fromarray(a2, 'L')
# 	# img2.show()

# # im = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD1.bmp")
# # im = im.convert('L')
# # im2 = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD2.bmp")
# # im2 = im2.convert('L')

# # valor = 0
# # bloque_im = div.sel_bloque(516,im)
# # bloque_im2 = div.sel_bloque(516,im2)
# # #bloque_im.show()
# # (ancho, largo) = bloque_im.size
# # #print (ancho)
# # a1 = np.array(bloque_im)
# # a2 = np.array(bloque_im2)

# # array_resultado = despl_abajo(valor, a1)
# # diferencia = comparacion_imagenes(array_resultado, a2)
# # print ("La diferencia es de: ", "%.2f" % (diferencia, ), "con un valor de entrada de: ", valor)

# # # array_resultado = zoom_negativo(3, a_imagen)
# # img = Image.fromarray(array_resultado, 'L')
# # img.show()




















# ############ EXPERIMENTO DE LOS TRES BLOQUES DONDE DISMINUYE 5% LA DIFERENCIA #############################
# # im = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD1.bmp")
# # im = im.convert('L')
# # im2 = Image.open("D:/Manuel/Downloads/Beca/Cosas_que_voy_haciendo/Fotogramas para usar/SD/frameSD2.bmp")
# # im2 = im2.convert('L')

# # valor = 0
# # bloque_im = div.sel_bloque(516,im)
# # bloque_im2 = div.sel_bloque(516,im2)
# # #bloque_im.show()
# # (ancho, largo) = bloque_im.size
# # #print (ancho)
# # a1 = np.array(bloque_im)
# # a2 = np.array(bloque_im2)

# # array_resultado = despl_abajo(valor, a1)
# # diferencia = comparacion_imagenes(array_resultado, a2)
# # print ("La diferencia es de: ", "%.2f" % (diferencia, ), "con un valor de entrada de: ", valor)

# # valor1 = 4
# # array_resultado1 = despl_abajo(valor1, a1)
# # diferencia1 = comparacion_imagenes(array_resultado1, a2)
# # print ("La diferencia es de: ", "%.2f" % (diferencia1, ), "con un valor de entrada de: ", valor1)

# # #Bloque del fotograma 2
# # array_resultado2 = despl_abajo(0, a2)

# # # array_resultado = zoom_negativo(3, a_imagen)
# # img = Image.fromarray(array_resultado, 'L')
# # img.show()
# # img1 = Image.fromarray(array_resultado1, 'L')
# # img1.show()
# # img2 = Image.fromarray(array_resultado2, 'L')
# # img2.show()