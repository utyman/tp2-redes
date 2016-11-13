from numpy.random.mtrand import np
from scipy import stats
from cmath import sqrt
import copy



def calcularDiferenciaPromedio(valores):
    media = calcularMedia(valores);
    desvioStandard = calcularDesvioStandard(valores);
    return map( (lambda v : calcularValorDesvioAbsoluto(v, media)/desvioStandard), valores)

def calcularDesvioStandard(valores):
    """Calcular el desvio standard
    valores: arreglo con los valores
    """
    return np.std(valores, ddof=1)

def calcularMedia(valores):
    """Calcular la media
    valores: arreglo con los valores
    """
    return np.mean(valores)



def calcularValorDesvioAbsoluto(v, media):
    """Calcular el desvio absoluto
    v: el valor a considerar
    media: la media
    """
    return np.abs(v - media)


def calcularTau(alpha, n):
    """Calcular el tau
    alpha
    n
    """
    tAlphaDiv2 = stats.t.ppf(1-alpha/2, n-2)
    numerador = tAlphaDiv2 * (n-1)
    denominador = sqrt(n)*sqrt(n - 2 + pow(tAlphaDiv2, 2))
    return float(np.real(numerador / denominador))





def esUnOutlier(maximoDesvioAbsoluto, desvioStandard, tau):
    return maximoDesvioAbsoluto > desvioStandard*tau


def obtenerDiferenciasRTT(RTTS):
    return [j-i for i, j in zip(RTTS[:-1], RTTS[1:])] 
    

def llenarCerosConElRTTAnterior(RTTS):
    for i in range(0, len(RTTS)):
        if RTTS[i] == 0 and i != 0:
            RTTS[i] = RTTS[i-1]
            
def cimbala(RTTS):
    llenarCerosConElRTTAnterior(RTTS)
    valores = obtenerDiferenciasRTT(RTTS)
    llenarCerosConElRTTAnterior(RTTS)  # necesario para usar el delta RTT anterior
    alpha = 0.05
    outliers = []
    noSeEncontraronCandidatosAOutliers = False
    valoresOriginales = copy.copy(valores)
    while not noSeEncontraronCandidatosAOutliers:
        media = calcularMedia(valores)
        desvioStandard = calcularDesvioStandard(valores)
        desviosAbsolutos = map( (lambda v : calcularValorDesvioAbsoluto(v, media)), valores)
        maximoDesvioAbsoluto = max(desviosAbsolutos)
        indiceMaximoDesvioAbsoluto = desviosAbsolutos.index(maximoDesvioAbsoluto)
        tau = calcularTau(alpha, len(valores))
        
        if esUnOutlier(maximoDesvioAbsoluto, desvioStandard, tau):
            outliers.append(valoresOriginales.index(valores[indiceMaximoDesvioAbsoluto]))
            valores.pop(indiceMaximoDesvioAbsoluto)
            noSeEncontraronCandidatosAOutliers = False
        else:
            noSeEncontraronCandidatosAOutliers = True
    
    return outliers;
    
