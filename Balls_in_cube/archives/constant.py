
import math

#Definimos las constantes a usar

#Aspectos generales:

#Definimos largo y ancho de la ventana
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
#Numero de BYTES
SIZE_IN_BYTES = 4


#Aristas del cubo:

#Largo de las aristas
EDGE_LARGE = 2
#Grosor de las aristas
EDGE_THICKNESS = 0.01


#Esferas

#Radio de las esferas
SPHERE_RADIO = 0.12
#Velocidades iniciales esferas
VEL_SPHERE = 0.4 * EDGE_LARGE           #La que llamamos solo V
VELX_SPHERE = VEL_SPHERE/math.sqrt(2)
VELY_SPHERE = VEL_SPHERE/math.sqrt(2)
#Numero maximo de esferas
SPHERE_MAXNUMBER = 20

