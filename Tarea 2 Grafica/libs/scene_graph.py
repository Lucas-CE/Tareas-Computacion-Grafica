# coding=utf-8
"""A simple scene graph class and functionality"""

from OpenGL.GL import *
import numpy as np
import libs.transformations as tr
import libs.gpu_shape as gs

__author__ = "Daniel Calderon"
__license__ = "MIT"


#Clase de nodos
class SceneGraphNode:
    """
    A simple class to handle a scene graph
    Each node represents a group of objects
    Each leaf represents a basic figure (GPUShape)
    To identify each node properly, it MUST have a unique name
    """
    
    def __init__(self, name):

        #Nombre del nodo
        self.name = name

        #Transformaciones aplicadas al nodo
        self.transform = tr.identity()

        #Lista de hijos del nodo
        self.childs = []


    #Funcion que limpia el nodo de la GPU
    def clear(self):
        """Freeing GPU memory"""

        for child in self.childs:
            child.clear()


#Funcion que retorna el nodo buscado segun el nombre y le nodo
def findNode(node, name):

    # The name was not found in this path
    if isinstance(node, gs.GPUShape):
        return None

    # This is the requested node
    if node.name == name:
        return node

    # All childs are checked for the requested name
    for child in node.childs:
        foundNode = findNode(child, name)
        if foundNode != None:
            return foundNode

    # No child of this node had the requested name
    return None


#Funcion que retorna la transformacion buscada segun el nombre del nodo
def findTransform(node, name, parentTransform=tr.identity()):

    # The name was not found in this path
    if isinstance(node, gs.GPUShape):
        return None

    newTransform = np.matmul(parentTransform, node.transform)

    # This is the requested node
    if node.name == name:
        return newTransform

    # All childs are checked for the requested name
    for child in node.childs:
        foundTransform = findTransform(child, name, newTransform)
        if isinstance(foundTransform, (np.ndarray, np.generic)):
            return foundTransform

    # No child of this node had the requested name
    return None


#Funcion que retorna la posicion dle nodo buscado
def findPosition(node, name, parentTransform=tr.identity()):
    foundTransform = findTransform(node, name, parentTransform)

    if isinstance(foundTransform, (np.ndarray, np.generic)):
        zero = np.array([[0, 0, 0, 1]], dtype=np.float32).T
        foundPosition = np.matmul(foundTransform, zero)
        return foundPosition

    return None


#Funcion que dibuja al nodo entregado
def drawSceneGraphNode(node, pipeline, transformName, parentTransform=tr.identity()):
    assert(isinstance(node, SceneGraphNode))

    # Composing the transformations through this path
    newTransform = np.matmul(parentTransform, node.transform)

    # If the child node is a leaf, it should be a GPUShape.
    # Hence, it can be drawn with drawCall
    if len(node.childs) == 1 and isinstance(node.childs[0], gs.GPUShape):
        leaf = node.childs[0]
        glUniformMatrix4fv(glGetUniformLocation(
            pipeline.shaderProgram, transformName), 1, GL_TRUE, newTransform)
        pipeline.drawCall(leaf)

    # If the child node is not a leaf, it MUST be a SceneGraphNode,
    # so this draw function is called recursively
    else:
        for child in node.childs:
            drawSceneGraphNode(child, pipeline, transformName, newTransform)
