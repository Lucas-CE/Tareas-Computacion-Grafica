from libs.generateCurveHermite import generateCurveH
from libs.setup import setView, setPlot, setLights
from libs.Scene_creators.scene_creator import *
import libs.lighting_shaders as ls 
from libs.keyboardConfig import *
from libs.gpu_generator import *
from libs.objFunctions import *
from libs.controllers import *
from libs.car_creator import *
import libs.scene_graph as sg
from OpenGL.GL import *
import numpy as np
import glfw


#Se crea el controlador de las camaras
camControl = camController()

#Se crea el controlador del sol y la luna
SunMoonControl = SunMoonController()

#Se crea un controlador para las luces de el auto
carLightsC = carLights()

#Se crea el controlador de la luz del semaforo
traffic_lightC = controller_TrafficLight()

#Se crea el pool que contendra las luces
spotlightsPool = dict()

#Se define la curva de hermite de largo 100
N = 100
CH = generateCurveH(N)

#Para la funcion on_key llamamos a la funcion sub_on_key que hace lo mismo que el 
#tipico on_key
def on_key(window, key, scancode, action, mods):
    sub_on_key(window, key, action, camControl, traffic_lightC)


def main():

    if not glfw.init():
        glfw.set_window_should_close(window, True)

    #Se crea la ventana
    window = glfw.create_window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.SCREEN_TITLE, None, None)

    #Condicion de cierre de la ventana
    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    #Se conecta la funcion on_key con las teclas presionadas
    glfw.set_key_callback(window, on_key)

    #Se crean los shaders de texturas y colores con iluminacion
    texPipeline = ls.MultipleLightTexturePhongShaderProgram()
    colorPipeline = ls.MultipleLightPhongShaderProgram()

    #Seteamos el color de fondo
    glClearColor(0.85, 0.85, 0.85, 1.0)

    glEnable(GL_DEPTH_TEST)

    #Se setean las luces en su estado inicial (apagadas)
    setLights(spotlightsPool, carLightsC, 0, traffic_lightC.greenON)

    #Se crea la variable auto que contiene el nodo del auto
    auto = createCar(colorPipeline)

    #Creamos la variable dibujo donde guardamos la escena deseada 
    dibujo = createScene(texPipeline)

    #Definimos cantidad de pasos inicial 0
    step = 0

    #Definimos el angulo iniciarl segun la curva
    angle=np.arctan2(CH[step+1,0]-CH[step,0], CH[step+1,1]-CH[step,1])

    #Definimos las posiciones iniciales de las luces y la direccion de estas
    light9pos = np.append(spotlightsPool['spot10'].position, 1)
    light10pos = np.append(spotlightsPool['spot9'].position, 1)
    dir_inicial9 = np.append(spotlightsPool['spot9'].direction, 1)

    #Llamamos t0 al tiempo tomado en la instancia actual
    t0 = glfw.get_time()

    #Creamos la variable hACTUAL para definir la hora actual que contendra el tiempo 
    hACTUAl = 12

    #Creamos la variable tt que contendra el tiempo total y contiene inicialmente el tiempo de
    #12 horas virtuales pero en tiempo real
    tt = hACTUAl * C.DURATION_VIRTUALHOUR

    #Se printea la hora actual (inicia a las 12)
    print("Son las : " + str(hACTUAl%24) + ":00")

    #Cuando la ventana sigue abierta
    while not glfw.window_should_close(window):

        #Se obtiene el tiempo al principio de cada ciclo para calcular un dt el cual usar para luego usarlo
        #para actualizar la posicion
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        #Se suma dt de tiempo al tiempo total
        tt += dt

        #Si es que el tiempo total es mayor a la duracion de la hora actual virtual siguiente a la 
        #hora actual virtual
        if tt >= C.DURATION_VIRTUALHOUR * (hACTUAl + 1):
            hACTUAl += 1
            print("Son las : " + str(hACTUAl%24) + ":00")

        #Si la hora actual esta entre las 8 y las 17:59 las luces estan apagas en caso contrario prendidas
        if 8 <= hACTUAl%24 <= 17: luz = 0
        else: luz = 1

        glfw.poll_events()

        #Se checkea si las teclas se mantienen presionadas
        check_key_inputs(window, camControl)

        #Se setean las luces, la proyeccion y la vista usadas
        setLights(spotlightsPool, carLightsC, luz, traffic_lightC.greenON)
        setPlot(colorPipeline, texPipeline, spotlightsPool, camControl, SunMoonControl)
        setView(colorPipeline, texPipeline, camControl)

        #Se limpia el color de fondo en cada iteracion
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #Se determina el uso del shader de texturas
        glUseProgram(texPipeline.shaderProgram)

        #Se dibuja la escena contenida en el nodo dibujo
        sg.drawSceneGraphNode(dibujo, texPipeline, "model")

        #Se determina el uso del shader de colores
        glUseProgram(colorPipeline.shaderProgram)

        #Se dibuja el auto contenida en el nodo auto
        sg.drawSceneGraphNode(auto, colorPipeline, "model")
        
        #Se le asigna el nodo del auto a la variable auto_0 y se tr
        auto_0 = sg.findNode(auto,'system-car')

        #Se crea la variable newPos que contiene la matriz con la nueva posicion del auto
        newPos = tr.matmul([tr.translate(CH[step,0], CH[step,1], CH[step,2]), tr.rotationZ(-angle)])

        #Se transforma el nodo del auto para llevarlo a su nueva posicion
        auto_0.transform = newPos

        #Se define y setea la posicion de las luces como la posicion nueva del auto + la pos de las 
        #luces relativa al auto
        carLightsC.moveLights(tr.matmul([newPos, light9pos]), tr.matmul([newPos, light10pos]))

        #Se define la direccion de las luces respecto como la direccion inicial + el angulo de la 
        #direccion del auto
        newDirection = tr.matmul([tr.rotationZ(-angle), dir_inicial9])

        #Se setean las direcciones de las luces del auto
        carLightsC.changeDirection(newDirection)

        #Al finalizar los nodos se intercambian con le buffer que contiene la imagen calculada
        glfw.swap_buffers(window)
        
        #Actualiza las posiciones para iniciar el siguiente ciclo
        SunMoonControl.update(dt)

        #Si la luz verde del semaforo esta prendida
        if traffic_lightC.greenON == 0 and step == 245:
            #Sumamos uno al paso de la curva
            step = step
        
        #Si la luz roja del semaforo esta prendida
        else:
            step = step + 1

        #Si es que el paso supera ese limite se determina que reinicie el contador de pasos
        if step > N*8-2: step = 0
        
        #Definimos prev_Angle como el angulo actual (previo a cambios)
        prev_Angle = angle

        #Se define la variable dircar como la direccion de movimiento segun la curva
        dircar = np.arctan2(CH[step+1,0]-CH[step,0], CH[step+1,1]-CH[step,1])
        
        #Si el angulo es negativo, lo pasamos a positivo
        if dircar < 0:
            dircar = 2*np.pi + dircar

        #Si el auto ya dio una vuelta, reseteamos el angulo previo a 0 (por lo siguiente)
        if step == 0:
            prev_Angle = 0

        #El siguiente arreglo se realiza por una discontinuidad en la funcion que calcula dircar
        #Si el cambio de direccion es muy brusco
        #Exceptuando cuando pasa de 359° a 0 grados (esto se arregla con lo anterior)
        if abs(dircar - prev_Angle) > np.pi/4:
            #Se conserva el angulo anterior
            angle = prev_Angle
            
        #Si el cambio de direccion no es muy bruto
        else:
            #Se determina que el angulo nuevo sea dado segun el siguiente punto de la curva
            angle = dircar


    
    #Se limpia la memoria usada en la gpu
    dibujo.clear()
    auto.clear()

    glfw.terminate()

    return 0

#Se ejecuta la funcion main
if __name__ == "__main__":
    main()
