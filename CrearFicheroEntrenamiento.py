#Archivo para recoger toda la información de entradas y salidas de la red neuronal para entrenarla
#Todas las lineas tienen que ser del estilo: 01->,1,1,1

from PIL import Image, ImageDraw
from optparse import OptionParser
import numpy as np
import math
import Funciones_div_im as div
import csv
import Funciones_BM as bm


contador_linea = 1
carpeta_frames = "/frame"
(options, args) = OptionParser().parse_args()

#It is possible to pass the args using the interactive menu or using the
#console command.
if (len(args) > 0):
	archivo = args[0] #ruta a fotogramas a procesar
	rutaMetricas = args[1] #ruta a metricas a procesar
	fichero_entrenamiento = args[2] #nombre fichero de entrenamiento
	carpeta_frames = args[3] #frame o frameSD
	bm.set_carpeta_metricas(args[4]) #metricasframe o metricasframeSD
	movimientos_bloques = False
	if (args[5] == 'yes'): #yes o no
		movimientos_bloques = True
else:
	print ("Introducir ruta de los fotogramas a procesar")
	archivo = input()

	print ("Escribir la ruta de las metricas del video")
	rutaMetricas = input()

	print ("Introducir nombre del csv a crear")
	fichero_entrenamiento = input()

with open(fichero_entrenamiento + ".csv", 'w', newline='') as csvfile:
	for f in range(2, 200):
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
		for bloq_x in range(2, 31):
			for bloq_y in range(2, num_filas-1):

				bloq = (bloq_y*32)+bloq_x
				bloque_im = div.sel_bloque(bloq,im)
				bloque_im2 = div.sel_bloque(bloq,im2)
				a1 = np.array(bloque_im, 'int16')
				a2 = np.array(bloque_im2, 'int16')

				array_pr1 = bm.metricas(f, bloq-33, rutaMetricas)
				array_pr2 = bm.metricas(f, bloq-32, rutaMetricas)
				array_pr3 = bm.metricas(f, bloq-31, rutaMetricas)
				array_pr4 = bm.metricas(f, bloq-1, rutaMetricas)
				array_pr5 = bm.metricas(f, bloq, rutaMetricas)
				array_pr6 = bm.metricas(f, bloq+1, rutaMetricas)
				array_pr7 = bm.metricas(f, bloq+31, rutaMetricas)
				array_pr8 = bm.metricas(f, bloq+32, rutaMetricas)
				array_pr9 = bm.metricas(f, bloq+33, rutaMetricas)
				array_pr10 = bm.metricas(f-1, bloq-33, rutaMetricas)
				array_pr11 = bm.metricas(f-1, bloq-32, rutaMetricas)
				array_pr12 = bm.metricas(f-1, bloq-31, rutaMetricas)
				array_pr13 = bm.metricas(f-1, bloq-1, rutaMetricas)
				array_pr14 = bm.metricas(f-1, bloq, rutaMetricas)
				array_pr15 = bm.metricas(f-1, bloq+1, rutaMetricas)
				array_pr16 = bm.metricas(f-1, bloq+31, rutaMetricas)
				array_pr17 = bm.metricas(f-1, bloq+32, rutaMetricas)
				array_pr18 = bm.metricas(f-1, bloq+33, rutaMetricas)

				writer = csv.writer(csvfile, delimiter=',',
										quotechar=',', quoting=csv.QUOTE_MINIMAL)

				if(movimientos_bloques):
					#(delta0, delta1, delta2, delta3, delta4, delta5, delta_1, delta_2, delta_3, delta_4, delta_5) = bm.deltas(f, bloq)
					(resultado, minimo, valorx, valory) = bm.experimento_despl_v2(a1, a2, bloq, ancho_bloq)

					writer.writerow([str(contador_linea)+"->",
						array_pr10[0] - array_pr1[0], array_pr10[0] - array_pr2[0], array_pr10[0]-array_pr3[0],
						array_pr11[0] - array_pr1[0], array_pr11[0] - array_pr2[0], array_pr11[0] - array_pr3[0],
						array_pr12[0] - array_pr1[0], array_pr12[0] - array_pr2[0], array_pr12[0] - array_pr3[0],

						array_pr10[2] - array_pr1[2], array_pr10[2] - array_pr2[2], array_pr10[2]-array_pr3[2],
						array_pr11[2] - array_pr1[2], array_pr11[2] - array_pr2[2], array_pr11[2] - array_pr3[2],
						array_pr12[2] - array_pr1[2], array_pr12[2] - array_pr2[2], array_pr12[2] - array_pr3[2],

						array_pr10[4] - array_pr1[4], array_pr10[4] - array_pr2[4], array_pr10[4]-array_pr3[4],
						array_pr11[4] - array_pr1[4], array_pr11[4] - array_pr2[4], array_pr11[4] - array_pr3[4],
						array_pr12[4] - array_pr1[4], array_pr12[4] - array_pr2[4], array_pr12[4] - array_pr3[4],

						array_pr10[6] - array_pr1[6], array_pr10[6] - array_pr2[6], array_pr10[6]-array_pr3[6],
						array_pr11[6] - array_pr1[6], array_pr11[6] - array_pr2[6], array_pr11[6] - array_pr3[6],
						array_pr12[6] - array_pr1[6], array_pr12[6] - array_pr2[6], array_pr12[6] - array_pr3[6],
						valorx+0.5, valory+0.5])

				else:
					writer.writerow([str(contador_linea)+"->",
						array_pr10[0] - array_pr1[0], array_pr10[0] - array_pr2[0], array_pr10[0]-array_pr3[0],
						array_pr11[0] - array_pr1[0], array_pr11[0] - array_pr2[0], array_pr11[0] - array_pr3[0],
						array_pr12[0] - array_pr1[0], array_pr12[0] - array_pr2[0], array_pr12[0] - array_pr3[0],

						array_pr10[2] - array_pr1[2], array_pr10[2] - array_pr2[2], array_pr10[2]-array_pr3[2],
						array_pr11[2] - array_pr1[2], array_pr11[2] - array_pr2[2], array_pr11[2] - array_pr3[2],
						array_pr12[2] - array_pr1[2], array_pr12[2] - array_pr2[2], array_pr12[2] - array_pr3[2],

						array_pr10[4] - array_pr1[4], array_pr10[4] - array_pr2[4], array_pr10[4]-array_pr3[4],
						array_pr11[4] - array_pr1[4], array_pr11[4] - array_pr2[4], array_pr11[4] - array_pr3[4],
						array_pr12[4] - array_pr1[4], array_pr12[4] - array_pr2[4], array_pr12[4] - array_pr3[4],

						array_pr10[6] - array_pr1[6], array_pr10[6] - array_pr2[6], array_pr10[6]-array_pr3[6],
						array_pr11[6] - array_pr1[6], array_pr11[6] - array_pr2[6], array_pr11[6] - array_pr3[6],
						array_pr12[6] - array_pr1[6], array_pr12[6] - array_pr2[6], array_pr12[6] - array_pr3[6]])

				contador_linea = contador_linea + 1
		print ("Procesado fotograma " + str(f) + " de 200")
