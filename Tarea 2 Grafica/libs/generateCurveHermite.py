
from libs.curvas import *


#Funcion que retorna una curva de hermite que coincide con una manzana en la escena creada
def generateCurveH(N):

    #Se definen valores correctores por el desplazamiento que se hizo para centrar la escena 
    Xc = -4.5
    Yc = -4

    #Primera recta
    P1 = np.array([[0.25 + Xc, 0.5 + Yc, 0]]).T
    P2 = np.array([[0.25 + Xc, 2.5 + Yc, 0]]).T
    T1 = np.array([[0, 0.5, 0]]).T
    T2 = np.array([[0, 0.5, 0]]).T

    #Se crea la matriz de hermite para estos puntos
    MH0 = hermiteMatrix(P1, P2, T1, T2)
    #Se crea la curva para esta matriz
    Hcurve0 = evalCurve(MH0, N)

    #Primera curva
    P1 = np.array([[0.25 + Xc,  2.5 + Yc, 0]]).T
    P2 = np.array([[ 0.5 + Xc, 2.75 + Yc, 0]]).T
    T1 = np.array([[0, 0.5, 0]]).T
    T2 = np.array([[0.5, 0, 0]]).T

    MH1 = hermiteMatrix(P1, P2, T1, T2)
    Hcurve1 = evalCurve(MH1, N)

    #Segunda recta
    P1 = np.array([[0.5 + Xc, 2.75 + Yc, 0]]).T
    P2 = np.array([[8.5 + Xc, 2.75 + Yc, 0]]).T
    T1 = np.array([[0.5, 0, 0]]).T
    T2 = np.array([[0.5, 0, 0]]).T

    MH2 = hermiteMatrix(P1, P2, T1, T2)
    Hcurve2 = evalCurve(MH2, N)

    #Segunda curva
    P1 = np.array([[ 8.5 + Xc, 2.75 + Yc, 0]]).T
    P2 = np.array([[8.75 + Xc,  2.5 + Yc, 0]]).T
    T1 = np.array([[0.5, 0, 0]]).T
    T2 = np.array([[ 0, -0.5, 0]]).T

    MH3 = hermiteMatrix(P1, P2, T1, T2)
    Hcurve3 = evalCurve(MH3, N)

    #Tercera recta
    P1 = np.array([[8.75 + Xc, 2.5 + Yc, 0]]).T
    P2 = np.array([[8.75 + Xc, 0.5 + Yc, 0]]).T
    T1 = np.array([[0, -0.5, 0]]).T
    T2 = np.array([[0, -0.5, 0]]).T

    MH4 = hermiteMatrix(P1, P2, T1, T2)
    Hcurve4 = evalCurve(MH4, N)

    #Tercera curva
    P1 = np.array([[8.75 + Xc,  0.5 + Yc, 0]]).T
    P2 = np.array([[ 8.5 + Xc, 0.25 + Yc, 0]]).T
    T1 = np.array([[   0, -0.5, 0]]).T
    T2 = np.array([[-0.5,    0, 0]]).T

    MH5 = hermiteMatrix(P1, P2, T1, T2)
    Hcurve5 = evalCurve(MH5, N)

    #Cuarta recta
    P1 = np.array([[8.5 + Xc, 0.25 + Yc, 0]]).T
    P2 = np.array([[0.5 + Xc, 0.25 + Yc, 0]]).T
    T1 = np.array([[-0.5, 0, 0]]).T
    T2 = np.array([[-0.5, 0, 0]]).T

    MH6 = hermiteMatrix(P1, P2, T1, T2)
    Hcurve6 = evalCurve(MH6, N)

    #Cuarta curva
    P1 = np.array([[ 0.5 + Xc, 0.25 + Yc, 0]]).T
    P2 = np.array([[0.25 + Xc,  0.5 + Yc, 0]]).T
    T1 = np.array([[-0.5,   0, 0]]).T
    T2 = np.array([[   0, 0.5, 0]]).T

    MH7 = hermiteMatrix(P1, P2, T1, T2)
    Hcurve7 = evalCurve(MH7, N)

    #Unimos las curvas
    C = np.concatenate((Hcurve0, Hcurve1, Hcurve2, Hcurve3, Hcurve4, Hcurve5, Hcurve6, Hcurve7), axis=0)

    return C







