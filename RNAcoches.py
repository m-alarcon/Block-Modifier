#Archivo para recoger toda la información de entradas y salidas de la red neuronal para entrenarla
#Todas las lineas tienen que ser del estilo: 01->,1,1,1

from PIL import Image, ImageDraw
import numpy as np
import math
import Funciones_div_im as div
import csv
import Funciones_BM as bm

contador_linea = 1

with open("entrenamientoPatinadores.csv", 'w', newline='') as csvfile:
	for f in range(2, 200):
		#Se cargan las imagenes que se van a comparar por bloques.
		im = Image.open("C:/Users/malarcon/Images/Ice/frame"+str(f)+".bmp")
		im = im.convert('L')
		im2 = Image.open("C:/Users/malarcon/Images/Ice/frame"+str(f-1)+".bmp")
		im2 = im2.convert('L')

		#Calculo el numero de bloques que tienen las imagenes
		(ancho, largo) = im.size
		ancho_bloq = int(ancho/32)
		num_filas = int(largo/ancho_bloq)
		num_bloques = 32*num_filas

		#Se coge el mismo bloque de las dos imagenes
		for bloq in range(1, num_bloques):

			bloque_im = div.sel_bloque(bloq,im)
			bloque_im2 = div.sel_bloque(bloq,im2)
			a1 = np.array(bloque_im, 'int16')
			a2 = np.array(bloque_im2, 'int16')

			(prx11, prx21, prx31, prx41, pry11, pry21, pry31, pry41) = bm.metricas(f, bloq)
			(prx12, prx22, prx32, prx42, pry12, pry22, pry32, pry42) = bm.metricas(f-1, bloq)

			(delta0, delta1, delta2, delta3, delta4, delta5, delta_1, delta_2, delta_3, delta_4, delta_5) = bm.deltas(f, bloq)
			(resultado, minimo, valorx, valory) = bm.experimento_despl_v2(a1, a2, bloq, ancho_bloq)

			writer = csv.writer(csvfile, delimiter=',',
			                        quotechar=',', quoting=csv.QUOTE_MINIMAL)
			writer.writerow([str(contador_linea)+"->", prx11, prx21, prx31, prx41, pry11, pry21, pry31, pry41, prx12, prx22, prx32, prx42, pry12, pry22, pry32, pry42, prx11-prx12, prx21-prx22, prx31-prx32, prx41-prx42, prx11-prx21, prx31-prx41, prx12-prx22, prx32-prx42, pry11-pry12, pry21-pry22, pry31-pry32, pry41-pry42, pry11-pry31, pry21-pry41, pry12-pry22, pry32-pry42,
				delta0, delta1, delta2, delta3, delta4, delta5, delta_1, delta_2, delta_3, delta_4, delta_5, valorx+0.5, valory+0.5])

			contador_linea = contador_linea + 1
		