"""
Funciones para generación de curvas.
"""

import numpy as np
import matplotlib.pyplot as plt

#Funcion que genera un vector con 1, t, t^2, t^3 (se usa para evaluar la curva)
def generateT(t):
    return np.array([[1, t, t ** 2, t ** 3]]).T


#Funcion que devuelve la matriz de una curva de hermite definida segun los Pi y Ti entregados
def hermiteMatrix(P1, P2, T1, T2):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, T1, T2), axis=1)

    # Hermite base matrix is a constant
    Mh = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])

    return np.matmul(G, Mh)


#Funcion que devuelve la matriz de una curva de bezier definida segun los Pi entregados
def bezierMatrix(P0, P1, P2, P3):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Bezier base matrix is a constant
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])

    return np.matmul(G, Mb)


#Funcion que grafica la cirva entregada
def plotCurve(ax, curve, label, color=(0, 0, 1)):
    xs = curve[:, 0]
    ys = curve[:, 1]
    zs = curve[:, 2]

    ax.plot(xs, ys, zs, label=label, color=color)


#Funcion que retorna la evaluacion de la matriz entregada con un vector de 4 coordenadas
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)

    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)

    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T # x, y, z

    return curve
