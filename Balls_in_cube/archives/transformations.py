import numpy as np

#Devuelve la matriz de traslacion de tx, ty, tz
def translate(tx, ty, tz):
    return np.array([
        [1,0,0,tx],
        [0,1,0,ty],
        [0,0,1,tz],
        [0,0,0,1]], dtype = np.float32)


#Devuelve la matriz de escalamiento de sx, sy, sz
def scale(sx, sy, sz):
    return np.array([
        [sx,0,0,0],
        [0,sy,0,0],
        [0,0,sz,0],
        [0,0,0,1]], dtype = np.float32)


#Devuelve la matriz de rotacion de x en theta 
def rotationX(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [1,0,0,0],
        [0,cos_theta,-sin_theta,0],
        [0,sin_theta,cos_theta,0],
        [0,0,0,1]], dtype = np.float32)

#Devuelve la matriz de rotacion de y en theta 
def rotationY(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta,0,sin_theta,0],
        [0,1,0,0],
        [-sin_theta,0,cos_theta,0],
        [0,0,0,1]], dtype = np.float32)

#Devuelve la matriz de rotacion de z en theta 
def rotationZ(theta):
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta,-sin_theta,0,0],
        [sin_theta,cos_theta,0,0],
        [0,0,1,0],
        [0,0,0,1]], dtype = np.float32)


#Funcion que retorna la multiplicacionn de las matrices que se le entreguen en un array
def matmul(mats):
    out = mats[0]
    for i in range(1, len(mats)):
        out = np.matmul(out, mats[i])

    return out


#Funcion que configura posiciones y atributos de la vista
def frustum(left, right, bottom, top, near, far):
    r_l = right - left
    t_b = top - bottom
    f_n = far - near
    return np.array([
        [ 2 * near / r_l,
        0,
        (right + left) / r_l,
        0],
        [ 0,
        2 * near / t_b,
        (top + bottom) / t_b,
        0],
        [ 0,
        0,
        -(far + near) / f_n,
        -2 * near * far / f_n],
        [ 0,
        0,
        -1,
        0]], dtype = np.float32)


#Funcion que determina desde que perspectiva se vera
def perspective(fovy, aspect, near, far):
    halfHeight = np.tan(np.pi * fovy / 360) * near
    halfWidth = halfHeight * aspect
    return frustum(-halfWidth, halfWidth, -halfHeight, halfHeight, near, far)


#Funcion que configura posiciones y atributos de la vista
def ortho(left, right, bottom, top, near, far):
    r_l = right - left
    t_b = top - bottom
    f_n = far - near
    return np.array([
        [ 2 / r_l,
        0,
        0,
        -(right + left) / r_l],
        [ 0,
        2 / t_b,
        0,
        -(top + bottom) / t_b],
        [ 0,
        0,
        -2 / f_n,
        -(far + near) / f_n],
        [ 0,
        0,
        0,
        1]], dtype = np.float32)


#La funcion recibe la posicion desde donde se vera, hacia donde se vera,
#y que direccion se considera que se tiene hacia arriba
#luego devuelve una matriz que determina la configuracion de la vista
def lookAt(eye, at, up):

    forward = (at - eye)
    forward = forward / np.linalg.norm(forward)

    side = np.cross(forward, up)
    side = side / np.linalg.norm(side)

    newUp = np.cross(side, forward)
    newUp = newUp / np.linalg.norm(newUp)

    return np.array([
            [side[0],       side[1],    side[2], -np.dot(side, eye)],
            [newUp[0],     newUp[1],   newUp[2], -np.dot(newUp, eye)],
            [-forward[0], -forward[1], -forward[2], np.dot(forward, eye)],
            [0,0,0,1]
        ], dtype = np.float32)