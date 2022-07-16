
import libs.transformations as tr
import libs.basic_shapes as bs
import libs.constant as C
import numpy as np
import math
from libs.typeLight import *
from OpenGL.GL import *

#Archivo basado en setup visto en clases auxiliares, pero con ciertos cambios

#Funcion que setea las caracteristicas de la luz
def setLights(spotlightsPool, carControl, c, lC):
    
    #Primera luz faroles de luz principales
    spot1 = Spotlight()

    #Se definen los atributos de la luz excepto los que se desean mantener por defecto
    spot1.ambient = np.array([0.01, 0.01, 0.01]) #luz ambiental
    spot1.diffuse = np.array([0.5 * c, 0.5 * c, 0.5 * c]) #luz difusa
    spot1.position = np.array([-4, -3.5, 0.78]) #posicion
    spot1.direction = np.array([0, 0, -1]) #direccion
    spot1.cutOff = np.cos(np.radians(12.5)) #apertura de la luz
    spot1.outerCutOff = np.cos(np.radians(40)) #apertura externa de la luz

    #Se anade la luz en la pool de luces spotlight
    spotlightsPool['spot1'] = spot1 


    #Segunda luz faroles de luz principales
    spot2 = Spotlight()
    spot2.ambient = np.array([0.01, 0.01, 0.01])
    spot2.diffuse = np.array([0.5 * c, 0.5 * c, 0.5 * c])
    spot2.position = np.array([-4, -1.0, 0.78])
    spot2.direction = np.array([0, 0, -1])
    spot2.cutOff = np.cos(np.radians(12.5))
    spot2.outerCutOff = np.cos(np.radians(40))
    spotlightsPool['spot2'] = spot2

    #Tercera luz faroles de luz principales
    spot3 = Spotlight()
    spot3.ambient = np.array([0.01, 0.01, 0.01])
    spot3.diffuse = np.array([0.5 * c, 0.5 * c, 0.5 * c])
    spot3.position = np.array([-4, 1.5, 0.78])
    spot3.direction = np.array([0, 0, -1])
    spot3.cutOff = np.cos(np.radians(12.5)) 
    spot3.outerCutOff = np.cos(np.radians(40)) 
    spotlightsPool['spot3'] = spot3

    #Cuarta luz faroles de luz principales
    spot4 = Spotlight()
    spot4.ambient = np.array([0.01, 0.01, 0.01])
    spot4.diffuse = np.array([0.5 * c, 0.5 * c, 0.5 * c])
    spot4.position = np.array([4, -3.5, 0.78])
    spot4.direction = np.array([0, 0, -1])
    spot4.cutOff = np.cos(np.radians(12.5))
    spot4.outerCutOff = np.cos(np.radians(40)) 
    spotlightsPool['spot4'] = spot4

    #Quinta luz faroles de luz principales
    spot5 = Spotlight()
    spot5.ambient = np.array([0.01, 0.01, 0.01])
    spot5.diffuse = np.array([0.5 * c, 0.5 * c, 0.5 * c])
    spot5.position = np.array([4, -1.0, 0.78])
    spot5.direction = np.array([0, 0, -1]) 
    spot5.cutOff = np.cos(np.radians(12.5)) 
    spot5.outerCutOff = np.cos(np.radians(40)) 
    spotlightsPool['spot5'] = spot5

    #Sexta luz faroles de luz principales
    spot6 = Spotlight()
    spot6.ambient = np.array([0.01, 0.01, 0.01])
    spot6.diffuse = np.array([0.5 * c, 0.5 * c, 0.5 * c])
    spot6.position = np.array([3.5, 1.5, 0.78]) 
    spot6.direction = np.array([0, 0, -1]) 
    spot6.cutOff = np.cos(np.radians(12.5))
    spot6.outerCutOff = np.cos(np.radians(40)) 
    spotlightsPool['spot6'] = spot6

    #Primera luz faroles cartel
    spot7 = Spotlight()
    spot7.ambient = np.array([0.01, 0.01, 0.01])
    spot7.diffuse = np.array([0.5 * c, 0.5 * c, 0.5 * c])
    spot7.position = np.array([1.2, 2.5, 1.23]) 
    spot7.direction = np.array([0, 0, -1]) 
    spot7.cutOff = np.cos(np.radians(12.5))
    spot7.outerCutOff = np.cos(np.radians(40)) 
    spotlightsPool['spot7'] = spot7

    #Segunda luz faroles cartel
    spot8 = Spotlight()
    spot8.ambient = np.array([0.01, 0.01, 0.01])
    spot8.diffuse = np.array([0.5 * c, 0.5 * c, 0.5 * c])
    spot8.position = np.array([2.3, 1.9, 1.23]) 
    spot8.direction = np.array([0, 0, -1]) 
    spot8.cutOff = np.cos(np.radians(12.5))
    spot8.outerCutOff = np.cos(np.radians(40)) 
    spotlightsPool['spot8'] = spot8

    #Primera luz focos auto
    spot9 = Spotlight()
    spot9.ambient = np.array([0.01, 0.01, 0.01])
    spot9.diffuse = np.array([0.8 * c, 0.8 * c, 0.8 * c])
    spot9.constant = 1.0
    spot9.linear = 0.09
    spot9.quadratic = 0.032
    spot9.position = np.array(carControl.posL9)
    spot9.direction = np.array(carControl.directL9) 
    spot9.cutOff = np.cos(np.radians(12.5)) 
    spot9.outerCutOff = np.cos(np.radians(20)) 
    spotlightsPool['spot9'] = spot9

    #Segunda luz focos auto
    spot10 = Spotlight()
    spot10.ambient = np.array([0.01, 0.01, 0.01])
    spot10.diffuse = np.array([0.8 * c, 0.8 * c, 0.8 * c])
    spot10.constant = 1.0
    spot10.linear = 0.09
    spot10.quadratic = 0.032
    spot10.position = np.array(carControl.posL10) 
    spot10.direction = np.array(carControl.directL10) 
    spot10.cutOff = np.cos(np.radians(12.5))
    spot10.outerCutOff = np.cos(np.radians(20)) 
    spotlightsPool['spot10'] = spot10

    #Luz verde semaforo
    spot11 = Spotlight()
    spot11.ambient = np.array([0.01, 0.01, 0.01])
    spot11.diffuse = np.array([0, 0.5 * lC, 0])
    spot11.constant = 1.0
    spot11.linear = 1
    spot11.quadratic = 1
    spot11.position = np.array([0.35, -1.49, 0.54]) 
    spot11.direction = np.array([-1, 0, 0]) 
    spot11.cutOff = np.cos(np.radians(12.5))
    spot11.outerCutOff = np.cos(np.radians(20)) 
    spotlightsPool['spot11'] = spot11

    #Luz roja semaforo
    spot12 = Spotlight()
    spot12.ambient = np.array([0.01, 0.01, 0.01])
    spot12.diffuse = np.array([0.5 * (1-lC), 0 , 0])
    spot12.constant = 1.0
    spot12.linear = 1
    spot12.quadratic = 1
    spot12.position = np.array([0.35, -1.49, 0.62]) 
    spot12.direction = np.array([-1, 0, 0]) 
    spot12.cutOff = np.cos(np.radians(12.5))
    spot12.outerCutOff = np.cos(np.radians(20)) 
    spotlightsPool['spot12'] = spot12


#Se crea una funcion que spotea las proyecciones que se usan
def setPlot(ColorPipeline, TexPipeline, spotlightsPool, camController, sunController):

    #Si la camara mira desde afuera, tendra proyeccion ortho
    if camController.camOUT:
        projection = tr.ortho(-5, 5, -5, 5, 0.1, 100)

    #Si la camara mira desde adentro, tendra proyeccion de perspectiva
    else:
        projection = tr.perspective(45, float(C.SCREEN_WIDTH)/float(C.SCREEN_HEIGHT), 0.1, 100)

    
    #Se obtienen las posiciones de el sol y la luna con el controlador de estos
    posSun = sunController.XYZpos()[0]
    sunX = posSun[0] ; sunY = posSun[1] ; sunZ = posSun[2]

    posMoon = sunController.XYZpos()[1]
    moonX = posMoon[0] ; moonY = posMoon[1] ; moonZ = posMoon[2]


    #Se determina el uso de la proyeccion del shader de color
    glUseProgram(ColorPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        ColorPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    #Se setean las 2 luces puntuales que simulan ser el sol y la luna para el shader de color
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[0].ambient"), 0.01, 0.01, 0.01)
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[0].diffuse"), 3.0, 3.0, 3.0)
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[0].specular"), 0, 0, 0)
    glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[0].position"), sunX, sunY, sunZ)

    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[1].ambient"), 0.01, 0.01, 0.01)
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[1].diffuse"), 0.6*173/255, 0.6*216/255, 230/255)
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[1].specular"), 0, 0, 0)
    glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[1].constant"), 0.1)
    glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[1].linear"), 0.1)
    glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[1].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "pointLights[1].position"), moonX, moonY, moonZ)

    #Se setean las propiedades de los materiales para el shader de color
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "material.ambient"), 10.0, 10.0, 10.0)
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "material.diffuse"), 10.0, 10.0, 10.0)
    glUniform3f(glGetUniformLocation(ColorPipeline.shaderProgram, "material.specular"), 10.0, 10.0, 10.0)
    glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, "material.shininess"), 32)

    #Se setea cada spotlight de las ingresadas en la pool de spotlights para el shader de color
    for i, (k,v) in enumerate(spotlightsPool.items()):

        baseString = "spotLights[" + str(i) + "]."
        
        glUniform3fv(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "linear"), 0.09)
        glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "quadratic"), 0.032)
        glUniform3fv(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(ColorPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)


    #Se determina el uso de la proyeccion del shader de texturas
    glUseProgram(TexPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        TexPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    #Se setean las 2 luces puntuales que simulan ser el sol y la luna para el shader de texturas
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[0].ambient"), 0.01, 0.01, 0.01)
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[0].diffuse"), 3.0, 3.0, 3.0)
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[0].specular"), 0, 0, 0)
    glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[0].position"), sunX, sunY, sunZ)

    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[1].ambient"), 0.01, 0.01, 0.01)
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[1].diffuse"), 0.6*173/255, 0.6*216/255, 230/255)
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[1].specular"), 0, 0, 0)
    glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[1].constant"), 0.1)
    glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[1].linear"), 0.1)
    glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[1].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "pointLights[1].position"), moonX, moonY, moonZ)

    #Se setean las propiedades de los materiales para el shader de texturas
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "material.ambient"), 10.0, 10.0, 10.0)
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "material.diffuse"), 10.0, 10.0, 10.0)
    glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "material.specular"), 10.0, 10.0, 10.0)
    glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, "material.shininess"), 32)

    #Se setea cada spotlight de las ingresadas en la pool de spotlights para el shader de texturas
    for i, (k,v) in enumerate(spotlightsPool.items()):

        baseString = "spotLights[" + str(i) + "]."
        
        glUniform3fv(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "linear"), 0.09)
        glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "quadratic"), 0.032)
        glUniform3fv(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(TexPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)



#Se crea una funcion que seteara el tipo de vista usado
def setView(ColorPipeline, TexPipeline, controller):

    #Variable creada para que la vista tenga una direccion hacia el infinito
    c = 99999999999

    #Si la camara mira desde afuera, el ojo se movera segun coordenadas esfericas del controlador
    if controller.camOUT:

        view = tr.lookAt(
            np.array([5*math.sin(controller.ThetaAngle)*math.cos(controller.AlphaAngle), 
                      5*math.sin(controller.ThetaAngle)*math.sin(controller.AlphaAngle),
                      5*math.cos(controller.ThetaAngle)]),
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

    #Si la camara mira desde dentro, el ojo se movera segun la posicion en x, y, z
    # y el a donde mira, se rige segun coordenadas esfericas, todo segun el controlador
    else:

        view = tr.lookAt(
            np.array([controller.pos[0], controller.pos[1], controller.pos[2]]),
            np.array([c*math.sin(controller.BetaAngle)*math.cos(controller.PhiAngle),
                      c*math.sin(controller.BetaAngle)*math.sin(controller.PhiAngle),
                      c*math.cos(controller.BetaAngle)]),
            np.array([0, 0, 1])
        )


    #Se determina que el programa use la vista para el shader de iluminacion con color
    glUseProgram(ColorPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        ColorPipeline.shaderProgram, "view"), 1, GL_TRUE, view)


    #Se determina que el programa use la vista shader de iluminacion texturas color
    glUseProgram(TexPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        TexPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

     #Si la camara mira desde afuera, el ojo se movera segun coordenadas esfericas del controlador
    if controller.camOUT:

        glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "viewPosition"),
                    5*math.sin(controller.ThetaAngle)*math.cos(controller.AlphaAngle), 
                    5*math.sin(controller.ThetaAngle)*math.sin(controller.AlphaAngle),
                    5*math.cos(controller.ThetaAngle))

    #Si la camara mira desde dentro, el ojo se movera segun la posicion en x, y, z
    # y el a donde mira, se rige segun coordenadas esfericas, todo segun el controlador
    else:

        glUniform3f(glGetUniformLocation(TexPipeline.shaderProgram, "viewPosition"),
                      c*math.sin(controller.BetaAngle)*math.cos(controller.PhiAngle),
                      c*math.sin(controller.BetaAngle)*math.sin(controller.PhiAngle),
                      c*math.cos(controller.BetaAngle))
