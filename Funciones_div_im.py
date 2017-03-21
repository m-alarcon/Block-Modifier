from PIL import Image, ImageDraw
import numpy as np
import math

def sel_bloque(n_bloque, img):

	pixeles = 0
	(ancho, largo) = img.size
	ancho_bloq = int(ancho/32)

	sobrante = (largo%ancho_bloq)/int(largo/ancho_bloq)
	num_filas = int(largo/ancho_bloq)
	fronteras_filas = np.zeros(num_filas+1, 'uint32')
	fronteras_columnas = np.zeros(33, 'uint32')

	#Creación vector con las fronteras de las filas
	for i in range(1, num_filas+1):
		pixeles += sobrante
		if pixeles >= 1:
			alto_bloque_actual = ancho_bloq + 1
			pixeles -= 1
		else:
			alto_bloque_actual = ancho_bloq
			
		fronteras_filas[i] = fronteras_filas[i-1] + alto_bloque_actual

	#Creación vector con las fronteras laterales de las columnas
	for i in range(1, 33):
		fronteras_columnas[i] = fronteras_columnas[i-1] + ancho_bloq

	#Dependiendo del numero de bloque que se pida, hay que saber en que fila y en que columna se encuentra
	n_fila = math.ceil(n_bloque/32)
	n_col = (n_bloque - ((n_fila-1)*32))
	imagen_bloque = img.crop((fronteras_columnas[n_col-1],fronteras_filas[n_fila-1],fronteras_columnas[n_col],fronteras_filas[n_fila]))

	return imagen_bloque
