from libs.gpu_shape import GPUShape
import libs.transformations as tr
from libs.basic_shapes import *
from OpenGL.GL import *
import numpy as np

def create_GPUFigure(figure, pipeline):

    nombre = figure
    gpuName = GPUShape().initBuffers()
    pipeline.setupVAO(gpuName)
    gpuName.fillBuffers(nombre.vertexData, nombre.indexData)
    return gpuName


class LogoDVD:
    
    #Creacion de objetos
    def __init__(self, pipeline, controller, r, g, b):

        self.pipeline = pipeline
        self.controller = controller

        (r2,g2,b2) = (10/255, 10/255, 10/255)

        #creamos el disco principal que va debajo de DVD
        gpuDisk = create_GPUFigure(createEllipse(30, 0.4, 0.1, r, g, b), pipeline)

        #creamos el disco interior que va al centro del disco principal
        gpuintDisk = create_GPUFigure(createEllipse(30, 0.11, 0.024, r2, g2, b2), pipeline)

        #creamos la primera D de la palabra DVD
        gpuD1 = create_GPUFigure(createHalfEllipse(20, 0.26, 0.3, r, g, b, -np.pi/2), pipeline)

        #creamos una D que representará el hueco que hay en la letra D creada en el paso anterior
        gpuintD1 = create_GPUFigure(createHalfEllipse(20, 0.12, 0.14, r2, g2, b2, -np.pi/2), pipeline)

        #creamos un triangulo que representará la V en DVD
        gpuV1 = create_GPUFigure(create_V_Triangle(0.5, r, g, b), pipeline)

        #creamos un triangulo que representará el hueco que debe tener la V
        gpuintV1 = create_GPUFigure(create_V_Triangle(0.25, r2, g2, b2), pipeline)
        
        #creamos la segunda D de la letra en DVD
        gpuD2 = create_GPUFigure(createHalfEllipse(20, 0.26, 0.3, r, g, b, -np.pi/2), pipeline)

        #creamos una D que representará el hueco que hay en la segunda letra D
        gpuintD2 = create_GPUFigure(createHalfEllipse(20, 0.12, 0.14, r2, g2, b2, -np.pi/2), pipeline)

        #Guardamos los gpus en el objeto
        self.gpuDisk = gpuDisk
        self.gpuintDisk = gpuintDisk
        self.gpuD1 = gpuD1
        self.gpuintD1 = gpuintD1
        self.gpuV1 = gpuV1
        self.gpuintV1 = gpuintV1
        self.gpuD2 = gpuD2
        self.gpuintD2 = gpuintD2


    #Funcion encargada de dibujar el logo del dvd
    def Draw_DVD(self, X_Position, Y_Position, cTX, cTY):

        pipeline = self.pipeline
        controller = self.controller

        #El escalamiento del tamano normal de dvd es 0.5
        #y esto se vuelve a escalar por las constantes de tamano
        (tamanoX, tamanoY) = (cTX/2, cTY/2)

        #Funcion que dibuja las figuras
        #Se define adentro para no tener que repetir los parametros de pipeline, controller, y los tamanos
        #siempre que se llame a la funcion
        def draw_figure(gpu, x, y, ListExtraTransforms=[]):

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, 
            tr.matmul([tr.rotationZ(controller.grades), tr.translate(x, y, 0.0), tr.scale(tamanoX, tamanoY, 0.0)]
                    + ListExtraTransforms))

            pipeline.drawCall(gpu)


        draw_figure(self.gpuDisk, X_Position, Y_Position - cTY*0.15)

        draw_figure(self.gpuintDisk, X_Position, Y_Position - cTY*0.15)

        draw_figure(self.gpuD1, X_Position - cTX*0.2, Y_Position + cTY*0.05)

        draw_figure(self.gpuintD1, X_Position - cTX*0.17, Y_Position + cTY*0.05)

        draw_figure(self.gpuV1, X_Position, Y_Position - cTY*0.07)

        draw_figure(self.gpuintV1, X_Position, Y_Position + cTY*0.055)

        draw_figure(self.gpuD2, X_Position + cTX*0.2, Y_Position + cTY*0.05, [tr.rotationY(np.pi)])

        draw_figure(self.gpuintD2, X_Position + cTX*0.17, Y_Position + cTY*0.05, [tr.rotationY(np.pi)])

    
    def clear_DVD(self):

        self.gpuDisk.clear()
        self.gpuintDisk.clear()
        self.gpuD1.clear()
        self.gpuintD1.clear()
        self.gpuV1.clear()
        self.gpuintV1.clear()
        self.gpuD2.clear()
        self.gpuintD2.clear()
 

class BartSimpson:

    def __init__(self, pipeline, controller):

        self.pipeline = pipeline
        self.controller = controller

        (r, g, b) = (1,1,0)

        gpuHead = create_GPUFigure(create_Rectangle(0.6, 0.9, r, g, b), pipeline)

        gpuBack_Ear = create_GPUFigure(createCircle(20, 0.068 ,0.0, 0.0, 0.0, 8*np.pi/5, np.pi/5), pipeline)

        gpuEar = create_GPUFigure(createCircle(20, 0.06 ,r, g, b), pipeline)

        gpuIntEar = create_GPUFigure(createQuad(0.02 ,0.0, 0.0, 0.0), pipeline)

        gpuHair = create_GPUFigure(create_BartSimpson_hair(r, g, b), pipeline)

        gpuOverEye1 = create_GPUFigure(create_inclined_parallelogram(r, g, b), pipeline)

        gpuBackEye1 = create_GPUFigure(createCircle(20, 0.16, 0.0, 0.0, 0.0), pipeline)

        gpuEye1 = create_GPUFigure(createCircle(20, 0.15, 1.0, 1.0, 1.0), pipeline)

        gpuBackEye2 = create_GPUFigure(createCircle(20, 0.16, 0.0, 0.0, 0.0), pipeline)

        gpuEye2 = create_GPUFigure(createCircle(20, 0.15, 1.0, 1.0, 1.0), pipeline)

        gpuIntEye1 = create_GPUFigure(createCircle(8, 0.02, 0.0, 0.0, 0.0), pipeline)

        gpuIntEye2 = create_GPUFigure(createCircle(8, 0.02, 0.0, 0.0, 0.0), pipeline)

        gpuBack_Part11_nose = create_GPUFigure(create_Rectangle(0.17, 0.06, 0.0, 0.0, 0.0), pipeline)

        gpuBack_Part12_nose = create_GPUFigure(create_Rectangle(0.1, 0.06, 0.0, 0.0, 0.0), pipeline)

        gpuBack_Part2_nose = create_GPUFigure(createHalfEllipse(20, 0.06, 0.06, 0.0, 0.0, 0.0, 0.0), pipeline)

        gpuPart1_nose = create_GPUFigure(create_Rectangle(0.22, 0.1, r, g, b), pipeline)

        gpuPart2_nose = create_GPUFigure(createHalfEllipse(20, 0.05, 0.05, r, g, b, -np.pi/2), pipeline)

        gpuPart1_mouth = create_GPUFigure(create_Rectangle(0.62, 0.15, r, g, b), pipeline)

        gpuNeck = create_GPUFigure(createQuad(0.25, r, g, b), pipeline)

        gpuUnder_mouth = create_GPUFigure(createTriangle(0.0, 0.0, 0.15, 0.0, 0.0, -0.15, r, g, b), pipeline)

        gpuSonrisa = create_GPUFigure(createHalfEllipse(30, 0.275, 0.05, 0.0, 0.0, 0.0, 28*np.pi/36), pipeline)

        gpuOver_sonrisa = create_GPUFigure(createHalfEllipse(20, 0.275, 0.05, r, g, b, 28*np.pi/36), pipeline)

        gpuOver_mouth = create_GPUFigure(createTriangle(0.0, 0.0, -0.02, 0.0, 0.0, -0.22, 0.0, 0.0, 0.0), pipeline)

        self.gpuHead = gpuHead
        self.gpuBack_Ear = gpuBack_Ear
        self.gpuEar = gpuEar
        self.gpuIntEar = gpuIntEar
        self.gpuHair = gpuHair
        self.gpuOverEye1 = gpuOverEye1
        self.gpuBackEye1 = gpuBackEye1
        self.gpuEye1 = gpuEye1
        self.gpuBackEye2 = gpuBackEye2
        self.gpuEye2 = gpuEye2
        self.gpuIntEye1 = gpuIntEye1
        self.gpuIntEye2 = gpuIntEye2
        self.gpuBack_Part11_nose = gpuBack_Part11_nose
        self.gpuBack_Part12_nose = gpuBack_Part12_nose
        self.gpuBack_Part2_nose = gpuBack_Part2_nose
        self.gpuPart1_nose = gpuPart1_nose
        self.gpuPart2_nose = gpuPart2_nose
        self.gpuPart1_mouth = gpuPart1_mouth
        self.gpuNeck = gpuNeck
        self.gpuUnder_mouth = gpuUnder_mouth
        self.gpuSonrisa = gpuSonrisa
        self.gpuOver_sonrisa = gpuOver_sonrisa
        self.gpuOver_mouth = gpuOver_mouth


    def Draw_Bart(self, xPosBart, yPosBart, cTX, cTY):

        pipeline = self.pipeline
        controller = self.controller

        #El escalamiento natural de Bart es 0.2
        #y esto se vuelve a escalar por las constantes de tamano
        (tamanhoBart_X, tamanhoBart_Y) = (cTX/5, cTY/5)

        def draw_figure(gpu, x, y, ListExtraTransforms=[]):

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, 
            tr.matmul([tr.rotationZ(controller.grades), tr.scale(tamanhoBart_X, tamanhoBart_Y, 0.0),
            tr.translate(x, y, 0.0)]))

            pipeline.drawCall(gpu)

        draw_figure(self.gpuHead, xPosBart, yPosBart)

        draw_figure(self.gpuBack_Ear, xPosBart + -0.3, yPosBart + -0.2)

        draw_figure(self.gpuEar, xPosBart + -0.3, yPosBart + -0.2)

        draw_figure(self.gpuIntEar, xPosBart + -0.3, yPosBart + -0.2)

        draw_figure(self.gpuHair, xPosBart + 0.0, yPosBart + 0.45)

        draw_figure(self.gpuOverEye1, xPosBart + 0.29, yPosBart + 0.07)

        draw_figure(self.gpuBackEye1, xPosBart + 0.25, yPosBart + -0.08)

        draw_figure(self.gpuEye1, xPosBart + 0.25, yPosBart + -0.08)

        draw_figure(self.gpuBackEye2, xPosBart + 0.0, yPosBart + -0.08)

        draw_figure(self.gpuEye2, xPosBart + 0.0, yPosBart + -0.08)

        draw_figure(self.gpuIntEye1, xPosBart + 0.25, yPosBart + -0.08)

        draw_figure(self.gpuIntEye2, xPosBart + -0.05, yPosBart + -0.08)

        draw_figure(self.gpuBack_Part11_nose, xPosBart + 0.225, yPosBart + -0.22)

        draw_figure(self.gpuBack_Part12_nose, xPosBart + 0.25, yPosBart + -0.28)

        draw_figure(self.gpuBack_Part2_nose, xPosBart + 0.31, yPosBart + -0.25)

        draw_figure(self.gpuPart1_nose, xPosBart + 0.21, yPosBart + -0.25)
        
        draw_figure(self.gpuPart2_nose, xPosBart + 0.31, yPosBart + -0.25)

        draw_figure(self.gpuPart1_mouth, xPosBart + 0.01, yPosBart + -0.385)

        draw_figure(self.gpuNeck, xPosBart + -0.175, yPosBart + -0.45, 0.0)

        draw_figure(self.gpuUnder_mouth, xPosBart + -0.05, yPosBart + -0.38)

        draw_figure(self.gpuSonrisa, xPosBart + 0.13, yPosBart + -0.425)

        draw_figure(self.gpuOver_sonrisa, xPosBart + 0.13, yPosBart + -0.41)

        draw_figure(self.gpuOver_mouth, xPosBart + 0.322, yPosBart + -0.3)


    def clear_Bart(self):

        self.gpuHead.clear()
        self.gpuBack_Ear.clear()
        self.gpuEar.clear()
        self.gpuIntEar.clear()
        self.gpuHair.clear()
        self.gpuOverEye1.clear()
        self.gpuBackEye1.clear()
        self.gpuEye1.clear()
        self.gpuBackEye2.clear()
        self.gpuEye2.clear()
        self.gpuIntEye1.clear()
        self.gpuIntEye2.clear()
        self.gpuBack_Part11_nose.clear()
        self.gpuBack_Part12_nose.clear()
        self.gpuBack_Part2_nose.clear()
        self.gpuPart1_nose.clear()
        self.gpuPart2_nose.clear()
        self.gpuPart1_mouth.clear()
        self.gpuNeck.clear()
        self.gpuUnder_mouth.clear()
        self.gpuSonrisa.clear()
        self.gpuOver_sonrisa.clear()
        self.gpuOver_mouth.clear()








