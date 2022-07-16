
#Primero, importamos las librerias
from archives.easy_shaders import SimpleTextureModelViewProjectionShaderProgram
from archives.easy_shaders import SimpleModelViewProjectionShaderProgram
from archives.easy_shaders import textureSimpleSetup
from archives.basic_shapes import create_Sphere
from archives.assets_path import getAssetPath
from archives.gpu_shape import GPUShape
import archives.transformations as tr
import archives.constant as C
from archives.cube import *
from OpenGL.GL import *
import numpy as np
import glfw
import math

#Para este codigo se uso como referencia el auxiliar 4 y 5

#Creamos el controlador de las esferas
class SphereController:
    
    def __init__(self):

        #L es el largo del cubo
        L = C.EDGE_LARGE

        #Definimos las posiciones velocidades y aceleraciones de las esferas
        self.pos = [[0, 0, 0.3 * L],[0.2*L, 0.3*L, 0.2*L]]
        self.vel = [[C.VELX_SPHERE,C.VELY_SPHERE,0],[C.VELX_SPHERE,C.VELY_SPHERE,0]]
        self.acl = [0,0,-9.8]

        #Determinamos a que distancia del centro de referencias la esfera golpea el cubo
        self.Hitbox_distance = L/2 - C.SPHERE_RADIO

        #Definimos el numero de esferas
        self.numSpheres = 2


    #Funcion para añadir una esfera
    def add_sphere(self):

        #Añadimos la posicion y velocidad de la nueva esfera a los datos del controlador
        self.pos += [[0,0,0.3 * C.EDGE_LARGE]]
        self.vel += [[C.VELX_SPHERE,C.VELY_SPHERE,0]]

        #Sumamos uno al numero de esferas
        self.numSpheres += 1


    #Entrega True si las esferas i y j colisionan, y False en caso contrario
    def collision_check(self, i, j):

        #Se guardan en pos1 y pos2 las posiciones de i y j como arrays
        pos1 = np.array(self.pos[i])
        pos2 = np.array(self.pos[j])

        #Se define la distancia entre las esferas como la norma de la diferencia de posiciones
        distance = np.linalg.norm(pos1-pos2)

        #Define la distancia a la que deben estar las esferas i y j para chocar
        hit_distance = 2*C.SPHERE_RADIO

        return distance < hit_distance


    #Funcion que modifica las velocidades de las esferas i y j
    #de forma que si colisionan se volteen los vectores velocidad
    #Esta funcion fue basada en una explicacion fisica dada en la pagina
    #https://studiofreya.com/3d-math-and-physics/simple-sphere-sphere-collision-detection-and-collision-response/
    def collision(self, i, j):

        #Condicion de que no estan en la misma posicion para que al calcular norma no se divida en 0
        #Puede ocurrir este caso si se crean 2 esferas al mismo tiempo
        if self.pos[i] != self.pos[j]:

            #Modelamiento del choque elastico entre 2 particulas
            x = np.array(self.pos[i])-np.array(self.pos[j])
            x /= np.linalg.norm(x)

            v1 = np.array(self.vel[i])
            x1 = np.dot(x,v1)
            v1x = x * x1
            v1y = v1 - v1x
            m1 = 1

            x = x*-1
            v2 = np.array(self.vel[j])
            x2 = np.dot(x,v2)
            v2x = x * x2
            v2y = v2 - v2x
            m2 = 1

            #Actualiza las velocidades a las post choque
            self.vel[i] = ( v1x*(m1-m2)/(m1+m2) + v2x*(2*m2)/(m1+m2) + v1y )
            self.vel[j] = ( v1x*(2*m1)/(m1+m2) + v2x*(m2-m1)/(m1+m2) + v2y )


    #Hace que la esfera i si choca con una pared choque y cambie su direccion
    def hitBox(self, i):

        #Si la posicion de la esfera es mayor que la distancia de hitbox o menor que
        #-la distancia de hitbox, se invierte su velocidad, excepto al tocar el techo,
        #en ese caso se detiene

        if self.pos[i][0] < -self.Hitbox_distance:
            self.vel[i][0] *= -1
            self.pos[i][0] = -self.Hitbox_distance

        elif self.pos[i][0] > self.Hitbox_distance:
            self.vel[i][0] *= -1
            self.pos[i][0] = self.Hitbox_distance

        elif self.pos[i][1] < -self.Hitbox_distance:
            self.vel[i][1] *= -1
            self.pos[i][1] = -self.Hitbox_distance

        elif self.pos[i][1] > self.Hitbox_distance:
            self.vel[i][1] *= -1
            self.pos[i][1] = self.Hitbox_distance

        elif self.pos[i][2] < -self.Hitbox_distance:
            self.vel[i][2] *= -1
            self.pos[i][2] = -self.Hitbox_distance

        elif self.pos[i][2] > self.Hitbox_distance:
            self.vel[i][2] *= 0
            self.pos[i][2] = self.Hitbox_distance


    #Funcion que determina si la posicion inicial de las esferas ([0,0,0.3]) esta libre para
    #dibujar una nueva esfera en esa posicion
    def initialPos_isFree(self):

        #Definimos initialPos como la posicion inicial
        initialPos = np.array([0,0,0.3 * C.EDGE_LARGE])

        #Apriori asumimos que esta libre
        isFree = True

        #Recorremos todas las esferas
        for k in range(self.numSpheres):
            
            #Guardamos en una variable la posicion de la esfera k
            posK = np.array(self.pos[k])
            #Guardamos en una variable la distancia entre la posicion inicial y la posicion de la esfera k
            distance = np.linalg.norm(posK-initialPos)

            #Si la distancia es menor que 2 radios de una bola, se dice que la posicion inicial esta ocupada
            if distance < 2*C.SPHERE_RADIO:
                
                isFree = False

        return isFree


    #Funcion que actualiza las posiciones de la esfera i considerando un movimiento de mov
    def move(self, i, mov):

        #Actualiza el vector posicion en x y z de la esfera i sumandole cada coordenada de mov
        self.pos[i][0] += mov[0]
        self.pos[i][1] += mov[1]
        self.pos[i][2] += mov[2]

        self.hitBox(i)

    #Funcion que actualiza las velocidades de la esfera i considerando un cambio de velocidad acel
    def accelerate(self, i, acel):

        #Actualiza el vector velocidad en x y z de la esfera i sumandole cada coordenada de acel
        self.vel[i][0] += acel[0]
        self.vel[i][1] += acel[1]
        self.vel[i][2] += acel[2]


    #Actualiza el estado de la esfera
    def update(self,dt):

        #Recorremos todas las esferas
        for i in range(self.numSpheres):

            #Para la esfera i:

            #Se calcula el cambio de velocidad en dt tiempo en los ejes x y z
            #Es el mismo para todas las esferas
            acel = [a*dt for a in self.acl]

            #Se actualizan las velocidades
            self.accelerate(i, acel)

            #Se calculan los movimientos en dt tiempo en las posiciones x y z
            mov = [p*dt for p in self.vel[i]]

            #Se actualizan las posiciones del controlador
            self.move(i, mov)

        #Recorremos todos los pares de esferas
        for i in range(self.numSpheres):
            for j in range(self.numSpheres):

                #Las esferas que esten colisionando 
                #i>j para que no se corran los pares (i,i) y para que no se corran (i,j) y (j,i)
                if i>j and self.collision_check(i, j):

                    #Realiza la colision entre esferas
                    self.collision(i, j)

                    #Si es que el numero de esferas es menor al maximo y la posicion inicial esta libre
                    if self.numSpheres < C.SPHERE_MAXNUMBER and self.initialPos_isFree():

                        #Se crea una esfera nueva
                        self.add_sphere()


#Creamos el controlador de la camara
class CameraController:

    def __init__(self):

        #Definimos si la camara esta posicionada en la esfera (POV eres una esfera)
        self.CameraSphere = False


    #Funcion para cambiar el pov entre que este en una esfera, y que este fuera del cubo
    def change_pov(self):
        self.CameraSphere = not self.CameraSphere


    #Funcion que devuelve True si la camara esta en la esfera y False si no
    def CamInSphere(self):
        return self.CameraSphere


#Creamos el controlador de la camara
CamController = CameraController()


#Creamos la variable alpha para el angulo de la camara
alpha = 0


#Definimos la funcion que detectara la tecla presionada
def key(window, key, scancode, action, mods):

    #Usaremos la variable alpha
    global alpha

    #Si es que detecta que presionamos una tecla
    if action == glfw.PRESS:

        #Si la tecla presionada es flecha a la izquierda, le restamos 2pi/15 a alpha
        if key == glfw.KEY_LEFT:
            alpha += -2*math.pi/15

        #Si la tecla presionada es flecha a la derecha, le sumamos 2pi/15 a alpha
        if key == glfw.KEY_RIGHT:
            alpha += 2*math.pi/15

        #Si la tecla presionada es el espacio, cambiamos el POV
        if key == glfw.KEY_SPACE:
            CamController.change_pov()
            
            

def main():

    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return -1

    #Se determinan las dimensiones de la ventana
    width = C.SCREEN_WIDTH
    height = C.SCREEN_HEIGHT

    #Se crea la ventana
    window = glfw.create_window(width, height, "Tarea 1 P2", None, None)

    #Condicion de cierre de la ventana
    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window)

    #Se conecta la funcion key con las teclas presionadas
    glfw.set_key_callback(window, key)

    #Se crea el shader que usaremos considerando que usaremos texturas y un modelo de vista
    pipelineTexture = SimpleTextureModelViewProjectionShaderProgram()
    pipelineColor = SimpleModelViewProjectionShaderProgram()

    #Creamos el controlador de la esfera
    SphereC = SphereController()

    #Creamos la esfera
    Sphere = create_Sphere(C.SPHERE_RADIO,20,20)
    gpuSphere = GPUShape().initBuffers()
    pipelineTexture.setupVAO(gpuSphere)
    gpuSphere.fillBuffers(Sphere.vertexData, Sphere.indexData, GL_STATIC_DRAW)

    #Le damos textura de jupiter a la esfera
    gpuSphere.texture = textureSimpleSetup(
        getAssetPath("jupiter.jpg"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    #Creamos el "cubo" compuesto por sus aristas y su gpu
    Cube = CubeEdges(pipelineColor)
    gpuCube = Cube.gpuEDGE

    #Definimos la textura de las aristas del cubo como ladrillos 
    #(no seran casi visibles) a menos que se aumente el grosor de las aristas
    gpuCube.texture = textureSimpleSetup(
        getAssetPath("bricks.jpg"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    #Definimos un tipo de proyeccion
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)
    
    #Seteamos el color de fondo
    glClearColor(0.15, 0.15, 0.15, 1.0)

    glEnable(GL_DEPTH_TEST)

    #Llamamos t0 al tiempo tomado en la instancia actual
    t0 = glfw.get_time()

    while not glfw.window_should_close(window):

        #Se obtiene el tiempo al principio de cada ciclo para calcular un dt el cual usar para luego usarlo
        #para actualizar la posicion
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        glfw.poll_events()
        
        #Definimos el punto de vista

        #Si el pov no es de la esfera, hacemos que la camara gire 2pi/15 si presionamos las flechas
        if not CamController.CamInSphere():
            view = tr.lookAt(
                np.array([4*math.cos(alpha), 4*math.sin(alpha), 0.5]),
                np.array([0,0,0]),
                np.array([0,0,1])
            )

        #Si el pov es de la esfera, la camara se ira moviendo con la esfera 0
        #y apuntara hacia donde se mueva la esfera 0
        if CamController.CamInSphere():
            view = tr.lookAt(
                np.array([SphereC.pos[0][0]+C.SPHERE_RADIO, SphereC.pos[0][1], SphereC.pos[0][2]]),
                np.array([100*SphereC.vel[0][0], 100*SphereC.vel[0][1], 100*SphereC.vel[0][2]]),
                np.array([0,0,1])
            )

        #Determinamos que las figuras que creamos se rellenen
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #Se determina el shader a usar en el programa
        glUseProgram(pipelineTexture.shaderProgram)

        #Setemos la proyeccion
        glUniformMatrix4fv(glGetUniformLocation(pipelineTexture.shaderProgram, "projection"), 1, GL_TRUE, projection)

        #Seteamos la vista
        glUniformMatrix4fv(glGetUniformLocation(pipelineTexture.shaderProgram, "view"), 1, GL_TRUE, view)

        #Para esfera de las numSpheres que hay
        for i in range(SphereC.numSpheres):

            #Se trasladan a sus posiciones
            glUniformMatrix4fv(glGetUniformLocation(pipelineTexture.shaderProgram, "model"), 1, GL_TRUE, 
                tr.matmul([tr.translate(SphereC.pos[i][0], SphereC.pos[i][1], SphereC.pos[i][2]),
                tr.scale(1.0, 1.0, 1.0)]))

            #Se dibujan las esferas
            pipelineTexture.drawCall(gpuSphere)

        #Se determina el shader a usar en el programa
        glUseProgram(pipelineColor.shaderProgram)

        #Setemos la proyeccion
        glUniformMatrix4fv(glGetUniformLocation(pipelineColor.shaderProgram, "projection"), 1, GL_TRUE, projection)

        #Seteamos la vista
        glUniformMatrix4fv(glGetUniformLocation(pipelineColor.shaderProgram, "view"), 1, GL_TRUE, view)

        #Se dibujan las aristas del cubo
        Cube.draw_CubeEdges()

        #Se actualiza el controlador de las esferas
        SphereC.update(dt)

        glfw.swap_buffers(window)


    #Se limpian los gpus de la memoria
    gpuSphere.clear()
    Cube.clear()

    glfw.terminate()

    return 0

if __name__ == "__main__":
    main()



