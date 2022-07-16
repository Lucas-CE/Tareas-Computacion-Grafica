from libs.shaders import SimpleTransformShader
from libs.logo import LogoDVD, BartSimpson
from libs.basic_shapes import createQuad
from libs.gpu_shape import GPUShape
from OpenGL.GL import *
import numpy as np
import glfw


#Calculando velocidades normalizadas
iniciales = "LC"
alpha = ord(iniciales[0]) * ord(iniciales[1])

#Se divide en la cantidad de pixeles/2 para normalizar la velocidad, considerando que una velocidad
#de 2 para x o y, va de lado a lado en 1 segundo 
velocidadX = 350 * np.cos(alpha) /400
velocidadY = 350 * np.sin(alpha) /300

#Calculando escalamiento version grande
#En caso de que querer revisar que se produzca un escalamiento (pues S produce una diferencia pequena)
#se puede cambiar S por cualquier valor (recomiendo 1.5) para notar que funciona el escalamiento
rut = 20665611
S = max((rut / 20000000)**3 , 1.5)

#Calculando rgb del logo
nombre = "Lucas"
l = len(nombre)
r = (ord(nombre[0%l]) * ord(nombre[1%l]) % 255) / 255
g = (ord(nombre[2%l]) * ord(nombre[3%l]) % 255) / 255
b = (ord(nombre[4%l]) * ord(nombre[5%l]) % 255) / 255


#Creando controlador
class Controller:

    def __init__(self):

        #Posiciones
        self.posX = 0.0
        self.posY = 0.0

        #Velocidades
        self.velX = velocidadX
        self.velY = velocidadY

        #Grados de cuan rotado esta
        self.grades = 0

        #Estado del tamano
        self.estado = "pequeno"

        #Constante relacionada al cambio de tamano para cada eje
        self.cTX = 1
        self.cTY = 1

        #Distancia de hitbox
        self.HitBox_X = 0.8
        self.HitBox_Y = 0.8

        #Distancias de hitbox dependiendo si es grande o pequena
        self.dist_hit_pequeno = 0.8
        self.dist_hit_grande_X = 1 - ( 0.2 * S ) * 3/4
        self.dist_hit_grande_Y = 1 - ( 0.2 * S ) * 4/3
        

    #funcion de cambio de estado entre "pequeno" y "grande"
    def cambiar_estado(self):
        
        if self.estado == "pequeno":
            self.estado = "grande"
        
        elif self.estado == "grande":
            self.estado = "pequeno"

    #Funcion que setea y retorna las constantes 
    def det_constante_tamano(self):

        #La constante sera 1 si el objeto esta en su tamano pequeno 
        if self.estado == "pequeno":
            self.cTX = 1
            self.cTY = 1

        #La constantes seran el escalamiento S * las correcciones para que el retangulo se rote
        #para cuando el tamano es grande
        elif self.estado == "grande":
            self.cTX = S*4/3
            self.cTY = S*3/4

        return (self.cTX, self.cTY)

    #Funcion que setea los hitbox en x e y para el objeto
    def det_HitBox(self):

        if self.estado == "pequeno":

            self.HitBox_X = self.dist_hit_pequeno
            self.HitBox_Y = self.dist_hit_pequeno

        elif self.estado == "grande":

            self.HitBox_X = self.dist_hit_grande_X
            self.HitBox_Y = self.dist_hit_grande_Y

    #funcion que mueve el controlador
    def move(self, x, y):

        #Seteamos el hitbox segun su tamaño
        self.det_HitBox()

        #Actualizamos las posiciones con el movimiento x,y
        self.posX += x
        self.posY += y

        #condicion de choque con pared izquierda
        if self.posX < -self.HitBox_X:

            #cambiamos sentido de la velocidad
            self.velX = self.velX * -1

            #si choca con una pared siendo chico, lo teletransportamos pues el hitbox crece
            if self.estado == "pequeno":
                self.posX = -(self.dist_hit_grande_X - 0.001)

            elif self.estado == "grande":
                self.posX = -(self.dist_hit_pequeno - 0.001)

            #Se actualizan los grados en los que esta girado en caso de chocar con una pared
            self.grades += np.pi / 2

            #Cambia de estado entre "grande" y "pequeno"
            self.cambiar_estado()

        #condicion de choque con pared derecha
        if self.posX > self.HitBox_X:

            self.velX = self.velX * -1

            if self.estado == "pequeno":
                self.posX = (self.dist_hit_grande_X - 0.001)
            
            elif self.estado == "grande":
                self.posX = (self.dist_hit_pequeno - 0.001)
            
            self.grades += np.pi / 2
            
            self.cambiar_estado()

        #condicion de choque con pared inferior
        if self.posY < -self.HitBox_Y:

            self.velY = self.velY * -1

            if self.estado == "pequeno":
                self.posY = -(self.dist_hit_grande_Y - 0.001)
            
            elif self.estado == "grande":
                self.posY = -(self.dist_hit_pequeno - 0.001)
            
            self.grades += np.pi / 2

            self.cambiar_estado()

        #condicion de choque con pared superior
        if self.posY > self.HitBox_Y:

            self.velY = self.velY * -1
            if self.estado == "pequeno":
                self.posY = (self.dist_hit_grande_Y - 0.001)
            
            elif self.estado == "grande":
                self.posY = (self.dist_hit_pequeno - 0.001)

            self.grades += np.pi / 2

            self.cambiar_estado()

        return

    #Actualiza el estado del controlador aplicando el movimiento correspondiente a la velocidad y el tiempo
    def update(self,dt):

        #Se calculan los movimientos en dt tiempo en las posiciones x e y
        movX = self.velX*dt
        movY = self.velY*dt

        #Se actualizan las posiciones del controlador
        self.move(movX, movY)
        

#Se crea un controlador para controlar el movimiento de los objetos y algunas propiedades de estos
controller = Controller()

def main():
    
    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return -1

    #Definimos el ancho y largo de la ventana
    width = 800 ; height = 600

    #Creamos la ventana
    window = glfw.create_window(width, height, "Salvapantallas DVD", None, None)

    #Condicion de cierre de la ventana
    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window)
 
    #Usamos el SimpleTransformShader() porque deseamos realizar transformaciones
    pipeline = SimpleTransformShader()
    glUseProgram(pipeline.shaderProgram)

    #Seteamos el color del fondo 
    glClearColor(0.0, 0.0, 0.0, 1.0)

    #Seteamos el color de el cuadrado
    (r2, g2, b2) = (10/255, 10/255, 10/255)

    #creamos el cuadrado del fondo del dvd
    PrincipalQ = createQuad(0.8, r2, g2, b2)
    gpuPQ = GPUShape().initBuffers()
    pipeline.setupVAO(gpuPQ)
    gpuPQ.fillBuffers(PrincipalQ.vertexData, PrincipalQ.indexData)

    #Creamos las figuras del logo
    DVD = LogoDVD(pipeline, controller, r, g, b)

    #Iniciamos Construccion de cabeza Bart Simspon
    Bart = BartSimpson(pipeline, controller)

    #Se llama una funcion que rellene los poligonos que creamos para que no sean solo lineas
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #Llamamos t0 al tiempo tomado en la instancia actual
    t0 = glfw.get_time()

    #Entramos en un bucle siempre que la ventana no este cerrada
    while not glfw.window_should_close(window):

        #Se obtiene el tiempo al principio de cada ciclo para calcular un dt el cual usar para luego usarlo
        #para actualizar la posicion
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        #Determinamos constantes de tamano
        (cTX, cTY) = controller.det_constante_tamano()

        #Las variables Tamano son las usadas para los escalamientos
        #El escalamiento natural de Bart es 0.2
        (tamanhoBart_X, tamanhoBart_Y) = (cTX/5, cTY/5)

        #Calculamos las posiciones en x e y, considerando una antirotacion a la efectuada por el logo, de esta forma
        #el eje coordenado x,y en el que trabajamos permanece en la posicion inicial
        X_Position = controller.posX * np.cos(-controller.grades) - controller.posY * np.sin(-controller.grades)
        Y_Position = controller.posX * np.sin(-controller.grades) + controller.posY * np.cos(-controller.grades)

        #Definimos las posiciones de Bart repecto a la posicion del dvd
        #anadiendo la correccion del tamano de Bart
        xPosBart = (0.04 + X_Position) * 1/tamanhoBart_X
        yPosBart = (-0.04 + Y_Position) * 1/tamanhoBart_Y

        #Dibujamos el lgoo del DVD
        DVD.Draw_DVD(X_Position, Y_Position, cTX, cTY)

        #Dibujamos la cabeza de Bart
        Bart.Draw_Bart(xPosBart, yPosBart, cTX, cTY)

        glfw.swap_buffers(window)

        #Actualiza las posiciones para iniciar el siguiente ciclo
        controller.update(dt)

    #Limpia la ventana de los objetos antes dibujados
    gpuPQ.clear()
    DVD.clear_DVD()
    Bart.clear_Bart()

    glfw.terminate()

    return 0

if __name__ == "__main__":
    main()
