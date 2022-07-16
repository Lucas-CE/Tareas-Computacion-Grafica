import numpy as np
import glfw
import math


#Definimos la funcion que detectara la tecla presionada
#Esta funcion realiza lo mismo que la funcion tipica on_key
def sub_on_key(window, key, action, camController, trafficController):

    #Si es que la accion no es presionar alguna tecla la funcion devuelve nada
    if action != glfw.PRESS:
        return

    # Movimiento de la camara

    #Si se presiona la tecla hacia arriba el angulo beta disminuye
    #haciendo que la vista IN mire hacia arriba
    if key == glfw.KEY_UP:
        if not camController.camOUT:
            camController.change_beta(-1)

    #Si se presiona la tecla hacia abajo el angulo beta aumenta
    #haciendo que la vista IN mire hacia abajo
    if key == glfw.KEY_DOWN:
        if not camController.camOUT:
            camController.change_beta(1)

    #Si se presiona la tecla hacia la izquierda se el angulo phi aumenta
    #haciendo que la vista IN gire hacia la izquierda
    if key == glfw.KEY_LEFT:
        if not camController.camOUT:
            camController.PhiAngle += camController.velAngleIN

    #Si se presiona la tecla hacia la derecha se el angulo phi disminuye
    #haciendo que la vista IN gire hacia la derecha
    if key == glfw.KEY_RIGHT:
        if not camController.camOUT:
            camController.PhiAngle -= camController.velAngleIN                      
        
    #Si se presiona la tecla W
    if key == glfw.KEY_W:

        #Si estamos en la camara por afuera, el angulo theta disminuye
        #haciendo que la camara gire hacia arriba
        if camController.camOUT:
            camController.change_theta(-1)

        #Si estamos en la camara por adentro, se cambia la posicion de la camara
        #haciendo que se mueva hacia adelante
        else:
            if not camController.camOUT:
                camController.move(camController.vel*math.cos(camController.PhiAngle),
                                camController.vel*math.sin(camController.PhiAngle))

    #Si se presiona la tecla S
    elif key == glfw.KEY_S:

        #Si estamos en la camara por afuera, el angulo theta aumenta
        #haciendo que la camara gire hacia abajo
        if camController.camOUT:
            camController.change_theta(1)

        #Si estamos en la camara por adentro, se cambia la posicion de la camara
        #haciendo que se mueva hacia atras
        else:
            camController.move(-camController.vel*math.cos(camController.PhiAngle),
                            -camController.vel*math.sin(camController.PhiAngle))

    #Si se presiona la tecla A
    elif key == glfw.KEY_A:

        #Si estamos en la camara por afuera, el angulo alpha disminuye
        #haciendo que la camara gire hacia la izquierda
        if camController.camOUT:
            camController.AlphaAngle -= camController.velAngleOut

        #Si estamos en la camara por adentro, se cambia la posicion de la camara
        #haciendo que se mueva hacia la izquierda
        else:
            camController.move(camController.vel*math.cos(camController.PhiAngle + np.pi/2),
                            camController.vel*math.sin(camController.PhiAngle + np.pi/2))
            
    #Si se presiona la tecla D
    elif key == glfw.KEY_D:

        #Si estamos en la camara por afuera, el angulo alpha aumenta
        #haciendo que la camara gire hacia derecha
        if camController.camOUT:
            camController.AlphaAngle += camController.velAngleOut

        #Si estamos en la camara por adentro, se cambia la posicion de la camara
        #haciendo que se mueva hacia la derecha
        else:
            camController.move(-camController.vel*math.cos(camController.PhiAngle + np.pi/2),
                            -camController.vel*math.sin(camController.PhiAngle + np.pi/2))  

    #Si se presiona la tecla E
    elif key == glfw.KEY_E:

        #Si estamos en la cama por afuera, se aumenta la posicion en z,
        #haciendo que la camara suba
        if not camController.camOUT:
            camController.pos[2] += camController.vel

    #Si se presiona la tecla Q
    elif key == glfw.KEY_Q:

        #Si estamos en la cama por afuera, se disminuye la posicion en z,
        #haciendo que la camara baje
        if not camController.camOUT:
            if camController.pos[2] > 0.1:
                camController.pos[2] -= camController.vel

    #Si se presiona la tecla 1
    elif key == glfw.KEY_1:
        #Cambia el estado del semaforo
        trafficController.change_state()

    #Si se presiona la tecla espacio, cambia entre la camara que mira desde afuera con la que mira
    #desde adentro
    elif key == glfw.KEY_SPACE:
        camController.camOUT = not camController.camOUT

    #Si se presiona esc, se cierra la ventana
    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)



#Esta funcion es parecida a la anterior, solo que no detecta el momento en que las teclas son
#son presionadas, si no si estas siguen siendo presionadas
#Las tareas ejecutadas al presionar las teclas son las mismas de la funcion anterior
def check_key_inputs(window, controller):

    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        if not controller.camOUT:
            controller.change_beta(-1)

    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        if not controller.camOUT:
            controller.change_beta(1)

    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        if not controller.camOUT:
            controller.PhiAngle += controller.velAngleIN


    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        if not controller.camOUT:
            controller.PhiAngle -= controller.velAngleIN     

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        if controller.camOUT:
            controller.change_theta(-1)
        else:
            if not controller.camOUT:
                controller.move(controller.vel*math.cos(controller.PhiAngle),
                                controller.vel*math.sin(controller.PhiAngle))


    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        if controller.camOUT:
            controller.change_theta(1)
        else:
            controller.move(-controller.vel*math.cos(controller.PhiAngle),
                            -controller.vel*math.sin(controller.PhiAngle))

    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        if controller.camOUT:
            controller.AlphaAngle -= controller.velAngleOut
        else:
            controller.move(controller.vel*math.cos(controller.PhiAngle + np.pi/2),
                            controller.vel*math.sin(controller.PhiAngle + np.pi/2))

    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        if controller.camOUT:
            controller.AlphaAngle += controller.velAngleOut
        else:
            controller.move(-controller.vel*math.cos(controller.PhiAngle + np.pi/2),
                            -controller.vel*math.sin(controller.PhiAngle + np.pi/2))  

    if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
        if not controller.camOUT:
            controller.pos[2] += controller.vel

    if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
        if not controller.camOUT:
            if controller.pos[2] > 0.1:
                controller.pos[2] -= controller.vel

