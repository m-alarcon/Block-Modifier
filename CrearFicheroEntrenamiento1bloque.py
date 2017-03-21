#Archivo para recoger toda la información de entradas y salidas de la red neuronal para entrenarla
#Todas las lineas tienen que ser del estilo: 01->,1,1,1

from PIL import Image, ImageDraw
import numpy as np
import math
import Funciones_div_im as div
import csv
import Funciones_BM as bm
from optparse import OptionParser

contador_linea = 1
bloq = 1#(bloq_y*32)+bloq_x
carpeta_frames = "/frame"
(options, args) = OptionParser().parse_args()

if (len(args) > 0):
	archivo = args[0] #ruta a fotogramas a procesar
	rutaMetricas = args[1] #ruta a metricas a procesar
	fichero_entrenamiento = args[2] #nombre fichero de entrenamiento
	bloq = args[3]
	carpeta_frames = args[4]
	bm.set_carpeta_metricas(args[5]) #metricasframe o metricasframeSD
	if (args[6] == 'yes'): #yes o no
		movimientos_bloques = True
else:
	print ("Introducir ruta de los fotogramas a procesar")
	archivo = input()

	print ("Introducir nombre del csv a crear")
	fichero_entrenamiento = input()

	print ("Escribir la ruta de las metricas del video")
	rutaMetricas = input()

with open(fichero_entrenamiento + ".csv", 'w', newline='') as csvfile:
	for f in range(2, 2):
		#Se cargan las imagenes que se van a comparar por bloques.
		im = Image.open(archivo+carpeta_frames+str(f)+".bmp")
		im = im.convert('L')
		im2 = Image.open(archivo+carpeta_frames+str(f-1)+".bmp")
		im2 = im2.convert('L')

		#Calculo el numero de bloques que tienen las imagenes
		(ancho, largo) = im.size
		ancho_bloq = int(ancho/32)
		num_filas = int(largo/ancho_bloq)
		num_bloques = 32*num_filas

		#Se coge el mismo bloque de las dos imagenes
		#for bloq in range(1,num_bloques):
		#for bloq_x in range(2, 32):
			#for bloq_y in range(1, num_filas):
		bloque_im = div.sel_bloque(bloq,im)
		bloque_im2 = div.sel_bloque(bloq,im2)
		a1 = np.array(bloque_im, 'int16')
		a2 = np.array(bloque_im2, 'int16')

		array_pr1 = bm.metricas(f, bloq-1, rutaMetricas)
		array_pr2 = bm.metricas(f, bloq, rutaMetricas)
		array_pr12 = bm.metricas(f-1, bloq-1, rutaMetricas)
		array_pr22 = bm.metricas(f-1, bloq, rutaMetricas)


		writer = csv.writer(csvfile, delimiter=',',
								quotechar=',', quoting=csv.QUOTE_MINIMAL)

		if (movimientos_bloques):
			#(delta0, delta1, delta2, delta3, delta4, delta5, delta_1, delta_2, delta_3, delta_4, delta_5) = bm.deltas(f, bloq)
			(resultado, minimo, valorx, valory) = bm.experimento_despl_v2(a1, a2, bloq, ancho_bloq)

			writer.writerow([str(contador_linea)+"->",
				array_pr1[0], array_pr1[1], array_pr2[1],
				array_pr12[0], array_pr12[1], array_pr22[1], valorx])

		else:
			writer.writerow([str(contador_linea)+"->",
				array_pr1[0], array_pr1[1], array_pr2[1],
				array_pr12[0], array_pr12[1], array_pr22[1]])


			#valorx+0.5, valory+0.5])

		contador_linea = contador_linea + 1
		print ("Procesado fotograma " + str(f) + " de 200")
