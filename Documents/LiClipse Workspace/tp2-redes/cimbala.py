from numpy.random.mtrand import np
from scipy import stats
from cmath import sqrt



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


def cimbala(valores):
    alpha = 0.05
    outliers = []
    noSeEncontraronCandidatosAOutliers = False
    
    while not noSeEncontraronCandidatosAOutliers:
        media = calcularMedia(valores)
        desvioStandard = calcularDesvioStandard(valores)
        desviosAbsolutos = map( (lambda v : calcularValorDesvioAbsoluto(v, media)), valores)
        
        maximoDesvioAbsoluto = max(desviosAbsolutos)
        
        indiceMaximoDesvioAbsoluto = desviosAbsolutos.index(maximoDesvioAbsoluto)
        tau = calcularTau(alpha, len(valores))
        
        if esUnOutlier(maximoDesvioAbsoluto, desvioStandard, tau):
            outliers.append(indiceMaximoDesvioAbsoluto)
            valores.pop(indiceMaximoDesvioAbsoluto)
        else:
            noSeEncontraronCandidatosAOutliers = True
    
    return outliers;
    

if __name__ == '__main__':
    print cimbala([48.9, 49.2, 49.2, 49.3, 49.3, 49.8, 49.9, 50.1, 150.2, 150.5])