#Archivo para recoger toda la información de entradas y salidas de la red neuronal para entrenarla
#Todas las lineas tienen que ser del estilo: 01->,1,1,1

from PIL import Image, ImageDraw
import numpy as np
import math
import Funciones_div_im as div
import csv
import Funciones_BM as bm

contador_linea = 1

print ("Introducir ruta de los fotogramas a procesar")
archivo = input()

print ("Introducir nombre del csv a crear")
fichero_entrenamiento = input()

print ("Escribir la ruta de las metricas del video")
rutaMetricas = input()

with open(fichero_entrenamiento + ".csv", 'w', newline='') as csvfile:
	for f in range(2, 200):
		#Se cargan las imagenes que se van a comparar por bloques.
		im = Image.open(archivo+"/frameSD"+str(f)+".bmp")
		im = im.convert('L')
		im2 = Image.open(archivo+"/frameSD"+str(f-1)+".bmp")
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

				#(delta0, delta1, delta2, delta3, delta4, delta5, delta_1, delta_2, delta_3, delta_4, delta_5) = bm.deltas(f, bloq)
				(resultado, minimo, valorx, valory) = bm.experimento_despl_v2(a1, a2, bloq, ancho_bloq)

				writer = csv.writer(csvfile, delimiter=',',
				                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
				writer.writerow([str(contador_linea)+"->", array_pr1[0], array_pr1[1], array_pr2[0], array_pr2[1], array_pr3[0], array_pr3[1], array_pr4[0], array_pr4[1], array_pr4[2], array_pr4[3], array_pr5[0], array_pr5[1], array_pr5[2], array_pr5[3],
					array_pr6[0], array_pr6[1], array_pr6[2], array_pr6[3], array_pr7[0], array_pr7[1], array_pr8[0], array_pr8[1], array_pr9[0], array_pr9[1], array_pr10[0], array_pr10[1], array_pr11[0], array_pr11[1], array_pr12[0], array_pr12[1], array_pr13[0], 
					array_pr13[1], array_pr13[2], array_pr13[3], array_pr14[0], array_pr14[1], array_pr14[2], array_pr14[3], array_pr15[0], array_pr15[1], array_pr15[2], array_pr15[3], array_pr16[0], array_pr16[1], array_pr17[0], array_pr17[1], array_pr18[0], array_pr18[1],
					array_pr1[4], array_pr1[5], array_pr2[4], array_pr2[5], array_pr3[4], array_pr3[5], array_pr4[4], array_pr4[5], array_pr4[4], array_pr4[5], array_pr5[4], array_pr5[5], array_pr5[6], array_pr5[7],
					array_pr6[4], array_pr6[5], array_pr6[6], array_pr6[7], array_pr7[4], array_pr7[5], array_pr8[4], array_pr8[5], array_pr9[4], array_pr9[5], array_pr10[4], array_pr10[5], array_pr11[4], array_pr11[5], array_pr12[4], array_pr12[5], array_pr13[4], 
					array_pr13[5], array_pr13[6], array_pr13[7], array_pr14[4], array_pr14[5], array_pr14[6], array_pr14[7], array_pr15[4], array_pr15[5], array_pr15[6], array_pr15[7], array_pr16[4], array_pr16[5], array_pr17[4], array_pr17[5], array_pr18[4], array_pr18[5],
					valorx+0.5, valory+0.5])		

				contador_linea = contador_linea + 1
		print ("Procesado fotograma " + str(f) + " de 200")
		