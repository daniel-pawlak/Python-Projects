"""Zawiera funkcje wykorzystywane do korekcji perspektywy"""
import numpy as np

def perspective_projection(original, params):
    """Przeprowadza transformację rzutową zbioru punktów
    
    :param original: krotka zawierająca zbiory współrzędnych x i y
    :param params: zestaw parametrów definiujących transformację

    :returns: (xp, yp), gdzie xp i yp są współrzędnymi po transformacji
    :rtype: krotka zawierająca dwie tablice ndarray
    """
    x, y = original
    A, B, C, D, E, F, G, H = params

    xp = (A*x+B*y+C)/(G*x+H*y+1)
    yp = (D*x+E*y+F)/(G*x+H*y+1)

    return xp, yp

def find_transformation(points, ref_points):
    M = np.zeros((8,8))
    v = np.zeros((8))

    for i in range(0, 4):
        x, y = ref_points[i]
        xp, yp = points[i]

        M[2*i, :] = np.array([x, y, 1, 0, 0, 0, -x*xp, -y*xp])
        M[2*i+1, :] = np.array([0, 0, 0, x, y, 1, -x*yp, -y*yp])

        v[2*i] = xp
        v[2*i+1] = yp

    params = np.linalg.solve(M, v)
    return params

def correct_perspective(img, params, width, height):
    rows = np.linspace(0, height-1, height)
    cols = np.linspace(0, width-1, width)

    x, y = np.meshgrid(cols, rows)
    x = x.astype(np.int32)
    y = y.astype(np.int32)

    xp, yp = perspective_projection((x, y), params)
    org_cols = np.floor(xp).astype(np.int32)
    org_rows = np.floor(yp).astype(np.int32)

    results = np.zeros((height, width, 3))      # y, x, RGB
    results[y, x, :] = img[org_rows, org_cols, :]
    results = results.astype(np.uint8)

    return results